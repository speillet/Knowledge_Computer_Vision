# Review — NMS — suppressing redundant detections — 2026-11-14

## Overview

6 cards audited in `approfondir` mode; the canonical reference body was audited,
completed and language-corrected from revision 9 to revision 10. Highest severity per
card before correction: 0 blocking, 0 important, 6 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is a method note (priority V0, depth *approfondissement*). Its body already
held a procedure, the inclusion analysis, Soft-NMS and a short diagnosis table. This pass
added the missing contract sections (intuition, assumptions, mathematics, parameters,
properties, implementation contracts, evaluation with a controlled variation,
alternatives), replaced the three-column diagnosis table by the four-column format,
corrected one implementation claim and fixed the language. The headings
`## Multiple detections, classes and sizes of boxes` and
`### Inclusion and boxes of very different sizes`, targets of links from
[CV-DETECTEURS](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md),
are unchanged.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-NMS-001 | Pilot result (IoU $2/3$; keep $A,C$ at 0.5 and $A,B,C$ at 0.7): confirmed by executing `examples/pilot_math.py` on 2026-11-14 and by checks/81-nms.py. Non-transitive example ($7/13$, $0.25$) recomputed. French decimal commas in the expected answer ("$2/3>0,5$"); "**check**" for *Proposed check*; "gluton selection"; "Overlay"; "greediness algorithm"; "related components" for *connected components* | Algorithm: runs greedy NMS by hand | 2 expected criteria; 391 → 394 lexical words | Question uses "$0,9;0,8;0,7$" (see defective questions) | Minor | Notation fix of the expected answer; language fixes |
| CV-NMS-002 | Three thresholds compare different pairs: consistent with torchvision 0.29 `nms` (prediction versus prediction) and Soft-NMS §4 ($N_t$ versus evaluation $O_t$). Expected answer said "evaluation threshold IoU"; explanation "rating threshold", "from IoU 0,6 with a score of GT" (garbled), decimal commas | Understanding: separates confidence, redundancy and evaluation | 3 expected criteria; 399 → 400 lexical words | ID, question, tags unchanged | Minor | Word-order fix of the expected answer; meaning-restoring fixes in the explanation |
| CV-NMS-003 | Global versus per-class scope: confirmed (torchvision 0.29 `batched_nms`: "NMS will not be applied between elements of different categories"); torchvision Faster R-CNN treats every class prediction as a separate instance (`roi_heads.py` L700–L732). Expected answer "the score candidate $0{,}9$ … the class NMS"; "piece" for *part*; "exit rules" for *output rules* | Comparison: chooses the scope of suppression | 3 expected criteria; 397 → 396 lexical words | Question uses "$0{,}9$", "$0{,}8$", "$0{,}5$" | Minor | Language and notation fix of the expected answer; language fixes |
| CV-NMS-004 | Linear and Gaussian rescoring, NMS as special case: confirmed (Soft-NMS §4); re-search of the maximum after rescoring: confirmed (original code `cpu_soft_nms` L36–L42); score floor: confirmed (§5; code L96–L105). $0.8e^{-0.64/0.5}=0.222$ recomputed. "recoveries" for *overlaps*, "occlusionss", "Navigating once the old ranking", decimal commas | Reasoning: why re-ranking is required | 2 expected criteria; 402 → 406 lexical words | ID, question, tags unchanged | Minor | Expected answer: "beyond a overlap" → "beyond an overlap threshold"; language fixes |
| CV-NMS-005 | Diagnosis by before/after comparison and replay on frozen outputs: project protocol, consistent with Soft-NMS §1 and torchvision post-processing order (score, top-k, NMS). "trackss", "reserved set" for *held-out set*, "the one in the box that deleted it" | Diagnosis: separates a missing proposal from a suppression | 3 expected criteria; 418 → 421 lexical words | ID, question, tags unchanged | Minor | Expected answer: contractions expanded only; language fixes |
| CV-NMS-006 | Inclusion IoU $=\lvert B\rvert/\lvert A\rvert=0.04$ and suppression condition $\lvert B\rvert>\tau\lvert A\rvert$: recomputed. "This last report would be worth 1" for *ratio*; "does not slice between" for *decide*; "exit contract"; "greedy suite" for *sequence*; decimal commas | Reasoning: IoU versus containment | 2 expected criteria; 307 → 312 lexical words | Question uses "$0{,}9$", "$0{,}8$", "$0{,}5$" | Minor | Notation fix of the expected answer; language fixes |

Expected-answer changes (notation or meaning-restoring language fixes, no change of
criteria):

- CV-NMS-001: "IoU $2/3>0,5$" → "IoU $2/3>0.5$".
- CV-NMS-002: "the evaluation threshold IoU compares a prediction to an annotation" → "the
  evaluation IoU threshold compares a prediction with an annotation".
- CV-NMS-003: "The global NMS retains only the score candidate $0{,}9$; the class NMS retains
  both." → "Global NMS keeps only the candidate with score $0.9$; per-class NMS keeps both."
- CV-NMS-004: "instead of an immediate deletion beyond a overlap" → "instead of an immediate
  deletion beyond an overlap threshold" (the hard rule of Soft-NMS §4).
- CV-NMS-005: "If it didn't exist, changing NMS won't recreate it." → "If it did not exist,
  changing NMS will not recreate it."
- CV-NMS-006: "IoU $=0{,}04$" → "IoU $=0.04$".

Defective questions (not edited; questions are verbatim invariants). French decimal commas
make the numbers ambiguous in English, especially the list "$0,9;0,8;0,7$":

- CV-NMS-001, proposed wording: "Three continuous boxes $A=(0,0,10,10)$, $B=(2,0,12,10)$ and
  $C=(20,0,30,10)$ have scores 0.9, 0.8 and 0.7. Which boxes are retained by hard NMS that
  suppresses candidates with IoU greater than 0.5?"
- CV-NMS-003, proposed wording: "Two candidates from different classes have scores 0.9 and
  0.8 and IoU 0.8. With NMS threshold 0.5, what tradeoff distinguishes global suppression
  from per-class suppression?"
- CV-NMS-006, proposed wording: "Two continuous boxes of the same class, $A=(0,0,100,100)$
  and $B=(40,40,60,60)$, have scores 0.9 and 0.8. Does B being contained in A imply
  suppression by hard NMS at IoU threshold $>0.5$? Justify the answer."

The appendix "Working question" and "Situation" lines of the reference quote these
questions and were left identical to the cards.

## Reference findings

Claims of revision 9 checked against their passages:

- "Torchvision and the original code delete for a strictly superior IoU": **imprecise**.
  Torchvision 0.29 documents and implements `IoU > iou_threshold` (docs; CPU kernel L87–L89;
  CUDA `devIoU` L41–L53). The original Soft-NMS file contains both conventions:
  `cpu_soft_nms` in hard or linear mode tests `ov > Nt` (L82, L89), while the classic
  `cpu_nms` suppresses at `ovr >= thresh` (L159–L160). The paper itself writes "greater than"
  in §1 and $\ge N_t$ in §4. Corrected in the Procedure section. No card repeats the claim
  (`rg` over `vault/`); the 2026-10-20 report states it and is not rewritten.
- Torchvision `nms` was cited at the unversioned "stable" URL: replaced by the 0.29
  documentation and v0.29.2 code.
- "Soft-NMS never deletes" is false: confirmed (§5, "After each iteration, detections which
  fall below the threshold are discarded"; code L96–L105), now contrasted with the abstract's
  "no object is eliminated in this process".
- DETR without NMS: confirmed (abstract, §2.1); refined with §4.2: NMS helps the first decoder
  layer and slightly lowers AP at the last layers.
- Gaussian rescoring, inclusion analysis, three-threshold distinction: confirmed.
- Language: "driver variant" → "pilot variant", "Pseudocode **Pedagogy**, materialized by" →
  "Teaching pseudocode, implemented by", "Entries" → "Inputs", "preserved clues" → "indices of
  the kept boxes", "candidates who overwhelm it" → "candidates that overlap it beyond a
  threshold", "Connexions", "Competences: unroll" → "Competencies: run … by hand", "[code
  original]" → "[original code]", "Score Threshold / Threshold NMS / Evaluation threshold IoU"
  → "Score threshold / NMS threshold / Evaluation IoU threshold", "neither the same pair of
  objects nor the same role" → "compare different pairs of objects and play different roles",
  "A crowd is precisely putting this hypothesis in default" → "A crowd is precisely where this
  assumption fails", "check required" → "Required check", "Contract of the objects to be
  detected" → "Output contract: which objects must be detected", "hard NMS overall to 0{,}5"
  → "global hard NMS at 0.5", "Journal scores/classes/IoU and contact information contract" →
  "Log scores, classes, IoU and the coordinate contract", "Explicit separation, targeted
  testing without concluding a gap in the network" → "Explicit tie rule; targeted test … do
  not conclude to a network defect", "A AP" → "An AP", and all French decimal commas in prose
  and math.

New claims verified for revision 10 (main ones):

- Soft-NMS: per-class NMS and false positives (§3), about 6,000 anchors before RPN NMS (§3),
  NMS in edge, keypoint and face detection with box averaging (§2), rescoring functions and
  $O(N^2)$ complexity and greedy non-optimality (§4), default $N_t=0.3$, timings 0.01 s and
  0.005 s, 400 detections and the 0.1 AP cap effect (§5), VOC and COCO gains, herd animals,
  SSD/YOLOv2 +0.5% (§6.1), $\sigma=0.5$ and stability ranges (§6.2), larger $\sigma$ at high
  $O_t$ (§6.3).
- Hosang et al.: GreedyNMS as greedy clustering with a fixed threshold forcing a
  recall–precision tradeoff (abstract, §1).
- DETR: set prediction without NMS (abstract, §2.1); NMS after each decoder layer (§4.2).
- torchvision 0.29 / v0.29.2: `nms` and `batched_nms` documentation; stable sort and
  areas without "+1" in the CPU kernel; 64-box mask words in the CUDA kernel; `batched_nms`
  strategy switch at 4,000 (CPU) and 100,000 (GPU) tensor elements and the coordinate trick;
  Faster R-CNN defaults (RPN 1,000/1,000 at test, RPN NMS 0.7, box score 0.05, box NMS 0.5,
  100 detections) and post-processing order (clip, score, small boxes, `batched_nms`, top
  100).

Disagreements between sources and implementations, recorded in the note (FR-036):

| Aspect | Paper | Implementation |
| --- | --- | --- |
| Equality at the threshold | §1 "greater than"; §4 $\ge N_t$ | torchvision `>`; original `cpu_soft_nms` `>`; original `cpu_nms` `>=` |
| Pixel convention | Not specified | Original code: inclusive "+1"; torchvision and the pilot example: continuous |
| Ties on equal scores | Not specified | torchvision: no documented CPU/GPU guarantee, though v0.29.2 kernels both use a stable sort; pilot: input index |
| Per-class scope | Per class (§3) | `batched_nms`: per-class loop or coordinate trick, which requires non-negative coordinates |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 1,237 → 3,942 (the
scope record's figure of about 1,265 used another counting rule). The method note now
covers each contract section; the per-card appendices were language-corrected, not
extended.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Developed (short) | Developed | Tensor shapes and preconditions, output indices, role in two-stage detectors, evaluation and tracking, upstream and downstream contracts |
| Intuition | Absent | Developed | Peak-and-neighborhood picture linked to edges and corners; constructed side-by-side pedestrians; Mermaid diagram of the greedy loop with hard and soft branches |
| Prerequisites | Shallow (one link) | Developed | Links to CV-IOU-AP, CV-DETECTEURS, CV-SORT, CV-ASSOCIATION, CV-CANNY-HOUGH, CV-CORNERS |
| Assumptions | Shallow | Developed | Duplicates versus neighbors, score comparability, common frame, deterministic order; observability limit; degenerate cases |
| Procedure | Developed | Developed | Corrected equality conventions; purpose of each step; per-class implementation strategies |
| Mathematics | Shallow (inclusion, Gaussian rule) | Developed | IoU definition and invariances, "+1" convention, side-by-side suppression limit $d<w(1-\tau)/(1+\tau)$, linear and Gaussian rescoring, NMS as special case, coordinate-trick offset; worked examples A, B, C, E, H |
| Parameters | Shallow (three thresholds) | Developed | Seven-row table with source values (Soft-NMS, torchvision Faster R-CNN, original code); four-step tuning approach |
| Properties | Absent | Developed | Pairwise-IoU output guarantee and idempotence; order dependence; no optimality; invariances; scope; implementation determinism |
| Cost and implementation | Shallow | Developed | Worst-case IoU count, Soft-NMS timings, CUDA mask memory; torchvision 0.29 and original-code contracts; execution status |
| Evaluation | Shallow (one paragraph) | Developed | Protocol, published Soft-NMS and DETR results with setting, proposed hard-versus-Soft-NMS variation with a score-scale confound, measurement limits |
| Failure modes and diagnosis | Shallow (three-column table) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow (DETR line) | Developed | Conditional choices among per-class, global, Soft-NMS, learned NMS and set prediction, box averaging; applications labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by [`checks/81-nms.py`](checks/81-nms.py) (18
assertions): pilot example; "+1" convention (99/143) and the decision flip at 0.68;
side-by-side IoU $(w-d)/(w+d)$, limits $w/3$ and $0.176w$, 13.3 px and 7.06 px for 40 px
boxes; inclusion (0.04; a $75\times75$ box suppressed); Soft-NMS values (0.2224, 0.16,
$e^{-0.5}$); non-transitivity; pairwise-IoU guarantee and idempotence on 200 random
configurations; invariance under translation and axis scaling; the coordinate trick with
non-negative and negative coordinates (IoU 0 and 0.99); CUDA mask size (12.56 MB), strategy
switch (1,000 and 25,000 boxes) and worst-case IoU count (49,995,000).

## Applied corrections

- [Reference](../../../vault/80-detection-pose/references/81-nms.md), revision 9 → 10: body
  completed as above; equality-convention claim corrected; torchvision link versioned;
  appendices language-corrected identically to the cards ("Question of work" → "Working
  question", "Reference Response" → "Reference answer", "**check**" → "**Proposed check**"
  after the French "Contrôle proposé", "gluton selection" → "greedy selection", decimal
  commas, "built geometric counterexamples" → "geometric counterexamples constructed by the
  project", and the explanation fixes listed below); sources split into scientific and
  implementation sources; reference-style link definitions kept and extended; closing
  provenance line replaced. Front matter unchanged except `revision`; H1, the twelve
  `### CV-…` headings and both protected headings kept.
- [Cards](../../../vault/80-detection-pose/81-nms.md): expected answers changed as quoted
  above. Further explanations: "Overlay is used as an index" → "Overlap is used as an
  indication"; "threshold check redundancy, not directly semantic accuracy" → "the threshold
  controls redundancy, not semantic correctness"; "build three boxes … are worth" → "construct
  three boxes … equal"; "greediness algorithm … related components" → "greedy algorithm …
  connected components"; "rating threshold changes the location requirement" → "evaluation
  threshold changes the localization requirement"; "from IoU 0,6 with a score of GT … at an
  allowable score" → "an IoU of 0.6 with a ground-truth box … if its score is admissible";
  "piece(s)" → "part(s)"; "exit rules/contract" → "output rules/contract"; "Conflict of
  taxonomy built" → "Constructed taxonomy conflict"; "acts on recoveries" → "acts on
  overlaps"; "occlusionss" → "occlusions"; "Navigating once the old ranking" → "Traversing
  the old ranking once"; "Example of check" → "Example of a check"; "A disjointed box … passes
  before B" → "A disjoint box … comes before B"; "trackss" → "tracks"; "reserved set" →
  "held-out set"; "the one in the box that deleted it" → "the ID of the box that suppressed
  it"; "This last report would be worth 1 … does not slice between" → "This last ratio would
  equal 1 … does not decide between"; "greedy suite" → "greedy sequence". Blocking errors put
  in gerund form and clarified ("remove from the box" → "remove a box"; "confuse proposal
  error and deletion" → "confusing a missing proposal with a suppression"). Source lines:
  "Consult the" → "consulted on", "built" → "constructed by the project". Questions, IDs,
  objectives, families, tags and target deck unchanged.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by this
subject run). Earlier reports registered no NMS proposal.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-NMS-01 | CV-NMS | For two equal boxes side by side, derive the center distance below which hard NMS at $\tau$ suppresses one, and apply it to a crowd of known object width | The crowd failure is stated but never quantified by a card | Reasoning; Mathematics, worked example C | 1 card, 3 criteria (IoU $(w-d)/(w+d)$; limit $w(1-\tau)/(1+\tau)$; numeric application) | [Soft-NMS §1 and §4](https://arxiv.org/abs/1704.04503); IoU definition [GIoU §3](https://arxiv.org/html/1902.09630v2) |
| P-CV-NMS-02 | CV-NMS | Design a boundary test that fixes an NMS implementation's equality, pixel and tie conventions before comparing two libraries | Implementation conventions ($>$ versus $\ge$, "+1", ties) are untested; the practice family is absent | Practice; Procedure and Implementation contracts | 1 card, 3 criteria | [torchvision 0.29 `nms`](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.nms.html); [original Soft-NMS code](https://github.com/bharatsingh430/soft-nms/blob/b8e69bdf8df2ad53025c9d198ded909b50471d4f/lib/nms/cpu_nms.pyx) |

## Sources

Scientific sources, opened at the passages listed:

- Bodla et al., [Soft-NMS, arXiv HTML v2](https://arxiv.org/html/1704.04503v2) (text extracted locally): abstract, §1, §2, §3, §4, §5, §6.1–§6.3.
- Hosang, Benenson and Schiele, [Learning non-maximum suppression, arXiv 1705.02950v2](https://arxiv.org/abs/1705.02950) (PDF, `pdftotext`): abstract and §1 opening.
- Carion et al., [DETR, arXiv 2005.12872v3](https://arxiv.org/abs/2005.12872) (PDF, `pdftotext`): abstract, §2.1, §4.2.
- GIoU §3 eq. 1: not re-opened in this pass (verified in earlier passes; used only for the IoU definition).

Implementation sources (read; only the repository example was executed):

- [torchvision 0.29 `nms`](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.nms.html) and [`batched_nms`](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html) documentation.
- [torchvision v0.29.2](https://github.com/pytorch/vision/tree/v0.29.2): `torchvision/ops/boxes.py` L57–L126; `csrc/ops/cpu/nms_kernel.cpp` L38–L89; `csrc/ops/cuda/nms_kernel.cu` L25–L100, L196–L202; `models/detection/faster_rcnn.py` L176–L200; `models/detection/roi_heads.py` L700–L732.
- [Original Soft-NMS code at `b8e69bd`](https://github.com/bharatsingh430/soft-nms/blob/b8e69bdf8df2ad53025c9d198ded909b50471d4f/lib/nms/cpu_nms.pyx): L17–L110, L113–L164.
- `examples/pilot_math.py` (repository), executed with `python3 examples/pilot_math.py` on 2026-11-14: IoU 0.6667, kept `[0, 2]` at 0.5 and `[0, 1, 2]` at 0.7.

Failed accesses and limits:

- Context7 was not available in this session (see the scope record); torchvision's versioned
  documentation and tagged source replaced it.
- Matrix NMS, DIoU-NMS and weighted box fusion were not opened and are not mentioned.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/81-nms.py` | 18 checks passed |
| `git diff --check -- vault/80-detection-pose/81-nms.md vault/80-detection-pose/references/81-nms.md` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/80-detection-pose/81-nms.md` | 6 cards, 312 to 421 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; front matter identical except `revision: 9` → `10`; H1, per-card headings and the two linked headings unchanged; `$$` balanced; table column counts consistent; reference-style link labels all defined and used |

No detector or torchvision call was executed; the proposed baseline and variation are
protocols, not results. The Mermaid diagram and tables were not rendered in Obsidian, and
AnkiDroid rendering of the corrected cards is unverified. This is agent self-review, without
independent scientific validation or measurement of learner proficiency. Export status:
**to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator: the
correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-NMS revision 10,
CV-NMS-001 to -006, corrections listed above, Agent Claude Code self-review, to republish
with `paquet-anki`) and the proposal register (P-CV-NMS-01, P-CV-NMS-02).
