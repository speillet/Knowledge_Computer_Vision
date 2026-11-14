---
id: CV-RENDU3D
type: comparaison
domaine: d12
poles: [B, D]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 7
prerequis: ["CV-EPIPOLAIRE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d12]
---
# NeRF, 3D Gaussian Splatting and reconstruction

This awareness-level comparison note contrasts two scene representations optimized
for novel-view synthesis: Neural Radiance Fields (NeRF) and 3D Gaussian Splatting
(3DGS). The engineering point is the difference between rendering quality and
geometric accuracy: both methods are judged by how well they reproduce held-out
images, which neither fixes metric scale nor certifies a surface.

## Problem and data contract

**Task.** From images of a static scene with known cameras, build a representation
that renders the scene from new viewpoints.

**Inputs.** RGB images, camera intrinsics and poses, and for NeRF the scene bounds.
NeRF uses ground-truth cameras for synthetic data and COLMAP structure-from-motion for
real scenes [Mildenhall et al., §5.3]; 3DGS takes SfM-calibrated cameras and also
initializes its Gaussians from the sparse SfM point cloud [Kerbl et al., §3]. The
scene frame, its units and its scale are those of the pose estimate: SfM alone fixes
the scene only up to a similarity (see [CV-BA](../../50-calibration-geometrie/references/54-bundle-adjustment.md)).

**Outputs.** NeRF: an MLP $F_\Theta:(\mathbf x,\mathbf d)\mapsto(\mathbf c,\sigma)$
giving colour and volume density at a 3-D point for a viewing direction [§3]. 3DGS: a
set of 3-D Gaussians with position, covariance, opacity $\alpha$ and spherical-harmonic
colour coefficients [Kerbl et al., §4–5.1]. Both produce images; depth or surfaces
must be extracted with an additional convention.

**Pipeline role.** Visualization, digital twins for inspection review, view
interpolation for training data, and scene capture where appearance matters more than
dimensions. Metrology belongs to calibrated stereo, multi-view stereo or scanning
([CV-STEREO](../../60-vision-3d/references/61-stereo-profondeur.md)).

## Intuition

NeRF treats the scene as a semi-transparent fog with a colour at every point; a pixel
is the colour accumulated along its ray, weighted by how much light survives to each
point. 3DGS represents the scene with many coloured, semi-transparent ellipsoids; a
pixel is obtained by projecting them onto the image and blending them front to back.
NeRF queries a network many times per ray; 3DGS rasterizes explicit primitives.

*Illustration (constructed example, recomputed by checks/123-nerf-gaussian-splatting.py).*
On one ray, a semi-transparent layer at depth 2 (optical thickness 0.7) and an opaque
layer at depth 4 receive rendering weights 0.503 and 0.493. The weighted mean depth is
about 2.99, where there is no matter at all. The rendered colour can be right while a
depth read from the same weights describes a floating surface.

## Prerequisites and competencies

**Required prerequisites**: [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md).
Useful: pose estimation and its gauge in
[CV-BA](../../50-calibration-geometrie/references/54-bundle-adjustment.md); metric
depth in [CV-STEREO](../../60-vision-3d/references/61-stereo-profondeur.md); geometric
comparison of point clouds in [CV-ICP](../../60-vision-3d/references/62-recalage-global-icp.md).
**Target competencies**: explain the mechanism, compare under constraints, interpret a
measurement and diagnose a failure. The level is awareness; not all variants mentioned
are detailed.

## Assumptions, observability and degenerate cases

- **Static scene and constant appearance.** Both methods assume a static scene; 3DGS
  states it explicitly [§3]. Moving objects or exposure changes are explained away by
  spurious structures.
- **Accurate poses.** Pose errors are absorbed by the representation as blur or
  duplicated structures.
- **Coverage.** A surface is constrained only where rays observe it; 3DGS reports
  artifacts in regions that are not well observed and notes that it applies no
  regularization [§7.4].
- **Gauge.** Without a metric reference, images do not determine absolute scale
  (example B).
- **Degenerate cases.** Few views, textureless or specular surfaces, transparent
  objects, and test views almost identical to training views, which test interpolation
  rather than extrapolation.

## Procedure

```text
NeRF (Mildenhall et al., Sec. 4-5)
  per iteration: sample 4096 rays; on each ray, 64 stratified coarse samples, then
    128 more where the coarse weights are high; query F(x, d) with positional
    encoding; composite with eq. 3; minimize squared colour error (coarse and fine)
  typical: 100-300k iterations, 1-2 days on one V100 GPU

3DGS (Kerbl et al., Sec. 5-6)
  init: Gaussians at SfM points
  per iteration: rasterize with a tile-based renderer (16 x 16 px tiles, depth-sorted);
    loss (1 - 0.2) L1 + 0.2 D-SSIM; every 100 iterations densify: clone small
    Gaussians, split large ones (scale / 1.6) where the view-space position gradient
    exceeds 0.0002; prune near-transparent Gaussians; reset opacities every 3000
```

Purpose. Stratified and hierarchical sampling let NeRF evaluate the continuous field
at varied positions and spend samples where content is [§4, §5.2]. Positional
encoding lets the MLP represent high frequencies [§5.1]. In 3DGS, densification adds
primitives where geometry is under- or over-reconstructed, and opacity resets limit
their growth [§5.2]; tile-based sorting makes rendering fast [§6].

## Mathematics, conventions and units

**Volume rendering.** For a ray $\mathbf r(t)=\mathbf o+t\mathbf d$ between near and
far bounds $t_n,t_f$ [NeRF, eq. 1],

$$C(\mathbf r)=\int_{t_n}^{t_f}T(t)\,\sigma(\mathbf r(t))\,\mathbf c(\mathbf r(t),\mathbf d)\,dt,\qquad T(t)=\exp\Big(-\int_{t_n}^{t}\sigma(\mathbf r(s))\,ds\Big).$$

$T$ is the transmittance (unitless), $\sigma$ has the unit of an inverse length when
$t$ is a length and $\mathbf d$ a unit vector. With samples $t_i$ and spacings
$\delta_i=t_{i+1}-t_i$, the quadrature is
$\hat C=\sum_i T_i\,(1-e^{-\sigma_i\delta_i})\,\mathbf c_i$ with
$T_i=\exp(-\sum_{j<i}\sigma_j\delta_j)$, which is alpha compositing with
$\alpha_i=1-e^{-\sigma_i\delta_i}$ [eqs. 2–3]. Density depends on position only and
colour on position and direction, which encourages multiview consistency [§3].

**Gaussians.** Each primitive has covariance $\Sigma=RSS^TR^T$ built from a scaling
vector and a unit quaternion, so it stays a valid covariance during gradient descent
[Kerbl et al., eq. 6]. For rendering it is projected as $\Sigma'=JW\Sigma W^TJ^T$, with
$W$ the viewing transformation and $J$ the Jacobian of the affine approximation of the
projection [eq. 5]. Opacity uses a sigmoid and scales an exponential activation [§5.1].

*Worked examples (constructed, recomputed by checks/123-nerf-gaussian-splatting.py).*

- A. Two layers on a ray: weights 0.503 and 0.493, mean depth 2.99 between them
  (illustration above).
- B. Scale gauge: multiplying distances by $a=2.5$ and densities by $1/a$ leaves every
  $\sigma_i\delta_i$, every weight and every pixel unchanged, while all depths scale by
  $a$. Images alone cannot distinguish the two scenes.
- C. A Gaussian with scales $(3,1,0.1)$ rotated by 30° has $\operatorname{tr}\Sigma=10.01$
  and variance 9 along its rotated first axis: a flat, elongated primitive that is not
  a surface patch with a normal.
- D. With position (3), scale (3), quaternion (4), opacity (1) and 4 spherical-harmonic
  bands per colour (48), a Gaussian stores 59 floats, 236 bytes in float32; one million
  Gaussians need about 236 MB, consistent with the "several hundred megabytes" the
  authors report for large scenes [§7.4].

## Parameters and tuning

| Parameter | Method | Effect | What to watch |
| --- | --- | --- | --- |
| Number and placement of views | Both | Constrained regions and gauge | Angular coverage of the surfaces that matter |
| Pose accuracy | Both | Sharpness and duplicated structures | Reprojection error of the SfM solution |
| Samples per ray ($N_c=64$, $N_f=128$) and positional-encoding frequencies ($L=10$ for $\mathbf x$, $L=4$ for $\mathbf d$) | NeRF | Detail against cost | Aliasing or blur |
| Densification threshold (0.0002), split factor (1.6), opacity reset (3000 iterations) | 3DGS | Number of Gaussians, memory, fine detail | Floaters and memory growth |
| Loss weight $\lambda=0.2$ (D-SSIM) | 3DGS | Structural versus pixel fidelity | — |
| Spherical-harmonic degree | 3DGS | View-dependent colour; 4 bands, introduced one per 1000 iterations [§7.1] | Popping in view-dependent regions [§7.4] |

Tuning approach (project method): fix the camera set and poses first, then tune the
representation on held-out views at stated angular distances; tune geometry extraction
only against an independent metric reference.

## Properties and limits of guarantees

- Both representations are optimized for photometric reconstruction of training
  images; neither objective constrains geometry where no ray observes it.
- NeRF's density is a rendering quantity; its weights can split across layers, so an
  expected depth may lie in empty space (example A).
- A 3D Gaussian is a blending primitive, not a surface element: 3DGS optimizes without
  normals because SfM points are too sparse to estimate them [§4].
- Neither method fixes metric scale (example B); scale comes from the poses or an
  external reference.
- Reported limitations of 3DGS: artifacts in poorly observed regions, elongated or
  "splotchy" Gaussians, popping in view-dependent regions, and higher memory than
  NeRF-based solutions, with peak training memory above 20 GB for large scenes in the
  prototype [§7.4].

## Cost and implementation

NeRF: per-scene optimization of 100–300k iterations, about 1–2 days on one V100, and
rendering cost proportional to rays × samples × network evaluations [§5.3]. 3DGS:
training of 35–45 minutes for the authors' configuration on an A6000, real-time
rendering at 1080p on the evaluated datasets, and memory proportional to the number of
Gaussians (example D) [§1, §7.2, §7.4]. These figures depend on scenes and hardware. No
training or rendering was executed for this note, and no library API is described.

## Evaluation and controlled variation

**Image protocol.** Held-out views compared with PSNR, SSIM and LPIPS; 3DGS follows
the Mip-NeRF360 split, taking every 8th photo for testing [§7.2], and NeRF reports the
same metrics on held-out test views [§6.2]. These measure pixel agreement, not geometry.

**Proposed baseline and controlled variation (not executed).**

- *Baseline*: one scene with a metric reference (scanned mesh or measured dimensions),
  the full camera set with SfM poses, held-out views at stated angular distances from
  the nearest training view.
- *Controlled variation*: remove one angular sector of training views, everything else
  fixed.
- *Measurements*: PSNR, SSIM and LPIPS per held-out view against angular distance;
  surface error against the reference in the removed sector and elsewhere, after a
  similarity alignment whose scale is reported.
- *Reading*: rendering metrics may drop only slightly while surface error grows in the
  unobserved sector; the two must be reported separately.

**Measurement limits.** Held-out views near training views mainly test interpolation;
geometry extraction (thresholds on density or opacity) adds its own parameters; a
similarity alignment before measuring hides scale errors unless the scale is reported.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Floaters or blobs appearing when the camera moves | Poorly observed region; no regularization | Map ray coverage of the region; render from a removed sector | More views of that region; regularization; treat as unknown |
| Ghosted or doubled structures | Pose errors or a moving object | SfM reprojection error; mask dynamic content | Re-estimate poses, remove moving objects |
| Colour or brightness inconsistent between views | Exposure change across images | Per-image exposure statistics | Fixed exposure at capture, per-image compensation |
| Good PSNR, wrong dimensions | Gauge or surface not constrained | Compare with a metric reference | Metric scale from calibration or a known baseline |
| Depth map inconsistent with rendering | Weights split across layers (example A) | Inspect weight distribution along rays | Use the dominant weight or a surface method |

## Alternatives and applications

- Prefer calibrated stereo, multi-view stereo, TSDF fusion or scanning when dimensions
  or surfaces are the deliverable.
- Prefer NeRF-type fields when compact storage matters more than rendering speed, and
  3DGS when real-time rendering of a captured scene matters and memory is available.
- Monocular depth networks and learned feed-forward reconstruction follow other
  contracts and are not covered here.

Industrial uses (project reasoning): visual digital twins of a site for remote review,
with measurements taken from a calibrated source; view interpolation for synthetic
training images, evaluated against real views.

## Guided reasoning and proposed checks

These constructed cases develop view synthesis, observation support and geometry. They explain or test reasoning; no image, video or hardware result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-RENDU3D-001

**Working question**: What is the central difference between NeRF and 3D Gaussian Splatting?

**Reference answer**: NeRF uses a density/radiance field with volume rendering; 3DGS an explicit representation of optimized Gaussians and a splatting rendering.

**Representation and operation**: An implicit field is queried along rays to calculate an image according to its volume model. Explicit primitives carry positions, extents, and appearances, and are then projected by another rendering mechanism. These choices shift optimization, storage, and synthesis costs.

**Constructed comparison**: Use the same views and poses, hold out viewing angles and then measure visual quality, memory and time on the same hardware. If geometry matters, add an independent surface or dimension reference. A representation can explain images with structures that are not suitable for metrology; a quick rendering does not prove an exact surface. In the original NeRF, also distinguish density that depends on position from radiance that depends on the view. The name of a family does not describe all variants or a universal performance.

### Case linked to CV-RENDU3D-003

**Working question**: Training views look plausible, but camera rotation reveals artifacts. What should be tested?

**Reference answer**: Angular coverage, poses and static scene hypothesis, then insufficiently constrained regions.

**Possible origins**: Training views can constrain some faces, contain biased poses, or mix up a scene that changes over time. A flexible representation can explain these images without reconstructing a coherent scene from all directions.

**Constructed investigation**: Map ray coverage and errors by viewing angle, inspect calibration and poses, and then compare held-out views at a stated angular distance. Separately vary the number of views and the quality of the poses, keeping the other factor controlled. An improvement on the views already in use may just be a better fit to this data. If a region has never been observed, more iterations do not bring its true appearance. The diagnosis must therefore distinguish between lack of information, a wrong scene model and an optimization problem, rather than considering any plausible synthesis in training as a complete validation.

**Source consulted for this pass**: [NeRF](https://arxiv.org/html/2003.08934v2), §3, field and volumetric rendering. The remaining developments are in the [flashcards](../123-nerf-gaussian-splatting.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-RENDU3D-001

**Situation**: What is the central difference between NeRF and 3D Gaussian Splatting?

**Weight along the ray**: For a ray $r(t)=o+td$, the ideal volume rendering uses $C(r)=\int T(t)\sigma(r(t))c(r(t),d)\,dt$, with $T(t)=\exp[-\int_{t_n}^t\sigma(r(s))ds]$. If $t$ is a length and $d$ a unit vector, $\sigma$ has an inverse length unit; $T$ is unitless. The density depends on the position, while the radiance may depend on the direction in the original NeRF. This integration differs from a single opaque mesh and explains how multiple density/appearance distributions can contribute to the same pixels. The useful geometry does not automatically read as a certified metric surface.

### CV-RENDU3D-002

**Situation**: Why does excellent PSNR on novel views fail to validate a reconstruction for metrology?

**Constructed scale gauge**: Multiplying camera positions and scene coordinates by a single factor can retain projection directions and similar images, if the representation and rendering are transformed consistently. Therefore, a view synthesis measurement does not set an absolute length on its own. A metric calibration, a known baseline, or a dimension reference must anchor this scale if necessary. Even with a fixed scale, surface errors can remain compensated by appearance. Comparing geometric errors, coverage and held-out images thus measures complementary properties, instead of improperly converting a PSNR into millimeter accuracy.

### CV-RENDU3D-003

**Situation**: Training views look plausible, but camera rotation reveals artifacts. What should be tested?

**Coverage and causality of the defect**: Held-out views close to the training views mainly test local interpolation, while more distant angles can reveal less constrained regions. State this angular distance and the visibility of the surfaces before talking about generalization. A controlled perturbation of the input poses, with the images unchanged, makes it possible to distinguish sensitivity to calibration from inadequate coverage. If the scene moves or the exposure changes, a representation can absorb the inconsistency in artificial structures. Examine these factors separately before increasing the iterations; a better fit to the same rays does not constitute a new observation of the hidden faces.

**Passages consulted for these developments**: [Mildenhall et al., NeRF](https://arxiv.org/html/2003.08934v2), §4, rendering and transmittance; the dimensional calculation, the gauge argument and the protocol are project reasoning.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-RENDU3D-001 — Anisotropy changes primitive support, not object identity

A 3D Gaussian has covariance $\Sigma=R\operatorname{diag}(s_1^2,s_2^2,s_3^2)R^T$, defining oriented spatial support. Optimizing many such primitives and their appearance can represent a radiance field efficiently, but a primitive is not automatically one physical surface patch or semantic object. Likewise, NeRF density is a rendering quantity. Geometry extraction and measurement need explicit conventions and validation beyond the representation's rendering objective.

### CV-RENDU3D-002 — View synthesis can hide a scale gauge

If scene coordinates and camera centers are scaled by $a>0$, corresponding rays preserve their directions. For a NeRF-style continuous rendering integral parameterized by physical distance, density must scale by $1/a$ to preserve optical thickness. Similar images therefore do not by themselves choose absolute length. A metrology protocol needs a metric reference and independent surface/dimension errors; PSNR measures agreement of rendered pixel values under its image protocol.

### CV-RENDU3D-003 — Holdout viewpoint distance is part of the test

A held-out camera almost identical to a training view tests a different extrapolation regime from a camera viewing the object's previously hidden side. Report angular/positional separation and joint surface visibility, and check camera-pose accuracy independently where possible. A proposed ablation perturbs poses or excludes view sectors while keeping optimization settings fixed. This separates poor geometric support from an unsupported claim that more optimization iterations will fix every artifact.

Consulted foundations: [NeRF](https://arxiv.org/html/2003.08934v2): §§3–4 position/direction-conditioned radiance and volume rendering; [3D Gaussian Splatting](https://arxiv.org/html/2308.04079v1): §§4–6 anisotropic primitives, density control and rasterization.

## Sources and flashcards

### Scientific sources

- [Mildenhall et al. 2020, NeRF](https://arxiv.org/html/2003.08934v2): §3 representation and view dependence, §4 eqs. 1–3, §5.1 positional encoding, §5.2 hierarchical sampling, §5.3 implementation and training time, §6.1–6.2 datasets and metrics.
- [Kerbl et al. 2023, 3D Gaussian Splatting](https://arxiv.org/html/2308.04079v1): §1 and §3 inputs and SfM initialization, §4 eqs. 5–6 and optimized parameters, §5.1 activations and loss, §5.2 densification, §6 tile-based rasterizer, §7.1 spherical-harmonic schedule, §7.2 hardware, timing and evaluation split, §7.4 limitations.
- Author pages: [NeRF project page](https://www.matthewtancik.com/nerf) and [3DGS project page](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/), retained but not re-read in this pass.

### Implementation sources

None: no library or code API is described in this awareness-level note.

### Related flashcards and references

- [Flashcards](../123-nerf-gaussian-splatting.md): CV-RENDU3D-001 to 003.
- [CV-BA](../../50-calibration-geometrie/references/54-bundle-adjustment.md), [CV-STEREO](../../60-vision-3d/references/61-stereo-profondeur.md), [CV-ICP](../../60-vision-3d/references/62-recalage-global-icp.md).

Drafted by agent, 2026-10-18. Revision 7, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/123-nerf-gaussian-splatting.md).
