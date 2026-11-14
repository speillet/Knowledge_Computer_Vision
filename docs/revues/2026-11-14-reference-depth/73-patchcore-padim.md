# Review — Inspection: golden templates, PatchCore and PaDiM — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is a method note covering three models of normality (golden template,
PatchCore, PaDiM) and the inspection protocol that decides whether one is usable.
Metric definitions shared with segmentation and other applications stay in
[CV-METRIQUES-APPLIQUEES](../../../vault/130-evaluation-fiabilite/references/134-metriques-applications.md);
this note gives the anomaly-specific protocol (MVTec threshold procedure, PRO limits,
statistics of rare defects) and links there for the rest.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ANOMALIES-001 | "PaDiM estimates covariance distributions by position": imprecise; PaDiM fits one multivariate Gaussian $\mathcal N(\mu_{ij},\Sigma_{ij})$ per patch position (PaDiM §III-B, Fig. 2). Mahalanobis geometry and $\epsilon I$ regularization confirmed (§III-B eq. 1, §III-C eq. 2). Template compared with an aligned reference: grounded in MVTec's variation model (§2.2.4, §4.1.5). Language: "none knows about any possible defects", "imposes of check" | Comparison: chooses a model of normality from alignment, variability and cost | 3 expected criteria; 362 → 369 lexical words | ID, question, tags and heading unchanged; wording aligned with the reference appendix | Minor | Sourced precision of the expected answer; language fixes in explanation and blocking errors |
| CV-ANOMALIES-002 | Coreset purpose (reduce redundancy, storage and inference time while keeping coverage) confirmed (PatchCore §1, §3.2, Algorithm 1, §4.4.2). Expected answer said "memory and research" for *search*: a mistranslation that alters meaning. "hedging" for *coverage*, "coin" for *part*, "gluton selection" for *greedy selection* | Reasoning: why coverage, not frequency, is the selection objective | 2 expected criteria; 336 → 342 lexical words | ID, question, tags and heading unchanged | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line label corrected |
| CV-ANOMALIES-003 | Diagnosis by paired acquisition, constant preprocessing and verified parts: project protocol, correctly labelled. Expected answer said "actually controlled parts" for parts whose condition was physically verified; "iron physically controlled parts", "Survey built", "Paired experience", "false releases", "pretreatment" | Diagnosis: separates acquisition shift from product drift | 3 expected criteria; 284 → 288 lexical words | ID, question, tags and heading unchanged | Minor | Meaning-restoring fix of the expected answer; language fixes; "deducted" → "deduced" in Source |
| CV-ANOMALIES-004 | Operating-point and sample-size reasoning: project protocol; AUROC as a ranking summary consistent with PatchCore §4.1 and MVTec §4.3. Expected answer "compare template/nominal anomaly then measure rejections" was obscure; "false discharges among the conformants", "A AUROC", "rare defects of need", "Criteria for correction of the case" | Design: baseline and validation with rare defects and a cycle time | 3 expected criteria; 382 → 395 lexical words | ID, question, tags, `cas_pole` tag and heading unchanged | Minor | Meaning-restoring fix of the expected answer; language fixes |

Expected-answer changes:

- CV-ANOMALIES-001 (sourced precision, PaDiM §III-B): "Template compares to an aligned
  reference; PatchCore uses a feature bank; PaDiM estimates covariance distributions by
  position." → "The template compares with an aligned reference; PatchCore uses a bank
  of nominal patch features; PaDiM estimates a multivariate Gaussian (mean and
  covariance) per patch position."
- CV-ANOMALIES-002 (meaning-restoring language fix): "Reduce the bank by maintaining a
  useful representation of its diversity, to limit memory and research." → "Reduce the
  bank while keeping a useful representation of its diversity, to limit memory and
  nearest-neighbor search cost."
- CV-ANOMALIES-003 (meaning-restoring language fix): "…feature distribution to nominal,
  then examine actually controlled parts." → "…feature distribution with the nominal
  reference, then examine parts whose condition has been physically verified."
- CV-ANOMALIES-004 (meaning-restoring language fix): "…compare template/nominal anomaly
  then measure rejections and defects missed…" → "…compare a template baseline with a
  nominal-only anomaly model, then measure false rejections and missed defects…".

## Reference findings

Claims of revision 7 checked against their passages:

- Nearest-neighbour proximity score with a distinct PatchCore aggregation and
  re-weighting: confirmed (PatchCore §3.3, eqs. 6–7).
- PaDiM score $\sqrt{(f-\mu)^{\mathsf T}\Sigma^{-1}(f-\mu)}$ with regularized covariance:
  confirmed (PaDiM §III-B eq. 1, §III-C eq. 2; $\epsilon=0.01$ in §IV-B).
- Golden template as a project baseline: retained, now grounded in MVTec's variation
  model (per-pixel mean and standard deviation after alignment, §2.2.4, §4.1.5) and its
  failure on randomly varying surfaces (§4.4.5).
- No scientific error was found in revision 7. Its body was shallow (one to three
  sentences per section) and contained mistranslations that obscured meaning:
  "Detect nominal deviations" (deviations from nominal), "nominal images of reference
  and acquisition", "fault produced", "Banking and finding neighbors", "Question of
  work", "Reference Response", "material results", "hedging policy", "furthest from its
  neighbor", "gluton selection", "false discharges among the conformants", "set-aside
  sets".

New claims verified for revision 8 (main ones):

- PatchCore: cold-start definition (abstract, §1); single anomalous patch suffices (§1);
  less reliance on alignment and no fixed input shape compared with PaDiM (§2); eqs. 1–4,
  mid-level features and ImageNet bias (§3.1); minimax facility location eq. 5, NP-hard,
  greedy approximation and random projection (§3.2, Algorithm 1); eqs. 6–7, bilinear
  upsampling, $\sigma=4$ "did not optimize" (§3.3); MVTec preprocessing 256/224 and
  class-average AUROC, pixel AUROC, PRO (§4.1); Tables 1–5; $p=3$ and blocks 2+3
  (§4.4.1); stride ablation 97.6/96.8, bank usage under 30% to nearly 95%, coreset beats
  random and proxies (§4.4.2); MTD on which PaDiM "cannot be applied directly" (§4.6);
  transferability limitation (§5); WideResNet-50 blocks 2 and 3 and faiss (App. A);
  backbone stability (App. C.2); resolution effect (App. C.3); 19 false positives and
  23 false negatives, error sources including cropping (App. C.4).
- PaDiM: one-class setting and complexity independent of training size (§I); grid
  from the largest activation map and random dimension selection (§III-A); eqs. 1–2
  (§III-B, §III-C); metrics, pixel-AUROC bias, PRO, Rd-MVTec AD (§IV-A); backbones,
  layers, $\epsilon=0.01$, bicubic resizing, $\sigma=4$ (§IV-B); Tables I and II (§V-A);
  Tables III and V (§V-B); Table VI and the 5.3/8.8/12.2 pp drops (§V-C); Tables VII and
  VIII, CPU timings and memory (§V-D).
- MVTec AD (CVPR 2019): dataset composition and per-category counts (§3, Table 1);
  variation model (§2.2.4, §4.1.5, §4.4.5); threshold estimation with a minimum defect
  area on defect-free validation images (§4.3).
- PRO definition and the 30% false-positive-rate limit (Bergmann et al., Uninformed
  Students, §IV-B).
- Greedy k-center factor-2 bound (Sener and Savarese, §4.3).
- ResNet output sizes $56\times56$, $28\times28$, $14\times14$ at $224$ px (He et al.,
  Table 1).

Disagreements between the paper and implementations, recorded in the note (FR-036):

| Aspect | Paper | Implementation |
| --- | --- | --- |
| PatchCore image score | Maximum patch distance re-weighted by eq. 7 (§3.3) | Official code `fcaa92f`: README command uses `--anomaly_scorer_num_nn 1`; image score is the plain maximum (`patchcore.py` L313–L322), no eq. 7. anomalib v2.3.0: eq. 7 with `num_neighbors=9` (`torch_model.py` L385–L442) |
| PatchCore distance | Euclidean norm | Official code: faiss `IndexFlatL2`, which reports squared distances (faiss wiki); ranking unchanged |
| Coreset initialization | Algorithm 1 starts from an empty subset | Official approximate sampler: mean distance to 10 random start points kept in the running minimum (`sampler.py` L118–L171) |
| PaDiM regularization | $\Sigma+\epsilon I$, $\epsilon=0.01$ | anomalib v2.3.0: $+0.01I$, then $+10^{-5}I$ before inversion (`multi_variate_gaussian.py` L140–L165) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 326 → 5,174. The length
comes from treating three models of normality and an inspection protocol; about 28%
of the tokens are tables, pseudocode and the Mermaid diagram. Metric
definitions shared with other tasks are linked to CV-METRIQUES-APPLIQUEES rather than
restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Cold-start and one-class definitions; MVTec input contract (counts, sizes, 256/224 preprocessing); output grids $28\times28$ and $56\times56$, upsampling, smoothing, image score; crop-frame mapping; pipeline role and downstream operating point |
| Intuition | Shallow | Developed | One mechanism per method; constructed date-code illustration tied to MVTec §4.4.5; Mermaid diagram of the inspection and refit loop |
| Prerequisites | Shallow (two links) | Developed | Links to CV-ECC, CV-HOMOGRAPHIE, CV-FLANN, CV-MORPHO, CV-METRIQUES-APPLIQUEES, CV-FIABILITE, CV-IMAGERIES |
| Assumptions | Shallow | Developed | Clean nominal set, covered variability, geometric consistency per method, defect visibility, local evidence; degenerate cases (rank deficiency, image size, crop, zero variance) |
| Procedure | Shallow | Developed | Pseudocode for the three methods; purpose of each step; comparison table |
| Mathematics | Shallow (two formulas) | Developed | Variation model and first-order misregistration tolerance; PatchCore eqs. 1–7 with the derived $[1-1/b,1)$ range of the eq. 7 weight; PaDiM eqs. 1–2, eigen-direction reading, $\mathbb E[M^2]=d$, affine invariance lost with $\epsilon I$; worked examples A–D |
| Parameters | Shallow (list) | Developed | Twelve-row table with source values and implementation defaults; four-step tuning approach |
| Properties | Shallow | Developed | Position dependence with the Rd-MVTec result and its limit; factor-2 coverage bound and why it does not transfer to the shipped code; coverage is not correctness; training-size dependence; uncalibrated scores; no detection guarantee |
| Cost and implementation | Shallow (one sentence) | Developed | Cost drivers with named variables; reported GPU and CPU timings with setting; worked example F (cycle time); official PatchCore and anomalib v2.3.0 contracts; execution status |
| Evaluation | Shallow | Developed | Metric table (image AUROC, pixel AUROC, PRO, MVTec threshold protocol, F1-optimal count); published results with setting; worked example E (zero-miss bound); proposed baseline and test-time shift variation with confounds; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices among the three methods, supervised models and rules; industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/73-patchcore-padim.py`](checks/73-patchcore-padim.py) (24 assertions):
resolution trace (56/28 grids, 32 and 96 original pixels per cell and neighbourhood,
64 px crop border, 12.5% of the width, 2.5 px scratch); PatchCore bank (156,800
features, 642/64/6.4 MB, $1.26\times10^{10}$ and $1.26\times10^9$ search MACs,
$3.15\times10^{11}$ selection MACs, 98.3 GB full distance matrix); PaDiM (126.7 MB and
3.80 GB, 1.91 GB triangular, 31.36 M and 948.6 M MACs, rank deficiency for MVTec, scores
10 versus 0.4994, $\sqrt{100}$ and $\sqrt{550}$); template tolerance ($z=5$ and 1,
0.35 px); zero-miss bound (13.9% for 20 parts, 299 parts for 1%, about 17 defective test
images per MVTec defect type); cycle time (utilization 1.2 and 0.34); eq. 7 weight range
(0.8889, 0.98336, 0.99772 after doubling distances).

## Applied corrections

- [Reference](../../../vault/70-reconnaissance-representations/references/73-patchcore-padim.md),
  revision 7 → 8: body rewritten and deepened as above; language fixed in both
  appendices ("Question of work" → "Working question", "Reference Response" → "Reference
  answer", "material results" → "hardware results", "On the contrary" → "Conversely",
  "relative to their size" → "relative to their dimension", "imposes of check" →
  "requires checking", "hedging policy … furthest from its neighbor" → "coverage policy …
  farthest from its nearest neighbor", "searching, extracting, and transferring memory" →
  "search, feature extraction and memory transfers", "Paired experience" → "Paired
  experiment", "compliant parts" → "conforming parts", "false releases" →
  "false-rejection rate", "Translation in industrial load" → "Translation into production
  load", "false discharges among the conformants" → "false rejections among conforming
  parts", "set-aside sets" → "held-out sets", "a drift produced at the nominal" → "a
  product drift into the nominal reference", "gluton selection" → "greedy selection");
  reference answers aligned with the corrected expected answers; sources split into
  scientific and implementation sources; closing provenance line replaced. Front matter
  unchanged except `revision`; H1 and the eight `### CV-…` headings kept.
- [Cards](../../../vault/70-reconnaissance-representations/73-patchcore-padim.md):
  expected answers of all four cards changed as quoted above. Identical language fixes in
  the further explanations, plus: "none knows about any possible defects" → "none of them
  models the possible defects"; "Describe these scores as universal probabilities of
  failure" → "Describing these scores as universal defect probabilities"; "Undersampling
  changes a hedging/cost trade-off; measuring defects and false releases" → "Subsampling
  trades coverage against cost; measure missed defects and false rejections";
  "Compromise of representation" → "Representation tradeoff"; "compliant coin" →
  "conforming part"; "coins misclassified as nominal" → "parts wrongly labeled as
  nominal"; "product utility" → "usefulness in production"; "light system" → "lighting
  system"; "Diagnosis by Hypotheses … a break in the pretreatment" → "Diagnosis by
  hypotheses … a change in preprocessing"; "Survey built: iron physically controlled
  parts under the two acquisitions" → "Constructed investigation: image physically
  inspected parts under both acquisition setups"; "Provide for review … rare defects of
  need" → "Plan review … evidence on the rare critical defects"; "Criteria for correction
  of the case … Case built" → "Grading criteria for the case … Constructed case". Source
  lines: "gluton selection" → "greedy selection", "deducted" → "deduced". Questions, IDs,
  objectives, families, tags and target deck unchanged.

No other vault card repeats a corrected claim (`rg` over `vault/` for PatchCore, PaDiM,
coreset, golden template and MVTec: only progress-log, inventory and index entries, plus
CV-METRIQUES-APPLIQUEES, which cites MVTec AD2 for PRO and does not contradict this note).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run; the register is a shared file). The 2026-10-20 proposal "Test the
contamination of the nominal bank" was never registered; its content now lives in the
CV-ANOMALIES-002 explanation (2026-11-08) and is not proposed again.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-ANOMALIES-01 | CV-ANOMALIES | From zero missed defects on $n$ defective parts, compute the one-sided 95% upper bound on the miss rate and the $n$ needed to support a stated requirement | No card trains quantitative operating-point evidence; the evaluation family is absent | Evaluation; Evaluation, worked example E | 1 card, 3 criteria ($(1-p)^n=\alpha$; 13.9% for 20; 299 for 1%) | Clopper and Pearson 1934 (binomial confidence limits); [MVTec AD, Table 1](https://openaccess.thecvf.com/content_CVPR_2019/papers/Bergmann_MVTec_AD_--_A_Comprehensive_Real-World_Dataset_for_Unsupervised_Anomaly_CVPR_2019_paper.pdf) |
| P-CV-ANOMALIES-02 | CV-ANOMALIES | Explain what $\epsilon$ decides in PaDiM when $d$ exceeds the number of nominal images, and predict the score of a deviation along a never-seen direction | Rank deficiency and the role of regularization are untested; the understanding family is absent | Understanding; Mathematics, worked example C | 1 card, 3 criteria (rank $\le N-1$; $1/\sqrt\epsilon$ amplification; threshold not transferable across $d$) | [PaDiM §III-B eq. 1, §IV-B, Table VIII](https://arxiv.org/html/2011.08785v1) |

No defective question was found.

## Sources

Scientific sources, opened at the passages listed:

- Roth et al., PatchCore, [arXiv HTML v2](https://arxiv.org/html/2106.08265v2) (text
  extracted locally): abstract, §1, §2, §3.1 (eqs. 1–4), §3.2 (eq. 5, Algorithm 1),
  §3.3 (eqs. 6–7), §4.1, Tables 1–5, §4.2, §4.3, §4.4.1, §4.4.2, §4.5, §4.6, §5,
  App. A, B, C.2, C.3, C.4.
- Defard et al., PaDiM, [arXiv HTML v1](https://arxiv.org/html/2011.08785v1): abstract,
  §I, §II, §III-A to §III-C, §IV-A, §IV-B, §V-A (Tables I–II), §V-B (Tables III–V),
  §V-C (Table VI), §V-D (Tables VII–VIII).
- Bergmann et al., MVTec AD, [CVPR 2019 PDF](https://openaccess.thecvf.com/content_CVPR_2019/papers/Bergmann_MVTec_AD_--_A_Comprehensive_Real-World_Dataset_for_Unsupervised_Anomaly_CVPR_2019_paper.pdf)
  (text extracted with `pdftotext`): §2.2.4, §3, Table 1, §4.1.5, §4.2, §4.3, §4.4.5.
- Bergmann et al., Uninformed Students, [arXiv HTML](https://arxiv.org/html/1911.02357): §IV-B PRO paragraph and Table I caption.
- Sener and Savarese, [ICLR 2018, arXiv 1708.00489v4 PDF](https://arxiv.org/abs/1708.00489): §4.3 and Algorithm 1.
- He et al., ResNet, [arXiv 1512.03385v1 PDF](https://arxiv.org/abs/1512.03385): Table 1.

Implementation sources (code read, not executed):

- [amazon-science/patchcore-inspection at `fcaa92f`](https://github.com/amazon-science/patchcore-inspection/tree/fcaa92f124fb1ad74a7acf56726decd4b27cbcad): `README.md` L26–L30; `src/patchcore/sampler.py` L39–L171; `src/patchcore/common.py` L14–L48, L186–L208, L332–L350; `src/patchcore/patchcore.py` L203–L228, L313–L322.
- [anomalib v2.3.0](https://github.com/open-edge-platform/anomalib/tree/v2.3.0): `models/image/patchcore/lightning_model.py` L143–L147; `models/image/patchcore/torch_model.py` L385–L442; `models/image/padim/torch_model.py` L54–L57, L112–L115; `models/components/stats/multi_variate_gaussian.py` L140–L165.
- [faiss wiki, MetricType and distances](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances): `METRIC_L2` reports squared Euclidean distances (read with WebFetch).

Failed accesses and limits:

- MVTec LOCO (Bergmann et al., IJCV 2022, Springer) was not read: the Springer page
  redirected to an authorization endpoint. The note therefore states the "locally
  normal but misplaced" limitation as a project deduction, without citing a
  logical-anomaly benchmark. The MVTec AD IJCV 2021 extension was not attempted; the
  CVPR 2019 paper and the PRO definition of Uninformed Students covered the claims made.
- Context7 was not available in this session (see the scope record); official code at
  a commit and a release tag replaced it.
- The year and venue of PatchCore and PaDiM are not stated in the note: the arXiv pages
  opened do not give them.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | ECHEC caused only by `40-features-matching/references/46-harris-shi-tomasi.md` (another agent's in-progress file); no error in the files of this subject |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/73-patchcore-padim.py` | 24 checks passed |
| `git diff --check -- vault/70-reconnaissance-representations/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/70-reconnaissance-representations/73-patchcore-padim.md` | 4 cards, 288 to 395 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged; `$$` balanced; local links resolve |

No anomaly model, registration or benchmark was executed; the proposed baseline and
variation are protocols, not results. The Mermaid diagram and tables were not rendered
in Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is agent
self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-ANOMALIES
revision 8, CV-ANOMALIES-001 to -004, expected-answer and language corrections listed
above, Agent Claude Code self-review, to republish with `paquet-anki`) and the proposal
register (P-CV-ANOMALIES-01, P-CV-ANOMALIES-02).
