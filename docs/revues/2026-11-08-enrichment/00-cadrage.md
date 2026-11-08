# Existing-card enrichment — 2026-11-08

Request: enrich the existing cards as far as their recall objectives justify,
check their relevance, commit through a pull request and merge it.
Mode: `approfondir` with source-based corrections.
Scope: all 60 existing subjects, 60 canonical references and 282 cards across
14 topics. The clean starting branch is `main`.

## Delivery criteria

- Review the reference before its cards and develop mechanisms, assumptions,
  calculations, counterexamples and diagnostic decisions specific to each question.
- Preserve all pedagogical IDs, derived Anki GUIDs, legacy synchronization
  comments, questions, objectives, families, tags and target decks. Correct an
  expected answer only where the source or an explicit calculation requires it.
- Keep finite recall criteria separate from optional explanation. More words
  are useful only when they explain something additional.
- Use English for new and revised repository prose. Increment each changed
  reference revision and preserve `statut: redige` and agent provenance.
- Consult primary scientific sources; use Context7 for implementation/API
  contracts. Distinguish checked source claims, constructed examples and proposed
  experiments. Record inaccessible sources and limits of verification.
- Record one report per subject and a final overview. Carry proposals through
  the existing register; do not add cards without the learner's decision.
- Run vault, catalogue, learning-path, unit-test and inventory checks; compare
  identities and protected fields against the external starting snapshot.
- Review the full diff, create focused commits on
  `docs/deepen-existing-cards-20261108`, open a PR and merge after checks.

## Baseline evidence

The following commands were executed before edits:

| Check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, 0 stale |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 253 lexical words |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 62 tests pass |
| `inventaire_cartes.py vault` | 60 card files, 282 cards, no anomalies |

The complete starting inventory and Markdown snapshot are saved outside the
repository for final comparison. No reference is independently reviewed by this
work; no learner proficiency or AnkiDroid rendering is established. A new Anki
package is outside this content-only pass and remains to be republished with
`paquet-anki` after merge.
