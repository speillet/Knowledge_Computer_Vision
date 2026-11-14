# Reference-note deepening — 2026-11-14

Request: "enrichie au maximum les fiches existantes, puis pr et merge" — deepen
the existing reference notes as far as their subjects justify, then open a pull
request and merge it. In this vault, *fiches* are the canonical reference notes
under `references/`; *cartes* are flashcards. The 2026-11-08 pass already
deepened all 282 card answers; this pass targets the reference notes.
Mode: `approfondir` with source-based corrections.
Scope: all 60 existing subjects, 60 canonical references and their 282 cards
across 14 topics. The clean starting point is `main` at `76fda5a`, on branch
`docs/reference-depth-20261114`.

## Starting state

The body of each reference before its per-card appendices ("Guided reasoning"
and "Additional technical explanations") contained 312 to 2,450 words, with a
median near 370. Most of the twelve contract sections of
`specs/001-cv-knowledge-base/learning-design.md` held one to three sentences.
The English migration also left mistranslations in references and cards, for
example "driver variant" for the project's *pilot* variant, "gel" for
*freeze*, and French decimal commas in English prose.

## Delivery criteria

- Develop every contract section of each reference (problem, intuition,
  prerequisites, assumptions, procedure, mathematics, parameters, properties,
  cost and implementation, evaluation with baseline and controlled variation,
  failure modes and diagnosis, alternatives and sources), or justify why a
  section does not apply. Additions explain a mechanism, derivation, parameter
  effect, assumption, counterexample, diagnostic check or conditional choice;
  length is not a goal.
- Verify central claims against the exact passage of a primary paper,
  versioned official documentation or code. Separate scientific sources from
  implementation sources (FR-036). Record inaccessible sources as not
  verifiable. Context7 is not available in this session; API claims fall back
  to official versioned documentation, and reports say so.
- Mark constructed calculations and proposed experiments as such. Each new
  numerical example is recomputed by a script under `checks/`.
- Fix mistranslations that alter or obscure technical meaning in references
  and cards. Change an expected answer only for a sourced correction or a
  meaning-restoring language fix, and record it.
- Preserve every pedagogical ID, card question, objective, family, provenance,
  tags, target deck, legacy synchronization comment, reference H1 title,
  front-matter field other than `revision`, per-card headings and heading
  anchors used by links. Increment each changed reference's `revision` once
  and keep `statut: redige`.
- Add no card. Register valuable new-card ideas as pending proposals in
  `docs/revues/propositions.md`; the learner decides.
- Write one report per subject and a final overview. Record corrections in
  `vault/01-Parcours/Suivi-pilote.md`.
- Run the vault, catalogue, learning-path, unit-test and inventory checks;
  compare identities and protected fields against the external starting
  snapshot; check local links and anchors; review the diff; commit; open a
  pull request and merge it after the checks pass.

## Baseline evidence

The following commands were executed before edits:

| Check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, 0 stale |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 62 tests pass |
| `inventaire_cartes.py vault` | 60 card files, 282 cards, no anomalies |

The starting inventory and a copy of the vault are saved outside the
repository for the final comparison. This pass is agent self-review: it
establishes neither independent scientific validation, learner proficiency nor
AnkiDroid rendering. A new Anki package remains to be built with `paquet-anki`.
