# Review — Global registration and local ICP — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-ICP-02. One card added,
CV-ICP-006; the five existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/62-recalage-global-icp.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 8 → 9.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-ICP-006 | $C=\sum a_ia_i^\top$ with $a_i=(p_i\times n_i;\,n_i)$, rotation first: Gelfand et al. eq. 4. $\Delta E=x^\top Cx$: eq. 5. Small eigenvalue → sliding along its eigenvector: §2.2; eigenvectors are screw motions, $c=\lambda_1/\lambda_6$, centroid to origin and unit mean distance to equalize "torque" and "force": §3.1. Plane leaves 2 translations and 1 rotation free, cylinder 1 rotation and 1 translation, extruded profile 1 translation: §2.2 and Fig. 3 (read on the rendered page). Uniform extra points do not help: §2.2. Invariance of the exact nullspace and dependence of ratios on unit and origin: project deduction ($W'=MWM^\top$, $M$ invertible), recomputed. Corridor, floor-plus-wall and door-jamb results: project constructions, recomputed. "A discrete symmetry is not revealed": project deduction already in the reference | Diagnosis: the field failure "low residual, pose slides along a corridor" and its discriminating check; a senior engineer must report or constrain the free direction rather than trust fitness | 3 expected criteria (matrix and eigen-decomposition; normalization and ratio; free direction for the corridor and for floor plus one wall); 561 lexical words | Notation $W$/$C$, rotation-first ordering and normalization as in the reference's "Which motions are constrained"; distinct from CV-ICP-002, which interprets one residual and its linearization, and from CV-ICP-005, which compares metrics | Diagnosis |

The question gives the scene, the symptoms and the second scene; it does not name
eigenvalues, the matrix, normalization or the free direction. The length exceeds
the siblings' because the constructed example carries the unit and origin effect that
criterion 2 tests.

## Reference findings

- **Imprecise:** "two planes leave two in-plane translations and the rotation about
  the normal free". Gelfand et al.'s "two planes" are one planar surface aligned with
  another [§2.2]; read next to worked example B (floor plus wall, one free
  translation), the sentence suggested that two non-parallel planes free three
  motions. The bullet now states the paper's meaning and distinguishes the
  two-non-parallel-planes case.
- **Attribution corrected:** the cylinder (1 rotation, 1 translation) and the sphere
  (3 rotations) were labelled project deductions because Fig. 3 had not been read.
  Fig. 3, read on the rendered page, shows plane, sphere, cylinder, cone and an
  extruded profile with their free motions; these are now cited. The corridor and the
  circular tunnel remain project applications of the extrusion and cylinder cases.
- **Added:** eq. 4 and eq. 5, the screw-motion reading, the rationale of the
  normalization, the invariance of an exact nullspace under centring and scaling
  versus the dependence of eigenvalue ratios (project deduction), the paper's
  reported condition numbers (66.1 → 3.7 for the grooved planes on which uniform
  sampling failed; §5, Figs. 4–5) and the absence of a universal threshold, and
  worked example E.

## Applied corrections

- `vault/60-vision-3d/62-recalage-global-icp.md`: CV-ICP-006 appended.
- `vault/60-vision-3d/references/62-recalage-global-icp.md`, revision 8 → 9:
  "Geometric constraint" bullet corrected and sourced to Fig. 3; "Which motions are
  constrained" developed; worked example E added; failure-mode row points to example E
  and CV-ICP-006; Gelfand source entry extended (§2.1 eqs. 4–5, §5 Figs. 4–6); the card
  listed under related flashcards; closing provenance line extended.

## Proposals

P-CV-ICP-02: accepted by the learner on 2026-11-15, completed as CV-ICP-006.

## Sources

Scientific sources:

- Gelfand, Ikemoto, Rusinkiewicz and Levoy 2003,
  [PDF](https://graphics.stanford.edu/papers/stabicp/stabicp.pdf), downloaded and read
  with `pdftotext` and as rendered page images (pages 2–6, because the equations and
  Fig. 3 labels do not extract as text): §2.1 eqs. 1–5, §2.2, Fig. 3 with caption,
  §3.1, §3.2 steps A1–B4, §5 with Figs. 4–7.

No implementation source carries this card. Context7 is not available in this
session; no library API is involved. No access failed.

## Checks and limitations

`python3 -I docs/revues/2026-11-15-accepted-proposals/checks/62-recalage-global-icp.py`
passes its 9 checks: scene sizes; one zero eigenvalue and the intersection-line
translation for floor plus wall; one zero eigenvalue and the axis translation for the
corridor, with the axis rotation at 0.098 of the largest eigenvalue; unit invariance
of the exact nullspace; normalized $c\approx125$ with the door jambs; 4,456 in metres
and $4.4\times10^9$ in millimetres without normalization; the weakest raw eigenvector
in a distant map frame; exact agreement of normalized metres and millimetres; the
$\Delta E$ values of eq. 5. A scratch cross-check outside the repository
(`python3 -I`, installed NumPy 2.2.6, `numpy.linalg.eigvalsh` on the same matrices)
reproduced the normalized condition number 125.2, 4,456 in metres, $4.36\times10^9$ in
millimetres, $5.15\times10^7$ in the distant map frame and the 0.098 ratio of the bare
corridor. Scenes are noise-free samples with exact normals; no ICP or LiDAR data was run, so the symptom figures in the question (fitness 0.97, 5 mm,
0.6 m) are illustrative. AnkiDroid rendering of the card is not verified.
