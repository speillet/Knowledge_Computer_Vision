# Creation — Structure from Motion: incremental and global pipelines — 2026-11-16

## Overview

New reference `CV-SFM` (`vault/150-photogrammetrie/references/152-sfm-incrementale-globale.md`,
type `pipeline`, tracks B and C, depth `approfondissement`, revision 1) and 5 new cards,
CV-SFM-001 to CV-SFM-005, in five families: comparison, reasoning, algorithm, diagnosis,
evaluation. Answer lengths: 433 to 451 lexical words (median 446), counted by the inventory
script. Every constructed number is recomputed by
`checks/152-sfm-incrementale-globale.py` (20 checks).
Self-review: Agent Claude Code. Editorial status: redige. No independent scientific
validation, no SfM run and no Anki or Obsidian rendering are claimed.

## Cards

| Card | Accuracy: central claims, verdict and exact passage | Relevance | Gradability: criteria and lexical words | Family |
| --- | --- | --- | --- | --- |
| CV-SFM-001 | Incremental cost dominated by repeated BA: confirmed, Snavely et al. §4.2 ("dominated by the iterative bundle adjustment"), Schönberger and Frahm §4.4 (global BA after growth, amortized linear). Global speed: confirmed, Wilson and Snavely §7 ("usually 2-4 times faster"), Pan et al. Table 5 (497.3 s against 4,051.0 s; AUC@3° 69.6 against 65.3). Cascades and drift: confirmed, Schönberger and Frahm §2.2, §4.2; Wilson and Snavely §1. Global failure modes: confirmed, Pan et al. §1 (scale, intrinsics, collinear motion), §4.1 and §4.4 (rotation-averaging collapse on symmetry). Outlier handling of global SfM: Wilson and Snavely §1 (filtering against the current model "not directly applicable in a global setting"); "a surviving wrong pair distorts the whole solution" is a project deduction | Senior choice between two pipeline families, with mechanisms rather than slogans; COLMAP FAQ L131–L159 grounds the default | 3 criteria (cost, outlier handling, accumulation and typical failure); 437 words | comparison |
| CV-SFM-002 | Directions fix positions up to translation and scale: confirmed, Wilson and Snavely §3 eq. 2 ("unique up to global gauge ambiguity"); parallel rigidity: Pan et al. §2.2. Collinear degeneracy and camera-to-point edges: confirmed, Wilson and Snavely §3 and §6, Pan et al. §3.2 ("a known degenerate case for translation averaging"). Skewed-triangle sensitivity: confirmed qualitatively, Pan et al. §1 ("especially prone to noise"); the numbers are a project construction | Mechanism behind the main weakness of global SfM and GLOMAP's design choice; frequent in road and corridor data | 3 criteria (collinear ambiguity, restoration by a point, amplification near collinearity); 433 words | reasoning |
| CV-SFM-003 | Candidate gate 30 visible points, PnP RANSAC 12 px, 30 inliers, ratio 0.25, 3 trials: confirmed, COLMAP 4.2.1 incremental_mapper.h L85–L92, L131–L132 and incremental_mapper_impl.cc L294–L364. Pyramid score: confirmed, Schönberger and Frahm §4.2 and visibility_pyramid.cc L39–L72 (6 levels, observation_manager.h L52–L53). Angle gates 1.5° and 16°: confirmed, incremental_triangulator.h L76, incremental_mapper.h L80, L129. Post-BA retriangulation and filtering: confirmed, Schönberger and Frahm §4.4 and incremental_mapper.cc L1255–L1337 (2 local passes below 0.1%, 5 global below 0.05%, robust loss in the first local pass only). Global-refinement trigger: confirmed, incremental_pipeline.cc L543–L555 | Core algorithm of the most used SfM system; the gates explain observable behaviour (missing far points, cascades) | 3 criteria (selection and acceptance, the two tracks, post-BA loop and stop); 451 words | algorithm |
| CV-SFM-004 | Mechanism of folding by duplicate structure in incremental SfM: confirmed, Heinly et al. §1 (registration "only to the facades of the tower"; only duplicate points register). Conflicting observations, camera-graph splits, edge cost eq. 1, merging by a similarity from disconnected inliers, need for unique structure: confirmed, §3.3–§3.5 and §4. GLOMAP symmetric collapse: confirmed, Pan et al. §4.1. Reprojection blindness and the 70.71 m chord: project deduction and construction | Diagnosis of a silent, frequent failure in urban and industrial scenes, distinct from the pair-level repetition cards of domains 4 and 5 | 3 criteria (mechanism and blind residual, checks, repair); 446 words | diagnosis |
| CV-SFM-005 | Free SfM up to a 7-dof similarity: confirmed via CV-BA (Triggs §9.1) and Snavely et al. §4.3. Umeyama closed form: confirmed, Umeyama 1991 eqs. 32–43. Robust RANSAC alignment: confirmed, COLMAP faq.rst L436–L448 (`model_aligner`, `alignment_max_error`), Wilson and Snavely §7 (RANSAC absolute orientation). Relative-pose metric, 180° for missing pairs, AUC convention: confirmed, COLMAP 4.2.1 benchmark utils.py L1262–L1408, L1561–L1590; GLOMAP §4 (relative AUC for unordered sets, absolute after robust alignment for sequences; relative error misses scale drift). Residuals 2.90 to 3.09 m, 20.6°/16.3°/36.9°, AUC 70, 73.88 against 75.92: project construction | Evaluation protocol for any SfM-based product; complements CV-METRIQUES-TEMPS-003 (choice of alignment group for metric VIO) with outlier sensitivity and gauge-free metrics | 3 criteria (alignment first, robust alignment, relative metrics and their blind spot); 447 words | evaluation |

Two angles were changed from the brief after checking existing cards. Suggested card 002
(gauge: what fixing one camera and one distance does) overlapped CV-BA-003 and
CV-EPIPOLAIRE-002, which already test scale gauge and a fixed baseline; it became the
observability of translation averaging, an SfM-specific mechanism. Suggested card 005
(similarity alignment before errors) overlapped CV-METRIQUES-TEMPS-003; it now centres on
least-squares versus robust alignment and on gauge-free relative metrics. The gauge content
stays in the reference (worked example A, COLMAP's two-frame gauge fixing). Card 004 differs
from the repeated-texture cards CV-SIFT-006, CV-MATCHING-004, CV-CORNERS-004 and CV-ECC-002: those diagnose
a wrong pairwise alignment; this one diagnoses a whole model folded by registration order.

## Reference content and verified claims

- **Problem and contract.** Definition and outputs [Schönberger and Frahm §2, §2.2];
  multiple sub-models and their defaults [incremental_pipeline.h L54–L69]; scene
  normalization [reconstruction.h L187–L201]; pixel-origin convention [faq.rst L109–L121];
  unit translation from E [essential_matrix.cc L61]; EXIF focal test [Snavely et al., App. A].
  Rotation conventions differ between 1DSfM (eq. 1) and GLOMAP (§2.2); flagged in the note.
- **Gauge and drift.** COLMAP's two-frame gauge fixing read in bundle_adjustment_ceres.cc
  L308–L416 and called at incremental_mapper.cc L1197–L1204; drift quotes from Schönberger
  and Frahm §2.2, Snavely et al. §4.3, Wilson and Snavely §1.
- **Degeneracies.** Panoramic and planar labels (two_view_geometry.h L60–L66,
  two_view_geometry.cc L362–L363, L955–L956), initial-pair gates (incremental_mapper_impl.cc
  L703–L708), epipole filtering [Pan et al. §3.1], collinear motion [Pan et al. §3.2; Wilson
  and Snavely §3, §6], symmetry [Pan et al. §4.1; Heinly et al. §1], watermarks
  [Schönberger and Frahm §4.1; two_view_geometry.h L68–L81]. The forward-motion explanation
  (epipole in the image) is a project deduction, labelled as such.
- **Procedures.** Incremental loop read in incremental_pipeline.cc L455–L738 and
  incremental_mapper.cc L1122–L1381; global loop in global_mapper.cc L124–L159, L368–L460,
  L528–L638 and Pan et al. §3; 1DSfM steps in Wilson and Snavely §4–§6, Alg. 1–2.
- **Mathematics.** Rotation averaging [Pan et al. eq. 1]; translation averaging and chordal
  distance [Wilson and Snavely eqs. 3–4, Table 1]; global positioning [Pan et al. eqs. 3–4];
  triangulation angle [Schönberger and Frahm eq. 3]; pyramid score [§4.2] and its code;
  Umeyama [eqs. 32–43]; benchmark metrics [utils.py].
- **Cost.** Photo Tourism runtimes [§4.2]; COLMAP tutorial matching times [tutorial.rst
  L396–L403]; 1DSfM timings and hardware [§7]; GLOMAP runtimes [Tables 1, 3, 4, 5], hardware
  not stated in the paper.

**Disagreements between sources.**

- *Local BA loss.* The 2016 paper uses a Cauchy loss in local BA [§4.4]; COLMAP 4.2.1 uses
  soft-L1 with scale 1 [incremental_pipeline.cc L222–L224], only in the first local pass
  [incremental_mapper.cc L1288–L1292], and a squared loss in global BA [L273]. CV-BA's
  parameter table says "COLMAP: Cauchy in local BA", which matches the paper but not the
  current code; the coordinator may want a dated note there (not edited by this agent).
- *Pyramid figure.* The paper's Fig. 3 shows scores of 66, 80, 146 and 200 for $L=3$; with
  the weights $w_l=K_l^2$ stated in its text (4, 16, 64), which the 4.2.1 code implements,
  every score is a multiple of 4, so 66 and 146 cannot arise. The note uses the code's
  weights and does not cite the figure's values.
- *Triangulation thresholds.* The paper's triangulation experiment used $\alpha=2^\circ$ and
  $t=8$ px [§5]; the 4.2.1 defaults are 1.5° and angular errors of 2° [incremental_triangulator.h
  L45–L91]. Both are stated with their context.

## Constructed examples

All recomputed by `checks/152-sfm-incrementale-globale.py` (stdlib, Fractions where exact):

- A: similarity invariance of projections (exact), residual scaling family when one camera is
  fixed, 7 = 6 + 1.
- B: $\arccos0.95=18.19^\circ$; baseline/depth 0.2811 for 16° and 0.0262 for 1.5°; 2.86° at
  20 m, 1.15° at 50 m, gate reached at 38.2 m for a 1 m baseline.
- C: pyramid scores 1,296 / 1,092 / 1,092 (three levels) and 1,380,624 / 1,328,196 /
  2,638,916 (six levels); maximum 17,895,696.
- D: collinear ambiguity, exact restoration of $(30,0)$ by a point, 30.02 → 23.13 or 52.11 m
  with a 0.5° error; rotation cycle error 10°; bounded residuals $\sin\theta$ and
  $2\sin(\theta/2)$.
- E: Heinly edge costs 1/4 and 2/3; chord 70.71 m.
- F: raw differences 5.39–47.20; least-squares residuals 2.90, 9.25, 5.81, 1.21, 3.09 m, RMS
  5.27 m, scale +2.9%, rotation 7.51°; robust refit 0 and 15.00 m; Umeyama's
  $\operatorname{tr}(DS)/\sigma_x^2$ equals the complex least-squares scale; relative errors
  20.56°, 16.31°, 36.87°; AUC 70.0, 70.0, 75.92 (73.88 with ordered pairs).
- G: 499,500 and 49,995,000 exhaustive pairs; 28, 52 and 79 global refinements for 100,
  1,000 and 10,000 frames (frame criteria only); cited runtime ratios 8.1, 28.6, 8.4, 2.4.

## Proposals

Not registered in `docs/revues/propositions.md` (coordinator decision):

- *Practice — read two-view labels.* Given COLMAP's labels for a few pairs (calibrated,
  uncalibrated, planar, panoramic, watermark) and their inlier counts, decide which may seed
  the model and which may triangulate. Source: Schönberger and Frahm §4.1;
  two_view_geometry.h/.cc at 4.2.1.
- *Design — choose a pairing strategy.* For 300, 5,000 and 50,000 images (unordered photos,
  video), choose exhaustive, sequential or retrieval matching with pair counts and the risk to
  connectivity. Source: COLMAP tutorial.rst L396–L403 and §5 of the 2016 paper; check overlap
  with CV-PLANIFICATION (batch 2) first.

## Sources

**Scientific (read in full text for the cited passages).**

- Schönberger and Frahm 2016, CVPR open access PDF (CVF): §1–§5, Tables 1–2, Figs. 2–5.
- Pan, Baráth, Pollefeys and Schönberger 2024, arXiv 2407.20219v2: §1–§5, Tables 1–7.
- Wilson and Snavely 2014, ECCV, project PDF at cs.cornell.edu: §1–§7, Alg. 1–2, Tables 1–3.
- Snavely, Seitz and Szeliski 2006, ACM TOG, project PDF: §4.1–§4.3, App. A.
- Heinly, Dunn and Frahm 2014, ECCV: archived author PDF (web.archive.org snapshot of
  cs.unc.edu/~jheinly/publications/eccv2014-heinly.pdf), §1–§5.
- Umeyama 1991, IEEE TPAMI 13(4): §II, eqs. 1–43, read as page images of a scanned copy hosted
  at web.stanford.edu/class/cs273/refs/umeyama.pdf; cited by DOI.

**Implementation and standards.**

- COLMAP 4.2.1 (release tag of 2026-09-29), raw files on GitHub: controllers/incremental_pipeline.h
  and .cc; sfm/incremental_mapper.h, .cc, incremental_mapper_impl.cc,
  incremental_triangulator.h, observation_manager.h and .cc, global_mapper.h and .cc;
  estimators/two_view_geometry.h and .cc, bundle_adjustment.h, bundle_adjustment_ceres.cc,
  global_positioning.h, rotation_averaging.h, alignment.h and .cc; scene/reconstruction.h,
  visibility_pyramid.cc; geometry/essential_matrix.cc;
  benchmark/reconstruction/evaluation/utils.py; doc/faq.rst, doc/tutorial.rst.
- GLOMAP repository: README at tag 1.2.0 and at main commit
  99806d0869f802fad218516a2e027793e7ca687d (deprecation notice, 2026-01-30); repository
  archived. GLOMAP's own source was not read; its pipeline was read in COLMAP 4.2.1.

**Failed or partial access.**

- Heinly et al.: the author's URL and project page returned HTTP 404; the Wayback copy was used.
- Umeyama 1991: IEEE version paywalled; the scanned copy has no text layer (read as images).
- Not read, therefore not cited for any claim: Hartley et al. 2013 (rotation averaging),
  Chatterjee and Govindu 2013, Özyeşil and Singer 2015, Arrigoni and Fusiello 2018, Manam and
  Govindu 2024, Zach et al. (loop constraints), Doppelgangers 2023, Triggs et al. 2000 (relied
  on through CV-BA). Context7 was unavailable.

## Checks and limitations

- `python3 -I docs/revues/2026-11-16-photogrammetry/checks/152-sfm-incrementale-globale.py`:
  20 checks passed.
- `python3 scripts/check_vault.py`: the only errors on these files are links to sibling
  references not yet written: first `151-colinearite-autocalibration.md` and
  `153-systemes-reference.md`, at the last run only `153-systemes-reference.md`.
- `python3 scripts/learning_path.py`: a first run reported errors naming CV-COLINEARITE and
  CV-GEODESIE only; the last run stopped with `FileNotFoundError` on the card file
  `151-colinearite-autocalibration.md` of a sibling still in progress. No error named CV-SFM;
  to rerun once the siblings are complete.
- `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py
  vault/150-photogrammetrie/152-sfm-incrementale-globale.md`: 5 cards, 433–451 words, no
  anomaly.
- `grep -n ' $'`: no trailing whitespace in the three files.
- No SfM processing was run; COLMAP, GLOMAP and Eigen code was read, not executed. No
  Obsidian or AnkiDroid rendering was verified; the cards are to republish with `paquet-anki`.
