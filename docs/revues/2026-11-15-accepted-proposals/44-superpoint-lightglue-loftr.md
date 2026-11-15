# Review — Learned matching: SuperPoint, LightGlue and LoFTR — 2026-11-15

## Overview

Learner decision applied to one card; no card added or re-audited.
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 8 → 9.

## Applied correction

The [2026-11-14 report](../2026-11-14-reference-depth/44-superpoint-lightglue-loftr.md)
found that the front of CV-MATCH-APPRIS-005 names "padding", which points to
the coordinate-conversion answer. On 2026-11-15 the learner adopted the wording
proposed in that report.

| Card | Before | After |
| --- | --- | --- |
| CV-MATCH-APPRIS-005 | After padding is added, matches look visually correct but the homography is biased. What should be tested? | After a change in image preprocessing, matches look correct when drawn on the network inputs, but the homography estimated in the original images is biased. What should be tested first? |

The ID, objective, family, expected answer, tags and Anki identity are
unchanged; the expected answer (convert positions from the network frame to
each real image, including resize and offsets) still answers the new front.
The two copies of the question in the reference's per-card appendices
("Working question" and "Situation") were aligned.

## Checks and limitations

Vault, catalogue, learning-path, unit-test and inventory checks are recorded
in the [overview](00-bilan.md). AnkiDroid rendering is not verified.
