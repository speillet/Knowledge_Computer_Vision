# Review — Hand–eye calibration — solving AX = XB with consistent coordinate frames — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 1 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for robot–camera calibration. Calibration between
other sensors and timing stay in
[CV-MULTICALIB](../../../vault/50-calibration-geometrie/references/55-calibration-multicapteurs.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HANDEYE-001 | Derivation $A=G_j^{-1}G_i$, $B=C_jC_i^{-1}$: confirmed by OpenCV 4.13.0 `calib3d.hpp` L2322–L2335 and the implementation (`calibration_handeye.cpp` L297–L304); synthetic generator recomputed. "**check**: … This check algebra without ordering a robot", "string residual", "poses robot" | Reasoning: derive the relative motions from a frame chain | 1 expected criterion with 3 steps; 354 → 357 lexical words | Notation identical to CV-MULTICALIB | Minor | Language fix of the expected answer; language fixes; Source line given exact lines |
| CV-HANDEYE-002 | Inputs gripper→base and target→camera, output camera→gripper: confirmed (L2210–L2233); `solvePnP` gives model→camera (L1031–L1032). "Why the exit is surprising", "check interface proposed", "control a rigid transformation", "To reverse it … never the only negation of $t$", "poses robot upside down" | Practice: API contract before calling the solver | 4 expected criteria; 397 → 393 lexical words | Consistent with the reference Problem section | Minor | Language fixes; Source line given exact lines |
| CV-HANDEYE-003 | At least two motions with non-parallel axes: confirmed by Horaud and Dornaika §3 (eq. 19 rank deficient for one motion) and OpenCV L2352–L2353. Missing limitation: OpenCV's default Tsai path discards motion pairs outside about 17°–116° and, with fewer than two left, returns the identity rotation and zero translation with only a log message (`calibration_handeye.cpp` L307–L336, L790–L820); "little constrained", "reserved validation", "closed strings", "learning subsets", "second member" | Design: excite observable directions | 3 expected criteria; 357 → 425 lexical words | Consistent with worked example B and the failure table | Important (misleading omission for a user of the default solver) | Language fix of the expected answer; added the sourced paragraph "OpenCV's default solver discards small motions"; Source line given exact passages |
| CV-HANDEYE-004 | $Y_i=G_iXC_i$ constant for a fixed target, closure $E_{ij}=Y_j^{-1}Y_i$: confirmed algebraically (check script). Expected answer "Note $G_i$ the …", "reserved poses", "coherent transformation"; "residual measurable closure", "digitally sensitive", "assembly unit" | Diagnosis: test the physical constancy of the target pose | 4 expected criteria; 398 → 405 lexical words | Consistent with Evaluation | Minor | Language fix of the expected answer; language fixes |
| CV-HANDEYE-005 | Eye-to-hand chain $G_i^{-1}XC_i=Y$ with $X={}^bT_c$: confirmed by OpenCV's eye-to-hand equations (L2336–L2346). Expected answer "write the constant string" (*chaîne*: chain); "Explicit eye-to-hand channel"; "reversing only an old exit" | Comparison: rebuild the chain when the mounting changes | 3 expected criteria; 323 → 322 lexical words | Consistent with the Mathematics section | Minor | Language fix of the expected answer; language fixes; Source line given exact lines |

Expected-answer changes (language fixes, meaning preserved or restored):

- CV-HANDEYE-001: "By multiplying left by $G_j^{-1}$ and right by $C_i^{-1}$, we get … then
  $AX=XB$." → "Multiplying on the left by $G_j^{-1}$ and on the right by $C_i^{-1}$ gives …
  hence $AX=XB$."
- CV-HANDEYE-003: "The number does not replace the diversity of movements: some components
  remain little constrained. Acquire rotations around non-parallel axes … and then examine
  conditioning and reserved validation." → "The number does not replace the diversity of
  motions: some components remain weakly constrained. Acquire rotations about non-parallel
  axes … and then examine the conditioning and a held-out validation."
- CV-HANDEYE-004: "Note $G_i$ the gripper→base transformation, … $X$ camera →gripper …
  Calculate $Y_i=G_iXC_i$ on several reserved poses: the fixed calibration target must give
  a coherent transformation calibration target→base." → "Let $G_i$ be the gripper→base
  transformation, … $X$ camera→gripper … Compute $Y_i=G_iXC_i$ on several held-out poses:
  the fixed calibration target must give a consistent calibration target→base
  transformation."
- CV-HANDEYE-005: "write the constant string" → "write the constant chain".

Protected objective lines that are mistranslated (not edited; proposed wording for a
learner-approved edit): CV-HANDEYE-001 "drift the relative movements" (*dériver*) →
"Derive the relative motions"; CV-HANDEYE-002 "respect the meaning of the poses API"
(*sens*: direction) → "Respect the direction of the poses in the API".

## Reference findings

Claims of revision 6 checked against their passages:

- Chain, $A$ and $B$, rotation and translation equations: confirmed (OpenCV `calib3d.hpp`
  L2322–L2346; Horaud and Dornaika §3).
- `calibrateHandEye` directions and minimum of two non-parallel motions: confirmed
  (L2210–L2233, L2352–L2353).
- "Some solvers estimate rotation and translation separately; others treat them together,
  for example with dual quaternions": confirmed (L2234–L2243 and the implementation).
- No scientific error found. Language defects: "grip a robot", "poses robot",
  "reserved residual", "string", "closing", "Question of work", "Reference Response",
  "**check**", "Example of Trap", "exit" for output.

New claims verified for revision 7 (main ones):

- Horaud and Dornaika: uses of hand–eye calibration and the $MY=M'YB$ formulation
  (abstract); $n_A=R_Xn_B$ (eq. 18), Tsai–Lenz form and rank deficiency, "at least two
  independent hand-eye motions (at least three positions)" (eq. 19), ill-conditioning of
  decoupled linear solutions (§3); closed-form and nonlinear methods (§5); simulation
  setup (1,000 trials, $\|t\|=157$ mm, 1–6% noise), separable methods "highly correlated",
  nonlinear "more accurate in all the situations", decoupling "introduces a bias", 4% versus
  6.5% translation error at 4 motions (§6).
- OpenCV 4.13.0 implementation: all pairs $i<j$; Tsai modified Rodrigues vectors, eqs. 12,
  14, 15; motion filter $0.3\le\|2\sin(\theta/2)\|\le1.7$ with its comment; failure path
  returning identity and zero; Park $M=\sum\beta\alpha^\top$, $R=(M^\top M)^{-1/2}M^\top$;
  Andreff Kronecker system; Daniilidis $6K\times8$ SVD with two quadratic constraints; at
  least 3 poses; matrix or Rodrigues rotations.

Implementation finding (FR-036): the Tsai filter's source comment states that the upper
bound corresponds to "greater than 120 degrees", whereas $\|2\sin(\theta/2)\|=1.7$ gives
$\theta=116.4°$ (recomputed). The note states 116° and records the comment.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 502 → 2,674.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Eye-in-hand and eye-to-hand unknowns; convention; inputs with `solvePnP` direction, rotation formats and minimum poses; output; pipeline role |
| Intuition | Absent | Developed | Paths through a fixed target; screw-motion reading; constructed inversion illustration; Mermaid data flow |
| Prerequisites | Developed (2 links) | Developed | Added CV-EPIPOLAIRE, CV-SVD, CV-BA, CV-MULTICALIB with the reason for each |
| Assumptions | Shallow | Developed | Rigidity, synchronization, error sources (Horaud and Dornaika §6); observability from eqs. 18–19; parallel axes, small rotations, moving target |
| Procedure | Absent | Developed | Eight-step procedure with the purpose of each step |
| Mathematics | Developed (chain only) | Developed | Eye-to-hand algebra; Tsai–Lenz, Park–Martin, Horaud–Dornaika, Andreff, Daniilidis formulations as implemented; closure residual; worked example B |
| Parameters | Shallow | Developed | Six-row table (method, pose count, angles and Tsai filter, axes, rotation format, PnP); four-step tuning approach |
| Properties | Absent | Developed | Exactness without noise, decoupling bias with simulation setup, correlated pairs, frame of the result, validity domain |
| Cost and implementation | Shallow | Developed | Pair counts and linear systems; OpenCV 4.13 contracts including the silent failure path and the comment discrepancy |
| Evaluation | Shallow | Developed | Metrics; baseline single-axis plan and controlled variation with three axes, expected effect and confound; limits of closure |
| Failure modes and diagnosis | Shallow | Developed | Seven-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Simultaneous, separable, robot–world–hand–eye and reprojection-based refinement; industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/57-calibration-hand-eye.py`](checks/57-calibration-hand-eye.py) (8 assertions):
exact closure and $AX=XB$ for six synthetic poses; broken closure when gripper→base is
inverted; pair counts 45 and 300; Tsai filter bounds 17.3° and 116.4°; singular values of
$R_A-I$ (0.087, 0.518, 1.414) and noise amplification (11.5×, 1.9×); zero singular value
along the rotation axis; leakage of a 0.1° rotation error into 1.7 mm of translation.

## Applied corrections

- [Reference](../../../vault/50-calibration-geometrie/references/57-calibration-hand-eye.md),
  revision 6 → 7: body rewritten and deepened as above; appendix language fixed
  identically to the cards ("Question of work" → "Working question", "Reference Response"
  → "Reference answer", "**check**" → "**Discriminating check**", "Example of Trap" →
  "Example of a trap", "Verification of matrices" → "Matrix checks", "Diagnostic by
  stacked system" → "Stacked-system diagnosis", "residual measurable closure" →
  "Measurable closure residual", "Explicit eye-to-hand channel" → "Explicit eye-to-hand
  chain", "Documentary reference" → "Source consulted"); sources split; closing provenance
  line replaced keeping the drafting date 2026-10-24. Front matter unchanged except
  `revision`; H1 and per-card headings kept.
- [Cards](../../../vault/50-calibration-geometrie/57-calibration-hand-eye.md): the four
  expected-answer fixes above; explanation and blocking-error fixes applied word for word
  in the reference appendices; CV-HANDEYE-003 received the paragraph "OpenCV's default
  solver discards small motions". Source lines now cite the 4.13.0 header and source with
  lines and Horaud and Dornaika §3. Questions, IDs, objectives, families, tags and target
  deck unchanged.

`rg` over `vault/` for "calibrateHandEye", "non-parallel" and "AX=XB": the only other file
is CV-MULTICALIB (revised in this pass, consistent).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-HANDEYE-01 | CV-HANDEYE | Explain why a separable hand–eye solver biases the translation and when to prefer a simultaneous or nonlinear method | Choice of solver is untested; decoupling bias is the main published comparison | Comparison; Properties and Alternatives | 1 card, 3 criteria (rotation error enters $R_Xt_B$; amplification by $1/(2\sin(\theta/2))$; simultaneous refinement) | [Horaud and Dornaika §3 and §6](https://arxiv.org/abs/2311.12655); [OpenCV 4.13.0 `calibration_handeye.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/calibration_handeye.cpp) |

## Sources

Scientific sources, opened at the passages listed:

- Horaud and Dornaika, Hand-Eye Calibration, [arXiv 2311.12655v2 PDF](https://arxiv.org/pdf/2311.12655v2)
  (author copy of IJRR 14(3), 1995; text extracted with `pdftotext`): abstract, §1 outline,
  §3, §6.
- Solà et al., [arXiv 1812.01537v9](https://arxiv.org/html/1812.01537v9#A4.SS1): retained
  from earlier passes, not re-read.

Implementation sources (official code at tag 4.13.0):

- [`calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp): L640–L653, L1031–L1032, L2210–L2358, L2361–L2505.
- [`calibration_handeye.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/src/calibration_handeye.cpp): L22–L66, L275–L453, L574–L722, L724–L820.

Failed accesses and limits:

- Daniilidis 1999 (University of Kiel PDF): connection refused by the proxy; Park and
  Martin 1994 and Tsai and Lenz 1989: no open copy found. These papers are not verifiable
  in this pass; their methods are stated through Horaud and Dornaika §3 and the OpenCV
  implementation, and the note says so.
- docs.opencv.org returned HTTP 403; Context7 was not available.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/57-calibration-hand-eye.py` | 8 checks passed |
| `git diff --check -- vault/50-calibration-geometrie/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/50-calibration-geometrie/57-calibration-hand-eye.md` | 5 cards, 357, 393, 425, 405 and 322 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 0 errors; 4 expected answers changed as recorded; front matter identical except `revision: 6` → `7` |
| Local link and anchor check over `vault/50-calibration-geometrie` | 164 local links, 0 errors |

No robot, solver or OpenCV call was executed; the baseline and variation are protocols.
Mermaid and tables were not rendered in Obsidian; AnkiDroid rendering is unverified. This
is agent self-review without independent validation. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-HANDEYE
revision 7, CV-HANDEYE-001 to 005, corrections above including the CV-HANDEYE-003
limitation, Agent Claude Code self-review, to republish with `paquet-anki`) and the
proposal register (P-CV-HANDEYE-01).
