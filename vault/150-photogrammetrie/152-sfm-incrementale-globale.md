# Flashcards — Structure from Motion: incremental and global pipelines

reference note: [[150-photogrammetrie/references/152-sfm-incrementale-globale|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::150-photogrammetrie

## CV-SFM-001

Objective: Compare incremental and global SfM on cost, outlier handling and error accumulation. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-SFM-001
Question: Two structure-from-motion pipelines receive the same scene graph of geometrically verified image pairs. Pipeline I grows a model from one seed pair, adding one image at a time. Pipeline G estimates every camera orientation at once from the pairwise rotations, then every camera position, then refines the result. Compare them on three points: where the computation time goes; how a wrong pairwise geometry is caught; how errors accumulate and which failure is typical of each.
Reponse: **Expected answer**: (1) Time: pipeline I spends it in repeated bundle adjustment of a growing model, local after every image and global after growth; pipeline G solves orientations and positions once and then runs a few global adjustments, which made it several times to orders of magnitude faster on the same matches. (2) Outliers: I tests each new image against the 3-D points already built (PnP–RANSAC inlier count and ratio, filtering after each adjustment), so a wrong pair seldom enters unless it agrees with the model; G has no model yet and must reject wrong pairs from redundancy alone (robust rotation averaging, residual thresholds, cycle or ordering consistency), and a surviving wrong pair distorts the whole solution at once. (3) Accumulation: I is order-dependent: a bad seed or registration cascades and drift grows along chains of images, which retriangulation and global adjustment only reduce; G treats all images equally, but recovering positions from directions is ill-posed for collinear motion, needs accurate intrinsics, and rotation averaging can collapse on symmetric scenes.

**Further explanation**: Both pipelines share the front end and end with the same reprojection-error bundle adjustment; they differ in how they build its initialization.

**Evidence on cost**: Photo Tourism's incremental run took about two weeks for 597 registered Notre Dame photos, "dominated by the iterative bundle adjustment". 1DSfM was usually 2–4 times faster than sequential SfM. GLOMAP reports 497.3 s against 4,051.0 s for COLMAP on IMC 2023, with matching excluded, and a higher average AUC at 3° (69.6 against 65.3); the paper does not state its hardware.

**Why the incremental order matters**: COLMAP's authors write that "a single bad decision may lead to a cascade of camera mis-registrations", and that without refinement SfM "drifts quickly to a non-recoverable state". Wilson and Snavely add that sequential methods treat images unequally.

**Where global pipelines break**: relative translations are only directions, reliable only with accurate intrinsics; nearly collinear motion makes positions ill-conditioned. GLOMAP replaces translation averaging by a joint positioning of cameras and points, which handles sequences and uncalibrated photos better, but its rotation averaging collapsed on a rotationally symmetric hall.

**Choosing**: COLMAP's documentation calls the incremental mapper the most robust and tested, and the global mapper faster on large, well-matched graphs, more sensitive to matching outliers and dependent on focal priors. Decide on the data with a reference, not from either slogan.

**Blocking errors**: Claiming that global SfM needs no bundle adjustment, or that it cannot drift and ignores outliers. Calling incremental SfM order-independent. Declaring either pipeline always more accurate.
Source: [[150-photogrammetrie/references/152-sfm-incrementale-globale|Full reference]]; [Schönberger and Frahm 2016, §2.2, §4.2, §4.4](https://openaccess.thecvf.com/content_cvpr_2016/papers/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.pdf); [Pan et al. 2024, GLOMAP, §1, §2.2, §3.2, §4.1, §4.4 and Table 5](https://arxiv.org/abs/2407.20219); [Wilson and Snavely 2014, 1DSfM, §1 and §7](https://www.cs.cornell.edu/projects/1dsfm/docs/1DSfM_ECCV14.pdf); [Snavely et al. 2006, Photo Tourism, §4.2](https://phototour.cs.washington.edu/Photo_Tourism.pdf); [COLMAP 4.2.1, doc/faq.rst L131–L159: choosing a mapper](https://github.com/colmap/colmap/blob/4.2.1/doc/faq.rst#L131-L159). Grouping into three criteria: project synthesis.
Tags: cv::pilote cv::d15 famille::comparaison cv_id::CV-SFM-001 provenance::agent pole::B pole::C
END

## CV-SFM-002

Objective: Reason about what relative camera directions determine in global SfM. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-SFM-002
Question: After rotation averaging, a global SfM pipeline knows every camera orientation and, for each verified pair, only the unit direction from one camera centre to the other. A drone flew a straight line and took three images at $x=0$, 10 and 30 m. (a) Besides the usual global translation and scale, what do these camera-to-camera directions leave undetermined here, and why? (b) A ground point at $(20,10)$ m appears in all three images; with the first two cameras fixed at $(0,0)$ and $(10,0)$ by convention, show how its rays restore the third position. (c) Suppose instead that the third camera is at $(30,1)$ m: the directions to it are $1.909^\circ$ above the line from the first camera and $2.862^\circ$ from the second. Roughly how far from the first camera would the solution put it if the second direction were wrong by $+0.5^\circ$, and what does this show?
Reponse: **Expected answer**: (1) All three camera-to-camera directions point along $\pm x$, so any placement that keeps the order of the cameras on the line satisfies every measurement: the ratio of the spacings, 10 m to 20 m, is unobservable, a degeneracy beyond the four gauge freedoms of directions (translation and positive scale). The graph is not parallel rigid. (2) Rays to a point off the line form triangles: from $(0,0)$ along $(2,1)$ and from $(10,0)$ along $(1,1)$ they meet at $(20,10)$; the third image's ray, which reaches the point along $(-1,1)$, crosses $y=0$ at $x=30$, so the third camera is at $(30,0)$. Camera-to-point constraints remove the degeneracy. (3) Near collinearity, the law of sines gives $|C_1C_3|=10\sin a_2/\sin(a_2-a_1)\approx10\,a_2/(a_2-a_1)$: about 30 m nominally, about 23 m with $a_2=3.362^\circ$ (52 m with $-0.5^\circ$). The tiny apex angle, $0.95^\circ$, amplifies a direction error into a large distance error.

**Further explanation**: Translation averaging seeks positions $c_i$ such that $(c_j-c_i)/\lVert c_j-c_i\rVert$ matches each measured direction. Directions carry no length, so every solution can be translated and scaled; Wilson and Snavely write the unknown edge lengths as factors "unique up to global gauge ambiguity". Positions are unique up to that gauge only when the graph is parallel (bearing) rigid.

**Why collinear motion fails**: when cameras lie on a line, each direction is the same unit vector or its opposite. Moving the third camera from 30 m to 50 m changes no measurement, so no optimizer can recover the true spacing; noise only decides where it stops.

**What points add**: a point off the line is seen along non-parallel rays, so each camera's position becomes the intersection of rays through shared points. 1DSfM adds camera-to-point edges for coverage and "for avoiding degeneracies arising from collinear motion". GLOMAP goes further: it drops relative translations and estimates cameras and points jointly from camera rays, with a bounded residual equal to the sine of the angular error.

**Skewed triangles**: the constructed nearly-collinear case illustrates why GLOMAP's authors call scales from "skewed triangles" "especially prone to noise": with $+0.5^\circ$ the exact value is 23.13 m and with $-0.5^\circ$ 52.11 m, instead of 30.02 m.

**Blocking errors**: Saying that three non-zero baselines fix the spacing. Treating the residual freedom as the ordinary similarity gauge. Expecting more camera-to-camera edges along the same line to remove the ambiguity.
Source: [[150-photogrammetrie/references/152-sfm-incrementale-globale|Full reference]]; [Wilson and Snavely 2014, 1DSfM, §3 eqs. 1–2 and §6: camera-to-point edges and collinear degeneracy](https://www.cs.cornell.edu/projects/1dsfm/docs/1DSfM_ECCV14.pdf); [Pan et al. 2024, GLOMAP, §1, §2.2 (parallel rigidity), §3.2 eqs. 3–4](https://arxiv.org/abs/2407.20219). Numerical cases: project constructions recomputed in checks/152-sfm-incrementale-globale.py.
Tags: cv::pilote cv::d15 famille::raisonnement cv_id::CV-SFM-002 provenance::agent pole::B pole::C
END

## CV-SFM-003

Objective: Trace one iteration of the incremental SfM loop and justify its gates. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-SFM-003
Question: An incremental mapper using COLMAP 4.2.1's defaults has registered 200 images. Trace its next iteration. (a) How does it choose the next image, and when does it accept the registration? (b) The new image creates two tracks with an already registered image: the rays of the first meet at $1.2^\circ$, those of the second at $4^\circ$; the triangulator's minimum pairwise angle is $1.5^\circ$. What happens to each? (c) After the local bundle adjustment, the mapper merges and completes tracks and filters observations again; from time to time it also retriangulates and repeats global adjustment. Why is this done after the adjustment, and when does it stop?
Reponse: **Expected answer**: (1) Candidates are unregistered images that see enough already triangulated points (30 by default); they are ranked by a score that grows with the number of visible points and with their spread over the image. The best candidate is registered by PnP inside RANSAC and kept only if its inliers and inlier ratio pass thresholds (30 and 0.25); otherwise the next candidate is tried, a limited number of times per image. (2) The $1.2^\circ$ track is not triangulated now: its depth is poorly conditioned; it may be triangulated later, when another registered image gives a wider angle. The $4^\circ$ track is triangulated if it also has positive depth and small angular error, then refined; later filtering removes observations above 4 px and deletes a point if no pair of its rays reaches $1.5^\circ$. (3) Bundle adjustment moves cameras and points: observations rejected before may now fit, so tracks are continued, merged and retriangulated, while others now have large errors and are filtered. Outliers bias the adjustment, so adjust, retriangulate and filter are repeated until few observations change; global refinement runs when the model has grown by 10% or by a fixed number of images or points.

**Further explanation**: Choosing the next image: COLMAP divides each image into grids of $2^l$ cells per side over six levels; a cell adds $4^l$ to the score the first time it holds a visible point. Spread points fill more coarse cells, and PnP is better conditioned with many well-spread correspondences. With few points per image, the score still mostly counts points.

**Angles in numbers**: with a 1 m baseline across the line of sight, the angle is $2\arctan(0.5/d)$: $2.86^\circ$ at 20 m, $1.15^\circ$ at 50 m, so the $1.5^\circ$ gate is reached at about 38 m. The initial pair is stricter: a median angle above $16^\circ$ and a unit translation with $|t_z|<0.95$.

**Why after the adjustment**: COLMAP's authors note that, because of drift or retriangulation before the adjustment, "usually a significant portion of the observations in BA are outliers", and that after a second iteration results improve dramatically. In 4.2.1, local refinement runs at most twice and stops below 0.1% changed observations, with a robust loss in the first pass only; global refinement runs up to five times and stops below 0.05%.

**Blocking errors**: Choosing the next image by file order or acquisition time. Lowering the angle gate to gain points without accounting for depth uncertainty. Treating a converged adjustment as final without re-filtering. Relying on the reprojection threshold alone to reject low-parallax points.
Source: [[150-photogrammetrie/references/152-sfm-incrementale-globale|Full reference]]; [Schönberger and Frahm 2016, §2.2, §4.2, §4.3 eq. 3, §4.4](https://openaccess.thecvf.com/content_cvpr_2016/papers/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.pdf); [COLMAP 4.2.1, incremental_mapper.h L68–L171: registration, filtering and initial-pair defaults](https://github.com/colmap/colmap/blob/4.2.1/src/colmap/sfm/incremental_mapper.h#L68-L171); [COLMAP 4.2.1, incremental_pipeline.cc L543–L738: global-refinement trigger and main loop](https://github.com/colmap/colmap/blob/4.2.1/src/colmap/controllers/incremental_pipeline.cc#L543-L738); [COLMAP 4.2.1, incremental_triangulator.h L45–L91: triangulation thresholds](https://github.com/colmap/colmap/blob/4.2.1/src/colmap/sfm/incremental_triangulator.h#L45-L91). Angle values: project constructions recomputed in checks/152-sfm-incrementale-globale.py.
Tags: cv::pilote cv::d15 famille::algorithme cv_id::CV-SFM-003 provenance::agent pole::B pole::C
END

## CV-SFM-004

Objective: Diagnose a reconstruction folded by duplicate scene structure. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-SFM-004
Question: An incremental SfM model of a square clock tower with four identical faces converges with a mean reprojection error of 0.6 px. Photographers walked all around the tower, yet every reconstructed camera stands in front of only two faces, and the surrounding buildings appear twice in the point cloud, superimposed at about $90^\circ$ to each other. (a) What went wrong, and why does the reprojection error not reveal it? (b) Which checks would confirm the diagnosis? (c) How can the model be repaired?
Reponse: **Expected answer**: (1) Duplicate structure: images of different but identical faces matched and passed geometric verification, so cameras photographing another face were registered to a face already in the model, rotated by about $90^\circ$ around the tower; their own surroundings were then triangulated in the wrong place. Each image remains consistent with its wrong pose, so residuals stay small: the error is a wrong association, not noise. (2) Checks: project points seen only by one group of cameras into images of the other group: unique structure lands where those images observe different unique structure (conflicting observations); look for camera groups linked only through points on the repeated faces; check whether a registration's inliers lie only on the repeated structure; compare with independent evidence such as GNSS, a compass or a run with another seed. (3) Repair: split the camera graph at the links carried only by duplicate structure, then merge the parts again with a similarity estimated from unique structure, or keep separate models if none links them; constrain later registrations to unique points, or add images that see two faces at once.

**Further explanation**: Heinly et al. explain the mechanism in incremental SfM: the next image is chosen by similarity to registered images, and an image that overlaps only another copy of the duplicate structure "registers, but only to the facades of the tower"; later images register correctly to it, so the error propagates.

**Why the residual is blind**: reprojection error measures agreement between observations and the model they built. A camera 50 m from the tower axis, placed on the face $90^\circ$ away, is misplaced by $2\cdot50\sin45^\circ=70.7$ m, yet its feature points on the identical face reproject perfectly, and its background is triangulated to agree with its wrong pose.

**Camera-graph signal**: Heinly et al. weight camera pairs by $1-|O_i\cap O_j|/|O_i\cup O_j|$ over their observed points. In a constructed case, two cameras on the same face with surroundings (300 and 260 points, 240 shared) cost $1/4$; two cameras on different faces sharing only 150 facade points out of 300 each cost $2/3$. A minimum spanning tree therefore groups cameras by instance and bridges instances through few costly edges, which are the candidate splits.

**Limits and alternatives**: the conflict test needs some unique structure; a model of duplicate structure only cannot be disambiguated this way. Global pipelines are not immune: rotation averaging collapsed on a rotationally symmetric hall in GLOMAP's tests.

**Blocking errors**: Tightening RANSAC or reprojection thresholds and expecting the fold to disappear. Calling it drift or a scale error. Trusting the model because its reprojection error is low.
Source: [[150-photogrammetrie/references/152-sfm-incrementale-globale|Full reference]]; [Heinly, Dunn and Frahm 2014, §1, §3.3 eq. 1, §3.4 eqs. 5–6, §3.5 and §4, archived author copy](https://web.archive.org/web/2020/https://www.cs.unc.edu/~jheinly/publications/eccv2014-heinly.pdf); [Pan et al. 2024, GLOMAP, §3.4 and §4.1 (exhibition_hall)](https://arxiv.org/abs/2407.20219). Chord and edge-cost values: project constructions recomputed in checks/152-sfm-incrementale-globale.py.
Tags: cv::pilote cv::d15 famille::diagnostic cv_id::CV-SFM-004 provenance::agent pole::B pole::C
END

## CV-SFM-005

Objective: Evaluate SfM camera positions against a reference with an appropriate alignment and metric. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-SFM-005
Question: An SfM model without control (arbitrary frame and scale) is compared with surveyed camera centres at $(0,0)$, $(40,0)$, $(40,30)$, $(0,30)$ and $(20,15)$ m. In this constructed test the model equals the survey scaled by 0.1, rotated by $90^\circ$ and shifted, except camera 2, misplaced 15 m north. (a) The raw coordinate differences range from 5.4 to 47.2: why are they not errors, and what must be estimated first? (b) A least-squares alignment leaves residuals of 2.90, 9.25, 5.81, 1.21 and 3.09 m: what does this show, and what should replace it? (c) Which metric needs no alignment at all, what would it report here, and what can it miss?
Reponse: **Expected answer**: (1) Without control, the model is defined only up to a similarity: rotation, translation and scale, 7 degrees of freedom. Its coordinates are in another frame and unit, so their differences with the survey mean nothing. First estimate the similarity from corresponding camera centres, for example with Umeyama's closed form, then measure errors in survey metres; without the misplaced camera the residuals would be zero. (2) Least squares spreads one gross error over all cameras: correct cameras show 1.2 to 5.8 m, camera 2 only 9.25 m, and the fitted scale and rotation are biased. Use a robust alignment, RANSAC with a stated threshold followed by a refit on inliers, as COLMAP's model aligner does; it gives 0 m on the four consistent cameras and 15 m on camera 2. Report the threshold and inlier count. (3) Relative pose errors per image pair (rotation angle and angle between translation directions, the larger of the two), summarized as an AUC with unregistered pairs counted as failures. Here 7 of 10 pairs are exact; pairs 1–2, 2–4 and 2–5 show $20.6^\circ$, $16.3^\circ$ and $36.9^\circ$, isolating camera 2. They can miss slow scale drift along nearly collinear sequences, where absolute errors after robust alignment are needed.

**Further explanation**: Umeyama minimizes $\frac1n\sum\lVert y_i-(cRx_i+t)\rVert^2$: center both sets, take the SVD $UDV^\top$ of their cross-covariance, then $R=USV^\top$, $c=\operatorname{tr}(DS)/\sigma_x^2$ and $t=\mu_y-cR\mu_x$, with $S$ flipping the last axis when needed to avoid a reflection.

**Why least squares misleads**: here the fitted scale is 2.9% high and the rotation $7.5^\circ$ off. Camera 3, perfectly placed, shows 5.81 m. The RMS of 5.27 m describes no camera.

**Alignment removes what it estimates**: a similarity is legitimate for free-scale SfM, but it also hides any scale error.

**Relative metrics in practice**: GLOMAP reports AUC of the maximum of rotation and translation-direction errors for unordered collections, and camera-position AUC after robust alignment for sequences because "the relative error does not capture the scale drift well". Here pair 2–3 shows $0^\circ$ because camera 2 moved along that baseline, and the AUC at $5^\circ$ is 70. COLMAP's benchmark counts ordered pairs, which changes the trapezoid AUC: 73.88 instead of 75.92 at $20^\circ$. State the convention.

**Blocking errors**: Reporting raw coordinate differences as accuracy. Accepting least-squares residuals as per-camera errors when an outlier is present. Dropping unregistered images from the denominator. Treating relative-pose AUC as a measure of metric scale.
Source: [[150-photogrammetrie/references/152-sfm-incrementale-globale|Full reference]]; [Umeyama 1991, §II, eqs. 32–43 (paywalled; DOI)](https://doi.org/10.1109/34.88573); [Pan et al. 2024, GLOMAP, §4 (metrics)](https://arxiv.org/abs/2407.20219); [Wilson and Snavely 2014, 1DSfM, §7: RANSAC absolute orientation on camera centres](https://www.cs.cornell.edu/projects/1dsfm/docs/1DSfM_ECCV14.pdf); [COLMAP 4.2.1, doc/faq.rst L410–L448: model_aligner with RANSAC threshold](https://github.com/colmap/colmap/blob/4.2.1/doc/faq.rst#L410-L448); [COLMAP 4.2.1, benchmark/reconstruction/evaluation/utils.py L1262–L1590: relative errors, failures at 180 degrees, AUC](https://github.com/colmap/colmap/blob/4.2.1/benchmark/reconstruction/evaluation/utils.py#L1262-L1590). Five-camera case: project construction recomputed in checks/152-sfm-incrementale-globale.py.
Tags: cv::pilote cv::d15 famille::evaluation cv_id::CV-SFM-005 provenance::agent pole::B pole::C
END
