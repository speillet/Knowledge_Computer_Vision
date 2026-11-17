# Review — Evaluating identities, trajectories and 3D localization — 2026-11-16

Reconstructed from the diff on 2026-11-17. The deepening session of 2026-11-16 edited this
subject and wrote its check script, but stopped before writing this report. Agent Claude
Code rebuilt it from the changes committed in `594603f` and audited the added claims during
the [2026-11-17 clarity pass](../2026-11-17-clarity/132-tracking-trajectoires.md). The
passages read by the original session are not documented beyond its check script.

## Overview

2 cards deepened in `approfondir` mode (CV-METRIQUES-TEMPS-001 and -003), the two shortest
of the subject (260 and 297 lexical words at `6cef833`), with one new figure. Highest
severity per card found by the 2026-11-17 audit of the added text: 0 blocking,
0 important, 1 minor (CV-METRIQUES-TEMPS-001), 1 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige. Reference revision 8 → 9.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-TEMPS-001 | Added numbers recomputed (MOTA $15/16$, IDF1 $26/32$, $30/32$, $24/32$, AssA $98/128$, HOTA 0.875, relabelled replay). HOTA §9.1 problem 6 and Ristani §3.3 confirmed. The sentence "an event-based count charges between 1 and $n-1$ errors … [§3.1, §3.3]" is not stated by Ristani et al.; it is a project deduction from their Fig. 1 | Evaluation: separates detection from identity with counts | 1 expected criterion, unchanged; 260 → 580 lexical words | Figure values match worked example A's conventions | Minor | Deepened: diagram, events versus frames, relabelled replay. Attribution corrected on 2026-11-17 |
| CV-METRIQUES-TEMPS-003 | Zhang and Scaramuzza §III-A, eqs. 11–12 confirmed (`pdftotext` of the IROS 2018 PDF: "remain unchanged only when $s=1$ and $R^\top g=g$"). Worked example B values recomputed | Evaluation: chooses an alignment group from what the sensor observes | 1 expected criterion, unchanged; 297 → 554 lexical words | Aligned with worked example B and card CV-VIO-003 | None identified | Deepened: why 4 DoF, constructed example, diagnosis |

## Applied changes (2026-11-16)

- `vault/130-evaluation-fiabilite/132-tracking-trajectoires.md`: CV-METRIQUES-TEMPS-001
  gained **Reading the diagram**, **Events versus frames** and **Diagnosis**;
  CV-METRIQUES-TEMPS-003 gained **Why 4 DoF for an inertial system**, **Constructed
  example** and **Diagnosis**. Both Source lines were extended.
- `vault/130-evaluation-fiabilite/references/132-tracking-trajectoires.md`, revision 8 → 9:
  events-versus-frames paragraph and figure in worked example A; the gravity argument
  after worked example B.
- `vault/99-Ressources/cv-metriques-temps-id-switch.svg`: new schematic figure, two
  panels, eight frames.

Expected answers, questions, objectives, families, tags and IDs were unchanged.

## Proposals

None registered by the 2026-11-16 session.

## Sources

Read on 2026-11-17 to audit the added claims: Ristani et al. 2016 (arXiv 1609.01775, PDF
extracted with `pdftotext`), §3.1 and Fig. 1, §3.3; Luiten et al. (arXiv HTML v2), §9.1,
problems 5 and 6; Zhang and Scaramuzza 2018 (IROS PDF, `pdftotext`), §III-A eqs. 11–12;
TrackEval `clear.py` at `12c8791`, L60–L100.

## Checks and limitations

`python3 -I docs/revues/2026-11-16-card-depth/checks/132-tracking-trajectoires.py`: 7
checks pass, including a check that reads the IDs and colours drawn in the SVG. The
figure was not re-rendered at phone width during this reconstruction. AnkiDroid and
Obsidian rendering are not verified. Export status: **to republish with `paquet-anki`**.
