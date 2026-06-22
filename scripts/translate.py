import anthropic
import os
import pathlib
import subprocess
import re

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
files = os.environ["FILES"].split()

SYSTEM = """Tu es traducteur technique français → anglais pour la documentation
de l'Association pour la transition Bas Carbone (ABC) — méthode Bilan Carbone®.

Règles impératives :
- Traduis uniquement le texte visible. Ne traduis jamais l'intérieur des blocs de code.
- Préserve exactement la syntaxe GitBook : {% hint %}, {% tabs %}, {% details %}, tableaux, cards, liens.
- Copie les balises <figure>, <img ...> et tout emoji exactement tels quels.
- Conserve la même structure de titres (même nombre de #).
- "Bilan Carbone®" ne se traduit pas. Conserve aussi les sigles : ADEME, ABC, CSRD, GHG, ISO.
- "GES" se traduit par "GHG", sauf quand il fait partie d'un sigle composé comme "BEGES-r" (à conserver tel quel).
- Si le fichier est SUMMARY.md, traduis uniquement les titres affichés, jamais les chemins entre parenthèses.
- Réponds uniquement avec le contenu traduit, sans commentaire ni balise supplémentaire."""

HEADING_RE = re.compile(r'^(#{1,6})\s+')


def parse_sections(content):
    """Split markdown into (frontmatter, [(heading, body), ...])."""
    lines = content.split('\n')
    frontmatter_lines = []
    i = 0

    if lines and lines[0].strip() == '---':
        frontmatter_lines.append(lines[0])
        i = 1
        while i < len(lines):
            frontmatter_lines.append(lines[i])
            if lines[i].strip() == '---':
                i += 1
                break
            i += 1

    frontmatter = '\n'.join(frontmatter_lines)
    sections = []
    current_heading = None
    current_body = []

    for line in lines[i:]:
        if HEADING_RE.match(line):
            sections.append((current_heading, '\n'.join(current_body)))
            current_heading = line
            current_body = []
        else:
            current_body.append(line)

    sections.append((current_heading, '\n'.join(current_body)))
    return frontmatter, sections


def split_paragraphs(body):
    """Split a section body into paragraphs (double-newline separated blocks)."""
    blocks = re.split(r'\n\n+', body)
    return blocks


def join_paragraphs(paras):
    return '\n\n'.join(paras)


def reconstruct(frontmatter, sections):
    parts = []
    if frontmatter:
        parts.append(frontmatter)
    for heading, body in sections:
        if heading is not None:
            parts.append(heading)
        if body:
            parts.append(body)
    return '\n'.join(parts)


def get_old_fr(rel_path):
    result = subprocess.run(
        ['git', 'show', f'HEAD~1:{rel_path}'],
        capture_output=True, text=True, encoding='utf-8', cwd='fr'
    )
    return result.stdout if result.returncode == 0 else None


def claude(prompt, max_tokens=8192):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


def translate_full(content):
    return claude(f"Traduis ce fichier markdown en anglais :\n\n{content}")


def translate_paragraph(heading, para):
    context = f"Section : {heading}\n\n" if heading else ""
    return claude(f"Traduis ce bloc markdown en anglais :\n\n{context}{para}", max_tokens=2048)


def translate_section(heading, body):
    text = f"{heading}\n{body}" if heading else body
    translated = claude(f"Traduis cette section markdown en anglais :\n\n{text}", max_tokens=4096)
    t_lines = translated.split('\n')
    if t_lines and HEADING_RE.match(t_lines[0]):
        return t_lines[0], '\n'.join(t_lines[1:])
    return heading, translated


def translate_frontmatter(fm):
    return claude(f"Traduis les valeurs de ce frontmatter YAML en anglais (pas les clés) :\n\n{fm}", max_tokens=256)


def find_changed_sections(old_content, new_content):
    _, old_secs = parse_sections(old_content)
    _, new_secs = parse_sections(new_content)

    if len(old_secs) != len(new_secs):
        return None  # structural change → full retranslation

    changed = {i for i, ((nh, nb), (oh, ob)) in enumerate(zip(new_secs, old_secs))
               if nh != oh or nb != ob}
    return changed


def translate_section_partial(heading, old_fr_body, new_fr_body, en_body):
    """Retranslate only changed paragraphs within a section, preserving EN manual edits."""
    old_paras = split_paragraphs(old_fr_body)
    new_paras = split_paragraphs(new_fr_body)
    en_paras = split_paragraphs(en_body)

    # If paragraph counts don't align → retranslate whole section
    if len(old_paras) != len(new_paras) or len(new_paras) != len(en_paras):
        label = (heading or '(intro)')[:60]
        print(f"    paragraph count mismatch in [{label}] → retranslating whole section")
        return translate_section(heading, new_fr_body)

    changed_paras = {i for i, (n, o) in enumerate(zip(new_paras, old_paras)) if n != o}

    if not changed_paras:
        # Heading changed but no body paragraphs changed — translate heading only
        translated_heading = claude(
            f"Traduis ce titre markdown en anglais :\n\n{heading}", max_tokens=128
        ) if heading else heading
        return translated_heading, en_body

    new_en_paras = list(en_paras)
    for j in sorted(changed_paras):
        print(f"    paragraph {j}")
        new_en_paras[j] = translate_paragraph(heading, new_paras[j])

    new_heading = heading
    if heading:
        # Check if heading itself changed vs old section heading
        # (handled by caller; retranslate heading along with first changed para)
        pass

    return new_heading, join_paragraphs(new_en_paras)


for rel_path in files:
    rel_path = rel_path.strip()
    if not rel_path.endswith('.md'):
        continue

    fr_path = pathlib.Path('fr') / rel_path
    en_path = pathlib.Path('en') / rel_path

    if not fr_path.exists():
        print(f"Skipping {rel_path}: not found in fr/")
        continue

    new_fr = fr_path.read_text(encoding='utf-8')
    old_fr = get_old_fr(rel_path)

    # New file or no previous FR version → full translation
    if not en_path.exists() or old_fr is None:
        print(f"[FULL] {rel_path}")
        en_path.parent.mkdir(parents=True, exist_ok=True)
        en_path.write_text(translate_full(new_fr), encoding='utf-8')
        print(f"  → done")
        continue

    fr_fm, fr_secs = parse_sections(new_fr)
    old_fr_fm, old_fr_secs = parse_sections(old_fr)
    changed = find_changed_sections(old_fr, new_fr)

    if changed is None:
        print(f"[FULL - structural change] {rel_path}")
        en_path.write_text(translate_full(new_fr), encoding='utf-8')
        print(f"  → done")
        continue

    if not changed and fr_fm == old_fr_fm:
        print(f"[SKIP] {rel_path} — no changes detected")
        continue

    en_content = en_path.read_text(encoding='utf-8')
    en_fm, en_secs = parse_sections(en_content)

    # Section count mismatch between EN and FR → full retranslation
    if len(fr_secs) != len(en_secs):
        print(f"[FULL - EN/FR mismatch] {rel_path}")
        en_path.write_text(translate_full(new_fr), encoding='utf-8')
        print(f"  → done")
        continue

    print(f"[PARTIAL] {rel_path} — {len(changed)} section(s) changed")

    new_en_secs = list(en_secs)
    for i in sorted(changed):
        new_h, new_b = fr_secs[i]
        old_h, old_b = old_fr_secs[i]
        _, en_b = en_secs[i]
        label = (new_h or '(intro)')[:60]
        print(f"  section {i}: {label}")
        new_en_secs[i] = translate_section_partial(new_h, old_b, new_b, en_b)

    # Translate frontmatter if changed
    if fr_fm != old_fr_fm:
        print(f"  translating frontmatter")
        en_fm = translate_frontmatter(fr_fm)

    en_path.write_text(reconstruct(en_fm, new_en_secs), encoding='utf-8')
    print(f"  → done ({len(changed)} section(s) processed, EN manual edits preserved)")
