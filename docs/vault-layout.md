# Organization of the vault by theme

The request of the 2026-10-18 resumes the organization of [Knowledge_AI_Engineering](https://github.com/speillet/Knowledge_AI_Engineering/tree/5fdbfe259e53d01361cf6337f6c494b4663db592): a folder numbered by theme, files numbered in the theme and central navigation. The full explanations and the flashcards keep their roles distinct.

```text
vault/
├── 00-Accueil.md
├── 01-Parcours/
├── 40-features-matching/
│   ├── 00-index.md
│   ├── 41-sift.md                    # flashcards
│   ├── 42-orb.md                     # flashcards
│   └── references/
│       ├── 41-sift.md                # complete explanation
│       └── 42-orb.md
├── 50-calibration-geometrie/
│   ├── 00-index.md
│   ├── 51-ransac-homographie.md
│   ├── 52-calibration-zhang.md
│   └── references/
│       ├── 51-ransac-homographie.md
│       └── 52-calibration-zhang.md
├── 80-detection-pose/
├── 110-tracking-association/
├── 130-evaluation-fiabilite/
└── 99-Ressources/
```

The fourteen themes each have an index and reference notes. The [Summary](../vault/00-Accueil.md) exposes this state and the inventory describes the gaps. `scripts/vault_sections.json` associates each file with its domain, title and introduction, and serves as the controller.

## Add a reference note and its flashcards

1. Choose the theme according to the problem, then the numbered file: for example `41-sift.md` in `40-features-matching`. After nine topics, use an explicit rank like `40-010-nouveau-sujet.md` to keep the theme stable.
2. Place the complete reference note with the same name in `references/`. Its front matter preserves the domain, the provenance, the depth and the editorial states.
3. Place the flashcards at the root of the theme. Their target is `CV::Pilote::<directory-name>`. The pilot uses the Obsidian_to_Anki-compatible source syntax with note type `CV-Pilote`, four fields and one template; `scripts/build_apkg.py` exports it directly to an Anki package.
4. Link reference notes and flashcards, update the theme index, home and inventory.
5. Run the controller and tests. The novelties of the pilot must still pass the application tests before generalization.

Guides, indexes, and references do not contain any start markers on an isolated line, even in a block of code: the scan of the plugin does not necessarily ignore these examples. Keep templates out of the vault, in `anki/`.

## Move existing content

Preserve the pedagogical ID, its tag and the digital comment Anki if it exists. Fix Markdown links, wikilinks from the root, media paths and target deck. The change of path does not create a new concept or identity. The move and change of deck must still be observed on a real note already revised before declaring the preserved history.

The 47 flashcards of the initial batch retained their identifiers and texts during the reclassification. The current catalog includes 60 reference notes and 282 flashcards in the 14 themes. `python3 scripts/sync_catalog.py` updates index, home, inventory and business paths; `--check` detects outdated navigation without writing.
