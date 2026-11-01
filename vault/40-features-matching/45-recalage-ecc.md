# Flashcards — Intensity-based registration and ECC

reference note: [[40-features-matching/references/45-recalage-ecc|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::40-features-matching

## CV-ECC-001

Objective: choose matching or photometric optimization. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ECC-001
Question: Which input/output contract distinguishes ECC from a SIFT + RANSAC pipeline?
Reponse: **Expected answer**: ECC optimizes an intensity criterion on an initialized warp; SIFT offers pairs and then a robust geometry.

**Further explanation**: Convergence pool, overlap and invariances differ; they can be combined for initialization and refinement.

**Interpreted mechanism**: ECC looks for transformation parameters by directly comparing intensities on a common area. Matches are not first expressed as a list of detected patches. SIFT and RANSAC can offer transformation from distinctive points; photometric refinement can then be tried if the model and the cover are suitable.

**Constructed example**: For two views close to a label, a suitable initialization can make it useful to optimize intensities. For a large move with low overlap, the same procedure can reach a bad optimum or fail. Check initialization, mask, photometric variations and motion pattern separately. A normalized correlation can tolerate a positive gain and a global offset on a fixed non-constant medium; this algebraic property does not cover a local shadow, a occlusion, or a global convergence of the registration.

**Understanding the Standardized Criteria**: on a fixed support, center the intensities $a_i$ and $b_i(\theta)$ gives $\bar a_i=a_i-\mu_a$ and $\bar b_i=b_i(\theta)-\mu_b$. The correlation is $\rho(\theta)=\sum_i\bar a_i\bar b_i/(\sqrt{\sum_i\bar a_i^2}\sqrt{\sum_i\bar b_i^2})$ if the norms are non-zero. Multiply an image by a positive gain and add a global offset retains this ideal value; a negative gain reverses its sign. Optimization modifies the warp, thus the interpolated intensities and their gradient with respect to the parameters. Valid media and hidden pixels must remain explicitly controlled: changing the overlap can change the compared criterion.

**Blocking errors**: Describe ECC as a separate descriptor.
Source: [[40-features-matching/references/45-recalage-ecc|Full reference]] ; [OpenCV 4.13.0, findTransformECC, model, initialization and reverse warping](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-ECC-001 provenance::agent pole::B pole::E
END

## CV-ECC-002

Objective: interpret an ECC convergence. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ECC-002
Question: ECC converges with high correlation on a repetitive grid, but the displacement is wrong. How should it be validated?
Reponse: **Expected answer**: Compare to reserved points/structures and movement constraints; the correlation can have several maxima.

**Further explanation**: Inspect initialization, overlap, and sense of warp.

**Origin of Ambiguity**: A translation of a period of a grid can align similar intensities almost as well as true translation. The numerical criterion then sees several plausible solutions in the image; a stable convergence only means that the optimizer has stopped according to its criteria.

**Validation construite**: add to check a unique mark or reserved points whose position is known, then compare the error of solutions obtained from several plausible initializations. Examine the actual cover used and the hidden parts. A movement constraint must come from the observed system and remain explicitly limited. If the only observations are perfectly repetitive, recognize that absolute displacement can remain ambiguous. This diagnosis distinguishes between optimization and identifiability: more iterations eventually enhance a local fit, but do not bring the distinctive information missing from the scene.

A reserved distinctive observation is then used to separate the solutions, without modifying the pixels used by the optimizer.

**Decouple score and plausibility**: A correlation close to 1 describes the standardized similarity of the actually compared content. It does not directly indicate the number of valid pixels, the uniqueness of the maximum, or the displacement error. A very small common area can therefore produce a high score with little geometric information. Report media size and error on reserved points, then test separate initializations of a period of the pattern. If several solutions keep scores close and physical constraints allowable, keep ambiguity in the decision. Turning the score into acceptance confidence requires calibration on representative cases, including false but visually plausible alignments.

**Blocking errors**: Take digital convergence as physical truth.
Source: [[40-features-matching/references/45-recalage-ecc|Full reference]]; [OpenCV 4.13.0, findTransformECC, model, initialization and reverse warping](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html); repetitive case and validation protocol deduced by the project.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-ECC-002 provenance::agent pole::B pole::E
END

## CV-ECC-003

Objective: Choose a movement model. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-ECC-003
Question: Why should a homography not always be chosen for ECC registration?
Reponse: **Expected answer**: More parameters can over-adjust or reduce stability while translation or affine is sufficient as needed.

**Further explanation**: The model must explain the capture and be validated on independent observations.

**Reasoning about degrees of freedom**: a translation model requires that all points share two displacements; a homography allows a more general projective deformation. This flexibility can explain real variations of view on a plane, but also absorb noise or a photometric disturbance when the data does not constrain its parameters.

**Comparison built**: on an installation where the planned movement is a small translation, first adjust this model, then a richer model with the same images and useful area. Compare errors on reserved points, stability of parameters and extrapolation near edges. A better score on the adjustment pixels is not enough. Conversely, keeping a translation if the perspective really changes introduces a bias. The choice therefore links capture geometry, the richness of observations and the admitted error, rather than a principle of simplicity or flexibility applied blindly.

**Dimension and identifiability of the warp**: translation: two parameters; plane Euclidean movement: rotation and two translations; affine: six parameters; homography: eight independent parameters after choice of scale. A homography acts by projective division: small changes in the denominator can strongly change the edges of the extrapolated region. With little overlap or texture, some parameters compensate and the local information matrix can become poorly conditioned. Compare models with reserved geometry rather than with the only optimized score. If a simpler model is sufficient, it can limit these compensations; if the capture violates its assumptions, this simplicity imposes on the contrary an irreducible bias.

**Blocking errors**: Assimilate maximum flexibility and maximum precision.
Source: [[40-features-matching/references/45-recalage-ecc|Full reference]]; [OpenCV 4.13.0, findTransformECC, model, initialization and reverse warping](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html); compromise between flexibility and stability deduced by the project.
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-ECC-003 provenance::agent pole::B pole::E
END
