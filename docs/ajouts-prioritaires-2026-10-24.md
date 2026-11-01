# Priority additions –  2026-10-24

Permitted Scope: Integrate existing RAs and complete priority gaps, as explicitly identified in the learner. Eight new reference notes and 38 flashcards targets classic matching, calibration and tracking. The 244 IDs of the batch after PR 16 are preserved; the current batch counts 60 reference notes and 282 flashcards.

## Choice of content and sources

The methods are chosen for their usefulness in choice or diagnosis, and not to artificially complete each family of flashcard. Each reference note provides contract data, mechanism, mathematics, limits, cost, evaluation and controlled variation. The proposed experiments are distinct from the analytical calculations actually performed.

| Subject | Gaps and skills | Source actually consulted |
| --- | --- | --- |
| Harris and Shi – Tomasi –  local structure and followable points | APP-017; APP-018: mechanism, choice, diagnosis and evaluation, operational use level | [Harris and Stephens 1988, self-correlation and corner response](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf) |
| FAST and BRIEF –  detect a corner and then describe its vicinity | APP-019; APP-020: mechanism, choice, diagnosis and evaluation, operational use level | [Rosten and Drummond 2006, §§2 – 3, test and learning segment](https://www.edwardrosten.com/work/rosten_2006_machine.pdf) |
| FLANN –  close search and distance contract | APP-022: mechanism, choice, diagnosis and evaluation, level of operational use | [Muja and Lowe 2009, §§2 – 3, approximate search and configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf) |
| Calibration fisheye –  Angular projection and off-centre validation | APP-026: mechanism, choice, diagnosis and evaluation, level of operational use | [OpenCV 4.13, fisheye, Detailed Description and EstimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html) |
| Hand-eye calibration –  solve AX = XB without mixing the coordinate frames | APP-027: mechanism, choice, diagnosis and evaluation, level of operational use | [OpenCV 4.13, CalibrateHandEye, coordinate frames, Equations and Minimum Movements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) |
| Farnebäck –  dense flow by polynomial expansion | APP-089: mechanism, choice, diagnosis and evaluation, level of operational use | [Farnebäck 2003, §§2 – 3, expansion and displacement, §3.5 multi-scale](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf) |
| MOSSE and KCF –  Correlation filter tracking | APP-093: mechanism, choice, diagnosis and evaluation, level of operational use | [Bolme et al. 2010, §§3.2 – 3.5, MOSSE, update and PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf) |
| MeanShift and CamShift –  follow an appearance distribution | APP-092: mechanism, choice, diagnosis and evaluation, level of operational use | [OpenCV 4.13, Meanshift and Camshift, Theory and Exit Contracts](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html) |

The OpenCV 4.13 documentation was consulted directly and with Context7: resolution `/websites/opencv_4_13_0`, then requests on fisheye/hand-eye conventions, corners/descriptors/matching, and flow/tracking. The interfaces have been checked, but no OpenCV or full solver calls have been executed. Publications FAST, BRIEF, FLANN, Farnebäck, MOSSE and KCF have been opened with their methodological passages; no historical speed figures are promised on the target material. The original PDF of Shi – Tomasi hosted by CMU was not accessible; the criterion and the contract OpenCV are supported by its official documentation.

## Inventory and depth

The ten corresponding APP entries remain versioned with their ID, skills, and dependencies, and point to the written reference notes. 119 targets remain open. A comparison of two methods shares a canonical reference note; it does not purport to process all their derivatives or implementations. A target promotion now requires a real reference note: the catalog refuses an absent reference or a duplicated APP ID.

## Controlled calculations

Standard Python, calculations executed out of repository: Harris answers −308,04 and 336 ; Hamming 2 ; example of built costs FLANN 2,1 against 0,3 s then 12 against 30 s; projection to 60° and focal length 300 px : 314,16 against 519,62 px; quadratic displacement (2,−1) px; converted flow (100,−50) px/s ; PSR 6 and Centroid 13 px. These calculations do not perform any detector, neighbor search, calibration, or video tracking. They are not a benchmark or a physical measure.

## Checks and limitations

Results executed: 37 successful tests; OK controller on 141 Markdown documents, 60 reference notes and 282 flashcards; up-to-date catalog on 18 documents; 129 APP IDs retained (ten reference notes associated, 119 open entries). The files of the 244 flashcards already present after PR 16 remain unchanged by this batch.

The official `main.js` Obsidian_to_Anki 3.6.0 has been reloaded and its SHA256 checked: `dcca559c8001a041ff11a5def4c6f9096969514249d1938db78ec6a7ee55bfef`. A temporary harness, with API Obsidian and simulated Anki identities, scanned the 141 files: 282 unique notes and IDs, 14 subdecks, then 282 updates and zero additions to the second pass. Maths, code block and SVG have been converted. No requests to Anki have been sent; harness is not included in the repository and does not prove the history or application rendering. Provenance agent and state `redige` preserved. Real export, historical Anki, Android rendering, recall and independent scientific validation remain open. The `.apkg` work present in the initial workspace is preserved without publication or reconstruction in this batch.

## Standards

`code-review` review of diff `046300b1…3776c973`, by a separate agent: no blocking or important deviation, no smell of actionable design. The catalog tests focus on target retention and denial of inconsistent metadata; they do not judge the scientific accuracy of flashcards.

## Spec

Two deviations identified and then corrected: priorities APP/reference notes now aligned in V0 for this lot devoted to the classical shortcomings expressed (FR-043); context eye-in-hand, calibration target fixed and sense of transformations redefined in CV-HANDEYE-004 for an autonomous revision (FR-007/016). Priority promotion is only for the ten targets processed, not the remaining 119. No other algorithmic blocking or perimeter overflow defects identified in this passage.

Standards: no observations to correct; Spec: two observations corrected. Application testing and the preparation of the 119 open targets remain distinct from this editorial delivery.
