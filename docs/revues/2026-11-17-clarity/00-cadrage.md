# Clarity pass on every card — 2026-11-17

Request: "je trouve des notions trop compliquées et il manque des étapes intermédiaires.
Corrige cela." The learner finds some notions too complicated and intermediate steps
missing. Asked to decide the scope and approach, the learner chose:

- **Scope:** a pilot on one subject, validation of the style, then the whole vault
  (60 references, 298 cards).
- **Gaps to fix:** calculations without their steps, undefined acronyms and terms,
  reasoning that skips steps, and missing prerequisite notions.
- **Strategy:** restructure without losing anything. The expected answer stays short; the
  explanation follows intuition → steps → formula → limits; advanced asides move to the
  reference note.
- **Branch:** clarify on top of the uncommitted 2026-11-16 deepening, on the same branch
  `docs/card-depth-20261116`, and complete that pass's missing subject reports. One pull
  request carries both passes.

Mode: `clarifier`, added to `revue-cartes` for this pass (SKILL.md step 4b; Clarity block
of the review grid). Card count unchanged (298); bridge cards are proposed only.

## Baseline

Measured at `594603f`, the commit of the 2026-11-16 deepening, by
`checks/clarity_metrics.py`: median answer 390.5 lexical words and 7 bold rubrics;
250 of 298 cards above six rubrics; 12 with a rubric-order problem; 209 using an acronym
that the card does not appear to define (heuristic, false positives included). Most
frequent: IoU, NMS, RANSAC, AP, ORB, SIFT, IMU, SORT, LiDAR, GT.

| Check at `594603f` | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 298 cards |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, 0 stale |
| `python3 scripts/learning_path.py` | OK, minimum 268 lexical words |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 71 tests pass |
| `inventaire_cartes.py vault --json` | Saved outside the repository for the final comparison |

State of the 2026-11-16 deepening: 40 of its 45 target cards were deepened, across 30
subjects. CV-FIABILITE-005, CV-STEREO-001, CV-STEREO-003, CV-OCR-003 and CV-BIOMETRIE-001
were not; the figure `cv-biometrie-scores-attack.svg` is not embedded, and
`checks/74-ocr-documents.py` has no matching edit. Reports exist for 5 subjects. As
decided, that deepening is not resumed; its 25 missing reports are reconstructed from the
diff during this pass.

## Delivery criteria

- Audit each card first (SKILL.md step 2). Claims added by the 2026-11-16 deepening are
  checked at their exact passage before being restructured.
- Answer order: **Expected answer**, optional **Key terms**, **Further explanation**
  (plain-language mechanism), one step rubric (**Step by step**, **Worked example**,
  **Reading the diagram** or **Decision procedure**), optional **Limits**, **Blocking
  errors**. At most six rubrics. Each list item on one line, a blank line before a list.
- Every acronym and symbol used outside formulas is defined in the card. Every number is
  shown as formula → substitution → result, recomputed by a stdlib script under `checks/`.
- Paragraphs leaving a card go to the reference: into the existing section that already
  holds their content, otherwise into `## Going further` (one `###` per card ID).
  `checks/nothing_lost.py` lists every removed paragraph and its best match; each one
  below 0.9 is justified in the subject report.
- Preserved: IDs and `## ID` headings, objectives, families, tags, `Source` lines, target
  decks and legacy comments (`checks/protected_fields.py`, against `594603f`). Questions
  change only to expand an acronym; expected answers keep their criteria, and every
  change is reported with its old and new text.
- Missing prerequisite notions: complete the reference's prerequisites with existing
  links; register a bridge-card proposal when no card teaches the notion.
- Increment each changed reference's `revision` once; keep `statut: redige`.
- One report per subject, an overview, entries in `vault/01-Parcours/Suivi-pilote.md`.
  Vault, catalogue, learning-path, unit-test and inventory checks must pass.

## Organization

The coordinating agent wrote the rules and scripts, then clarified subject 132
(CV-METRIQUES-TEMPS) as a pilot and stopped for the learner's validation of the style.
On 2026-11-17 the learner asked to merge this state: the rules, the scripts and the pilot
are delivered, and the other 59 subjects remain to be clarified. The planned organization
for them is two waves of five subagents on disjoint files, each reporting proposals and
log entries in its subject reports for the coordinator to consolidate. This is agent
self-review: it establishes neither independent scientific validation, learner
proficiency nor AnkiDroid rendering.
