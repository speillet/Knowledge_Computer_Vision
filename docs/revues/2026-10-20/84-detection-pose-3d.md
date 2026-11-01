# Review –  Detection 3D, pose of object and pose articulated –  2026-10-20

## Overview

4 flashcards audited. Two major sources are missing, without changing the objectives. Self-reviewed documentary by Agent Codex (`revue-cartes`); status `redige` preserved.

4 flashcards audited. Maximum gravity recorded by flashcard before correction: 0 blocking, 2 large, 2 minor, 0 without detected defect. The observations relating only to the reference note are detailed separately below.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-POSE3D-001 | Confirmed with source added | name the output of pose. | 40 words at entry; Distinction finished | reference note and controlled format | important | Ajouter OpenPose |
| CV-POSE3D-002 | Detailed Project Reasoning | check a box 3D. | 43 words at entry; Criteria finished; case not executed | reference note and controlled format | Minor | Specify attribution |
| CV-POSE3D-003 | Confirmed after source accuracy | distinguish nuScenes and COCO. | 50 words at the entrance; Finished core, objective retained | reference note and controlled format | Minor | Targeting the source |
| CV-POSE3D-004 | Confirmed with source added | respect the symmetries of pose. | 55 words at the entrance; Ambiguity conditioned by observations | reference note and controlled format | important | Ajouter BOP |

### reference note and flashcards claims

- Confirmed: PointPillars produces a pseudo-image of pillars; CenterPoint detects 3D centers and properties (summary).
- Not initially supported by detection sources alone, the articulated part pose is supported by OpenPose, fig. 2; BOP metrics support symmetry and visible ambiguity.
- Confirmed: nuScenes uses the distance 2D to the ground, with thresholds 0,5/1/2/4 m for AP; NDS weighs mAP and five errors. The flashcards do not equate this protocol to COCO.
- The rotation of a cylinder is ambiguous only if the observations do not break its symmetry; this condition is already present in the response. Axis/unit controls are a built-in diagnostic.

## Corrections applied

Bibliography of the completed reference note and sources of the four targeted flashcards.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No Priority Addition | Existing objectives are sufficient for the scope announced | — | No reminders added | Sources ci-dessous |

Absent families: algorithm, understanding, design, reasoning. Their absence does not require automatic filling; the proposals aim at a concrete gap. No flashcard added.

## Sources

- [PointPillars, architecture §2.1](https://arxiv.org/abs/1812.05784), also reviewed in the journal 64.
- [CenterPoint, summary](https://arxiv.org/abs/2006.11275).
- [OpenPose, summary and fig. 2](https://arxiv.org/abs/1611.08050).
- [BOP, tasks and metrics](https://bop.felk.cvut.cz/tasks/), accessed on 20 October 2026.
- [nuScenes, fichier officiel lu via sa version raw, Metrics](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md), accessed on 20 October 2026.

## Checks and limitations

The lengths come from the initial inventory; they are those of the entire verso, not just the core. No arbitrary ceiling; duration and recall load not measured.

Controller, 34 unit tests, comparison of 224 IDs and identities Anki and diff: final results in the [bilan commun](00-bilan.md). Context7 unavailable; direct use of official API documentation.

Real export Anki, rendering Obsidian/AnkiDroid, control of the learner and independent scientific validation not verified. Propositions of protocols and diagnoses remain reasonings of the project, not experiments performed.
