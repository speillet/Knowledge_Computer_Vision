---
name: paquet-anki
description: "Build and verify CV-Pilote.apkg from the vault, compare package versions and guide AnkiDroid import. Use for Anki export, package generation, phone import and requested releases. Preserve update identities. Use revue-cartes for changes to card content."
---

# Anki package for AnkiDroid

Cards live in the vault in `START/END` format. The phone reads Anki packages.
Build `CV-Pilote.apkg` with `scripts/build_apkg.py`, verify it, publish a GitHub
release when requested, and explain its AnkiDroid import.

The package replaces the historical Obsidian_to_Anki → AnkiConnect → Anki Desktop
workflow, suspended for the pilot. Do not feed the same collection through both
workflows: their note identities differ and would create duplicates.

## What preserves updates

Each note GUID is derived from its pedagogical ID, such as `CV-SIFT-003`.
Reimporting a newer package updates existing notes when the package's notes are
newer. The 2026-10-24 simulation with `anki` 26.9.3 also preserves review history
after content and style changes. Therefore:

- Never change an existing card's ID: that creates a different note and leaves
  the old one on the phone.
- Preserve `modelId`, name, fields and template count in `anki/model.json`.
  Simulate any `anki/*.html` or `style.css` change first.
- Imports never delete a note. Remove retired cards manually in AnkiDroid.
- Keep the vault authoritative. A newer phone edit can block a conditional update;
  resolve the conflict in the vault and rebuild.

## 1. Check status

```sh
git status --short
git branch --show-current
python3 scripts/check_vault.py
python3 -m unittest discover -s tests
```

If validation fails, stop and report it; the generator rejects invalid content.
Use `revue-cartes` for card corrections.

## 2. Build and verify

```sh
uv run --no-project --with genanki==0.13.1 python scripts/build_apkg.py
```

This writes the unversioned `dist/CV-Pilote.apkg` and
`dist/CV-Pilote-manifest.json`, then verifies the package. Require `OK`, a note
count matching the vault's card count, 14 decks and the expected media.
`ConversionError` identifies the card and unsupported syntax: heading, table,
quotation or unmatched `$`. Compare the error with `docs/export-apkg.md`;
fix a converter that rejects supported syntax, and use `revue-cartes` for actual
card defects.

To identify changes since the latest release:

```sh
gh release download --pattern CV-Pilote-manifest.json --dir <tmp>
python3 scripts/build_apkg.py --compare <tmp>/CV-Pilote-manifest.json
```

No existing release means an initial publication. List added, modified and
**removed** cards; removed cards require manual deletion on the phone.

## 3. Simulate when required

Simulation is mandatory when the builder, `anki/` or genanki version changes,
and recommended before the first publication:

```sh
uv run --no-project --python 3.12 --with anki==26.9.3 --with genanki==0.13.1 \
  python scripts/simulate_anki_import.py
```

The simulation builds and imports into a disposable collection, reimports an
unchanged package, reviews three cards, changes content and then style, and
imports again. Duplicates, recreated notes, unapplied updates or changed review
history fail the check. This does not establish phone behavior or rendering.

## 4. Publish on request, after confirmation

A release is public, as is the repository. Reference links point to `main`;
publish only from a clean, synchronized `main` so content, links and tag agree.

1. Require `main`, empty `git status --porcelain`, and `HEAD` equal to `origin/main`
   after fetching. Rebuild; the manifest must not have a `-modifie` suffix.
2. Show the proposed tag, counts and added/modified/removed cards. Wait for explicit
   user confirmation before publication.
3. Publish:

   ```sh
   gh release create anki-YYYYMMDD-HHMM dist/CV-Pilote.apkg dist/CV-Pilote-manifest.json \
     --target "$(git rev-parse HEAD)" --latest \
     --title "Anki package YYYY-MM-DD" --notes "<counts; added; modified; removed>"
   ```

4. Verify that the stable download URL redirects to the new asset:
   `curl -sI https://github.com/speillet/Knowledge_Computer_Vision/releases/latest/download/CV-Pilote.apkg`.

## 5. Import on the phone

Explain these steps:

1. If a package release exists, open
   <https://github.com/speillet/Knowledge_Computer_Vision/releases/latest/download/CV-Pilote.apkg>
   in the Android browser. Otherwise use the local copy below.
2. Open the download with AnkiDroid, or use its **Import** menu and select the file.
   Keep the default update-if-newer option.
3. On first import, `CV::Pilote` appears with topic subdecks.
4. For updates, repeat the import. The tested engine preserves identities and
   history; confirm this behavior on the installed AnkiDroid version.
5. For a removed card, search `tag:cv_id::<ID>` in AnkiDroid's browser and delete
   the note.

A local copy also works: transfer `dist/CV-Pilote.apkg` by cable or email, then
open it with AnkiDroid.

## 6. Report

State commands and results, counts and changes since the latest release, and
any release link. Identify remaining phone checks: MathJax, SVG image, code,
links and reimport after reviewing cards.

Record publications and actual phone trials in `vault/01-Parcours/Suivi-pilote.md`
with date, AnkiDroid version and observations. Never commit `dist/`.
