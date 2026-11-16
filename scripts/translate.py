"""Traduction FR → EN du guide Bilan Carbone®, paragraphe par paragraphe.

Principe : on compare l'ancienne et la nouvelle version FR d'une page, paragraphe par
paragraphe (blocs séparés par une ligne vide, titres compris). Seuls les paragraphes
ajoutés ou modifiés sont traduits ; les paragraphes supprimés en FR sont supprimés en EN ;
tout le reste de la page EN (y compris les retouches manuelles) est conservé.

Le paragraphe EN correspondant à un paragraphe FR est retrouvé par sa position : chaque
page EN doit donc avoir le même nombre de paragraphes que la page FR. Si ce n'est pas le
cas, la page n'est pas modifiée et un avertissement est affiché dans GitHub Actions.

Les traductions suivent le glossaire officiel (glossaire.csv), inclus dans les consignes.

Post-traitement appliqué à chaque page EN écrite :
- les images FR sont remplacées par leur version EN (table scripts/images-en.json) ;
- les lignes « 🌐 English version of this image » sont supprimées.

Variables d'environnement :
- FILES             chemins des pages FR à traiter (séparés par des espaces)
- BASE_REF          commit FR de référence pour la comparaison (défaut : HEAD~1)
- ANTHROPIC_API_KEY clé API (inutile en DRY_RUN)
- DRY_RUN=1         n'appelle pas l'API : les traductions sont remplacées par « [EN] <texte FR> »
- FR_DIR / EN_DIR   dossiers des deux branches (défaut : fr / en)
"""

import csv
import difflib
import html
import json
import os
import pathlib
import re
import subprocess
import sys
import unicodedata
import urllib.parse

MODEL = "claude-opus-5"
FR_DIR = pathlib.Path(os.environ.get("FR_DIR", "fr"))
EN_DIR = pathlib.Path(os.environ.get("EN_DIR", "en"))
BASE_REF = os.environ.get("BASE_REF") or "HEAD~1"
DRY_RUN = os.environ.get("DRY_RUN") == "1"
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent

# Pages jamais traduites automatiquement.
EXCLUDED = {
    "annexes/glossaire.md",  # EN réorganisé par ordre alphabétique anglais : maintenu à la main
    "COHERENCE-METHODO-GLOSSAIRE.md",  # documents de travail internes, hors GitBook
    "PROPOSITION-AJOUTS-GLOSSAIRE.md",
    "TUTO-NOUVEAU-GITBOOK.md",
}

SYSTEM = """Tu es traducteur technique français → anglais pour la documentation
de l'Association pour la transition Bas Carbone (ABC) — méthode Bilan Carbone®.

Règles impératives :
- Traduis uniquement le texte visible. Ne traduis jamais l'intérieur des blocs de code.
- Préserve exactement la syntaxe GitBook : {% hint %}, {% tabs %}, {% details %}, tableaux, cards, liens.
- Copie les balises <figure>, <img ...> et tout emoji exactement tels quels.
- Conserve la même structure de titres (même nombre de #).
- Conserve exactement le découpage en paragraphes : autant de blocs séparés par une ligne vide que dans le texte source.
- "Bilan Carbone®" ne se traduit pas. Conserve aussi les sigles : ADEME, ABC, CSRD, GHG, ISO.
- "GES" se traduit par "GHG", sauf quand il fait partie d'un sigle composé comme "BEGES-r" (à conserver tel quel).
- Si le fichier est SUMMARY.md, traduis uniquement les titres affichés, jamais les chemins entre parenthèses.
- Réponds uniquement avec le contenu traduit, sans commentaire ni balise supplémentaire."""


def load_glossary():
    """Glossaire officiel FR → EN (glossaire.csv à la racine du repo, colonnes en,fr,…)."""
    path = SCRIPT_DIR.parent / "glossaire.csv"
    if not path.exists():
        return ""
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            fr, en = (row.get("fr") or "").strip(), (row.get("en") or "").strip()
            if fr and en:
                rows.append(f"- {fr} → {en}")
    if not rows:
        return ""
    return (
        "\n\nGlossaire officiel de la méthode (FR → EN). Quand un de ces termes apparaît, "
        "utilise obligatoirement la traduction indiquée, en adaptant seulement le nombre, "
        "la casse ou l'article à la phrase. Pour les termes absents du glossaire, reste "
        "cohérent avec ces choix.\n" + "\n".join(rows)
    )


SYSTEM += load_glossary()

HEADING_RE = re.compile(r"^#{1,6}\s")
LINK_PARA_RE = re.compile(r"🌐.*English version", re.S)
# Références d'images : <img src="…">, ![](<…>) et ![](…). Le nom peut contenir
# espaces et parenthèses (« Criteres (2).jpg ») dans les deux premières formes.
IMG_REF_RES = [
    re.compile(r'(src=")([^"]*\.gitbook/assets/)([^"]+)(?=")'),
    re.compile(r"(\]\(<)([^<>]*\.gitbook/assets/)([^<>]+)(?=>)"),
    re.compile(r"(\]\()([^<\s)]*\.gitbook/assets/)([^\s)]+)(?=[\s)])"),
]
PARA_SEP_RE = re.compile(r"\n[ \t]*\n+")

_client = None
warnings = []
blocking = []  # problèmes qui font échouer le run (page non traitée)


def warn(rel_path, message, block=False):
    print(f"::warning file={rel_path}::{message}")
    warnings.append(f"{rel_path} : {message}")
    if block:
        blocking.append(rel_path)


# ---------------------------------------------------------------- découpage

def split_frontmatter(content):
    content = content.replace("\r\n", "\n").lstrip("﻿")  # BOM éventuel
    lines = content.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[: i + 1]), "\n".join(lines[i + 1 :])
    return "", content


def split_paragraphs(body):
    body = body.strip("\n").rstrip()
    if not body.strip():
        return []
    return [p for p in PARA_SEP_RE.split(body)]


def is_link_para(para):
    return bool(LINK_PARA_RE.search(para))


def paragraphs(content):
    """(frontmatter, paragraphes sans les lignes « English version »)."""
    fm, body = split_frontmatter(content)
    return fm, [p for p in split_paragraphs(body) if not is_link_para(p)]


def assemble(fm, paras):
    body = "\n\n".join(paras)
    if fm:
        return f"{fm}\n\n{body}\n"
    return f"{body}\n"


def needs_translation(para):
    """Faux pour les paragraphes sans texte (&#x20;, {% endhint %}, image sans légende…)."""
    text = re.sub(r"\{%.*?%\}", "", para, flags=re.S)
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"&#?\w+;", "", text)
    text = re.sub(r"!?\[[^\]]*\]\([^)]*\)", lambda m: m.group(0).split("](")[0], text)
    return bool(re.search(r"[A-Za-zÀ-ÿ]", text))


# ---------------------------------------------------------------- images EN

def nfc(name):
    # Les noms de fichiers peuvent avoir des accents composés (é) ou décomposés (e + ´)
    return unicodedata.normalize("NFC", name)


def load_image_map():
    path = SCRIPT_DIR / "images-en.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {nfc(k): v for k, v in data.items() if not k.startswith("_")}


IMAGE_MAP = load_image_map()


def apply_image_map(text):
    def repl(m):
        prefix, folder, name = m.groups()
        decoded = nfc(urllib.parse.unquote(html.unescape(name)))
        target = IMAGE_MAP.get(decoded)
        return f"{prefix}{folder}{target}" if target else m.group(0)

    for regex in IMG_REF_RES:
        text = regex.sub(repl, text)
    return text


# Ligne « 🌐 English version of this image » avec la ligne vide qui la précède.
LINK_LINE_RE = re.compile(r"\n[ \t]*\n[^\n]*🌐[^\n]*English version[^\n]*(?=\n|$)")


def postprocess(content):
    """Modifie uniquement les chemins d'images et les lignes « English version »,
    sans toucher au reste de la mise en forme."""
    content = content.replace("\r\n", "\n")
    return LINK_LINE_RE.sub("", apply_image_map(content))


# ---------------------------------------------------------------- appels API

def client():
    global _client
    if _client is None:
        import anthropic

        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def claude(prompt, source, max_tokens=16000):
    if DRY_RUN:
        return f"[EN] {source}"
    with client().messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        # Consignes + glossaire identiques à chaque appel : mis en cache pour la durée du run
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        output_config={"effort": "medium"},
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        response = stream.get_final_message()
    if response.stop_reason == "max_tokens":
        raise RuntimeError("réponse tronquée (max_tokens atteint)")
    if response.stop_reason == "refusal":
        raise RuntimeError("requête refusée par le modèle")
    return "".join(b.text for b in response.content if b.type == "text").strip()


def nearest_heading(paras, index):
    for p in reversed(paras[:index]):
        if HEADING_RE.match(p):
            return p
    return None


def translate_para(rel_path, fr_paras, index, en_before):
    para = fr_paras[index]
    if not needs_translation(para):
        return para
    context = []
    heading = nearest_heading(fr_paras, index)
    if heading:
        context.append(f"Section : {heading}")
    if index > 0:
        context.append(f"Paragraphe précédent (FR) :\n{fr_paras[index - 1]}")
    if en_before:
        context.append(f"Paragraphe précédent (traduction EN existante) :\n{en_before}")
    if index + 1 < len(fr_paras):
        context.append(f"Paragraphe suivant (FR) :\n{fr_paras[index + 1]}")
    prompt = (
        f"Page : {rel_path}\n\n<contexte>\nÀ ne pas traduire, uniquement pour comprendre :\n\n"
        + "\n\n".join(context)
        + "\n</contexte>\n\n<source>\n"
        + para
        + "\n</source>\n\nTraduis en anglais le bloc markdown contenu dans <source>. "
        "Réponds uniquement avec sa traduction anglaise : ne recopie pas le texte français, "
        "n'ajoute pas les balises <source>, et ne mets pas de ligne vide si l'original n'en a pas."
    )
    if DRY_RUN:  # « [EN] <texte FR> » : pas de validation possible
        return claude(prompt, para)
    single_block = not PARA_SEP_RE.search(para)
    problem = None
    for attempt in range(2):
        out = claude(prompt if attempt == 0 else prompt + RETRY_NOTE.format(problem=problem), para)
        out = re.sub(r"^\s*</?source>\s*|\s*</?source>\s*$", "", out).strip()
        source = para.strip()
        if source in out and out != source:  # français recopié avant/après la traduction
            out = out.replace(source, "").strip()
        if single_block and PARA_SEP_RE.search(out):
            problem = "ta réponse contenait plusieurs blocs séparés par une ligne vide"
        elif out == source:
            problem = "ta réponse était identique au texte français"
        else:
            return out
    if problem.startswith("ta réponse était identique"):
        # Peut être légitime (noms propres, sigles…) : on garde, mais on le signale
        warn(rel_path, f"paragraphe {index} laissé identique au français, à vérifier")
        return out
    raise RuntimeError(f"paragraphe {index} : traduction invalide ({problem}), page non écrite")


RETRY_NOTE = (
    "\n\nAttention : lors d'une première tentative, {problem}. Réponds uniquement avec "
    "la traduction anglaise du bloc, en un seul bloc."
)


def translate_frontmatter(fm):
    if not fm or not needs_translation(fm):
        return fm
    return claude(
        f"Traduis les valeurs de ce frontmatter YAML en anglais (pas les clés), "
        f"en conservant les délimiteurs --- :\n\n{fm}",
        fm,
        max_tokens=2048,
    )


# ---------------------------------------------------------------- traitement d'une page

def git_show(ref, rel_path):
    result = subprocess.run(
        ["git", "show", f"{ref}:{rel_path}"],
        capture_output=True, text=True, encoding="utf-8", cwd=FR_DIR,
    )
    return result.stdout if result.returncode == 0 else None


def translate_new_page(rel_path, new_fr):
    """Nouvelle page : traduction paragraphe par paragraphe, alignement garanti."""
    fm, fr_paras = paragraphs(new_fr)
    en_paras = []
    for i in range(len(fr_paras)):
        en_paras.append(translate_para(rel_path, fr_paras, i, en_paras[-1] if en_paras else None))
    return assemble(translate_frontmatter(fm), en_paras)


def para_key(para):
    """Forme normalisée d'un paragraphe, pour la comparaison uniquement : ignore les
    retouches de mise en forme de GitBook (espaces, &#x20;, balises vides,
    largeur des séparateurs de tableau, images FR renommées ayant la même version EN)."""
    key = apply_image_map(para)
    key = key.replace("&#x20;", " ")
    key = re.sub(r"<(\w+)[^>]*>\s*</\1>", "", key)  # balises vides : <mark></mark>, <p></p>…
    key = re.sub(r"-{3,}", "---", key)
    key = re.sub(r"\s+", " ", key)
    key = re.sub(r" ?(<[^>]+>) ?", r"\1", key)
    key = re.sub(r" ?(\\) ?", r"\1", key)
    return key.strip()


def merge_en(old_paras, en_paras, new_paras):
    """Si chaque nouveau paragraphe FR est la réunion de paragraphes FR consécutifs
    (lignes vides retirées par GitBook), renvoie les paragraphes EN regroupés de la
    même façon ; sinon None."""
    result, cur = [], 0
    for new in new_paras:
        target = para_key(new)
        for k in range(cur + 1, len(old_paras) + 1):
            if para_key("\n".join(old_paras[cur:k])) == target:
                result.append("\n".join(en_paras[cur:k]))
                cur = k
                break
        else:
            return None
    return result if cur == len(old_paras) else None


def update_page(rel_path, old_fr, new_fr, en):
    old_fm, old_paras = paragraphs(old_fr)
    new_fm, new_paras = paragraphs(new_fr)
    en_fm, en_paras = paragraphs(en)

    if len(en_paras) != len(old_paras):
        warn(
            rel_path,
            f"page EN non alignée sur le FR ({len(en_paras)} paragraphes EN pour "
            f"{len(old_paras)} FR) : page non modifiée, à corriger à la main",
            block=True,
        )
        return None

    # Comparaison sur une forme normalisée : les retouches de mise en forme faites par
    # GitBook (espaces de fin, doubles espaces, images renommées) ne déclenchent pas
    # de retraduction.
    old_keys = [para_key(p) for p in old_paras]
    new_keys = [para_key(p) for p in new_paras]
    matcher = difflib.SequenceMatcher(a=old_keys, b=new_keys, autojunk=False)
    result = []
    changes = 0
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            result.extend(en_paras[i1:i2])
            continue
        if op == "replace":
            merged = merge_en(old_paras[i1:i2], en_paras[i1:i2], new_paras[j1:j2])
            if merged is not None:  # paragraphes FR recollés par GitBook, texte inchangé
                print(f"  = paragraphes FR {i1}..{i2 - 1} regroupés sans changement de texte")
                result.extend(merged)
                changes += 1
                continue
        if op in ("delete", "replace"):
            print(f"  - suppr./remplacement des paragraphes FR {i1}..{i2 - 1}")
        for j in range(j1, j2):
            print(f"  + traduction du paragraphe {j}")
            result.append(translate_para(rel_path, new_paras, j, result[-1] if result else None))
        changes += max(i2 - i1, j2 - j1)

    fm = translate_frontmatter(new_fm) if new_fm != old_fm else en_fm
    if not changes and fm == en_fm:
        print("  aucun changement de contenu (hors lignes « English version »)")
        return en  # mise en forme d'origine conservée
    return assemble(fm, result)


def process(rel_path):
    fr_path = FR_DIR / rel_path
    en_path = EN_DIR / rel_path
    if not fr_path.exists():
        print(f"[IGNORÉ] {rel_path} : absent côté FR")
        return
    new_fr = fr_path.read_text(encoding="utf-8")

    if not en_path.exists():
        print(f"[NOUVELLE PAGE] {rel_path}")
        en_path.parent.mkdir(parents=True, exist_ok=True)
        en_path.write_text(
            postprocess(translate_new_page(rel_path, new_fr)), encoding="utf-8", newline="\n"
        )
        return

    old_fr = git_show(BASE_REF, rel_path)
    if old_fr is None:
        warn(rel_path, f"aucune version FR à {BASE_REF} pour comparer : page EN non modifiée",
             block=True)
        return

    en = en_path.read_text(encoding="utf-8")
    print(f"[MISE À JOUR] {rel_path}")
    updated = update_page(rel_path, old_fr, new_fr, en)
    if updated is None:
        return
    updated = postprocess(updated)
    if updated != en.replace("\r\n", "\n"):
        en_path.write_text(updated, encoding="utf-8", newline="\n")
        print("  → page EN écrite")


def main():
    files = [f.strip() for f in os.environ.get("FILES", "").split() if f.strip()]
    errors = []
    for rel_path in files:
        if not rel_path.endswith(".md"):
            continue
        if rel_path in EXCLUDED:
            print(f"[EXCLU] {rel_path}")
            continue
        try:
            process(rel_path)
        except Exception as exc:  # une page en échec ne bloque pas les autres
            print(f"::error file={rel_path}::{exc}")
            errors.append(f"{rel_path} : {exc}")

    if warnings or errors:
        print("\nÀ vérifier :")
        for line in warnings + errors:
            print(f"  - {line}")
    # Échec du run uniquement si une page n'a pas pu être traitée ; les simples
    # avertissements restent visibles dans le résumé du run sans le faire échouer.
    sys.exit(1 if errors or blocking else 0)


if __name__ == "__main__":
    main()
