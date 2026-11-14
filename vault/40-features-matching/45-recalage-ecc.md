# Flashcards — Intensity-based registration and ECC

reference note: [[40-features-matching/references/45-recalage-ecc|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::40-features-matching

## CV-ECC-001

Objective: choose matching or photometric optimization. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-ECC-001
Question: Which input/output contract distinguishes ECC from a SIFT + RANSAC pipeline?
Reponse: **Expected answer**: ECC optimizes an intensity criterion on an initialized warp; SIFT proposes point pairs, from which a robust estimator computes the geometry.

**Further explanation**: Convergence basin, overlap and invariances differ; they can be combined for initialization and refinement.

**Interpreted mechanism**: ECC looks for transformation parameters by directly comparing intensities on a common area. Matches are not first expressed as a list of detected patches. SIFT and RANSAC can provide a transformation from distinctive points; photometric refinement can then be tried if the model and the overlap are suitable.

**Constructed example**: For two nearby views of a label, a suitable initialization can make it useful to optimize intensities. For a large motion with low overlap, the same procedure can reach a bad optimum or fail. Check initialization, mask, photometric variations and motion model separately. A normalized correlation can tolerate a positive gain and a global offset on a fixed, non-constant support; this algebraic property does not cover a local shadow, an occlusion, or global convergence of the registration.

**Understanding the normalized criterion**: on a fixed support, centring the intensities $a_i$ and $b_i(\theta)$ gives $\bar a_i=a_i-\mu_a$ and $\bar b_i=b_i(\theta)-\mu_b$. The correlation is $\rho(\theta)=\sum_i\bar a_i\bar b_i/(\sqrt{\sum_i\bar a_i^2}\sqrt{\sum_i\bar b_i^2})$ if the norms are non-zero. Multiplying an image by a positive gain and adding a global offset preserves this ideal value; a negative gain reverses its sign. Optimization modifies the warp, hence the interpolated intensities and their gradient with respect to the parameters. Valid supports and masked pixels must remain explicitly controlled: changing the overlap can change the compared criterion.

**Constant patches make normalization undefined**: The normalized correlation denominator vanishes when either compared patch has zero centered-intensity norm. Almost constant support makes it poorly conditioned before exact degeneracy. Restricting to a seemingly clean ROI can therefore remove the texture required for alignment. A proposed check records support variance, valid overlap and the warp direction along with the returned score. Brightness normalization removes a global offset/gain under its assumptions, not missing geometric information.

**Blocking errors**: Describing ECC as a separate descriptor.
Source: [[40-features-matching/references/45-recalage-ecc|Full reference]] ; [OpenCV 4.13.0, tracking.hpp L314–L375, findTransformECC: warp direction, motion types, initialization and WARP_INVERSE_MAP](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp); [Evangelidis and Psarakis 2008, abstract: photometric invariance, iterative closed-form maximization](https://doi.org/10.1109/TPAMI.2008.113). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-ECC-001 provenance::agent pole::B pole::E
END

## CV-ECC-002

Objective: interpret an ECC convergence. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-ECC-002
Question: ECC converges with high correlation on a repetitive grid, but the displacement is wrong. How should it be validated?
Reponse: **Expected answer**: Compare with held-out points or structures and with motion constraints; the correlation can have several maxima.

**Further explanation**: Inspect initialization, overlap, and direction of the warp.

**Origin of the ambiguity**: A translation by one period of the grid can align similar intensities almost as well as the true translation. The numerical criterion then sees several plausible solutions in the image; a stable convergence only means that the optimizer has stopped according to its criteria.

**Constructed validation**: add, for checking, a unique mark or held-out points whose position is known, then compare the error of solutions obtained from several plausible initializations. Examine the overlap actually used and the masked parts. A movement constraint must come from the observed system and remain explicitly limited. If the only observations are perfectly repetitive, recognize that absolute displacement can remain ambiguous. This diagnosis distinguishes between optimization and identifiability: more iterations may improve a local fit, but do not bring the distinctive information missing from the scene.

A reserved distinctive observation is then used to separate the solutions, without modifying the pixels used by the optimizer.

**Decouple score and plausibility**: A correlation close to 1 describes the normalized similarity of the content actually compared. It does not directly indicate the number of valid pixels, the uniqueness of the maximum, or the displacement error. A very small common area can therefore produce a high score with little geometric information. Report the support size and the error on held-out points, then test initializations separated by one period of the pattern. If several solutions keep close scores and remain physically admissible, carry the ambiguity into the decision. Turning the score into acceptance confidence requires calibration on representative cases, including false but visually plausible alignments.

**A periodic image permits several equally good optima**: For an ideal intensity pattern with period $P$, translations separated by integer multiples of $P$ produce identical overlap content away from boundaries. A high normalized correlation cannot determine which period is physically correct. Initialize within a justified capture range and validate on nonperiodic structures or an external movement constraint. Repeated convergence from nearby initializations checks local stability; it does not establish uniqueness over the whole search region.

**Blocking errors**: Taking numerical convergence as physical truth.
Source: [[40-features-matching/references/45-recalage-ecc|Full reference]]; [OpenCV 4.13.0, ecc.cpp L519–L611: stopping on the change of the correlation, returned value](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/ecc.cpp); [Baker and Matthews 2002, §3.4: evaluation on canonical-point errors](https://www.ri.cmu.edu/pub_files/pub3/baker_simon_2002_3/baker_simon_2002_3.pdf); repetitive case and validation protocol deduced by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-ECC-002 provenance::agent pole::B pole::E
END

## CV-ECC-003

Objective: Choose a motion model. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-ECC-003
Question: Why should a homography not always be chosen for ECC registration?
Reponse: **Expected answer**: More parameters can overfit or reduce stability when a translation or an affine model is sufficient for the need.

**Further explanation**: The model must explain the capture and be validated on independent observations.

**Reasoning about degrees of freedom**: a translation model requires that all points share two displacements; a homography allows a more general projective deformation. This flexibility can explain real viewpoint changes on a plane, but can also absorb noise or a photometric disturbance when the data do not constrain its parameters.

**Constructed comparison**: on a setup where the expected motion is a small translation, first fit this model, then a richer model with the same images and useful area. Compare errors on held-out points, stability of the parameters and extrapolation near the edges. A better score on the fitted pixels is not enough. Conversely, keeping a translation when the perspective really changes introduces a bias. The choice therefore links capture geometry, the richness of the observations and the tolerated error, rather than a principle of simplicity or flexibility applied blindly.

**Dimension and identifiability of the warp**: translation: two parameters; planar Euclidean motion: rotation and two translations; affine: six parameters; homography: eight independent parameters after fixing the scale. A homography acts through a projective division: small changes in the denominator can strongly change the edges of the extrapolated region. With little overlap or texture, some parameters compensate each other and the local information matrix can become poorly conditioned. Compare models on held-out geometry rather than on the optimized score alone. If a simpler model is sufficient, it can limit these compensations; if the capture violates its assumptions, this simplicity instead imposes an irreducible bias.

**Compare model complexity on held-out geometry**: A project comparison can fit translation, affine and projective warps on the same textured support, then measure transfer on independently selected landmarks. Additional parameters may lower the fitted intensity cost while increasing held-out error or instability near the image boundary. Choose the simplest model meeting the geometric tolerance under the scene assumptions, recording failures as well as correlation. A homography is physically justified for a plane or pure rotation, not arbitrary parallax.

**Blocking errors**: Equating maximum flexibility with maximum precision.
Source: [[40-features-matching/references/45-recalage-ecc|Full reference]]; [OpenCV 4.13.0, tracking.hpp L263–L269 and L321–L329: motion types and parameter counts](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp); [Baker and Matthews 2002, §2.4 cost in the number of parameters, §3.4 canonical-point error](https://www.ri.cmu.edu/pub_files/pub3/baker_simon_2002_3/baker_simon_2002_3.pdf); compromise between flexibility and stability deduced by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-ECC-003 provenance::agent pole::B pole::E
END
