# Flashcards — NeRF, 3D Gaussian Splatting and reconstruction

reference note: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::120-generatif-multimodal

## CV-RENDU3D-001

Objective: Distinguish implicit and primitive-based representations. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-RENDU3D-001
Question: What is the central difference between NeRF and 3D Gaussian Splatting?
Reponse: **Expected answer**: NeRF uses a density/radiance field with volume rendering; 3DGS an explicit representation of optimized Gaussians and a splatting rendering.

**Further explanation**: Compare optimization, memory and rendering on the same scene and hardware; no universal speed follows from the name.

**Representation and operation**: An implicit field is queried along rays to calculate an image according to its volume model. Explicit primitives carry positions, extents, and appearances, and are then projected by another rendering mechanism. These choices shift optimization, storage, and synthesis costs.

**Constructed comparison**: Use the same views and poses, hold out viewing angles and then measure visual quality, memory and time on the same hardware. If geometry matters, add an independent surface or dimension reference. A representation can explain images with structures that are not suitable for metrology; a quick rendering does not prove an exact surface. In the original NeRF, also distinguish density that depends on position from radiance that depends on the view. The name of a family does not describe all variants or a universal performance.

**Weight along the ray**: For a ray $r(t)=o+td$, the ideal volume rendering uses $C(r)=\int T(t)\sigma(r(t))c(r(t),d)\,dt$, with $T(t)=\exp[-\int_{t_n}^t\sigma(r(s))ds]$. If $t$ is a length and $d$ a unit vector, $\sigma$ has an inverse length unit; $T$ is unitless. The density depends on the position, while the radiance may depend on the direction in the original NeRF. This integration differs from a single opaque mesh and explains how multiple density/appearance distributions can contribute to the same pixels. The useful geometry does not automatically read as a certified metric surface.

**Anisotropy changes primitive support, not object identity**: A 3D Gaussian has covariance $\Sigma=R\operatorname{diag}(s_1^2,s_2^2,s_3^2)R^T$, defining oriented spatial support. Optimizing many such primitives and their appearance can represent a radiance field efficiently, but a primitive is not automatically one physical surface patch or semantic object. Likewise, NeRF density is a rendering quantity. Geometry extraction and measurement need explicit conventions and validation beyond the representation's rendering objective.

**Blocking errors**: Equating either representation with a guaranteed metric mesh.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Full reference]]; [Mildenhall et al., NeRF, §3 and §4 eqs. 1–3: position-dependent density, view-dependent colour, volume rendering](https://arxiv.org/html/2003.08934v2); [Kerbl et al., 3DGS, §4 eqs. 5–6, §5 and §6: anisotropic Gaussians, density control, tile-based rasterization](https://arxiv.org/html/2308.04079v1). The unit analysis is a project deduction.
Tags: cv::pilote cv::d12 famille::comparaison cv_id::CV-RENDU3D-001 provenance::agent pole::B pole::D
END

## CV-RENDU3D-002

Objective: Separate rendering and geometry. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-RENDU3D-002
Question: Why does excellent PSNR on novel views fail to validate a reconstruction for metrology?
Reponse: **Expected answer**: It evaluates an image similarity under protocol, not directly the accuracy of a surface or a physical dimension.

**Further explanation**: Use a geometric reference, stated units and held-out angles; examine areas never observed.

**Difference in error spaces**: The PSNR compares intensities between a rendered view and a reference. A geometric error can have little effect on neighboring views or be compensated by the appearance represented. The score does not therefore have an automatic conversion to millimetres of surface.

**Proposed protocol**: Fix poses and scale, hold out genuinely new angles, then compare the geometry with independent measurements adapted to the useful region. Also examine hidden or never seen areas: a representation can produce a hypothesis without direct observation. Report errors and reference coverage, and separate rendering quality from reconstruction quality. A magnificent view may be sufficient for visualization and insufficient for checking a dimension; these are two different uses whose criteria must be defined before choosing the method and evaluation.

**Constructed scale gauge**: Multiplying camera positions and scene coordinates by a single factor can retain projection directions and similar images, if the representation and rendering are transformed consistently. Therefore, a view synthesis measurement does not set an absolute length on its own. A metric calibration, a known baseline, or a dimension reference must anchor this scale if necessary. Even with a fixed scale, surface errors can remain compensated by appearance. Comparing geometric errors, coverage and held-out images thus measures complementary properties, instead of improperly converting a PSNR into millimeter accuracy.

**View synthesis can hide a scale gauge**: If scene coordinates and camera centers are scaled by $a>0$, corresponding rays preserve their directions. For a NeRF-style continuous rendering integral parameterized by physical distance, density must scale by $1/a$ to preserve optical thickness. Similar images therefore do not by themselves choose absolute length. A metrology protocol needs a metric reference and independent surface/dimension errors; PSNR measures agreement of rendered pixel values under its image protocol.

**Blocking errors**: Deducing millimetre accuracy from a perceptual or pixel score.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Full reference]]; distinction between image metrics and geometry deduced by the project; [Mildenhall et al., NeRF, §4: volume rendering; §6.2: PSNR, SSIM and LPIPS on held-out views](https://arxiv.org/html/2003.08934v2); [Kerbl et al., 3DGS, §7.2: test views taken every 8th photo, image metrics](https://arxiv.org/html/2308.04079v1). The scale-gauge argument is a project deduction.
Tags: cv::pilote cv::d12 famille::evaluation cv_id::CV-RENDU3D-002 provenance::agent pole::B pole::D
END

## CV-RENDU3D-003

Objective: Check a poorly observed scene. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-RENDU3D-003
Question: Training views look plausible, but camera rotation reveals artifacts. What should be tested?
Reponse: **Expected answer**: Angular coverage, poses and static scene hypothesis, then insufficiently constrained regions.

**Further explanation**: Compare with held-out views; increasing iterations without new constraints can only overfit.

**Possible origins**: Training views can constrain some faces, contain biased poses, or mix up a scene that changes over time. A flexible representation can explain these images without reconstructing a coherent scene from all directions.

**Constructed investigation**: Map ray coverage and errors by viewing angle, inspect calibration and poses, and then compare held-out views at a stated angular distance. Separately vary the number of views and the quality of the poses, keeping the other factor controlled. An improvement on the views already in use may just be a better fit to this data. If a region has never been observed, more iterations do not bring its true appearance. The diagnosis must therefore distinguish between lack of information, a wrong scene model and an optimization problem, rather than considering any plausible synthesis in training as a complete validation.

**Coverage and causality of the defect**: Held-out views close to the training views mainly test local interpolation, while more distant angles can reveal less constrained regions. State this angular distance and the visibility of the surfaces before talking about generalization. A controlled perturbation of the input poses, with the images unchanged, makes it possible to distinguish sensitivity to calibration from inadequate coverage. If the scene moves or the exposure changes, a representation can absorb the inconsistency in artificial structures. Examine these factors separately before increasing the iterations; a better fit to the same rays does not constitute a new observation of the hidden faces.

**Holdout viewpoint distance is part of the test**: A held-out camera almost identical to a training view tests a different extrapolation regime from a camera viewing the object's previously hidden side. Report angular/positional separation and joint surface visibility, and check camera-pose accuracy independently where possible. A proposed ablation perturbs poses or excludes view sectors while keeping optimization settings fixed. This separates poor geometric support from an unsupported claim that more optimization iterations will fix every artifact.

**Blocking errors**: Treating training views as a complete validation.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Full reference]]; diagnosis of coverage and poses proposed by the project; [Mildenhall et al., NeRF, §§3–4 and §5.3: representation, rendering, poses from COLMAP for real scenes](https://arxiv.org/html/2003.08934v2); [Kerbl et al., 3DGS, §3 static scene and §7.4: artifacts in poorly observed regions, no regularization](https://arxiv.org/html/2308.04079v1).
Tags: cv::pilote cv::d12 famille::diagnostic cv_id::CV-RENDU3D-003 provenance::agent pole::B pole::D
END
