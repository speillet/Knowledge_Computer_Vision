# Flashcards — GrabCut, regions and appearance models

reference note: [[90-segmentation/references/92-grabcut-regions|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::90-segmentation

## CV-GRABCUT-001

Objective: Explain the GrabCut alternation. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-GRABCUT-001
Question: Which two main operations does GrabCut alternate?
Reponse: **Expected answer**: Estimate the background and foreground appearance models, then optimize the labels by graph cut on the defined energy.

**Further explanation**: The definite and probable labels of the initialization play different roles; the process is not a generic semantic classifier.

**Intuition of alternation**: Current labels give colour examples for background and foreground; the appearance models then set the cost of each assignment. Relations between neighbors add a spatial preference. The new partition is used for a new estimate, within the constraints of the initialization.

**Example of a limitation**: If a part of the target looks like the background, its appearance cost can favor the wrong label. A user indication can provide information that colour alone does not. The process does not name an object according to a taxonomy, and an energy minimum is not proof that the mask is correct for the application. Check the initialization and the definite labels before increasing iterations. To compare with a learned promptable method, also count interventions, failures and the full cost, not just the time of the last optimization.

**Energy and cut**: For a binary label $L_p$, a unary term can be set to $-\log p(I_p\mid L_p)$ under the corresponding colour mixture. A schematic neighbor term $w_{pq}\mathbf1[L_p\ne L_q]$ penalizes a boundary between similar pixels; high contrast reduces $w_{pq}$. With fixed appearance parameters and a graph-representable binary energy, the minimum cut solves this sub-problem exactly. Alternating with the estimation of the mixtures does not imply a joint global optimum over all the unknowns. Naming the sub-problem that is solved prevents confusing the solver's guarantee with the correctness of the object model used.

**Blocking errors**: Describing only a fixed colour threshold.
Source: [[90-segmentation/references/92-grabcut-regions|Full reference]] ; [Rother et al. 2004, §3.1–§3.2, eqs. 7–11 and Fig. 3](https://www.microsoft.com/en-us/research/wp-content/uploads/2004/08/siggraph04-grabcut.pdf) ; [Boykov and Jolly 2001, §3 Theorem 1](https://www.csd.uwo.ca/~yboykov/Papers/iccv01.pdf) ; [OpenCV 4.13.0, grabcut.cpp L545–L598](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/grabcut.cpp#L545-L598).
Tags: cv::pilote cv::d09 famille::algorithme cv_id::CV-GRABCUT-001 provenance::agent pole::A pole::E
END

## CV-GRABCUT-002

Objective: Check an initialization constraint. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-GRABCUT-002
Question: GrabCut consistently excludes part of an object despite more iterations. What should be checked first?
Reponse: **Expected answer**: The initial rectangle and the definite background labels: a needed part of the object can be made impossible by a hard constraint.

**Further explanation**: Test a manual correction of the labels on a copy, then observe the mask; distinguish a wrong initialization from an insufficient appearance model.

**Causal chain**: A pixel imposed as definite background is not among the labels that the optimization can switch to foreground. If the initial rectangle excludes a part of the target, the procedure can comply perfectly with its contract while producing a truncated mask.

**Constructed check**: Overlay the definite and probable labels on the image, then fix only the wrong area on a copy. Keep the other parameters and measure the effect. If this correction is not enough, compare the colour distributions and the boundary, because several defects can coexist. Repeating the same optimization does not replace correct initial information. Distinguishing a false constraint from an insufficient appearance model helps choose the useful intervention: changing the starting mask, adding a cue or considering another mechanism, rather than assuming a numerical failure.

**Hard constraint and preference**: A definite label forbids the other assignment, while a probable label lets the energy choose. If a real part of the object is assigned to definite background, changing the appearance settings does not make the correct solution admissible. In a constructed test, correct only this constraint, then compare iterations from the same saved initial state. An improvement locates a defect in the constraint; a persistent exclusion may still come from close colours or regularization. Keeping the four states of the mask until the final decision avoids losing interaction information by binarizing the labels too early.

**Blocking errors**: Assuming that convergence will undo any erroneous constraint.
Source: [[90-segmentation/references/92-grabcut-regions|Full reference]] ; [Rother et al. 2004, §3.3, firm background labels](https://www.microsoft.com/en-us/research/wp-content/uploads/2004/08/siggraph04-grabcut.pdf) ; [OpenCV 4.13.0, grabcut.cpp L352–L363 and L526–L543, rectangle init and probable-only update](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/grabcut.cpp#L526-L543) ; [OpenCV 4.13.0, GrabCut tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/py_tutorials/py_imgproc/py_grabcut/py_grabcut.markdown). Constructed checks: project deduction.
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-GRABCUT-002 provenance::agent pole::A pole::E
END

## CV-GRABCUT-003

Objective: Choose an interaction. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-GRABCUT-003
Question: When extracting an object whose colors resemble the background, why compare interaction cost and assumptions rather than optimization time alone?
Reponse: **Expected answer**: Labels added by the user can provide the missing information; a method that is fast per call can still require many corrections.

**Further explanation**: Evaluate the mask, the number of corrections and robustness on held-out images; an energy optimum is not enough.

**Cost actually paid**: A fast algorithm can require several retouches if its colour model separates target and background poorly. A method that is more expensive per call can reduce interaction; the opposite is also possible. Times must include the whole procedure needed to reach a defined quality.

**Proposed protocol**: Fix held-out images, a reset rule and a correction budget, then measure mask quality, number of interventions, total time and failure rate. Separately, make the background closer to the target in colour to test the appearance assumption. Keep unresolved cases in the results. An energy optimum indicates that the procedure has satisfied its model; it does not say that this model has enough information to distinguish the object of interest. The comparison must therefore weigh the method's assumptions against human effort, without choosing on solver duration alone.

**Quality–interaction curve**: Set a common rule for placing the initial rectangle, then a budget of corrections or user time. Measure quality after zero, one and several interactions, and report the share of images that do not reach the target within the maximum budget. Clicks are comparable only if their policy and the information available to the clicker are stated; a correction chosen with the reference mask is a different oracle from a real operator. Also compare boundaries and small regions of interest. This protocol gives a usable trade-off curve instead of an isolated optimization time obtained after a particularly favorable initialization.

**Blocking errors**: Presenting a low computation time as the complete performance of the process.
Source: [[90-segmentation/references/92-grabcut-regions|Full reference]] ; [Rother et al. 2004, §5, failure cases and interaction comparisons](https://www.microsoft.com/en-us/research/wp-content/uploads/2004/08/siggraph04-grabcut.pdf) ; [OpenCV 4.13.0, GrabCut tutorial source](https://github.com/opencv/opencv/blob/4.13.0/doc/py_tutorials/py_imgproc/py_grabcut/py_grabcut.markdown). Protocols: project constructions.
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-GRABCUT-003 provenance::agent pole::A pole::E
END
