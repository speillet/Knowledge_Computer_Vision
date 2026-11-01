# Review of depth and consistency –  2026-10-24

## Result

The 60 subjects and their 282 flashcards were examined on the recall objective, relevance to a confirmed engineer and the development of explanations. **274 enriched answers**, eight preserved because already developed; no additions or removals of flashcard. The canonical 60 reference notes take a revision and link their properties to two guided cases, with reference question and answer.

| Lexical words by answer | Before | After |
| --- | ---: | ---: |
| Minimum | 32 | 180 |
| Median | 57 | 200,5 |
| Maximum | 252 | 329 |

Calculation: `len(re.findall(r'\w+', Reponse))`, not including question, Source or tags. The threshold of 180 is an editorial choice specific to this request: it coordinate frame answers a few lines, without establishing an optimal length or guaranteeing quality. The answer remains noted on a finite core; long explanations serve to understand and reconstruct, without integral recitation.

## Relevance and design corrections

The lot is relevant to the profile: classical mechanisms, contracts of modern methods, geometry, evaluation and industrial decisions. The recurring weakness was to give a correct conclusion without explaining enough how to find it or verify that it applies. The additions explicitly discriminate mechanism, interpreted case, assumptions, and check, rather than an isolated definition or benchmark result without context.

The synthesis flashcards and their further study remain distinct: SIFT pipeline versus descriptor construction; apparent flow versus Farnebäck algorithm; SORT filtering versus association choice; rank/identification versus local covariance. There is no reason to withdraw from this pass. Relevant families depend on the topic: adding eight families to each algorithm would create repetitions without any useful new purpose.

The new calculations are deductions under assumptions and the ablations are proposed. They do not constitute published measurements or executed image, video, sensor or hardware experiments. The earlier nuclei remain preserved. The TensorRT Quantization Workflows link has been confirmed since primary navigation after a first extraction failure; the reference note lookup date is updated, without changing the flashcards Source fields.

## Consistency of the course

The [Senior Course](../../../vault/01-Parcours/Parcours-senior.md) gives nine steps and an explicit order of the 60 subjects, adapted to the ML/DL/segmentation achievements. Thematic numbers no longer implicitly define progress. The IoU precedes NMS/SORT; the filtering precedes the association; coordinate frames and calibration precedes fusion/reconstruction. Prerequisites are required: not all the AP COCO is required for SORT, nor all the ESKF for the linear Kalman.

Each step has a passing criterion. Three integrations verify the transfer: registration/metrology, detection/monitoring, spatial perception. These are proposed exercises, with no result announced. The order and coverage are script-controlled; an unknown prerequisite, cycle, duplicate, or absent subject causes the check to fail.

The 119 further study APP remains open. This work improves the current batch and does not claim to cover all computer vision algorithms or certify senior mastery.

## Reports by subject

Each report indicates the flashcards, the sources actually consulted and the scope of the confrontation. The length figures and traceability are automatic; the relevant verdicts are a self-review per agent.

| Rapport | Flashcards | Enriched answers | Point developed |
| --- | ---: | ---: | --- |
| [CV-SVD](11-moindres-carres-svd.md) | 9 | 5 | whitening, loss of rank and distinction adjustment – identifiability |
| [CV-SE3](12-rotations-se3.md) | 6 | 5 | coordinate frames composition and left/right disturbances |
| [CV-FUSION](13-kalman-ekf-eskf.md) | 6 | 5 | innovations, covariance and reset of the ESKF |
| [CV-FACTEURS](14-graphes-facteurs.md) | 5 | 4 | graph, gauge and cost of disposal |
| [CV-ACQUISITION](21-exposition-bruit-echantillonnage.md) | 4 | 4 | exposure, noise and sampling related to the task |
| [CV-CAPTEURS](22-capteurs-horodatage.md) | 4 | 4 | separate exposure time, reading and synchronization |
| [CV-IMAGERIES](23-imageries-specialisees.md) | 3 | 3 | physical geometry, line-scan and generalization unit |
| [CV-FILTRES](31-filtrage-gradients.md) | 4 | 4 | effect of support, bilateral units and sub-sampling |
| [CV-CANNY-HOUGH](32-canny-hough.md) | 4 | 4 | linking contours, votes and geometric validation |
| [CV-MORPHO](33-morphologie-composantes.md) | 3 | 3 | Geometric support, topology and connectivity convention |
| [CV-SIFT](41-sift.md) | 7 | 7 | normalizations, ratio ambiguity and geometric coverage |
| [CV-ORB](42-orb.md) | 6 | 6 | separate detection, orientation, representation and norm |
| [CV-MATCHING](43-detecteurs-matchers.md) | 4 | 4 | contracts of steps and diagnosis before change of method |
| [CV-MATCH-APPRIS](44-superpoint-lightglue-loftr.md) | 5 | 5 | compatibility features – matcher, resolution and validation |
| [CV-ECC](45-recalage-ecc.md) | 3 | 3 | photometric criterion, convergence basin and masks |
| [CV-CORNERS](46-harris-shi-tomasi.md) | 5 | 5 | structure tensor, observable directions and repeatability |
| [CV-FAST-BRIEF](47-fast-brief.md) | 5 | 5 | Segment testing and binary signature under transformations |
| [CV-FLANN](48-flann.md) | 4 | 4 | neighbor recall, index ratio and depreciation |
| [CV-HOMOGRAPHIE](51-ransac-homographie.md) | 7 | 7 | sampling success, coverage and validity of the model |
| [CV-ZHANG](52-calibration-zhang.md) | 7 | 7 | View constraints, resize and check out of learning |
| [CV-EPIPOLAIRE](53-epipolaire-pnp-triangulation.md) | 5 | 5 | Epipolarity, pose and depth distinguished by their contract |
| [CV-BA](54-bundle-adjustment.md) | 4 | 4 | gauge, robust residuals and optimization blocks |
| [CV-MULTICALIB](55-calibration-multicapteurs.md) | 3 | 3 | separating spatial transformations and desynchronization |
| [CV-FISHEYE](56-calibration-fisheye.md) | 5 | 5 | Angular coverage and projection model compatibility |
| [CV-HANDEYE](57-calibration-hand-eye.md) | 5 | 5 | AX=XB conventions, excitation and independent validation |
| [CV-STEREO](61-stereo-profondeur.md) | 4 | 4 | disparity, depth uncertainty and rectified geometry |
| [CV-ICP](62-recalage-global-icp.md) | 5 | 5 | initialization, correspondences and directions with minimal constraints |
| [CV-VIO](63-slam-vio.md) | 5 | 5 | inertial fusion, gauges and evaluation without masking errors |
| [CV-BEV](64-nuages-bev-occupation.md) | 5 | 5 | visibility, unknown and limits of spatial representation |
| [CV-REPRESENTATIONS](71-representations-transfert.md) | 5 | 5 | architecture bias, scale and transfer protocol |
| [CV-CLIP](72-clip-siglip.md) | 4 | 4 | image – text contrast, candidates and domain offset |
| [CV-ANOMALIES](73-patchcore-padim.md) | 4 | 4 | normal reference, near patches and business decision |
| [CV-OCR](74-ocr-documents.md) | 3 | 3 | OCR string, standardization and document-specific metric |
| [CV-BIOMETRIE](75-embeddings-biometrie.md) | 2 | 2 | verification, identification and point of operation |
| [CV-NMS](81-nms.md) | 6 | 6 | removal, equality threshold and recall of nearby objects |
| [CV-DETECTEURS](82-detection-fasterrcnn-yolo-detr.md) | 13 | 12 | Architecture contracts, matching and decomposition of errors |
| [CV-OPENVOC](83-detection-open-vocabulary.md) | 3 | 3 | Variable vocabulary, protocol, and localized output |
| [CV-POSE3D](84-detection-pose-3d.md) | 4 | 4 | metric contract and ambiguities of pose/symmetry |
| [CV-WATERSHED](91-otsu-distance-watershed.md) | 5 | 5 | histogram, distance and role of markers |
| [CV-GRABCUT](92-grabcut-regions.md) | 3 | 3 | Conditional optimization and the role of user constraints |
| [CV-SEGMENTATION](93-semantique-instances-panoptique.md) | 4 | 4 | Output unit and aggregation of segmentation errors |
| [CV-SAM](94-sam-sam2.md) | 3 | 3 | prompts, mask ambiguity, and time memory |
| [CV-FLOT](101-flot-optique.md) | 4 | 4 | luminance stress, aperture and dense correspondence |
| [CV-VIDEO](102-points-actions-video.md) | 4 | 4 | point trajectories, visibility and time horizon |
| [CV-FARNEBACK](103-farneback.md) | 5 | 5 | quadratic approximation and displacement capture domain |
| [CV-SORT](111-sort.md) | 8 | 8 | filtering, assignment and life cycle of tracks |
| [CV-ASSOCIATION](112-deepsort-bytetrack.md) | 4 | 4 | gating, appearance and association of low scores |
| [CV-SOT](113-tracking-monoobjet.md) | 2 | 2 | Local search, adaptation and identity after occlusion |
| [CV-CORRELATION](114-mosse-kcf.md) | 5 | 5 | circulation, window and risk of contamination of the model |
| [CV-MEANSHIFT](115-meanshift-camshift.md) | 4 | 4 | backprojection, local mode and window adaptation |
| [CV-VLM](121-vlm-grounding.md) | 4 | 4 | connector, visual anchor and image dependency test |
| [CV-DIFFUSION](122-generation-restauration.md) | 3 | 3 | Conditional distribution and restoration fidelity |
| [CV-RENDU3D](123-nerf-gaussian-splatting.md) | 3 | 3 | synthesis of views, observation support and geometry |
| [CV-IOU-AP](131-iou-ap-coco.md) | 7 | 7 | matching, classification and COCO conventions |
| [CV-METRIQUES-TEMPS](132-tracking-trajectoires.md) | 5 | 5 | identity, HOTA aggregation and trajectory alignment |
| [CV-FIABILITE](133-donnees-generalisation.md) | 5 | 5 | Split unit, selection and calibration of probabilities |
| [CV-METRIQUES-APPLIQUEES](134-metriques-applications.md) | 4 | 4 | topology, physical surfaces and uncertain references |
| [CV-PIPELINE](141-contrats-profiling-video.md) | 5 | 5 | Contracts, queues and information age |
| [CV-QUANT](142-quantification-runtimes.md) | 5 | 5 | scale, saturation and real runtime execution |
| [CV-DEPLOIEMENT](143-edge-reproductibilite.md) | 4 | 4 | sequential neck, thermal regime and reproducibility |

## Controls carried out

Comparison reference: `8c428b458753740737bbc79659eaa2fd797a6a17`. Initial preparation on `docs/deepen-cards-and-learning-path`. The evidence below describes local controls before publication; PRs and their mergers follow in the repository's GitHub history.

- `python3 scripts/check_vault.py` : **OK, 142 Markdown, 60 reference notes, 282 flashcards**.
- `python3 scripts/learning_path.py` : **OK, 60 ordered topics, 282 answers, minimum 180 lexical words, no errors**.
- `python3 scripts/sync_catalog.py --check` : **19 documents, no expired**.
- `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests`: **55 successful tests**, none ignored. Five new tests cover dependency order, cycle, unknown prerequisite, absent/duplicated/unknown subject and the actual path.
- `python3 examples/pilot_math.py`: Pilot calculations performed, without changing their expectations. These are not experiments on images.
- `revue-cartes` skill inventory, compared to the initial snapshot: **no ID missing, added or identity changed Anki**. Complementary verification: questions, objectives, source, tags, subdecks, kernels and blocking errors unchanged.
- `uv run --no-project --with genanki==0.13.1 python scripts/build_apkg.py`, then `python3 scripts/build_apkg.py --verifier dist/CV-Pilote.apkg`: **OK, 282 notes and flashcards, 14 subdecks, an embedded SVG**.
- Comparison to the initial local package: **274 modified notes, zero addition, zero withdrawal; the 282 GUID and the 1153189853 model are retained**. This is a work package from a modified tree, not a release.
- `uv run --no-project --python 3.12 --with anki==26.9.3 --with genanki==0.13.1 python scripts/simulate_anki_import.py`: **OK**, import and reimport of the same package, three revised flashcards, response modification and then response/style in a copy. Preserved identities and history, applied updates, no duplicates in the disposable collection.
- `git diff --check`: no space error. Catalog and links of the controlled vault; the generated packet remains out of Git.

## Scope of the review and limits

Educational self-review and documentary confrontation **Targeted**, agent Codex, 2026-10-24. Central sources are primary articles or documentation; Context7 was used for OpenCV checks. The reports distinguish the passages read from the summaries, deductions and failed accesses with their fold. Not all statements in the previous content are reconfirmed line by line in this pass. No content is declared “re-read” by an independent person.

The tests verify the structure, identities and import in the Anki engine, without proving the Obsidian/AnkiDroid rendering, the import on the phone or the effectiveness of the recall. The learning sessions and application tests are still to be carried out. Previous dated evidence from the journal is retained.

## Standards

Review `code-review` separate from diff `8c428b4…c729455`: no documented violation established. Commits follow Conventional Commits and separate their intentions in accordance with `CONTRIBUTING.md`. The reports distinguish documentary self-review, built calculations, engine tests Anki and made Android as yet unverified, as requested by `AGENTS.md` and educational/export contracts. No unwarranted changes in identity or format found in the Hunks examined.

A minor design judgment was retained: possible **Shotgun Surgery** in `scripts/learning_path.py`. The generator froze “60 subjects”, “119 further study” and “180 words”, while these values existed in the data or constant. An evolution could leave inaccurate accounts in a page that `sync_catalog --check` considered up to date.

Resolved in `758f57d`: calculated accounts from entries and catalog, threshold shared with `MIN_ANSWER_WORDS`, without duplication of target partition. The targeted confirmation has relaunched the six tests of the course, including the regression on subjects, backlog and threshold; the 19 documents generated are unchanged. The twelve heuristics of the skill were examined; no other sufficiently concrete smell was retained. No violation or judgment remaining on the scope under review.

## Spec

No actionable deviation identified between `8c428b4` and `c729455` on the controlled perimeter:

- **Depth and Correctibility**: framing lines 10 – 17, FR-015; 274 responses modified, 282 flashcards preserved, minimum 180 lexical words and median 200,5. Inspected examples develop mechanism, assumptions, diagnosis or limitations related to the issue. The threshold remains editorial; kernels and blocking errors remain unchanged.
- **Consistency**: framing lines 18 – 21, T030; nine steps covering the 60 subjects only once, prerequisites met, passage criteria and three integrations proposed. Dependencies are about useful notions, without requiring all the AP COCO for SORT.
- **Invariants**: line framing 10, FR-016/020; comparison of 282 IDs, questions, sources, kernels and blocking errors without deviation. The 60 reference notes takes a single revision and retains status, provenance and prerequisites.
- **Scope**: framing lines 22 – 26, FR-037; balance sheet, reports and journal identify the self-review and its limits. Examples built, tests executed, Android rendering, recall and 119 open targets remain distinguished.

No unjustified enlargement noted. Targeted confirmation of `758f57d`: inventory accounts, shared threshold and variations covered by a test; no new deviations. This editorial and structural review does not replace any exhaustive scientific validation or tests on the phone.

Views: **Standards, zero violation and one minor judgment resolved; Spec, zero deviation**. After correction: **56 successful tests**, none ignored with genanki 0.13.1; OK scan and 19 up-to-date documents. These results complement the initial evidence of 55 tests, without rewriting them.
