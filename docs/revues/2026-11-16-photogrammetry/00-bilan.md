# Photogrammetry domain — overview — 2026-11-16

This overview covers batch 1. It will be extended when batch 2 (CV-MVS,
CV-ORTHO, CV-SATELLITE, CV-PLANIFICATION) is delivered.

## Result

The learner asked for a substantial photogrammetry section and chose a new
domain, all four contexts and eight subjects ([scope record](00-cadrage.md)).

- **Structure:** domain 15, `150-photogrammetrie` (`d15`), with its index,
  subdeck `CV::Pilote::150-photogrammetrie` and learning-path stage
  `photogrammetrie` after `geometrie`. The validator derives the allowed
  domains from `scripts/vault_sections.json`; two unit tests cover it. The
  spec, curriculum table, layout guide and quickstart now state fifteen
  domains; dated evidence keeps its fourteen.
- **Batch 1:** four references at revision 1 and 20 cards, 298 → **318
  cards**, 60 → 64 references. No existing card, ID, expected answer or
  reference changed.

| Reference | Cards and families | Lexical words | Report |
| --- | --- | --- | --- |
| CV-COLINEARITE — Collinearity, orientations and photogrammetric self-calibration | 001 practice, 002 reasoning, 003 diagnosis, 004 design, 005 evaluation | 431–455 | [151](151-colinearite-autocalibration.md) |
| CV-SFM — Structure from Motion: incremental and global pipelines | 001 comparison, 002 reasoning, 003 algorithm, 004 diagnosis, 005 evaluation | 433–451 | [152](152-sfm-incrementale-globale.md) |
| CV-GEODESIE — Reference systems for photogrammetry: datums, projections and heights | 001 understanding, 002 practice, 003 reasoning, 004 algorithm, 005 diagnosis | 422–445 | [153](153-systemes-reference.md) |
| CV-AEROTRIANGULATION — Aerotriangulation and georeferencing: ground control, GNSS/IMU and accuracy | 001 evaluation, 002 reasoning, 003 diagnosis, 004 design, 005 comparison | 437–485 | [154](154-aerotriangulation-georeferencement.md) |

The 20 answers run from 422 to 485 lexical words, median 443; each expected
answer lists three gradable criteria. The references run from 521 to 654
lines, above the 300–500 target, because each carries five to seven worked
examples. Length flags short answers; it does not measure quality.

## Coordinator review

The coordinating agent recomputed the numbers of all 20 cards independently
of the subagents' scripts (OpenCV-to-photogrammetric conversion, law-of-sines
spacing, least-squares versus robust alignment residuals, relative-pose
angles, ECEF and East–North–Up coordinates, curvature and scale-factor
effects, plate-motion offsets, ASPRS Edition 2 accuracy with survey error,
radial doming fit, error budgets). One defect was found and corrected before
delivery: CV-AEROTRIANGULATION-002 gave a 0.003° boresight error in roll and
in pitch but counted one axis in its root-sum-square (0.18 m instead of
0.21 m); the card, worked example C and check 7 were corrected.

Subagents changed three suggested objectives to avoid duplicates with
existing cards: CV-SFM-002 (gauge fixing is already in CV-BA-003 and
CV-EPIPOLAIRE-002), CV-SFM-005 (alignment-group choice is in
CV-METRIQUES-TEMPS-003) and CV-COLINEARITE-001 (the camera centre alone is in
CV-SE3-002).

## Source findings

Reading the sources found discrepancies, recorded in the subject reports and
not propagated into the cards:

- ASPRS Edition 2, Version 2 (2024): §7.10 prints the elevation GCP rule with
  RMSE_V where Addendum III implies RMSE_H; Addendum V both allows "minimal or
  no GCPs" for PPK and "highly recommends" surveyed GCPs.
- James and Robson 2014: the conclusions credit Fig. 4 with flight plans
  shown in Fig. 5, and a stated corner distortion does not recompute from
  their sensor.
- Hastedt and Luhmann 2015, Table 1: the decentring conversion is given in
  1/mm², where dimensional analysis and a reprojection check give 1/mm.
- IOGP 373-7-2: a time-dependent Helmert example prints a rotation rate that
  its own parameter list and result contradict.
- Schönberger and Frahm 2016: COLMAP 4.2.1 uses a soft-L1 loss in its first
  local adjustment, where the paper describes a Cauchy loss.

## Follow-up for batch 2 and later passes

- **Links from existing references.** Several notes would point to the new
  domain: CV-BA, CV-ZHANG, CV-EPIPOLAIRE, CV-SE3, CV-IMAGERIES, CV-MULTICALIB,
  CV-RENDU3D, CV-VIO. Each link needs a revision increment and a log entry;
  they will be added once, after batch 2, so that each note changes once.
- **CV-BA.** Its parameter table says "COLMAP: Cauchy in local BA", true of
  the 2016 paper but not of COLMAP 4.2.1; a dated correction belongs to a
  `revue-cartes` pass.
- **Proposals.** Each subject report lists up to two further card ideas. They
  are not registered in `docs/revues/propositions.md` until the learner sees
  them.

## Checks performed

Executed on the batch-1 tree, in the dedicated worktree, against `main` at
`d53ea2f`.

| Executed check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 151 Markdown files, 64 references, 318 cards |
| `python3 scripts/sync_catalog.py --check` | 20 generated documents, 0 stale (6 regenerated, one new index) |
| `python3 scripts/learning_path.py` | OK: 64 references, 318 cards, minimum 260 lexical words, 0 errors |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 64 tests pass (2 new) |
| `inventaire_cartes.py vault` and `--compare` with the starting inventory | 318 cards, no anomalies; 20 IDs added, none removed |
| `compare_protected.py` (2026-11-14 tool) against `d53ea2f` | 0 existing cards, expected answers or references changed; new files only |
| `check_anchors.py` (2026-11-14 tool) on `vault/` and `docs/revues/` | 5,377 local links and heading anchors resolve |
| `python3 -I checks/15[1-4]-*.py` | 4 scripts pass (115 checks) |
| `git diff --check` and trailing-whitespace search | Clean |

## Limitations

This is agent self-review. It establishes neither independent scientific
validation (FR-037) nor learner proficiency. No photogrammetric processing
was run: every number is a constructed example or a cited value, and the
covariance studies of CV-COLINEARITE are first-order computations on
constructed networks. Several sources were inaccessible (Brown 1971, Fraser
1997, Luhmann et al. 2016, James et al. 2019, NGA.STND.0036, the ITRF2020
paper, the OEEPE official publication); none is cited for an unread passage.

Obsidian and AnkiDroid rendering are not verified, including the wide
tables and a Mermaid diagram in the references. No Anki package is rebuilt:
the new subdeck reaches the phone only through a package built with
`paquet-anki`.
