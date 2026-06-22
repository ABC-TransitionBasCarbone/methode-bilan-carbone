# Tuto : Mettre en place la traduction automatique FR → EN sur un nouveau GitBook

Ce guide explique comment reproduire le pipeline de traduction automatique sur un nouveau GitBook ABC.
Le système utilise GitHub Actions + l'API Claude (Anthropic) pour traduire automatiquement les pages FR en EN, paragraphe par paragraphe, en préservant les modifications manuelles faites directement sur la version EN.

---

## Ce dont tu as besoin avant de commencer

- Un accès GitHub à l'organisation **ABC-TransitionBasCarbone**
- Un accès à l'espace GitBook FR à connecter (et créer l'espace EN correspondant)
- La clé API Anthropic → disponible sur **Claude Platform** avec le compte Gmail ABC (`associationbilancarbone@gmail.com`)

---

## Étape 1 — Créer le repo GitHub

1. Sur GitHub, dans l'organisation **ABC-TransitionBasCarbone**, créer un nouveau repo (ex. `guide-de-com`, `referentiel-conformite`, etc.)
2. Initialiser avec un premier commit (README suffit)
3. Créer une deuxième branche appelée `translated-en` :
   ```
   git checkout -b translated-en
   git push origin translated-en
   git checkout main
   ```

À la fin de cette étape, le repo a deux branches :
- `main` → contiendra les pages FR (source)
- `translated-en` → contiendra les pages EN (générées automatiquement)

---

## Étape 2 — Connecter les GitBook à GitHub (Git Sync)

### Espace FR → branche `main`

1. Dans GitBook, ouvrir l'espace FR concerné
2. Aller dans **Settings → GitHub**
3. Sélectionner l'organisation `ABC-TransitionBasCarbone`, le repo créé à l'étape 1, branche **`main`**
4. Choisir **GitBook → GitHub** (GitBook est la source)
5. Lancer la synchronisation

### Espace EN → branche `translated-en`

1. Créer un nouvel espace GitBook vide (ce sera la version EN)
2. Aller dans **Settings → GitHub**
3. Même repo, branche **`translated-en`**
4. Choisir **GitHub → GitBook** (GitHub est la source — c'est le bot qui écrira ici)
5. Lancer la synchronisation

---

## Étape 3 — Copier le workflow de traduction

1. Dans le repo, créer le dossier `.github/workflows/` s'il n'existe pas
2. Copier le fichier `translate-to-english.yml` depuis le repo `methode-bilan-carbone`
3. Copier aussi le fichier `scripts/translate.py` dans un dossier `scripts/` à la racine du repo

> **Conseil : utiliser Claude Code ou Codex**
> Tu peux demander directement à Claude Code (terminal) ou Codex d'adapter le prompt de traduction :
> *"Dans le fichier scripts/translate.py, adapte le prompt SYSTEM pour ce nouveau contexte : [décrire le GitBook]"*

### Adapter le prompt si nécessaire

Dans `scripts/translate.py`, le bloc `SYSTEM` contient les instructions de traduction.
Il est déjà générique mais tu peux l'ajuster :

```python
SYSTEM = """Tu es traducteur technique français → anglais pour la documentation
de l'Association pour la transition Bas Carbone (ABC) — méthode Bilan Carbone®.
...
```

**Ce qu'on change selon le GitBook :**
- Mentionner le nom du document concerné (ex. "guide de communication", "référentiel de conformité")
- Ajouter des termes à ne pas traduire spécifiques au document (ex. noms propres, sigles métier)
- Adapter les règles si la structure markdown est différente

**Ce qu'on ne change pas :**
- Les règles sur la syntaxe GitBook (`{% hint %}`, tableaux, etc.)
- Le modèle (`claude-sonnet-4-6`)
- La logique de traduction partielle (paragraphe par paragraphe)

---

## Étape 4 — Ajouter la clé API Anthropic comme secret GitHub

1. Aller sur le repo GitHub → **Settings → Secrets and variables → Actions**
2. Cliquer **New repository secret**
3. Nom : `ANTHROPIC_API_KEY`
4. Valeur : récupérer la clé sur **Claude Platform** → [console.anthropic.com](https://console.anthropic.com) → connecté avec `associationbilancarbone@gmail.com` → **API Keys**
5. Sauvegarder

---

## Étape 5 — Traduction initiale de toutes les pages existantes

Avant de brancher l'automatisation, il faut traduire une première fois l'intégralité des pages FR déjà existantes. Cette étape se fait **en local, une seule fois**, via **Claude Code** directement dans le terminal — pas besoin de script ni de clé API à configurer.

### Procédure

1. Télécharger **Claude Code** : [claude.ai/code](https://claude.ai/code) et l'installer

2. Cloner le repo en local :
   ```bash
   git clone https://github.com/ABC-TransitionBasCarbone/[nom-du-repo].git
   cd [nom-du-repo]
   ```

3. Ouvrir Claude Code dans le dossier du repo :
   ```bash
   claude
   ```

4. Demander à Claude Code de traduire toutes les pages, par exemple :
   > *"Traduis tous les fichiers .md du dossier en anglais, en suivant les mêmes règles que pour la méthode Bilan Carbone® (préserver la syntaxe GitBook, ne pas traduire Bilan Carbone®, GES → GHG sauf BEGES-r, etc.). Écris les fichiers traduits dans le dossier `en/` en conservant la même arborescence."*

   Claude Code lira les fichiers FR et écrira directement les fichiers EN traduits.

5. Vérifier quelques fichiers dans le dossier `en/` pour s'assurer que la traduction est correcte.

6. Pousser le résultat sur `translated-en` :
   ```bash
   git checkout translated-en
   git add -A
   git commit -m "Initial translation of all FR pages to EN"
   git push origin translated-en
   ```

7. GitBook EN se synchronisera automatiquement depuis la branche `translated-en`.

À partir de là, le workflow GitHub Actions prend le relais automatiquement pour toutes les modifications futures.

---

## Étape 6 — Tester

### Test manuel via GitHub Actions

1. Sur GitHub, aller dans **Actions → Translate FR to EN**
2. Cliquer **Run workflow**
3. Dans le champ `files`, entrer le chemin d'un fichier FR (ex. `README.md`)
4. Lancer et vérifier que le fichier traduit apparaît dans la branche `translated-en`

### Fonctionnement automatique ensuite

Dès qu'une page est modifiée dans GitBook FR (et donc pushée sur `main`), le workflow se déclenche automatiquement et met à jour uniquement les paragraphes modifiés sur `translated-en`.

---

## Comportement du système

| Situation | Comportement |
|-----------|-------------|
| Nouvelle page FR | Traduction complète |
| Paragraphe FR modifié | Seul ce paragraphe est retraduit en EN |
| Paragraphe EN édité manuellement, FR inchangé | Modification EN préservée |
| Paragraphe EN édité manuellement ET même paragraphe modifié en FR | Le FR écrase l'EN (logique : FR = source de référence) |
| Structure de la page changée (ajout/suppression de sections) | Retraduction complète de la page |

---

## En cas de problème

- **Le workflow ne se déclenche pas** → vérifier que le fichier `.yml` est bien dans `.github/workflows/` sur la branche `main`
- **Erreur `ANTHROPIC_API_KEY`** → vérifier que le secret est bien ajouté dans Settings → Secrets
- **GitBook ne synchronise pas** → aller dans GitBook Settings → GitHub → relancer une synchronisation manuelle
- **La traduction écrase des modifs EN** → vérifier que la modification FR ne porte pas sur le même paragraphe

Pour toute question, demander à **Quentin** ou utiliser **Claude Code** directement dans le terminal en ouvrant le dossier du repo.
