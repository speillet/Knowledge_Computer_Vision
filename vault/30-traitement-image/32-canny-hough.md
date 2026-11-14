# Flashcards — Canny and Hough: edges, lines and segments

reference note: [[30-traitement-image/references/32-canny-hough|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::30-traitement-image

## CV-CANNY-HOUGH-001

Objective: Explain the hysteresis. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-001
Question: Why does Canny use two thresholds instead of a single gradient threshold?
Reponse: **Expected answer**: Strong contours initiate structures; weaker responses can be retained when they are connected to strong ones according to hysteresis.

**Further explanation**: Non-maximum suppression thins the responses first. Thresholds do not give any semantic class.

**Interpreted procedure**: The gradient measures a local variation in intensity. Non-maximum suppression keeps the ridges along the gradient direction in order to avoid thick bands. Hysteresis then decides which weak ridges extend a sufficiently strong structure. The low threshold allows conditional continuity; it does not make every weak response admissible.

**Constructed example**: An unevenly lit edge has a high-contrast portion and a weak portion. A single high threshold fragments the edge; a single low threshold also keeps a lot of texture. Two thresholds make it possible to keep weak portions connected to the strong portion. If the entire contour is weak and has no strong seed, it may remain absent. The setting depends on the smoothing scale, the contrast and the gradient definition; none of these steps on its own distinguishes part edges from background texture.

**Describe hysteresis as a graph traversal**: after computing the gradient and suppressing non-maxima, initialize a queue with the pixels above the high threshold. Visit their neighbors and recursively keep those above the low threshold; discard the other, unconnected responses. This scheme explains how a long, weak portion can be retained without a single one of its pixels exceeding the high threshold. The gradient direction is normal to the contour, computed with a convention such as $\operatorname{atan2}(G_y,G_x)$; the suppression compares the magnitudes along this normal. Changing the L1/L2 norm, the smoothing or the bit depth changes the scale of the scores and therefore the meaning of the thresholds.

**Weak chains need a surviving strong seed**: Constructed graph interpretation: a chain of pixels between the low and high thresholds survives only if its connected component reaches a strong pixel. A disconnected chain with identical gradient magnitudes is discarded. A single noise bridge can conversely connect an unwanted chain to a valid seed. Inspect nonmaximum-suppressed responses and connectivity before changing thresholds; increasing the high threshold changes the seeds, whereas increasing the low threshold can break the connecting path.

**Blocking errors**: Describing the low threshold as a second, independent segmentation.
Source: [[30-traitement-image/references/32-canny-hough|Full reference]] ; [OpenCV 4.13.0 imgproc.hpp, `Canny`: smallest threshold for edge linking, largest for strong-edge seeds](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L1903-L1922) ; [Canny 1986, abstract](https://doi.org/10.1109/TPAMI.1986.4767851). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d03 famille::algorithme cv_id::CV-CANNY-HOUGH-001 provenance::agent pole::B pole::E pole::F
END

## CV-CANNY-HOUGH-002

Objective: interpret a Hough vote. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-002
Question: What do $\rho$ and $\theta$ represent in $\rho=x\cos\theta+y\sin\theta$?
Reponse: **Expected answer**: For image coordinates $x,y$ in pixels, $\rho$ is the signed distance from the chosen image origin in pixels; $\theta$ is the angle of the line's normal in radians, according to the stated convention. Each edge point votes for the straight lines passing through it.

**Further explanation**: Bins impose a resolution; a maximum can group several neighboring structures.

**Geometric reading**: vector $(\cos\theta,\sin\theta)$ is a unit normal. The scalar product with $(x,y)$ gives the projection of the point on this normal; all the points on the same line share this projection. Thus, for $\theta=0$, the equation becomes $x=\rho$: a vertical line. For $\theta=\pi/2$, it becomes $y=\rho$: a horizontal line, in the stated axes.

**Construction of votes**: each contour point can belong to several lines and therefore votes for several pairs. A high accumulation means that a set of points supports a hypothesis, without certifying their belonging to the same object. Too wide bins mix up close lines; too thin bins disperse the noisy votes. If the origin changes after a crop, the value of $\rho$ also changes: return the parameters in the original coordinate frame before any physical measurement.

**Angular accuracy and position**: A small error $\delta\theta$ changes $\rho$ by about $(-x\sin\theta+y\cos\theta)\delta\theta$, with $\delta\theta$ in radians. The effect grows with the distance from the origin along the line: an angular bin does not represent a uniform tolerance in pixels everywhere. At a lever arm of 500 px, one degree corresponds to about 8.7 px. This derivation does not give the final error of a detector, but helps to choose a reasonable discretization and to understand an extrapolation. The pairs $(\rho,\theta)$ and $(-\rho,\theta+\pi)$ represent the same line; the angle interval and the allowed sign of $\rho$ must be handled together.

**Moving a Hough line from ROI to full-image coordinates**: Let ROI coordinates satisfy $p_{full}=p_{ROI}+o$, with offset $o=(x_0,y_0)^T$ in full-image pixels. Substituting in $n^Tp=\rho$, where $n=(\cos\theta,\sin\theta)^T$, gives $\rho_{full}=\rho_{ROI}+x_0\cos\theta+y_0\sin\theta$; theta is unchanged by translation. For an ROI starting at $(100,50)$, its local vertical line $x=20$ has full-image rho 120 px. This project derivation assumes a translated crop without resize or rotation; those transformations require another normal/scale conversion.

**Blocking errors**: Confusing the normal with the segment direction, or forgetting the pixel unit.
Source: [[30-traitement-image/references/32-canny-hough|Full reference]] ; [Duda and Hart 1972, §2, normal parameterization and eq. 1](https://doi.org/10.1145/361237.361242) ; [OpenCV 4.13.0 imgproc.hpp, `HoughLines` output convention](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L2174-L2206). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d03 famille::raisonnement cv_id::CV-CANNY-HOUGH-002 provenance::agent pole::B pole::E pole::F
END

## CV-CANNY-HOUGH-003

Objective: Distinguish a line from a segment. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-003
Question: Why does HoughLines not directly return the endpoints of a real line segment?
Reponse: **Expected answer**: It parameterizes an infinite line; the limits of its support must be estimated separately or with a segment variant such as HoughLinesP.

**Further explanation**: Check the minimum length, the gaps and the observed region; extending a line beyond its support is not a measurement.

**Difference between model and support**: A line is an infinite set of points satisfying an equation; a segment adds two ends and an observed support. A maximum of votes indicates an orientation and a position supported by contours, but distant points or several objects can contribute to the same maximum.

**Constructed example**: Two small collinear edges separated by a large gap can support the same line. Automatically connecting the farthest points would extend the segment into an unobserved area. To measure a part, project the support points on the direction of the line, examine interruptions and apply length and continuity constraints consistent with the task. A variant that returns segments also uses grouping parameters. Its end points do not, however, become exact physical limits without checking the image and the uncertainty.

**Find a finite support**: from the normal $n=(\cos\theta,\sin\theta)$, take a point $p_0=\rho n$ and the unit direction $d=(-\sin\theta,\cos\theta)$. For each edge point $p$, test its normal distance $|n^Tp-\rho|$, then project the compatible points with $s=d^T(p-p_0)$. Contiguous groups in $s$ give segments whose ends are $p_0+s_{min}d$ and $p_0+s_{max}d$. This process separates the perpendicular tolerance from longitudinal gaps. The choice of support, the presence of occlusions and a possible re-estimation of the line on its points determine the ends. Taking the minimum and maximum of all collinear points of the image is not enough.

**Disconnected support should not become one segment**: Two collinear 10 px edges separated by 100 px can vote for the same infinite line. Taking the extreme support projections would return a segment crossing a large unobserved gap. Separate longitudinal support clusters using an explicit gap tolerance, then assess whether an occlusion model justifies reconnecting them. A line fit and a segment-existence decision use related geometry but answer different questions.

**Blocking errors**: Interpreting an infinite line as the complete contour of a part.
Source: [[30-traitement-image/references/32-canny-hough|Full reference]] ; [Duda and Hart 1972, §4, collinear points found "without regard to contiguity"](https://doi.org/10.1145/361237.361242) ; [OpenCV 4.13.0 imgproc.hpp, `HoughLines` and `HoughLinesP` outputs](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp#L2174-L2238). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d03 famille::comparaison cv_id::CV-CANNY-HOUGH-003 provenance::agent pole::B pole::E pole::F
END

## CV-CANNY-HOUGH-004

Objective: Differentiate texture and structure. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-004
Question: Hough detects many lines on a textured surface. Which check avoids blindly tuning the voting threshold?
Reponse: **Expected answer**: Inspect the Canny edge map, the angular distribution, the useful region and the spatial support of candidates.

**Further explanation**: Test a controlled texture perturbation and the task's geometric constraints before validating a line.

**Proposed investigation**: Overlay the lines and their support points on the image. If the votes come from repeated streaks, the detector may respond correctly to contours that are simply not those of the part. Then examine the distribution of angles and the number of fragments: this distinguishes a structured texture from scattered noise.

**Constructed ablation**: Fix the bins and thresholds, restrict a region of interest, then separately change the smoothing and the expected orientation constraint. Measure the task-relevant lines found, the false candidates and the position error. Raising only the voting threshold can eliminate a useful low-contrast edge while keeping a long, repetitive texture. A geometric constraint helps only if it remains valid for the orientations actually encountered. The accumulator has photometric support; validating the part model is an additional decision of the pipeline.

**Distinguishing votes from fitting error**: a long texture provides many points and therefore many votes, even if it is not the desired structure. For a candidate, also compute the normal distances $r_i=x_i\cos\theta+y_i\sin\theta-\rho$ of its support points, their longitudinal extent and the fraction of positions actually covered. A very precise short line and a long discontinuous line do not serve the same purpose. Also compare its relationship to other expected edges: parallelism, intersections or distances, if these properties are legitimate for the part. These validations are choices of the proposed pipeline; the accumulator score is not a calibrated probability that a task-relevant edge is present.

**Normal consistency can reject texture support**: For a proposed line, compare its normal with local edge-gradient directions as well as perpendicular distances. Many texture pixels can lie close to the line while having incompatible orientations. This is a proposed verification feature, not a guarantee: corners, noisy gradients and thick edges require tolerance. Evaluate its effect on the target structure rather than treating a large accumulator peak as a probability or automatically raising the voting threshold.

**Blocking errors**: Concluding that every accumulator maximum is a physical edge.
Source: [[30-traitement-image/references/32-canny-hough|Full reference]]; [Duda and Hart 1972, §4, meaningless groups of collinear points at lower thresholds](https://doi.org/10.1145/361237.361242); texture diagnosis proposed by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d03 famille::diagnostic cv_id::CV-CANNY-HOUGH-004 provenance::agent pole::B pole::E pole::F
END
