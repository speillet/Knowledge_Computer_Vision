# Flashcards — GrabCut, regions and appearance models

reference note: [[90-segmentation/references/92-grabcut-regions|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::90-segmentation

## CV-GRABCUT-001

Objective: Explain the GrabCut alternation. Family: algorithm. Provenance: agent.

START
CV-Pilote
ID: CV-GRABCUT-001
Question: Which two main operations does GrabCut alternate?
Reponse: **Expected answer**: Estimate the background/object appearance patterns and then optimize the labels via graph cut in the defined energy.

**Further explanation**: The safe and probable constraints of initialization have a distinct role; the process is not a generic semantic classifier.

**Intuition of alternation**: Current labels give color examples for background and foreground; appearance patterns then influence the cost of each attribution. Relations between neighbors add a spatial preference. The new partition is used for a new estimate, within the constraints of the initialization.

**Example of limit**: If a part of the target looks like the bottom, its cost of appearance can favor the wrong region. A user indication can provide information that color alone does not provide. The process does not automatically name an object according to a taxonomy and a minimum of energy is not proof of business truth. Check initialization and safe labels before increasing iterations. To compare to a learned promptable method, also count interventions, failures and full cost, and not just the time of the last optimization.

**Energy and Cut**: for a binary label $L_p$, a unary term can be linked to $-\log p(I_p\mid L_p)$ under the corresponding color mixture. A schematic neighbor term $w_{pq}\mathbf1[L_p\ne L_q]$ penalizes a boundary between similar pixels; high contrast can reduce $w_{pq}$. With fixed appearance parameters and for a compatible binary energy, the cutoff of the graph optimizes this sub-problem. Alternating with the estimation of the mixtures does not imply an overall joint optimum of all the unknowns. Defining the solved sub-problem prevents confusing the solver's warranty with the correctness of the object model used.

**Blocking errors**: Describe only a fixed color threshold.
Source: [[90-segmentation/references/92-grabcut-regions|Full reference]] ; [OpenCV GrabCut, theory and masks](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
Tags: cv::pilote cv::d09 famille::algorithme cv_id::CV-GRABCUT-001 provenance::agent pole::A pole::E
END

## CV-GRABCUT-002

Objective: check is an initialization constraint. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-GRABCUT-002
Question: GrabCut consistently excludes part of an object despite more iterations. What should be checked first?
Reponse: **Expected answer**: The initial zone and the safe background labels: a useful region can be made impossible by constraint.

**Further explanation**: Test a manual correction of labels on copy and then observe the mask; distinguish initialization and insufficient appearance.

**Causal chain**: A pixel imposed as a safe background is not one of the labels that optimization can freely transform into an object. If the initial rectangle excludes a part of the target, the procedure can perfectly comply with its contract while producing a truncated mask.

**Verification built**: Overlay safe and probable labels on the image, and then fix only the wrong area on a copy. Keep other parameters and measure the effect. If this correction is not enough, compare the color distributions and the border, because several defects can coexist. An additional repetition of the same optimization does not replace correct initial information. This distinction between a false constraint and a model of insufficient appearance helps to choose the useful intervention: changing the starting mask, adding a clue or considering another mechanism rather than assuming a digital failure.

**Hard Constraint and Preference**: A certain label conceptually prohibits the other attribution, while a probable label lets the energy choose. If an actual part of the object is attached to the bottom, changing the appearance settings does not make this solution admissible. In a built test, only correct this constraint, and then compare iterations on the same initial saved state. An improvement locates a contract defect; a persistent exclusion may still come from close colors or regularization. Distinguishing the four states of the mask until the final decision avoids losing interaction information by prematurely binarizing the labels.

**Blocking errors**: Assume that convergence must cancel out any erroneous constraint.
Source: [[90-segmentation/references/92-grabcut-regions|Full reference]] ; [OpenCV GrabCut, theory and masks](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-GRABCUT-002 provenance::agent pole::A pole::E
END

## CV-GRABCUT-003

Objective: Choose an interaction. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-GRABCUT-003
Question: When extracting an object whose colors resemble the background, why compare interaction cost and assumptions rather than optimization time alone?
Reponse: **Expected answer**: Labels added by the user can provide the missing information; a quick fix can require a lot of corrections.

**Further explanation**: Evaluate mask, number of corrections and robustness on reserved images; an optimum energy is not enough.

**Cost actually paid**: A fast algorithm can require several retouches if its color model separates wrong target and background. A more expensive per-call method can reduce interaction; the opposite is also possible. The times must include the procedure necessary to achieve a defined quality.

**Proposed Protocol**: fix reserved images, a reset rule and a correction budget, then measure mask quality, number of interventions, total time and failure rate. Separately add a background closer to the target to test the appearance hypothesis. Keep unresolved cases in the balance sheet. An energy optimum indicates that the procedure has satisfied its model; it does not say that this model has enough information to distinguish the useful object. The comparison must therefore relate hypotheses of the method and human effort, without choosing only on the duration of the solver.

**Quality curve – interaction**: Set a common rule to place the initial rectangle, and then a budget for corrections or user time. Measure quality after zero, one, and then multiple interactions and keep the rate of images that do not reach the target to the maximum budget. Clicks are only comparable if their policy and accessible information are announced; a correction chosen with the reference mask constitutes a different oracle from a real operator. Compare also borders and small useful regions. This protocol gives an exploitable compromise curve, instead of an isolated optimization time obtained after a particularly favorable initialization.

**Blocking errors**: Present a low computing time as the complete performance of the process.
Source: [[90-segmentation/references/92-grabcut-regions|Full reference]] ; [OpenCV GrabCut, theory and masks](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-GRABCUT-003 provenance::agent pole::A pole::E
END
