# Accepted proposals and pending decisions — overview — 2026-11-15

## Result

The learner decided on the items left pending by the
[2026-11-14 reference-deepening pass](../2026-11-14-reference-depth/00-bilan.md)
([scope record](00-cadrage.md)):

- **Twelve proposals accepted and written** in `ajouter` mode, one card each:
  282 → **294 cards**. No ID was removed, and no existing expected answer,
  objective, family, tag or target deck changed.
- **Two questions reworded**, CV-SOT-002 and CV-MATCH-APPRIS-005, with the
  wording proposed on 2026-11-14 so that their fronts no longer hint at the
  answers. IDs, objectives and expected answers are unchanged, so the Anki notes
  keep their identity and history.
- **Four overlapping cards kept**: CV-MATCHING-001 with CV-CORNERS-001, and
  CV-MATCHING-002 with CV-FAST-BRIEF-003.
- **98 proposals left pending**, 94 from 2026-11-14 and the four earlier ones.

Writing the cards against their sources also found imprecise or wrong
statements in **twelve references**: eleven of the twelve card subjects (all but
CV-SORT) and CV-HOMOGRAPHIE. They were corrected before the cards relied on
them. One clause of a proposal (P-CV-IOU-AP-01) proved false. Fifteen references
received exactly one revision increment and keep `statut: redige`. This is
agent self-review by Claude Code, not independent validation.

| Added card | Proposal | Family | Recall objective | Lexical words | Report |
| --- | --- | --- | --- | ---: | --- |
| CV-ECC-004 | P-CV-ECC-01 | practice | State the direction of an ECC warp and warp the input accordingly | 411 | [CV-ECC](45-recalage-ecc.md) |
| CV-PIPELINE-006 | P-CV-PIPELINE-02 | reasoning | Map a detector box back through a letterbox and recognize a forgotten padding term | 462 | [CV-PIPELINE](141-contrats-profiling-video.md) |
| CV-MATCHING-005 | P-CV-MATCHING-02 | diagnosis | Diagnose a homography that `findHomography` returns without error but cannot be trusted | 492 | [CV-MATCHING](43-detecteurs-matchers.md) |
| CV-EPIPOLAIRE-006 | P-CV-EPIPOLAIRE-01 | diagnosis | Diagnose a two-view initialization on a pure rotation or a planar scene | 568 | [CV-EPIPOLAIRE](53-epipolaire-pnp-triangulation.md) |
| CV-SORT-009 | P-CV-SORT-01 | diagnosis | Diagnose a fast small object that never keeps a SORT identity | 462 | [CV-SORT](111-sort.md) |
| CV-ICP-006 | P-CV-ICP-02 | diagnosis | Detect a degenerate registration and name its free motion | 561 | [CV-ICP](62-recalage-global-icp.md) |
| CV-STEREO-005 | P-CV-STEREO-01 | algorithm | Explain the SGM smoothness penalties $P_1$ and $P_2$ | 475 | [CV-STEREO](61-stereo-profondeur.md) |
| CV-WATERSHED-006 | P-CV-WATERSHED-01 | understanding | State which relief `cv::watershed` floods and its consequences for the distance pipeline | 520 | [CV-WATERSHED](91-otsu-distance-watershed.md) |
| CV-FLANN-005 | P-CV-FLANN-01 | practice | Restructure `FlannBasedMatcher` calls so that the index is built once and reused | 445 | [CV-FLANN](48-flann.md) |
| CV-HANDEYE-006 | P-CV-HANDEYE-01 | comparison | Compare separable and simultaneous hand–eye solvers for translation accuracy | 586 | [CV-HANDEYE](57-calibration-hand-eye.md) |
| CV-DETECTEURS-014 | P-CV-DETECTEURS-01 | practice | Assign, encode and decode an anchor with the right box-coder weights | 497 | [CV-DETECTEURS](82-detection-fasterrcnn-yolo-detr.md) |
| CV-IOU-AP-008 | P-CV-IOU-AP-01 | reasoning | Separate the effect of a low-score tail on COCO AP from the deployed operating point | 514 | [CV-IOU-AP](131-iou-ap-coco.md) |

The new answers run from 411 to 586 lexical words, median 495. Existing cards
of the same subjects run from 268 to 452. The gap comes from the worked
numbers and the diagnostic checks that each objective requires. Each expected
answer still lists two or three gradable criteria. Length flags short answers;
it does not measure quality.

Each front gives the numbers needed and asks for the mechanism without naming
it. For CV-ECC-004, the front names the default-flag call, because predicting
its result is part of the objective; it does not name `WARP_INVERSE_MAP`.

## Main corrections

The [correction log](../../../vault/01-Parcours/Suivi-pilote.md#accepted-proposals--2026-11-15)
has one row per corrected reference. By kind:

- **Implementation behaviour stated too narrowly or wrongly**:
  - ECC: without `WARP_INVERSE_MAP`, the warp applies the motion a second
    time, $T(W^{-2}\mathbf x)$, rather than "the inverse motion".
  - CV-HOMOGRAPHIE: `findHomography` method 0 also has its mask recomputed
    since OpenCV 4.12.0
    ([opencv#26742](https://github.com/opencv/opencv/pull/26742)).
  - FLANN: `add` triggers a full index rebuild.
  - SGBM: any $P_2\le P_1$ is silently raised to $P_1+1$, not only a zero
    $P_2$.
  - Letterbox: `resize` applies the rounded size ratio.
  - torchvision: the RPN label boundary is IoU $\ge0.7$, and decoding divides
    by the coder weights before clamping.
- **Overstated conclusions**:
  - A capped RANSAC run is not "a coin flip": 0.637 is the nominal guarantee,
    and OpenCV redraws degenerate samples.
  - The low-score-tail argument for COCO AP does not extend to a larger
    per-image cap. A constructed counterexample lowers AP from 1 to 0.835.
  - The essential matrix is not a sound model for planar data: its linear
    estimate has rank 6, and a second exact $E$ exists.
  - A scaled distance map passed to `cv::watershed` does not flood a nearly
    constant relief. Its differences vanish across the saddle, so the neck
    becomes the cheapest crossing.
- **Attribution**:
  - The highest-IoU anchor clause belongs to the RPN rule, not to the
    RetinaNet paper.
  - Horaud and Dornaika's 1995 comparison did not include Daniilidis or
    Andreff.
  - "Two planes" in Gelfand et al. means one plane aligned with a copy of
    itself; a floor plus a wall leaves a single free translation.
  - The cylinder and sphere cases are shown in Gelfand et al.'s Fig. 3, so
    they are no longer labelled project deductions.

P-CV-IOU-AP-01 said that raising the per-image cap cannot lower AP. That
clause is false. The card states the exact condition: every added detection
must score below every detection already evaluated in its category, which a
lower global score threshold guarantees. The register records this in the
proposal's status.

## Proposals awaiting decisions

The [register](../propositions.md#review-of-2026-11-15) marks the twelve
proposals completed with their IDs and records the decisions above. **98
proposals remain pending**. No rejection or deferral is inferred from the
decision to leave them pending.

## Checks performed

| Executed check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 vault Markdown files, 60 references, 294 cards |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, 0 stale (13 regenerated by `sync_catalog.py`) |
| `python3 scripts/learning_path.py` | OK: 60 references, 294 cards, minimum 260 lexical words, 0 errors |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 62 tests pass |
| `inventaire_cartes.py vault` and `--compare` with the starting inventory | 294 cards, no anomalies; 12 IDs added, none removed or changed |
| `compare_protected.py` (2026-11-14 tool) against `951c0b3` | 0 existing expected answers, answers or Source lines changed; 2 questions changed (CV-SOT-002, CV-MATCH-APPRIS-005); 12 additions; 15 references changed |
| `check_anchors.py` (2026-11-14 tool) on `vault/` and this directory | 3,500 local links and heading anchors resolve |
| `python3 -I checks/<subject>.py` for the 12 subjects | 12 scripts pass (92 checks) |
| `git diff --check` | No whitespace errors |

Card-file diffs only append lines, except for the two reworded question lines.
In the reference front matter, only `revision` changed.

## Sources and access

Each subject report lists the passages read. Implementation claims were
checked in code at a release tag or commit:

- OpenCV 4.13.0 on GitHub raw, because docs.opencv.org returns HTTP 403 from
  this environment;
- torchvision v0.29.0;
- pycocotools at `8c9bcc3`;
- the official SORT code at `2236dff` and filterpy at `5df4e09`;
- scikit-image v0.25.2.

Scientific claims were checked in the papers themselves:

- Faster R-CNN, RetinaNet and Fast R-CNN;
- LVIS App. B;
- Bewley et al. 2016;
- ORB-SLAM (arXiv 1502.00956);
- Horaud and Dornaika (arXiv 2311.12655);
- Hirschmüller 2008;
- Gelfand et al. 2003, including Fig. 3 read on the rendered page;
- Beucher and Meyer.

Context7 is unavailable in this session. Torr's degeneracy and GRIC papers
were not reachable (core.ac.uk returned 403). Hartley and Zisserman remains
unread.

**Executed code beyond the stdlib scripts:**

- A synthetic RANSAC check and a FLANN timing run with a locally installed
  OpenCV 4.11.0, not 4.13.0. The report gives the source comparison that
  supports the equivalence.
- A NumPy cross-check of the ICP eigenvalues.
- A run of `cv2.watershed` 4.11.0 against scikit-image 0.25.2, which
  confirmed the mislabelled pixel counts.

The pinned `sort.py` was not run. filterpy is not installed, and installing
it was refused by the session's permission policy. The card rests on a
pure-Python port of the relevant lines.

## Limitations

This is agent self-review. It establishes neither independent scientific
validation (FR-037) nor learner proficiency. Every number is a constructed
example. No image, video, LiDAR or robot experiment was run, and the proposed
checks are not executed protocols. The date was kept at 2026-11-15 for the
whole batch, although part of the work ran after midnight.

Obsidian and AnkiDroid rendering are not verified. To check on the phone: the
inline matrix in CV-ECC-004, and the long fronts of CV-EPIPOLAIRE-006,
CV-ICP-006 and CV-DETECTEURS-014.

No Anki package is rebuilt. The twelve new notes and the two reworded
questions reach the phone only through a new package: **to republish with
`paquet-anki`**, then check the import (twelve additions, 282 updates or
unchanged) and the rendering on the device.
