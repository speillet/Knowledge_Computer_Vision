# Review — Point clouds, BEV and occupancy representations — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 0 important, 5 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the comparison note for spatial representations built from LiDAR
and cameras. Detection heads and 3D box metrics stay in
[CV-POSE3D](../../../vault/80-detection-pose/references/84-detection-pose-3d.md) and
neural reconstruction in
[CV-RENDU3D](../../../vault/120-generatif-multimodal/references/123-nerf-gaussian-splatting.md).
Inventory items APP-045 (Lift-Splat-Shoot) and APP-046 (BEVFormer) name this note as
their introduction; their mechanisms are now developed at comparison depth, which
does not close those items. The anchor `#cv-bev-005` of the card file, targeted by
`vault/01-Parcours/Poles-metiers.md`, is unchanged.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BEV-001 | Pillars group a vertical column and scatter learned features into a pseudo-image, with no z-binning hyperparameter: confirmed (PointPillars §2.1). Expected answer "then encoded in pseudo-image" was ungrammatical and blurred the scatter step. Source line cited OctoMap, unrelated to the claim | Comparison: what pillars, voxels and BEV keep of height | 2 expected criteria; 370 → 370 lexical words | "Box for each altitude" (cell for each height), "terminals" (bounds) mistranslated | Minor | Meaning-restoring fix of the expected answer; language fixes; Source line replaced by PointPillars §2.1, LSS §3 and BEVFormer §3.3 |
| CV-BEV-002 | Free, occupied and unknown are distinct states created by ray casting: confirmed (OctoMap §3.1, §3.2). Expected answer "masked" meant *occluded*; "Radius Model" meant *ray model*; "seniority" meant *age* | Understanding: keep unknown space explicit | 2 expected criteria; 350 → 351 | Wording aligned with the reference appendices | Minor | Expected-answer language fix; language fixes; Source line given OctoMap sections |
| CV-BEV-003 | Occupancy map as belief versus occupancy network as inside/outside function: confirmed (OctoMap §3.2; Mescheder et al. §3.1, §3.3); SDF sign convention and zero-level set confirmed (DeepSDF §3). "A high indoor score of a learned form" altered the meaning (*inside score of a learned shape*); the revision-6 body had the same error ("indoor/outdoor function") | Comparison: two meanings of "occupancy" | 2 expected criteria; 277 → 278 | Source line cited BEVFormer §3.4, unrelated | Minor | Expected-answer language fix ("form" → "shape"); meaning-restoring fixes; Source line updated |
| CV-BEV-004 | History alignment by ego-motion: confirmed (BEVFormer §3.4); transport formula and the range dependence of rotation-induced errors are project deductions (worked example D). "Rotation of the wearer" meant *platform*; "Verification built", "Aligning the historical" mistranslated | Diagnosis: timing and frame errors before architecture changes | 2 expected criteria; 294 → 295 | Wording aligned with the reference appendix | Minor | Expected-answer language fix ("deskew", "coordinate frame BEV"); language fixes; Source line updated |
| CV-BEV-005 | Interface needing frame, time, visibility and unknown semantics: consistent with OctoMap §3.1 and the `castRay` default that treats unknown cells as non-free (v1.10.0). "Single terms and merger" (single sensors and fusion), "validation of the order" (control), "collection" (perception module), "initial vacuum" (initial empty value) obscured the protocol | Design: warehouse perception interface and its evaluation | 3 expected criteria; 395 → 386 | Wording aligned with the reference appendices | Minor | Expected-answer language fix; language fixes; grading-criteria label fixed; Source line given OctoMap §3.1, the `castRay` lines and LSS §5 |

Expected-answer changes (no change of criteria):

- CV-BEV-001 (meaning-restoring, PointPillars §2.1): "The voxel also discretizes the
  height; the pillar groups the points of a column, then encoded in pseudo-image." →
  "The voxel also discretizes height; the pillar groups the points of a vertical
  column, whose learned features are then scattered into a pseudo-image."
- CV-BEV-002 (language): "The area may be masked, out of range or never observed; …"
  → "The area may be occluded, out of range or never observed; …"
- CV-BEV-003 (language): "The first represents a belief in observed/free/occupied
  space; the second models a continuous function inside/outside a form." → "The
  first represents a belief about observed free or occupied space; the second models
  a continuous inside/outside function of a shape."
- CV-BEV-004 (language): "Timestamps, ego-motion, deskew and transformation to the
  coordinate frame BEV before changing the architecture." → "Timestamps, ego-motion,
  deskewing and the transformation to the BEV frame, before changing the
  architecture."
- CV-BEV-005 (language): "Define expected objects/occupation, coordinate
  frames/time, visibility and uncertainty; design fusion and behavior in case of loss
  and then test rare obstacles, occlusions and latency." → "Define the expected
  objects or occupancy, frames and time, visibility and uncertainty; design the
  fusion and the behavior on sensor loss, then test rare obstacles, occlusions and
  latency."

## Reference findings

Claims of revision 6 checked against their passages:

- Probabilistic mapping separates free, occupied and unknown: confirmed (OctoMap
  §3.1). The body said "free, busy, and unknown": mistranslation of *occupied*.
- "An Occupancy Network approximates a continuous indoor/outdoor function":
  mistranslation of *inside/outside* that altered the meaning; corrected
  (Mescheder et al. §3.1).
- "A SDF uses a signed distance and a zero-level surface": confirmed (DeepSDF §3).
- "Lift-Splat-Shoot projects image features … with depth assumptions": confirmed and
  made precise (LSS §3.1, eq. 1).
- "BEVFormer aggregates views and time": confirmed (BEVFormer §3.3, §3.4).
- PointNet++ and BEVFusion are retained as links but were not re-read; the new body
  makes no specific claim about them.

Other language defects of revision 6: "no model BEV or robot executed", "merge
count", "Single terms", "field output". No scientific error was found apart from the
meaning-altering mistranslations above.

New claims verified for revision 7 (main ones):

- PointPillars: decoration to $D=9$, tensor $(D,P,N)$, simplified PointNet and max,
  scatter to $(C,H,W)$, no z-binning hyperparameter, 6k–9k non-empty pillars and ∼97%
  sparsity (§2.1); car ranges, 0.16 m, $P=12000$, $N=100$ (§4.2); VoxelNet 4.4 Hz
  (§1.1); 62 Hz on an Intel i7 with a 1080 Ti (abstract, §6).
- Lift-Splat-Shoot: inputs $X_k$, $E_k$, $I_k$ (§3); lift with $c_d=\alpha_d c$ and its
  one-hot and uniform limits (§3.1, eq. 1); pillar sum pooling (§3.2); 128×352
  inputs, 200×200 grid at 0.5 m over ±50 m, depth bins 4–45 m by 1 m, 35 Hz on a Titan
  V (§4.1); cumulative-sum trick and 2× training speedup (§4.2); three symmetries
  preserved (§1, §3); noisy-extrinsic training and camera dropout (§5, Fig. 6); IoU
  versus distance and weather (Fig. 10).
- BEVFormer: grid queries, ego-centered origin, eq. 3 index-to-meter mapping, eq. 4
  projection, spatial cross-attention over hit views (eq. 2), temporal alignment by
  ego-motion (§3.2–§3.4); 3 previous samples from the past 2 s in training (§3.6);
  NDS formula (§4.1); 200×200 queries at 0.512 m, $N_{\text{ref}}=4$ heights from
  $-5$ to 3 m (§4.2); 56.9% NDS (abstract).
- OctoMap: explicit free and unknown (§3.1); eqs. 1–4, counting equivalence for a
  symmetric model, clamping (§3.2); $l_{\text{occ}}=0.85$, $l_{\text{free}}=-0.4$,
  $l_{\min}=-2$, $l_{\max}=3.5$ (§5.1); map accuracy and cross-validation (§5.3,
  Table 1); runtime factors (§5.5).
- Occupancy networks: $o:\mathbb R^3\to\{0,1\}$, $f_\theta\in[0,1]$ (§3.1), MISE and
  threshold $\tau$ (§3.3), $\tau=0.2$ (§4.2), arbitrary resolution (§1).
- DeepSDF: negative inside, positive outside, zero-level set, clamp $\delta=0.1$ (§3),
  unit-sphere normalization (§5).

Ambiguity recorded in the note: LSS states depth bins "between 4.0 meters and 45.0
meters spaced by 1.0 meters" (§4.1), which gives 41 or 42 bins depending on whether
45 m is included; the official code was not read, so the note gives both.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 315 → 4,351. As a
comparison note across six representations, it exceeds 3,000 words; detection-head
depth is linked to CV-POSE3D rather than restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | LiDAR, camera and pose inputs with frames, units and per-point time; grid specification as part of the output; output table by consumer; pipeline role |
| Intuition | Shallow | Developed | The question each representation answers; constructed warehouse illustration; Mermaid diagram of LiDAR, camera and mapping paths |
| Prerequisites | Shallow (three links) | Developed | Links to CV-SE3, CV-CAPTEURS, CV-MULTICALIB, CV-EPIPOLAIRE, CV-STEREO, CV-ICP, CV-VIO, CV-POSE3D, CV-IOU-AP |
| Assumptions | Shallow | Developed | Calibration and timing; static world for accumulation; height structure; unobserved camera depth; LiDAR sampling; unknown as a state; independence of measurements |
| Procedure | Shallow | Developed | Pseudocode for pillars, lift-splat, BEV queries and occupancy mapping with the purpose of each step; six-way comparison table |
| Mathematics | Shallow | Developed | Grid indexing and BEVFormer eqs. 3–4; PointPillars encoding; LSS eq. 1; BEVFormer attention settings; OctoMap eqs. 2–4 and sensor model; implicit shapes; ego-motion transport; worked examples A–E |
| Parameters | Shallow (one sentence) | Developed | Nine-row parameter table with source values and interactions; tuning approach |
| Properties | Absent (merged with parameters) | Developed | Height in PointPillars; LSS symmetries and robustness results; BEVFormer hit views and temporal dependence; OctoMap clamping and counting; implicit functions; no evidence from absence |
| Cost and implementation | Shallow | Developed | Cost drivers with variables; reported speeds with hardware; OctoMap v1.10.0 contract (defaults, insertion, ray casting with unknown cells); execution status |
| Evaluation | Shallow | Developed | Metrics by contract (AP, NDS, BEV IoU, map accuracy, unknown-as-free rate); published results with protocol; proposed baseline and timing variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (three sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices across six representations; industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/64-nuages-bev-occupation.py`](checks/64-nuages-bev-occupation.py)
(16 assertions): 440 × 500 PointPillars canvas and 95.9–97.3% sparsity; 10.8 M values
in the capped tensor; 40× more voxel cells and the 4×/8× scaling; BEVFormer eq. 3 corner
convention (−51.2 m, 50.688 m, half cell 0.256 m) and grid extents; 41 or 42 LSS depth
bins; BEVFormer anchor spacing; OctoMap log-odds of 0.7, 0.4, 0.12 and 0.97; 3 hits
after clamping versus 10 without; one hit giving 0.7; 1.5° from 50 ms at 30°/s moving a
point 0.52 m at 20 m and 0.13 m at 5 m; 0.5 m from 10 m/s; LiDAR spacing 0.17 m and
0.35 m at 50 m and the 25-fold density drop from 10 m to 50 m.

## Applied corrections

- [Reference](../../../vault/60-vision-3d/references/64-nuages-bev-occupation.md),
  revision 6 → 7: body rewritten and deepened as above; mistranslations fixed in the
  appendices, identically to the cards ("Question of work" → "Working question",
  "Reference Response" → "Reference answer", "Radius Model" → "Ray model",
  "Aligning the historical" → "Aligning past observations", "Testable Grid Contract"
  → "Testable grid contract", "Transfer Protocol" → "Transfer protocol", "terminals"
  → "bounds", "documentation officielle" → "official documentation", "Documentary
  reference" → "Documentation consulted"); OctoMap preprint linked over HTTPS;
  sources split into scientific and implementation sources; closing provenance line
  replaced. Front matter unchanged except `revision`; H1, per-card headings and
  appendix headings kept.
- [Cards](../../../vault/60-vision-3d/64-nuages-bev-occupation.md): five expected
  answers given language or meaning-restoring fixes (quoted above); further
  explanations and blocking errors corrected for language; grading-criteria label
  fixed; Source lines cleaned of "see the 2026-10-30" fragments and of unrelated
  citations, and given sections relevant to each card. Questions, IDs, objectives,
  families, tags, `cas_pole` tag and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for
"indoor/outdoor", "indoor score", `log-odds`, `OctoMap`, `pseudo-image`). The
CV-POSE3D reference also describes PointPillars as encoding pillars into
pseudo-images, which is consistent.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run). No CV-BEV proposal is registered yet; P-CV-BEV-01 takes up the
unregistered 2026-10-20 proposal "Quantify grid memory and cell size".

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-BEV-01 | CV-BEV | Size a BEV or voxel grid for a stated obstacle size and range: cell count, scaling when the cell is halved, and sampling density of returns at that range | Reasoning family absent; resolution choice is untested (revives the 2026-10-20 proposal) | Reasoning; Mathematics, worked examples A and E | 1 card, 3 criteria | [PointPillars §2.1 and §4.2](https://arxiv.org/abs/1812.05784) |
| P-CV-BEV-02 | CV-BEV | Predict how many hits or misses change an occupancy cell's state with and without clamping, and explain why repeated scans from one viewpoint overstate confidence | Algorithm family absent; the log-odds update and clamping are not trained | Algorithm; Mathematics, worked example C | 1 card, 3 criteria | [Hornung et al., OctoMap, §3.2 and §5.1](https://www.arminhornung.de/Research/pub/hornung13auro.pdf) |

## Sources

Scientific sources, opened at the passages listed:

- Lang et al., PointPillars, [arXiv 1812.05784v2 PDF](https://arxiv.org/pdf/1812.05784v2)
  (text extracted with `pdftotext`): abstract, §1.1, §2.1, §4.2, §6.
- Philion and Fidler, Lift-Splat-Shoot, [arXiv 2008.05711v1 PDF](https://arxiv.org/pdf/2008.05711v1):
  §1, §3, §3.1, §3.2, §4.1, §4.2, §5 (Tables 1–2, Figs. 6 and 10).
- Li et al., BEVFormer, [arXiv HTML 2203.17270v2](https://arxiv.org/html/2203.17270v2):
  abstract, §3.1–§3.4, §3.6, §4.1, §4.2.
- Hornung et al., OctoMap, [preprint](https://www.arminhornung.de/Research/pub/hornung13auro.pdf):
  §3.1, §3.2 (eqs. 1–4), §5.1, §5.3 (Table 1), §5.5.
- Mescheder et al., Occupancy Networks, [arXiv HTML 1812.03828v1](https://arxiv.org/html/1812.03828v1):
  §1, §3.1, §3.3, §4.2.
- Park et al., DeepSDF, [arXiv 1901.05103v1 PDF](https://arxiv.org/pdf/1901.05103v1):
  §3, §5.

Implementation sources (official code at tag v1.10.0):

- [`octomap/src/AbstractOccupancyOcTree.cpp`](https://github.com/OctoMap/octomap/blob/v1.10.0/octomap/src/AbstractOccupancyOcTree.cpp): L40–L48.
- [`octomap/include/octomap/OccupancyOcTreeBase.h`](https://github.com/OctoMap/octomap/blob/v1.10.0/octomap/include/octomap/OccupancyOcTreeBase.h): L78–L97, L283–L303.

Failed accesses and limits:

- The CVF endpoints for PointPillars and Occupancy Networks returned HTTP 403 in the
  2026-11-08 pass; arXiv versions were used instead.
- Not re-read: PointNet++, BEVFusion (retained links without claims), Elfes's original
  occupancy-grid papers (cited through OctoMap §3.2). The LSS and BEVFormer official
  code were not read, hence the open depth-bin count.
- Context7 was not available in this session; OctoMap sources at a tag replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors (minimum 260 lexical words, set by a card outside this subject) |
| `python3 docs/revues/2026-11-14-reference-depth/checks/64-nuages-bev-occupation.py` | 16 checks passed |
| `git diff --check -- vault/60-vision-3d/ docs/revues/2026-11-14-reference-depth/checks/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/60-vision-3d/64-nuages-bev-occupation.md` | 5 cards, 278–386 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…` (including the anchor `cv-bev-005`), `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; reference front matter identical except `revision: 6` → `7`; H1 and the 10 per-card headings unchanged; `$$` balanced |

No model, map or sensor pipeline was run; the proposed baseline and variation are
protocols, not results. The Mermaid diagram and tables were not rendered in
Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is
agent self-review, without independent scientific validation or measurement of
learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-BEV revision 7, CV-BEV-001 to CV-BEV-005, corrections listed above, Agent Claude
Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-BEV-01, P-CV-BEV-02).
