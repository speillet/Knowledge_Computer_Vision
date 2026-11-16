# Four approved cards — scope — 2026-11-09

Request: the learner explicitly accepted the four registered proposals by
selecting “Ajouter les quatre cartes proposées”. Continue the earlier delivery
instruction: commit through a PR and merge after review and checks.
Mode: `ajouter`, following `revue-cartes`.
Starting point: clean `main`, commit `76fda5a87a41a9fd742a44d2774abe69eea24807`.
Branch: `docs/add-four-approved-cards-20261109`.

## Approved additions

| Proposal | New ID | Recall objective | Distinction from existing cards |
| --- | --- | --- | --- |
| P-CV-FUSION-01 | CV-FUSION-007 | Evaluate bias and temporal structure when mean NIS looks nominal | CV-FUSION-002 defines NIS and its gate; this card judges competing innovation sequences |
| P-CV-SE3-01 | CV-SE3-007 | Calculate a transported SE(3) covariance and interpret its coupling | CV-SE3-003 compares perturbation conventions; this card computes a lever-arm covariance and distinguishes tangent translation from origin displacement |
| P-CV-SEGMENTATION-01 | CV-SEGMENTATION-005 | Calculate PQ through explicit segment matching and SQ/RQ decomposition | Existing questions define output types or assess metrics; none requires a numerical PQ calculation |
| P-CV-METRIQUES-TEMPS-01 | CV-METRIQUES-TEMPS-006 | Calculate global identity counts and IDF1 after a trajectory fragmentation | CV-METRIQUES-TEMPS-001 distinguishes detection from identity; this card quantifies the effect of fragmentation duration |

## Delivery criteria

- Consult exact primary passages before authoring each reference section and
  dependent card. Label constructed cases, deductions and unexecuted protocols.
- Write English prose, finite expected answers, useful explanations and
  plausible blocking errors; use the existing card template and answer-depth
  requirement without padding.
- Preserve the complete existing 282 card blocks and their IDs, GUIDs,
  questions, answers, tags, decks and legacy synchronization comments.
- Add exactly the four approved IDs; update four canonical references first,
  increment each revision once and preserve status/provenance.
- Regenerate the catalogue, update current-state counts and preserve dated
  experiment/translation evidence. Mark accepted proposals completed only
  after their cards are written and verified.
- Recalculate the examples, review links and diff, and run vault, catalogue,
  curriculum, unit-test, conversion and inventory-comparison checks.
- Record one report per subject and a final overview. No independent scientific
  review, real CV experiment, phone rendering or package publication is implied.

## Baseline

Before content edits, the resumed session verified: 60 references, 282 cards,
142 vault Markdown documents; catalogue 19 documents with none stale;
prerequisite/depth validation OK; 62 unit tests pass. The complete inventory
and vault Markdown snapshot are stored outside the repository for comparison.

## Resumption on 2026-11-16

The 2026-11-09 session stopped after drafting CV-FUSION-007 and its reference
section, without committing. Meanwhile #27 deepened the 60 references, #28
added twelve cards from proposals accepted on 2026-11-15, and #29 recorded the
first package release. Because the 2026-11-09 decision was only in this
unmerged branch, the register sections of 2026-11-14 and 2026-11-15 still
describe the four proposals as pending.

On the learner's request, the branch was brought up to `main` at `6cef833` and
the uncommitted draft reapplied; the conflicts in the register and the Kalman
reference were resolved by keeping `main` and adding the draft. The criteria
above still apply, with these updates:

- Preserve the 294 existing card blocks (282 at the original baseline); the
  pass adds four cards, 294 → 298.
- Build each card on the deepened reference, which already develops the
  material of the four proposals, and increment each reference revision once
  from its value on `main`.
- Recompute every constructed number with a stdlib script under `checks/`,
  as in the 2026-11-15 pass. Context7 is unavailable in this session; API and
  evaluator conventions rest on versioned code.
- CV-FUSION-007 was finished by the coordinating agent; CV-SE3-007,
  CV-SEGMENTATION-005 and CV-METRIQUES-TEMPS-006 were written by three
  subagents from a shared brief, on disjoint files. Shared files (register,
  progress log, catalogue, counts) were edited only by the coordinator.
- Record the completion in the register without rewriting the 2026-11-14 and
  2026-11-15 sections, and deliver through a pull request merged once the
  checks pass.

Baseline executed on 2026-11-16 in a clean worktree of `main` at `6cef833`:

| Check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 294 cards |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, 0 stale |
| `python3 scripts/learning_path.py` | OK: 60 references, 294 cards, minimum 260 lexical words |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 62 tests pass |
| `inventaire_cartes.py vault --json` | Saved outside the repository for the final comparison |
