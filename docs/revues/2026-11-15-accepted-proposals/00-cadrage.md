# Accepted proposals and pending decisions — 2026-11-15

Request: `/revue-cartes` without an argument, after the
[2026-11-14 reference-deepening pass](../2026-11-14-reference-depth/00-bilan.md).
Asked for the scope, the learner chose the pending decisions, then decided:

- **Accept** the twelve priority proposals of the 2026-11-14 overview:
  P-CV-ECC-01, P-CV-PIPELINE-02, P-CV-MATCHING-02, P-CV-EPIPOLAIRE-01,
  P-CV-SORT-01, P-CV-ICP-02, P-CV-STEREO-01, P-CV-WATERSHED-01, P-CV-FLANN-01,
  P-CV-HANDEYE-01, P-CV-DETECTEURS-01 and P-CV-IOU-AP-01.
- **Reword** the questions of CV-SOT-002 and CV-MATCH-APPRIS-005 with the
  wording proposed in the 2026-11-14 subject reports, because their fronts hint
  at the answers.
- **Keep** the four partly overlapping cards: CV-MATCHING-001 with
  CV-CORNERS-001, and CV-MATCHING-002 with CV-FAST-BRIEF-003. Their angles
  differ: concept against calculation, and stage roles against the differences
  with ORB.
- **Leave pending** the other 98 proposals: 94 from 2026-11-14 and the 4
  earlier ones.
- **Deliver** through a pull request, merged once the checks pass.

Mode: `ajouter` for the twelve accepted proposals. Scope: twelve subjects
receive one card each (282 → 294 cards), and two subjects receive a reworded
question.

## Delivery criteria

- Write each card from its registered proposal, following the card template,
  with the next free ID, `Provenance: agent`, the proposal's family and
  criteria, a standalone front that does not reveal the answer, and at least
  180 lexical words in the answer.
- Verify each central claim at the exact passage of a primary paper or of code
  at a release tag or commit. Mark constructed numbers as such and recompute
  them with a stdlib script under `checks/`. Context7 is unavailable in this
  session; API claims rest on versioned code.
- Correct the reference first where verification shows it is wrong or
  imprecise, list the new card under its related flashcards, increment
  `revision` once and keep `statut: redige`.
- Preserve every existing ID, Anki identity, objective, family, tag, target
  deck and expected answer. The two reworded questions keep their IDs and
  recall objectives.
- Mark the twelve proposals completed with their IDs, record the decisions in
  the register and the additions in `vault/01-Parcours/Suivi-pilote.md`, and
  update current-state card counts outside generated files.
- Write one report per subject and an overview; run the vault, catalogue,
  learning-path, unit-test and inventory checks; compare the inventory with
  the starting one (twelve additions, no removal); review the diff; open a pull
  request and merge it.

## Baseline evidence

Executed on `main` at `951c0b3` before edits, on branch
`docs/accepted-proposals-20261115`:

| Check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, 0 stale |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 62 tests pass |
| `inventaire_cartes.py vault --json` | Saved outside the repository for the final comparison |

The first card, CV-ECC-004, was written as a pilot by the coordinating agent;
four subagents wrote the other eleven from a shared brief, on disjoint files.
This is agent self-review: it establishes neither independent scientific
validation, learner proficiency nor AnkiDroid rendering.
