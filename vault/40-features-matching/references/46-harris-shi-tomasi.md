---
id: CV-CORNERS
type: methode
domaine: d04
poles: ["B", "C", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-FILTRES", "CV-SVD"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# Harris and Shi–Tomasi — local structure and trackable points

## Prerequisites and competencies

**Required prerequisites**: [CV-FILTRES](../../30-traitement-image/references/31-filtrage-gradients.md), [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md). **Target competencies**: Interpret local eigenvalues; distinguish Harris and Shi – Tomasi scores; set a selection of corners; distinguish matching detection and ambiguity; evaluate a selection for tracking. Related notions remain alternatives, not implicit dependencies.

## Problem and data contract

Choose points whose displacement is identifiable in two directions. Input: grayscale image, gradients and local window; output: pixel coordinates and response score, not a descriptor or a match. To follow the points, you then need an algorithm like Lucas – Kanade. The units of intensity, the scale of derivation and the edges of the image must remain consistent.

## Intuition and mechanism

A small displacement barely changes a flat patch, changes the image mainly in the direction normal to an edge, and changes it in both directions around a corner. Harris turns this observation into a score; Shi – Tomasi tests the least constrained direction. Procedure: derive → aggregate gradient products → calculate score → remove non-local maxima → impose spacing and point budget. They are local texture detectors, without object recognition.

## Mathematics and conventions

For a displacement $d=(u,v)^T$ in pixels, the quadratic variation is approximated by $E(d)\approx d^TMd$, with $M=\sum_{p\in W}w_p\nabla I_p\nabla I_p^T$. $w_p\ge0$ weights the $W$ window, the gradients are in intensity/pixel and $M$ is $2\times2$, semi-definite positive. Its eigenvalues $\lambda_1,\lambda_2$ measure variations in two directions. Harris uses $R_H=\det M-k(\mathrm{tr}M)^2$, with $k$ without unit; Shi – Tomasi uses $R_S=\min(\lambda_1,\lambda_2)$. Their thresholds and units differ: do not directly compare the numerical scores.

## Assumptions, parameters and implementation

Linearization involves small displacements and a sufficiently stable appearance. An edge has a small value of its own: the aperture problem remains along the edge. In OpenCV 4.13, `goodFeaturesToTrack` uses Shi – Tomasi by default; `qualityLevel` is relative to the highest score and `minDistance` is expressed in pixels. Window, derivative, and pyramid level modify responses. These parameters do not guarantee invariance of scale or sustainable monitoring. No OpenCV calls were executed for this reference note.

## Cost, evaluation and controlled variation

The dense calculation depends on the number of pixels and the size of the neighborhood; a budget of points especially reduces the work of the next tracker. Baseline: selection of the strongest points; proposed variation: impose a coverage by cells with equal budget. Measure survival, tracking error, coverage and geometric error on reserved sequences, not just the number of corners. Analytical calculation of the project: $M=\mathrm{diag}(100,1)$ gives $R_H=-308{,}04$ for $k=0{,}04$, and $R_S=1$; $M=\mathrm{diag}(20,20)$ gives $336$ and $20$. A very strong derivative in one direction is not enough.

## Failure modes, diagnosis and alternatives

Concentrated points on a textured panel may misconstrain the overall geometry; check their distribution. Repeated patterns produce strong corners but ambiguous associations. If the score falls after a change in resolution or contrast, compare gradients and windows in consistent units. FAST reduces the cost of corner testing; SIFT and ORB add a separate description and scale/orientation mechanisms.

## Guided reasoning and proposed checks

These constructed cases develop structure tensor, observable directions and repeatability. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-CORNERS-001

**Question of work**: One window produces $M=\mathrm{diag}(100,1)$, and another produces $M=\mathrm{diag}(20,20)$. Which better constrains a small 2D displacement, and why?

**Reference Response**: The second: its smallest eigenvalue is 20 instead of 1. The two directions are constrained; the first one looks like an edge, even if its total gradient is stronger.

**Interpretation of directions**: With the first matrix, a shift in the direction associated with the value 1 changes the patch little. The large 100 value does not compensate for this weak direction. With the second, a unit displacement in any proper direction produces the same local curvature of 20.

**Proposed use**: Before a Lucas – Kanade follow-up, examine the smallest binding term and the distribution of points. A set of well-conditioned corners but grouped in a small area does not guarantee a stable overall registration. The numbers assume the local model of small translations and the same gradient units; comparing matrices from different normalizations without aligning them would not have the same meaning.

### Case linked to CV-CORNERS-005

**Question of work**: Why is the number of detected corners insufficient for comparing settings intended for Lucas–Kanade tracking?

**Reference Response**: Measure survival, displacement error, spatial coverage and geometry error with comparable budget and resolution. A setting that produces more dots can add noise or redundant dots.

**Example of comparison**: One hundred corners on a single texture can be redundant and leave the piece useful without observations. Fifty distributed points can best constrain the requested movement, but only if their movements are reliable. The number does not describe this coverage or how long the dots remain visible.

**Protocol built**: Set resolution, total budget and tracking criteria, then vary selection score and space quotas separately. Measure errors on annotated point trajectories or on independent geometry, also counting points lost. A low photometric residual can remain misleading in case of repetition. Report performance on blur, low texture and occlusion, with the same rejection rules for all settings.

**Documentary reference for this pass**: [OpenCV 4.13, Harris Corner Detection](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html), Theory, local matrix and eigenvalues. The other developments are in the [flashcards](../46-harris-shi-tomasi.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-CORNERS-001

**Situation**: One window produces $M=\mathrm{diag}(100,1)$, and another produces $M=\mathrm{diag}(20,20)$. Which better constrains a small 2D displacement, and why?

**Diverting the local tensor**: for a small displacement $d$, $I(p+d)-I(p)\approx\nabla I(p)^Td$. The weighted sum of these squared deviations gives $d^T(\sum_p w_p\nabla I_p\nabla I_p^T)d$, so $M$. Constant error contours are ellipses: their large axis corresponds to the direction in which the image changes little. If the photometric noise model is isotropic and the problem is correctly posed, the local uncertainty of displacement is related to a matrix proportional to $M^{-1}$. A small eigenvalue then becomes a great directional uncertainty; it is a link with the followability, under assumptions, not a guarantee of future visibility.

### CV-CORNERS-002

**Situation**: How do Harris and Shi–Tomasi differ in corner selection, and can the same numerical threshold be retained?

**Avoid confusing score and model**: Harris can calculate determinant and trace directly without diagonalizing $M$; Shi – Tomasi evaluates the smallest eigenvalue, $(\operatorname{tr}M-\sqrt{(M_{11}-M_{22})^2+4M_{12}^2})/2$ for a symmetric matrix $2\times2$. These are two summaries of the same tensor, not two new proofs of identity of the point. In the isotropic case $\lambda_1=\lambda_2=\lambda$, Harris gives $(1-4k)\lambda^2$ while Shi – Tomasi gives $\lambda$. Their evolution with the contrast and scale of the patch therefore differs even when the visual ranking of the best corners seems similar. Removing maxima and spacing remain separate steps of these formulas.

### CV-CORNERS-003

**Situation**: In OpenCV 4.13 goodFeaturesToTrack, how do qualityLevel, minDistance and maxCorners differ?

**Read the selection as a suite of filters**: first calculate the quality map, retain the local maxima, eliminate insufficient scores, then consider the candidates in descending order respecting the minimum distance and budget. Therefore, the quota does not replace a quality threshold. In a built-in case, if the only good points are close, increasing the spacing can get a lot and leave less than the number requested; this is not necessarily a failure of the API. To limit concentration, a mask of interest or quotas by region are choices of system to compare, keeping the same notion of score and the same units of distance.

### CV-CORNERS-004

**Situation**: Strong corners on a repetitive grid still produce a poor homography. Which checks distinguish detection failure from incorrect association?

**Distinguish between local and global observation**: $M$ describes the curvature of a small translation cost around a given patch. It does not compare this patch to all other patches in an image. A grid can therefore give a strong curvature around each intersection, while producing several remote minima for matching between images. A known initial move can make local tracking possible without resolving the overall recognition of the correct box. To evaluate the detector alone, use a reference transformation and check the distance to the projected position; to match it, then examine which identity is selected among the candidates. Both rates do not have the same denominator.

### CV-CORNERS-005

**Situation**: Why is the number of detected corners insufficient for comparing settings intended for Lucas–Kanade tracking?

**check round trip built**: Following $p_t$ to $\hat p_{t+1}$, then following the latter to $\hat p_t$ gives a $e_{FB}=\|\hat p_t-p_t\|_2$ cycle error in pixels. A big error signals a useful inconsistency to reject; a small error can also come from the same bad pattern found in both directions. It must therefore complete a displacement reference, not replace it. Compare the fraction of valid points by keeping the occlusions in the balance sheet. If a setting rejects almost all the hard points, its average error on survivors can drop while degrading the availability of the registration. Reliable monitoring and refusal policy must be evaluated together.

**Passages consulted for these developments**: [OpenCV 4.13, Harris](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html), Theory, tensor and response; [OpenCV 4.13, Shi–Tomasi](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html), Theory and selection goodFeaturesToTrack.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-CORNERS-001 — The error ellipse gives a quantitative comparison

With equal unit photometric noise in the local linearized model, $M^{-1}$ for the first window is $\operatorname{diag}(0.01,1)$ and for the second is $\operatorname{diag}(0.05,0.05)$. The second window has a much smaller worst-direction variance despite lower total gradient energy. This constructed calculation explains choosing by the weakest direction. It assumes a shared local displacement and does not establish robustness to occlusion or an incorrect brightness model.

### CV-CORNERS-002 — Contrast scaling changes the response power

If all intensities are multiplied by $\alpha$, gradients scale by $\alpha$ and tensor eigenvalues by $\alpha^2$. Shi–Tomasi then scales by $\alpha^2$, whereas Harris scales by $\alpha^4$. A fixed absolute threshold therefore changes its meaning with intensity units, and the two scores cannot share a numerical threshold. Relative-to-maximum selection can cancel a uniform scale, but clipping and spatially varying illumination do not preserve this ideal relation.

### CV-CORNERS-003 — A relative threshold can accept uniformly weak images

If the best response in a blurred image is small, a fixed fraction of that response is also small. Thus qualityLevel does not provide an absolute guarantee of trackability. Record the best score and retained-score distribution as well as the returned count. minDistance may then exclude clustered candidates and maxCorners may truncate the survivors; increasing the cap cannot create strong points where the image lacks usable gradients.

### CV-CORNERS-004 — Repeatability and identity need separate denominators

Given a known image transformation, first count whether a detected point has a nearby detected counterpart in the visible transformed region. Then, among described points, measure whether matching chooses that counterpart rather than a repeated intersection. This proposed decomposition separates missed detections from wrong identities. Exclude points truly outside shared visibility from repeatability denominators, and report exclusions so a method cannot appear robust simply by discarding difficult regions.

### CV-CORNERS-005 — Survivor-only error can reward excessive rejection

Constructed comparison: method A retains 90 of 100 points with 1 px mean error; method B retains 10 with 0.5 px mean error. B has better conditional error but may fail to support the required geometry. Report survival and spatial coverage jointly with error, and count whether a valid transform is available. Forward/backward consistency is useful evidence, but repeated texture can generate a consistent wrong cycle in both directions.

Consulted foundations: [OpenCV Harris](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html): structure tensor, eigenvalue interpretation and Harris response; [OpenCV tracking](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html): goodFeaturesToTrack quality and spacing contract.

## Sources and flashcards

- [Harris and Stephens 1988, self-correlation and corner response](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf).
- [OpenCV 4.13, Shi – Tomasi, Theory and goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html).
- [OpenCV 4.13, Harris, Theory](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html).
- [Related flashcards](../46-harris-shi-tomasi.md): CV-CORNERS-001 to 005.

Editor: Agent Codex, 2026-10-24. Primary sources consulted and API OpenCV 4.13 verified with Context7. Analytical calculations and proposed protocols are distinguished from experiments; no actual export, video benchmark or independent scientific validation announced.
