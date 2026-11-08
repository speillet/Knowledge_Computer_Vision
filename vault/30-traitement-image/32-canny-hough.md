# Flashcards — Canny and Hough: edges, lines and segments

reference note: [[30-traitement-image/references/32-canny-hough|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::30-traitement-image

## CV-CANNY-HOUGH-001

Objective: Explain the hysteresis. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-001
Question: Why does Canny use two thresholds instead of a single gradient threshold?
Reponse: **Expected answer**: Strong contours initiate structures; weaker responses can be retained when they are related to strong ones according to hysteresis.

**Further explanation**: Removing non-maxima thins the answers first. Thresholds do not give any semantic class.

**Interpreted procedure**: The gradient measures a local variation in intensity. The removal of non-maxima keeps the ridges in the direction of the gradient in order to avoid thick bands. The hysteresis then decides which weak ridges extend a sufficiently strong structure. The low threshold allows for conditional continuity; it does not make all weak responses admissible.

**Constructed example**: An unevenly lit edge has a contrasting portion and a weak portion. A high single threshold fragments the edge; a low single threshold also retains a lot of texture. The two thresholds make it possible to keep certain small portions connected to the strong portion. If the entire contour is weak and without a strong primer, it may remain absent. The setting depends on the smoothing scale, contrast, and gradient definition; none of these steps single-handedly distinguishes part edges and background texture.

**Describe hysteresis as a journey**: after calculating the gradient and removing non-maxima, initialize a queue with pixels above the high threshold. Browse their neighbors and recursively keep those above the low threshold; discard other unrelated answers. This diagram explains how a long, small portion can be retained without a single pixel exceeding the high threshold. The direction of the gradient is a normal to the contour, calculated with a convention such as $\operatorname{atan2}(G_y,G_x)$; the suppression compares the amplitudes along this normal. Changing norm L1/L2, smoothing or digital depth changes the scale of scores and therefore the direction of the thresholds.

**Weak chains need a surviving strong seed**: Constructed graph interpretation: a chain of pixels between the low and high thresholds survives only if its connected component reaches a strong pixel. A disconnected chain with identical gradient magnitudes is discarded. A single noise bridge can conversely connect an unwanted chain to a valid seed. Inspect nonmaximum-suppressed responses and connectivity before changing thresholds; increasing the high threshold changes the seeds, whereas increasing the low threshold can break the connecting path.

**Blocking errors**: Describe the low threshold as a second independent segmentation.
Source: [[30-traitement-image/references/32-canny-hough|Full reference]] ; [OpenCV 4.13.0, Canny, Non-maximum Removal and Hysteresis Thresholding](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d03 famille::algorithme cv_id::CV-CANNY-HOUGH-001 provenance::agent pole::B pole::E pole::F
END

## CV-CANNY-HOUGH-002

Objective: interpret a Hough vote. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-002
Question: What do $\rho$ and $\theta$ represent in $\rho=x\cos\theta+y\sin\theta$?
Reponse: **Expected answer**: For image coordinates $x,y$ in pixels, $\rho$ is the signed distance from the chosen image origin in pixels; $\theta$ is the angle of normal in radians, according to the convention announced. Each edge point votes for the straight lines passing through it.

**Further explanation**: Bins impose a resolution; a maximum can group several neighboring structures.

**Geometric reading**: vector $(\cos\theta,\sin\theta)$ is a unit normal. The scalar product with $(x,y)$ gives the projection of the point on this normal; all the points on the same line share this projection. Thus, for $\theta=0$, the equation becomes $x=\rho$: a vertical line. For $\theta=\pi/2$, it becomes $y=\rho$: a horizontal line, in the announced axes.

**Construction of votes**: each contour point can belong to several lines and therefore vote for several couples. A high accumulation means that a set of points supports a hypothesis, without certifying their belonging to the same object. Too wide bins mix up close lines; too thin bins disperse the noisy votes. If the origin changes after a crop, the value of $\rho$ also changes: return the parameters in the original coordinate frame before any physical measurement.

**Angular accuracy and position**: A small $\delta\theta$ error causes $\rho$ to vary by about $(-x\sin\theta+y\cos\theta)\delta\theta$, with $\delta\theta$ in radians. The effect grows with distance at the origin: an angular bin does not represent a uniform tolerance in pixels everywhere. At a leverage of 500 px, a degree corresponds to an order of magnitude of 8,7 px. This derivation does not give the final error of a detector, but helps to choose a reasonable discretization and to understand an extrapolation. Couples $(\rho,\theta)$ and $(-\rho,\theta+\pi)$ represent the same straight line; the angle interval and the allowed sign of $\rho$ must be processed together.

**Moving a Hough line from ROI to full-image coordinates**: Let ROI coordinates satisfy $p_{full}=p_{ROI}+o$, with offset $o=(x_0,y_0)^T$ in full-image pixels. Substituting in $n^Tp=\rho$, where $n=(\cos\theta,\sin\theta)^T$, gives $\rho_{full}=\rho_{ROI}+x_0\cos\theta+y_0\sin\theta$; theta is unchanged by translation. For an ROI starting at $(100,50)$, its local vertical line $x=20$ has full-image rho 120 px. This project derivation assumes a translated crop without resize or rotation; those transformations require another normal/scale conversion.

**Blocking errors**: Confound normal and segment direction or forget the pixel unit.
Source: [[30-traitement-image/references/32-canny-hough|Full reference]] ; [OpenCV 4.13.0, Hough, How does it work? and Standard and Probabilistic Hough Line Transform](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d03 famille::raisonnement cv_id::CV-CANNY-HOUGH-002 provenance::agent pole::B pole::E pole::F
END

## CV-CANNY-HOUGH-003

Objective: Distinguish between right and segment. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-003
Question: Why does HoughLines not directly return the endpoints of a real line segment?
Reponse: **Expected answer**: Sets a straight line; support limits must be estimated separately or with a segment variant like HoughLinesP.

**Further explanation**: Check minimum length, holes and region observed; extending a straight out of support is not a measurement.

**Difference Between Model and Support**: A line is an infinite set of points satisfying an equation; a segment adds two ends and an observed support. A maximum of votes indicates an orientation and a position supported by contours, but distant points or several objects can contribute to the same maximum.

**Constructed example**: Two small collinear edges separated by a large space can support the same straight line. Automatically connecting the furthest points would move the segment into an area without observation. To measure a part, project the support points on the direction of the right, examine interruptions and apply length and continuity constraints consistent with the task. A variant that returns segments also uses grouping parameters. Its extremities do not, however, become exact physical limits without check of image and uncertainty.

**Find a Finished Support**: from the normal $n=(\cos\theta,\sin\theta)$, take a point $p_0=\rho n$ and the unit direction $d=(-\sin\theta,\cos\theta)$. For each $p$ contour point, test its normal $|n^Tp-\rho|$ distance, then project the points compatible with $s=d^T(p-p_0)$. Contiguous groups in $s$ offer segments, whose ends are equal to $p_0+s_{min}d$ and $p_0+s_{max}d$. This process distinguishes perpendicular tolerance and longitudinal holes. The choice of support, the presence of occlusions and a possible re-estimation of the line on its points condition the ends. It is not enough to take the minimum and maximum of all the collinear points of the image.

**Disconnected support should not become one segment**: Two collinear 10 px edges separated by 100 px can vote for the same infinite line. Taking the extreme support projections would return a segment crossing a large unobserved gap. Separate longitudinal support clusters using an explicit gap tolerance, then assess whether an occlusion model justifies reconnecting them. A line fit and a segment-existence decision use related geometry but answer different questions.

**Blocking errors**: Interpret an infinite line as the complete contours of a part.
Source: [[30-traitement-image/references/32-canny-hough|Full reference]] ; [OpenCV 4.13.0, Hough, How does it work? and Standard and Probabilistic Hough Line Transform](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html). Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d03 famille::comparaison cv_id::CV-CANNY-HOUGH-003 provenance::agent pole::B pole::E pole::F
END

## CV-CANNY-HOUGH-004

Objective: Differentiate texture and structure. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-004
Question: Hough detects many lines on a textured surface. Which check avoids blindly tuning the voting threshold?
Reponse: **Expected answer**: Inspect map Canny, angular distribution, useful region and spatial support of candidates.

**Further explanation**: Test a controlled texture disturbance and business constraints before validating a line.

**Proposed investigation**: Overlapping the lines and their support points to the image. If the votes come from repeated streaks, the detector may respond correctly to contours that are simply not those of the part. Then examine the distribution of angles and the number of fragments: this distinguishes a structured texture from a dispersed noise.

**Constructed ablation**: Set the bins and thresholds, restrict a region of interest, and then separately change the smoothing and the expected orientation constraint. Measure business lines found, false candidates and position error. Increasing only the voting threshold can eliminate a useful edge that is not very contrasting while retaining a long and repetitive texture. A geometric constraint helps only if it remains valid for the orientations actually encountered. The accumulator has a photometric support; the validation of the part model is an additional decision of the pipeline.

**Differentiating Vote and Adjustment Error**: a long texture provides a lot of points and therefore votes, even if it is not the desired structure. For a candidate, calculate in addition the normal distances $r_i=x_i\cos\theta+y_i\sin\theta-\rho$ on her support points, their longitudinal extent and the fraction of the positions actually covered. A very precise short line and a long discontinuous line do not have the same use. Also compare its relationship to other expected edges: parallelism, intersections or distances, if these properties are legitimate for the part. These validations are choices of the proposed pipeline; the accumulator score is not a calibrated probability of the presence of a business edge.

**Normal consistency can reject texture support**: For a proposed line, compare its normal with local edge-gradient directions as well as perpendicular distances. Many texture pixels can lie close to the line while having incompatible orientations. This is a proposed verification feature, not a guarantee: corners, noisy gradients and thick edges require tolerance. Evaluate its effect on the target structure rather than treating a large accumulator peak as a probability or automatically raising the voting threshold.

**Blocking errors**: Conclude that each maximum accumulator is a physical edge.
Source: [[30-traitement-image/references/32-canny-hough|Full reference]]; [OpenCV 4.13.0, Hough, How does it work? and Standard and Probabilistic Hough Line Transform](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html); texture diagnosis proposed by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d03 famille::diagnostic cv_id::CV-CANNY-HOUGH-004 provenance::agent pole::B pole::E pole::F
END
