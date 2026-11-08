# Flashcards — NeRF, 3D Gaussian Splatting and reconstruction

reference note: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::120-generatif-multimodal

## CV-RENDU3D-001

Objective: Implicit and primitive representation. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-RENDU3D-001
Question: What is the central difference between NeRF and 3D Gaussian Splatting?
Reponse: **Expected answer**: NeRF uses a density/radiance field with volume rendering; 3DGS an explicit representation of optimized Gaussians and a splatting rendering.

**Further explanation**: Compare optimization, memory, and rendering under the same scene/material; no universal speed follows the name.

**Representation and operation**: An implicit field is interrogated along rays to calculate an image according to its volume model. Explicit primitives carry positions, extents, and appearances, and are then projected by another rendering mechanism. These choices shift optimization, storage, and synthesis costs.

**Comparison built**: use the same views and poses, reserve angles and then measure visual quality, memory and time on the same hardware. If geometry matters, add a surface or independent dimension reference. A representation can explain images with structures that are not suitable for metrology; a quick rendering does not prove an exact surface. In NeRF original, distinguish also density dependent on position and radiance dependent on view. The name of a family does not describe all variants or a universal performance.

**Weight along the radius**: for a radius $r(t)=o+td$, the ideal volume rendering uses $C(r)=\int T(t)\sigma(r(t))c(r(t),d)\,dt$, with $T(t)=\exp[-\int_{t_n}^t\sigma(r(s))ds]$. If $t$ is a length and $d$ unit, $\sigma$ has an inverse length unit; $T$ is without unit. The density depends on the position, while the radiance may depend on the direction in the original NeRF. This integration differs from a single opaque mesh and explains how multiple density/appearance distributions can contribute to the same pixels. The useful geometry does not automatically read as a certified metric surface.

**Anisotropy changes primitive support, not object identity**: A 3D Gaussian has covariance $\Sigma=R\operatorname{diag}(s_1^2,s_2^2,s_3^2)R^T$, defining oriented spatial support. Optimizing many such primitives and their appearance can represent a radiance field efficiently, but a primitive is not automatically one physical surface patch or semantic object. Likewise, NeRF density is a rendering quantity. Geometry extraction and measurement need explicit conventions and validation beyond the representation's rendering objective.

**Blocking errors**: Assimilate both to a guaranteed metric mesh.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Full reference]]; [NeRF, §§3 – 4](https://arxiv.org/abs/2003.08934); [3DGS, summary and §§4 – 6](https://arxiv.org/abs/2308.04079); [Mildenhall et al., NeRF, §4, rendering and transmittance; dimensional calculation, gauge and project protocol](https://arxiv.org/html/2003.08934v2), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d12 famille::comparaison cv_id::CV-RENDU3D-001 provenance::agent pole::B pole::D
END

## CV-RENDU3D-002

Objective: separating rendering and geometry. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-RENDU3D-002
Question: Why does excellent PSNR on novel views fail to validate a reconstruction for metrology?
Reponse: **Expected answer**: It evaluates an image similarity under protocol, not directly the accuracy of a surface or a physical dimension.

**Further explanation**: Use geometric reference, reserved units and angles; examine areas never observed.

**Difference in error spaces**: The PSNR compares intensities between a rendered view and a reference. A geometric error can have little effect on neighboring views or be compensated by the appearance represented. The score does not therefore have an automatic conversion to millimetres of surface.

**Proposed Protocol**: fix poses and scale, reserve really new angles, then compare the geometry to independent measurements adapted to the useful region. Also examine hidden or never seen areas: a representation can produce a hypothesis without direct observation. Report errors and reference coverage, and separate rendering quality and rebuild quality. A magnificent view may be sufficient for visualization and insufficient for check one dimension; these are two different uses whose criteria must be defined before choosing the method and evaluation.

**Scale gauge built**: Multiplying camera positions and scene coordinates by a single factor can retain projection directions and similar images, if the representation and rendering are transformed consistently. Therefore, a view synthesis measurement does not set an absolute length on its own. A metric calibration, a known baseline, or a dimension reference must anchor this scale if necessary. Even fixed scale, surface errors can remain compensated by appearance. Compare geometric errors, cover and reserved images thus measures complementary properties, instead of improperly converting a PSNR into millimeter accuracy.

**View synthesis can hide a scale gauge**: If scene coordinates and camera centers are scaled by $a>0$, corresponding rays preserve their directions. For a NeRF-style continuous rendering integral parameterized by physical distance, density must scale by $1/a$ to preserve optical thickness. Similar images therefore do not by themselves choose absolute length. A metrology protocol needs a metric reference and independent surface/dimension errors; PSNR measures agreement of rendered pixel values under its image protocol.

**Blocking errors**: Deduct an accuracy in millimeters from a perceptual score or pixel.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Full reference]]; Distinction between image metrics and geometry deduced by the project; [NeRF, §6: synthesis evaluation of views](https://arxiv.org/abs/2003.08934); [Mildenhall et al., NeRF, §4, rendering and transmittance; dimensional calculation, gauge and project protocol](https://arxiv.org/html/2003.08934v2), consulted the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d12 famille::evaluation cv_id::CV-RENDU3D-002 provenance::agent pole::B pole::D
END

## CV-RENDU3D-003

Objective: Check out a little-observed scene. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-RENDU3D-003
Question: Training views look plausible, but camera rotation reveals artifacts. What should be tested?
Reponse: **Expected answer**: Angular coverage, poses and static scene hypothesis, then insufficiently constrained regions.

**Further explanation**: Compare to reserved views; increasing iterations without new constraints can only over-adjust.

**Possible origins**: Learning views can constrain some faces, contain biased poses, or mix up a scene that changes over time. A flexible representation can explain these images without reconstructing a coherent scene from all directions.

**Survey built**: map coverage of radii and errors at angle, inspect calibration and poses, and then compare reserved views at announced angular distance. Separately vary the number of views and quality of the poses, keeping the other factor controlled. An improvement on the views already in use may just be a better fit to this data. If a region has never been observed, more iterations do not bring its true appearance. The diagnosis must therefore distinguish between lack of information, false scene pattern and optimization problem, rather than considering any plausible synthesis in training as a complete validation.

**Coverage and causality of the defect**: Reserve views close to those of training mainly tests local interpolation, while more distant angles can reveal less constrained regions. Announce this angular distance and the visibility of the surfaces before talking about generalization. A controlled perturbation of the input poses makes it possible to distinguish sensitivity to calibration and coverage inadequacy, at still images. If the scene moves or the exhibition changes, a representation can absorb the inconsistency in artificial structures. Examine these factors separately before increasing the iterations; a better adjustment of the same rays does not constitute a new observation of the hidden faces.

**Holdout viewpoint distance is part of the test**: A held-out camera almost identical to a training view tests a different extrapolation regime from a camera viewing the object's previously hidden side. Report angular/positional separation and joint surface visibility, and check camera-pose accuracy independently where possible. A proposed ablation perturbs poses or excludes view sectors while keeping optimization settings fixed. This separates poor geometric support from an unsupported claim that more optimization iterations will fix every artifact.

**Blocking errors**: Consider training views as a complete validation.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Full reference]]; Diagnosis of coverage/poses proposed by the project; [NeRF, §§3 – 4: representation and observations](https://arxiv.org/abs/2003.08934); [Mildenhall et al., NeRF, §4, rendering and transmittance; dimensional calculation, gauge and project protocol](https://arxiv.org/html/2003.08934v2), consult the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d12 famille::diagnostic cv_id::CV-RENDU3D-003 provenance::agent pole::B pole::D
END
