# Flashcards — Farnebäck — dense optical flow through polynomial expansion

reference note: [[100-mouvement-video/references/103-farneback|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::100-mouvement-video

## CV-FARNEBACK-001

Objective: Explain the polynomial mechanism. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-FARNEBACK-001
Question: How does Farnebäck estimate displacement from two image neighborhoods without point descriptors?
Reponse: **Expected answer**: It approximates neighborhoods by quadratic polynomials, connects their coefficient changes to a translation, and then aggregates constraints and refines to multiple scales. For an ideal model $f_2(x)=f_1(x-d)$, we have $2Ad=b_1-b_2$.

**Further explanation**: $A$ is the symmetric matrix of quadratic coefficients, $b_i$ the linear coefficient vector of neighborhood $i$, and $d$ a 2D displacement in pixels. This relation assumes a local translation; the actual method works with noisy approximations.

**Interpretation of the local model**: Quadratic coefficients describe the shape of the intensities in a neighborhood, rather than an independent signature to match. An ideal translation creates a specific relationship between the coefficients of the two polynomials. The aggregation exploits several constraints to limit the fragility of an isolated inversion.

**Example of a limit**: A uniform wall provides no informative curvature in either direction; a neighborhood straddling two objects can mix two motions. Enlarging the window can reduce noise but smooths this boundary. Evaluate these regions separately. A dense method outputs a vector everywhere by construction; local accuracy still depends on the image information and on the fit of the model.

**Expanding the translation**: Replacing $x$ by $x-d$ in $x^TAx+b_1^Tx+c_1$ gives $x^TAx+(b_1-2Ad)^Tx+d^TAd-b_1^Td+c_1$ when $A$ is symmetric. Comparing the linear terms gives $b_2=b_1-2Ad$. This derivation is exact for the constructed model; real images do not carry the same polynomial translated everywhere. The method therefore seeks a weighted, aggregated solution of the local constraints, over a region where translation is an acceptable approximation. The constant terms also change, but do not supply the directional information needed to identify both displacement components.

**Constant terms provide a consistency check**: For an exact translation of a quadratic polynomial, the constant coefficient must also satisfy $c_2=c_1+d^TAd-b_1^Td$. Recovering a displacement from linear coefficients alone does not test that full identity. A constructed polynomial can verify both relations without running a flow implementation. In real images, coefficient estimates and visibility violate the ideal translated-polynomial model, so agreement is an assumption-sensitive diagnostic rather than physical proof.

**Blocking errors**: Presenting the dense output as proof that each pixel is well constrained.
Source: [[100-mouvement-video/references/103-farneback|Full reference]]; [Farnebäck 2003, §2 polynomial expansion, §3 eqs. 2–8, §3.2 neighborhood solution, §3.5 iterative and multi-scale estimation](https://www.ida.liu.se/ext/WITAS-ev/Computer_Vision_Technologies/Papers/scia03_farneback.pdf). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d10 famille::algorithme cv_id::CV-FARNEBACK-001 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-002

Objective: Solve an ideal local constraint. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FARNEBACK-002
Question: For an ideal quadratic model, $A=\mathrm{diag}(2,1)$ and $b_1-b_2=(8,-2)^T$. If $2Ad=b_1-b_2$, what displacement is obtained, and which limitation must be kept in mind?
Reponse: **Expected answer**: $d=(2,-1)^T$ px. The solution comes from the ideal model with invertible matrix; it does not guarantee a reliable estimate if the coefficients are noisy or the window does not contain information in two directions.

**Further explanation**: A singular $A$ does not allow ordinary inversion. In a real image, spatial aggregation, weighting and conditioning matter more than an isolated formula.

**Interpreted calculation**: The two equations are $4d_x=8$ and $2d_y=-2$, hence the predicted displacement. The coefficients are assumed to follow the same conventions. The exercise checks a translational relation on modeled intensities; it does not measure a physical velocity and does not simulate every stage of the dense flow.

**Unfavorable case**: If the neighborhood shows almost no variation in one direction, the corresponding component becomes sensitive to small coefficient errors. Adding more similar pixels does not necessarily restore this information. Examine the conditioning and the mixing of motions, then compare another aggregation on known translations. This is the link with least squares: a small residual and a well-identified displacement are not equivalent.

**Directional sensitivity**: With $A=\operatorname{diag}(2,\varepsilon)$, the ideal equations become $4d_x=\Delta b_x$ and $2\varepsilon d_y=\Delta b_y$. A small error on $\Delta b_y$ is amplified by $1/(2\varepsilon)$ when $\varepsilon$ is small. A small residual can therefore coexist with a large error on $d_y$. Solving the system with a suitable factorization and inspecting its conditioning is more informative than blindly applying an inverse. A regularization stabilizes the weak direction numerically by adding a preference; it does not turn this preference into a certain observation. The diagonal example shows this without running a complete flow.

**The equation is sensitive to coefficient scale and rank**: In the question, $2A=\operatorname{diag}(4,2)$ maps $(2,-1)^T$ to $(8,-2)^T$, directly checking the sign and factor of two. If the second diagonal entry approaches zero, an unchanged linear-coefficient error yields a large second displacement error. This mirrors the aperture problem: a numerical solution exists only with usable directional information. Regularization can select a result but adds an assumption rather than another observation.

**Blocking errors**: Inverting a matrix without checking its rank; converting the result directly to m/s.
Source: [[100-mouvement-video/references/103-farneback|Full reference]]; [Farnebäck 2003, §3 eqs. 5–8 and §3.2 uniqueness unless the neighborhood is exposed to the aperture problem](https://www.ida.liu.se/ext/WITAS-ev/Computer_Vision_Technologies/Papers/scia03_farneback.pdf). The diagonal example is a project construction recomputed in the 2026-11-14 review checks.
Tags: cv::pilote cv::d10 famille::raisonnement cv_id::CV-FARNEBACK-002 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-003

Objective: Read the coordinate frame and units of the flow. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-FARNEBACK-003
Question: An OpenCV calculation returns flow[y,x]=(4,-2) between frames 40 ms apart. Where should the correspondence be sought, and what can be concluded about velocity?
Reponse: **Expected answer**: To $(x+4,y-2)$ in the second image. The displacement is in pixels; in this example the image speed approximation is $(100,-50)$ px/s. A speed in m/s requires additional geometry and depth or metric scale.

**Further explanation**: Do not confuse the row/column order of array access with the component order. At an irregular frame rate, use the acquisition timestamps. The presence of a vector does not prove that the pixel is visible in the second image.

**Reading the coordinate frame**: Array access uses row then column, but the vector gives the horizontal then the vertical displacement. Here, a negative vertical component means a position two pixels higher in the usual image coordinate frame. The point reached is in the second image, not a value to add to an arbitrary row index.

**Discriminating check**: Translate a textured image synthetically in a known direction and check the direction, components and units. Keep the timestamps if some frames are dropped. An average image speed can be computed from a valid pair, but perspective, depth and camera motion prevent equating it with the object's 3D speed. Conversion is therefore a separate modeling step.

**Transport relation**: The forward convention reads $I_1(x,y)\approx I_2(x+u(x,y),y+v(x,y))$ when photometry and visibility are compatible. To resample the second image on the grid of the first, use these destination positions. Building a destination image by pushing every source pixel forward can create holes and collisions; it is a different resampling operation. For the vector $(4,-2)$, keep a mask of destination positions that fall outside the image. This direction check distinguishes a valid displacement, an inverted warp and a display whose axes have been swapped.

**Blocking errors**: Reading (4,-2) as (row, column); announcing a metric speed without a scale.
Source: [[100-mouvement-video/references/103-farneback|Full reference]]; [OpenCV 4.13.0 tracking.hpp, calcOpticalFlowFarneback flow convention, L215–L217](https://github.com/opencv/opencv/blob/4.13.0/modules/video/include/opencv2/video/tracking.hpp#L215-L217). The speed conversion and resampling rule are project deductions.
Tags: cv::pilote cv::d10 famille::pratique cv_id::CV-FARNEBACK-003 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-004

Objective: interpret a round-trip inconsistency. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FARNEBACK-004
Question: To check forward flow $F(x)$, can you add backward flow $B(x)$ evaluated at the same pixel?
Reponse: **Expected answer**: The point reached is $x+F(x)$: evaluate $B$ at this position, usually by interpolation, and then verify $F(x)+B(x+F(x))$. The same pixel in the second image can represent another surface.

**Further explanation**: A large deviation can come from an occlusion, an exit from the field of view or a matching error. A small residual does not prove the right association on a repetitive texture. The check is a project diagnostic, not a certification of the flow.

**Analytical example**: If the source point is at 10 and the forward displacement is 4 pixels along one axis, the point to examine in the other image is 14. The correct backward flow at this point should bring 14 back to 10. Reading the backward value at 10 would test another observation.

**Validity policy**: If the reached position is outside the image or in a hidden region, do not present the round-trip residual as an ordinary accuracy measure. Keep a mask and an explicit rule. On a repetitive pattern, two opposite errors can also be mutually consistent; an independent reference remains necessary to establish the true correspondence. This check is a useful alarm, not a complete proof.

**Composition of fields**: Composing a displacement $F_{12}$ and then $F_{23}$ gives $F_{13}(x)=F_{12}(x)+F_{23}(x+F_{12}(x))$, provided the matches are valid. The round trip is the special case where one expects to return to the starting point, hence the residual formula. Adding the fields at the same indices would assume that these indices already denote the same surfaces in all images. Interpolating the second field can still mix two motions at a boundary; keep this source of error in the interpretation. Composition across many frames also accumulates errors and does not by itself become long-term tracking with visibility and re-identification.

**Composing flows requires transporting the lookup point**: Constructed one-dimensional case: $F(x)=1$ and $B(y)=-y$. At $x=0$, evaluating the backward field at $x+F(x)=1$ gives a zero round-trip residual, while evaluating at zero gives residual one. The difference comes from sampling different surface positions, not merely from a sign convention. Interpolation and out-of-bounds handling must accompany the composition rule when the displaced location is noninteger or outside the valid image.

**Blocking errors**: Comparing the two vectors at the same coordinate without accounting for the displacement.
Source: [[100-mouvement-video/references/103-farneback|Full reference]]; [Farnebäck 2003, §3.4 comparing the second expansion at the displaced position](https://www.ida.liu.se/ext/WITAS-ev/Computer_Vision_Technologies/Papers/scia03_farneback.pdf); [OpenCV 4.13.0 lk_track.py, backward check L56–L59](https://github.com/opencv/opencv/blob/4.13.0/samples/python/lk_track.py#L56-L59). The composition rule is a project derivation.
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-FARNEBACK-004 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-005

Objective: Adjust the pyramid without masking the failures. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-FARNEBACK-005
Question: Why can adding optical-flow pyramid levels help with large motions while degrading small objects?
Reponse: **Expected answer**: The displacement shrinks at coarse levels, but downsampling can make small structures disappear and mix motion boundaries. Evaluate the capturable amplitude, the error on small objects and the motion boundaries together.

**Further explanation**: Vary the resolution levels and windows on fixed sequences. Measure the end-point error where ground truth exists, with an occlusion mask, and the total cost. A color-coded flow map often looks smooth even when the geometry is wrong.

**Scale trade-off**: At coarse levels, a large displacement of the original image spans fewer pixels, which eases a local search. But an object of a few pixels can merge into the background and no longer contribute its own motion. Fine refinement then starts from an estimate already biased by its neighborhood.

**Constructed experiment**: Use a scene with large background motion and a small independent object, then vary only the pyramid. Report the error on the background, on the object and at its boundary, as well as invalid pixels. An average improvement dominated by the background may hide the loss of the small object. This reasoning links the parameter to the useful signal, without assuming that a larger budget improves every region uniformly.

**Orders of magnitude**: With a spatial reduction by two at each level, a displacement of 32 px in the original image becomes 4 px after three reductions. An object 6 px wide, on the other hand, spans only 0.75 px before the effects of filtering and sampling: its own motion can disappear. Propagating the field to a finer level requires resizing the grid and multiplying the components by the scale factor. Interpolating the array without rescaling the amplitude breaks the data contract. This constructed example explains the trade-off between capturing large displacements and preserving small structures, without setting a universal optimal number of levels.

**Coarse scales can mix motions across a thin object**: A small moving object and its differently moving background can contribute to the same coarse neighborhood after smoothing. The resulting local polynomial no longer describes one common translation, even when the displacement magnitude falls within the solver's capture range. Compare errors separately on interiors, boundaries and small objects when adding levels or enlarging windows. A lower global average flow error can conceal the disappearance of the task-critical object.

**Blocking errors**: Concluding that more levels improve every region of the image.
Source: [[100-mouvement-video/references/103-farneback|Full reference]]; [Farnebäck 2003, §3.5 multi-scale estimation and §4 smoothing of discontinuities](https://www.ida.liu.se/ext/WITAS-ev/Computer_Vision_Technologies/Papers/scia03_farneback.pdf); [OpenCV 4.13.0 optflowgf.cpp, flow propagated with factor 1/pyr_scale, L1163–L1167](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/optflowgf.cpp#L1163-L1167). Added reasoning: project deduction.
Tags: cv::pilote cv::d10 famille::evaluation cv_id::CV-FARNEBACK-005 provenance::agent pole::B pole::C pole::D
END
