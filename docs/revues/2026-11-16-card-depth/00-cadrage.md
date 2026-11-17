# Deepening of the shortest cards, with figures — 2026-11-16

Request: "continue à enrichir les cartes les moins fournies. Si tu peux, regarde pour
certains concepts complexes si tu peux mettre des schémas". The learner asked to keep
deepening the least developed cards and, where possible, to add diagrams for complex
concepts. Asked to decide the scope, the figure format and the delivery, the learner
chose:

- **Scope:** the 45 cards whose answers have fewer than 340 lexical words. These
  are the cards below the 15th percentile of the 294-card deck (minimum 260,
  median 374, maximum 586). They span 33 subjects.
- **Figures:** SVG files in `vault/99-Ressources/`, embedded in cards and references,
  like the existing SORT figure. Figures are packaged for AnkiDroid and rendered by
  Obsidian. Roughly 8 to 12 targeted figures for concepts that text explains poorly:
  geometry, graphs, timelines, distributions and data flows.
- **Delivery:** a pull request, merged once the checks pass, then a rebuilt Anki
  package and a new release.

Mode: `approfondir`. Card count unchanged (294); no card is added.

## Delivery criteria

- Audit each card first. Check the central claims at their exact passage, in a
  primary paper or in code at a tag or commit. Classify findings by severity and
  correct the reference first.
- Deepen each card with what its recall objective still needs: a mechanism, a
  derivation, a constructed calculation, a parameter effect, a counterexample or a
  discriminating check. Do not paraphrase or pad. Constructed numbers are labelled
  as such and recomputed by a stdlib script under `checks/`.
- Preserve IDs, questions, objectives, families, tags, target decks, legacy
  comments, reference H1 titles and per-card headings. Change an expected answer
  only for a sourced correction, recorded with its old and new text. Increment
  each changed reference's `revision` once and keep `statut: redige`.
- Figures:
  - self-contained SVG with a light background, a title and a description;
  - labels legible at phone width;
  - figures drawn to scale have their coordinates recomputed, and other figures
    are captioned as schematic;
  - each figure is rendered at 380 px and 1080 px and inspected before
    embedding.
- Write one report per subject and an overview. Log corrections in
  `vault/01-Parcours/Suivi-pilote.md`. Run the vault, catalogue, learning-path,
  unit-test and inventory checks, plus a protected-field comparison against `main`.
  Build the package, open the pull request and merge it, then publish the
  release.

## Baseline evidence

Executed on `main` before edits: at `498b6ae` and `6cef833`, which differ only in the
progress log. The work branch is `docs/card-depth-20261116`.

| Check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 294 cards |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, 0 stale |
| `python3 scripts/learning_path.py` | OK, minimum 260 lexical words |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 62 tests pass |
| `inventaire_cartes.py vault --json` (at `6cef833`) | Saved outside the repository for the final comparison |

The coordinating agent deepened CV-PIPELINE-001 as a pilot and drew the first two
figures. Six subagents then processed the other 44 cards from a shared brief, on
disjoint files. This is agent self-review: it establishes neither independent
scientific validation, learner proficiency nor AnkiDroid rendering.
