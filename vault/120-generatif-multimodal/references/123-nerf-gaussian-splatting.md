---
id: CV-RENDU3D
type: comparaison
domaine: d12
poles: [B, D]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 5
prerequis: ["CV-EPIPOLAIRE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d12]
---
# NeRF, 3D Gaussian Splatting and reconstruction

## Problem, data and assumptions

Synthesize views of a scene and distinguish quality of rendering and geometric accuracy. Inputs: images and poses/calibration according to method; outputs: representation and new views. The monocular depth methods or DUSt3R/MASt3R fall under other reconstruction contracts, to be deepened separately.

## Prerequisites and competencies

**Required prerequisites**: [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

In the original NeRF, the density depends on the 3D position alone; the color/radiance also depends on the direction of view. The rendering uses a volume integration. 3D Gaussian Splatting optimizes explicit anisotropic primitives, their appearance and densification, and then renders by splatting.

## Mathematics, conventions and units

The volume integration weights a color by density and transmittance along the radius; the coordinates, units and poses must be consistent. A high PSNR on neighboring views does not establish any exact metric area or quality on angles not observed.

## Parameters and properties

Coverage of views, poses, background, exposure and supposed static scene; number of primitives, regularization and training protocol. The ambiguities of regions never observed remain real.

## Cost and implementation

Training/optimization, storage and rendering cost differently. Authors’ SPFs depend on the material and scenes. No rendering or training performed.

## Evaluation and controlled variation

Baseline: Views and poses known with split angles reserved; vary coverage and noise from pose separately. Measure synthesis of views and geometric reference distinctly if geometry matters.

## Failure modes and diagnosis

Good rendering but floating surface: check reserved views, poses, unconstrained regions and objective. An optimizer can explain the images with a geometry inadequate to the measurement.

## Alternatives and applications

MVS/TSDF for other hypotheses and outputs; reconstruction learned for another supervision. None of these names guarantees an absolute scale without a suitable contract.

## Guided reasoning and proposed checks

These constructed cases develop a synthesis of views, observation support and geometry. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-RENDU3D-001

**Question of work**: What is the central difference between NeRF and 3D Gaussian Splatting?

**Reference Response**: NeRF uses a density/radiance field with volume rendering; 3DGS an explicit representation of optimized Gaussians and a splatting rendering.

**Representation and operation**: An implicit field is interrogated along rays to calculate an image according to its volume model. Explicit primitives carry positions, extents, and appearances, and are then projected by another rendering mechanism. These choices shift optimization, storage, and synthesis costs.

**Comparison built**: use the same views and poses, reserve angles and then measure visual quality, memory and time on the same hardware. If geometry matters, add a surface or independent dimension reference. A representation can explain images with structures that are not suitable for metrology; a quick rendering does not prove an exact surface. In NeRF original, distinguish also density dependent on position and radiance dependent on view. The name of a family does not describe all variants or a universal performance.

### Case linked to CV-RENDU3D-003

**Question of work**: Training views look plausible, but camera rotation reveals artifacts. What should be tested?

**Reference Response**: Angular coverage, poses and static scene hypothesis, then insufficiently constrained regions.

**Possible origins**: Learning views can constrain some faces, contain biased poses, or mix up a scene that changes over time. A flexible representation can explain these images without reconstructing a coherent scene from all directions.

**Survey built**: map coverage of radii and errors at angle, inspect calibration and poses, and then compare reserved views at announced angular distance. Separately vary the number of views and quality of the poses, keeping the other factor controlled. An improvement on the views already in use may just be a better fit to this data. If a region has never been observed, more iterations do not bring its true appearance. The diagnosis must therefore distinguish between lack of information, false scene pattern and optimization problem, rather than considering any plausible synthesis in training as a complete validation.

**Documentary reference for this pass**: [NeRF](https://arxiv.org/html/2003.08934v2), §3, field and volumetric rendering. The other developments are in the [flashcards](../123-nerf-gaussian-splatting.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-RENDU3D-001

**Situation**: What is the central difference between NeRF and 3D Gaussian Splatting?

**Weight along the radius**: for a radius $r(t)=o+td$, the ideal volume rendering uses $C(r)=\int T(t)\sigma(r(t))c(r(t),d)\,dt$, with $T(t)=\exp[-\int_{t_n}^t\sigma(r(s))ds]$. If $t$ is a length and $d$ unit, $\sigma$ has an inverse length unit; $T$ is without unit. The density depends on the position, while the radiance may depend on the direction in the original NeRF. This integration differs from a single opaque mesh and explains how multiple density/appearance distributions can contribute to the same pixels. The useful geometry does not automatically read as a certified metric surface.

### CV-RENDU3D-002

**Situation**: Why does excellent PSNR on novel views fail to validate a reconstruction for metrology?

**Scale gauge built**: Multiplying camera positions and scene coordinates by a single factor can retain projection directions and similar images, if the representation and rendering are transformed consistently. Therefore, a view synthesis measurement does not set an absolute length on its own. A metric calibration, a known baseline, or a dimension reference must anchor this scale if necessary. Even fixed scale, surface errors can remain compensated by appearance. Compare geometric errors, cover and reserved images thus measures complementary properties, instead of improperly converting a PSNR into millimeter accuracy.

### CV-RENDU3D-003

**Situation**: Training views look plausible, but camera rotation reveals artifacts. What should be tested?

**Coverage and causality of the defect**: Reserve views close to those of training mainly tests local interpolation, while more distant angles can reveal less constrained regions. Announce this angular distance and the visibility of the surfaces before talking about generalization. A controlled perturbation of the input poses makes it possible to distinguish sensitivity to calibration and coverage inadequacy, at still images. If the scene moves or the exhibition changes, a representation can absorb the inconsistency in artificial structures. Examine these factors separately before increasing the iterations; a better adjustment of the same rays does not constitute a new observation of the hidden faces.

**Passages consulted for these developments**: [Mildenhall et al., NeRF](https://arxiv.org/html/2003.08934v2), §4, rendering and transmittance; dimensional calculation, gauge and project protocol.

## Sources and flashcards

- [NeRF, §§3 – 4](https://arxiv.org/abs/2003.08934): Dependencies of the field and volume rendering.
- [3D Gaussian Splatting, §§4 – 6](https://arxiv.org/abs/2308.04079): Anisotropic primitives, optimization/densification and rendering.

- [NeRF, author's page and paper](https://www.matthewtancik.com/nerf).
- [3D Gaussian Splatting, authors](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/).
- [Related flashcards](../123-nerf-gaussian-splatting.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
