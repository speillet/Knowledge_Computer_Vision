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

**Further explanation**: $A$ is the symmetrical quadratic matrix, $b_i$ the linear coefficient of the neighbourhood $i$, and $d$ a Displacement 2D in pixels. This relationship assumes local translation; the actual method deals with noisy approximations.

**Interpretation of the local model**: Quadratic coefficients describe the shape of the intensities in a neighborhood, rather than an independent signature to match. An ideal translation leaves a special relationship between the terms of the two polynomials. The aggregation exploits several constraints to limit the fragility of an isolated inversion.

**Example of limit**: A uniform wall does not provide informational curvature in both directions; a neighborhood straddling two objects can mix two movements. Growing the window can reduce noise but smooth this border. check these regions separately in an assessment. A dense method offers output anywhere according to its format; local accuracy always depends on the image information and the adequacy of the model.

**Development of translation**: Replace $x$ with $x-d$ in $x^TAx+b_1^Tx+c_1$ gives $x^TAx+(b_1-2Ad)^Tx+d^TAd-b_1^Td+c_1$ when $A$ is symmetrical. The comparison of linear terms therefore provides $b_2=b_1-2Ad$. This derivation is accurate for the built model; the real images do not have the same polynomial transported everywhere. We then look for an aggregated and weighted solution to local constraints, with a domain where translation is an acceptable approximation. Constant terms also change, but do not replace the directional information needed to identify the two components of displacement.

**Constant terms provide a consistency check**: For an exact translation of a quadratic polynomial, the constant coefficient must also satisfy $c_2=c_1+d^TAd-b_1^Td$. Recovering a displacement from linear coefficients alone does not test that full identity. A constructed polynomial can verify both relations without running a flow implementation. In real images, coefficient estimates and visibility violate the ideal translated-polynomial model, so agreement is an assumption-sensitive diagnostic rather than physical proof.

**Blocking errors**: Present the dense output as proof that each pixel is well constrained.
Source: [[100-mouvement-video/references/103-farneback|Full reference]]; [Farnebäck 2003, §§2 – 3, expansion and displacement, §3.5 multi-scale](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf); [OpenCV 4.13.0, Optical Flow, Dense Optical Flow; project-specific quadratic derivations, original PDF inaccessible by timeout during this pass](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
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

**Calculation interpreted**: the two equations are $4d_x=8$ and $2d_y=-2$, hence the predicted displacement. The coefficients are assumed to be expressed in common conventions. The exercise checks a translational relationship on modelled intensities; it does not measure a physical velocity and does not simulate all stages of the dense flow.

**Unfavourable case**: If there is almost no variation in the direction of the neighborhood, the corresponding solution becomes sensitive to small coefficient errors. Increasing the number of similar pixels does not necessarily recreate this information. Examine the conditioning and mixing of movements, then compare a different aggregation on known translations. This is the link with the least squares: residual weak and well-identified displacement are not equivalent.

**Directional Sensitivity**: with $A=\operatorname{diag}(2,\varepsilon)$, the ideal equations become $4d_x=\Delta b_x$ and $2\varepsilon d_y=\Delta b_y$. A small error on $\Delta b_y$ is amplified by $1/(2\varepsilon)$ when $\varepsilon$ is small. A weak residual can thus coexist with a strong error on $d_y$. Solving the system by proper factorization and inspecting its conditioning is more informative than blindly applying an inverse. A regularization numerically stabilizes the weak direction by adding a preference; it does not transform this preference into certain observation. This is precisely what the diagonal example makes it possible to understand without executing a complete flow.

**The equation is sensitive to coefficient scale and rank**: In the front, $2A=\operatorname{diag}(4,2)$ maps $(2,-1)^T$ to $(8,-2)^T$, directly checking the sign and factor of two. If the second diagonal entry approaches zero, an unchanged linear-coefficient error yields a large second displacement error. This mirrors the aperture problem: a numerical solution exists only with usable directional information. Regularization can select a result but adds an assumption rather than another observation.

**Blocking errors**: Invert any array without checking its rank; directly convert the result to m/s.
Source: [[100-mouvement-video/references/103-farneback|Full reference]]; [Farnebäck 2003, §§2 – 3, expansion and displacement, §3.5 multi-scale](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf); [OpenCV 4.13.0, Optical Flow, Dense Optical Flow; project-specific quadratic derivations, original PDF inaccessible by timeout during this pass](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d10 famille::raisonnement cv_id::CV-FARNEBACK-002 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-003

Objective: read the coordinate frame and the units of the stream. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-FARNEBACK-003
Question: An OpenCV calculation returns flow[y,x]=(4,-2) between frames 40 ms apart. Where should the correspondence be sought, and what can be concluded about velocity?
Reponse: **Expected answer**: To $(x+4,y-2)$ in the second image. The displacement is in pixels; in this example the image speed approximation is $(100,-50)$ px/s. A speed in m/s requires additional geometry and depth or metric scale.

**Further explanation**: Do not reverse the line/column components. At irregular rate, take the acquisition timestamps. The presence of a vector does not prove that the pixel is visible in the second image.

**Reading the coordinate frame**: array access uses row then column, but the vector provides horizontal then vertical displacement. Here, a negative vertical component means a two-pixel higher position in the usual coordinate frame image. The point reached is in the second image, not a value to be added to a random line index.

**check**: synthetically move a textured image in a known direction and check direction, components and units. Keep timestamps if some frames are lost. An average image speed can be calculated from a valid pair, but perspective, depth and camera motion prevent it from being identified directly at the object’s 3D speed. Conversion is therefore a distinct model step.

**Transport relationship**: The front convention is written $I_1(x,y)\approx I_2(x+u(x,y),y+v(x,y))$ when photometry and visibility are compatible. To sample the second image on the grid of the first, we therefore use these destination positions. Creating a destination image by projecting all the source pixels can produce holes and collisions; it is not the same resampling operation. For vector $(4,-2)$, keep the mask of the positions reached out of field. This check sense distinguishes a valid displacement, a warp inversion and a simple display whose axes have been swapped.

**Blocking errors**: Read (4,-2) as (line,column); announce a metric speed without scale.
Source: [[100-mouvement-video/references/103-farneback|Full reference]] ; [OpenCV 4.13, Optical Flow, Dense Optical Flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html).
Tags: cv::pilote cv::d10 famille::pratique cv_id::CV-FARNEBACK-003 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-004

Objective: interpret a round-trip inconsistency. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FARNEBACK-004
Question: To check forward flow $F(x)$, can you add backward flow $B(x)$ evaluated at the same pixel?
Reponse: **Expected answer**: The point reached is $x+F(x)$: evaluate $B$ at this position, usually by interpolation, and then verify $F(x)+B(x+F(x))$. The same pixel in the second image can represent another surface.

**Further explanation**: A large deviation can come from a occlusion, a field output or an error. A small gap does not prove the right association in a repetitive texture. The check is a diagnosis of the project, not a certification of the flow.

**Analytical example**: If the source point is 10 and the forward displacement is 4 pixels on one axis, the point to be examined in the other image is 14. The correct inverse flow for this point should fall from 14 to 10. Reading the inverse value to 10 would test another observation.

**Validity policy**: If the reached position is out of the image or in a hidden region, do not present the residual round trip as an ordinary measure of accuracy. Keep a mask and an explicit rule. In a repetition, two opposite errors can also be consistent between them; an independent reference remains necessary to establish the true correspondence. This check is a useful alarm, not a complete proof.

**Composition of fields**: dial a $F_{12}$ move and then $F_{23}$ gives $F_{13}(x)=F_{12}(x)+F_{23}(x+F_{12}(x))$, under valid matches. The return is the particular case where one hopes to return to the same point, hence the formula of the residual. Adding the fields to the same indices would assume that these indices already denote the same surfaces in all images. The interpolation of the second field can still mix two movements at a border; keep this source of error in the interpretation. Consistent composition across multiple frames also accumulates errors and does not automatically become long-term tracking with visibility and re-identification.

**Composing flows requires transporting the lookup point**: Constructed one-dimensional case: $F(x)=1$ and $B(y)=-y$. At $x=0$, evaluating the backward field at $x+F(x)=1$ gives a zero round-trip residual, while evaluating at zero gives residual one. The difference comes from sampling different surface positions, not merely from a sign convention. Interpolation and out-of-bounds handling must accompany the composition rule when the displaced location is noninteger or outside the valid image.

**Blocking errors**: Compare the two vectors systematically to the same coordinate without taking into account the displacement.
Source: [[100-mouvement-video/references/103-farneback|Full reference]]; [Farnebäck 2003, §§2 – 3, expansion and displacement, §3.5 multi-scale](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf); [OpenCV 4.13.0, Optical Flow, Dense Optical Flow; project-specific quadratic derivations, original PDF inaccessible by timeout during this pass](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-FARNEBACK-004 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-005

Objective: Adjust the pyramid without masking the failures. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-FARNEBACK-005
Question: Why can adding optical-flow pyramid levels help with large motions while degrading small objects?
Reponse: **Expected answer**: The displacement is reduced to coarse levels, but the reduction can make small structures disappear and mix boundaries. Evaluate both catchable amplitude, error of small objects and limits of movement.

**Further explanation**: To vary the resolution levels, windows and fixed sequences. Measure endpoint error on available ground truth, occlusion mask and full cost. A color-coded flow map often looks smooth even if the geometry is wrong.

**Compromise of scale**: At coarse levels, a large displacement of the initial image represents fewer pixels, which facilitates a local search. But an object of a few pixels can mix at the bottom and no longer provide its own movement. Fine refinement then starts from a hypothesis already influenced by its neighborhood.

**Experience built**: Use a scene with large background movement and small independent object, then vary only the pyramid. Report error on the background, on the object and at its border, as well as invalid pixels. An average bottom-dominated improvement may mask the loss of the small object. This reasoning links the parameter to the useful signal, without assuming that a larger budget uniformly improves all regions.

**Orders of magnitude**: With a spatial reduction of two at each level, a displacement of 32 px in the original image becomes 4 px after three reductions. A wide object of 6 px, on the other hand, occupies only 0,75 px before the effects of filtering and sampling: its own movement can disappear. Moving up the field requires resizing the grid and multiplying the components by the appropriate scaling factor. Interpolating only the array without adjusting the amplitude produces a contract defect. This constructed example explains the trade-off between capturing large displacement and preserving small structures, without setting an optimal universal number of levels.

**Coarse scales can mix motions across a thin object**: A small moving object and its differently moving background can contribute to the same coarse neighborhood after smoothing. The resulting local polynomial no longer describes one common translation, even when the displacement magnitude falls within the solver's capture range. Compare errors separately on interiors, boundaries and small objects when adding levels or enlarging windows. A lower global average flow error can conceal the disappearance of the task-critical object.

**Blocking errors**: Conclude that more levels enhance each region of the image.
Source: [[100-mouvement-video/references/103-farneback|Full reference]]; [Farnebäck 2003, §§2 – 3, expansion and displacement, §3.5 multi-scale](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf); [OpenCV 4.13.0, Optical Flow, Dense Optical Flow; project-specific quadratic derivations, original PDF inaccessible by timeout during this pass](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d10 famille::evaluation cv_id::CV-FARNEBACK-005 provenance::agent pole::B pole::C pole::D
END
