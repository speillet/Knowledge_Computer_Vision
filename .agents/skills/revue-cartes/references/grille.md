# Flashcard review grid

Detailed criteria for step 2 of `revue-cartes`, following the pedagogical
contract (`specs/001-cv-knowledge-base/learning-design.md`) and requirements
FR-007–FR-016, FR-031, FR-032 and FR-036.

1. [Accuracy](#accuracy)
2. [Relevance to senior engineering](#relevance-to-senior-engineering)
3. [Gradability](#gradability)
4. [Answer development](#answer-development)
5. [Clarity](#clarity)
6. [Consistency](#consistency)
7. [Warning signals](#warning-signals)
8. [Severity](#severity)

## Accuracy

- Does the cited passage support each central claim, rather than merely
  discussing the general subject?
- Do general properties (paper) and implementation details (documentation or
  code at a version or commit) each have their own source (FR-036)?
- Are guarantees, approximations, assumptions and empirical results distinguished (FR-011)?
- Does a threshold, score or cost specify its protocol, variant and relevant hardware (FR-013)?
- Does each equation define its symbols, conventions, validity conditions and units (FR-007)?
- Is the data contract explicit: coordinate frame, coordinate origin,
  normalization, resizing, cropping and padding (FR-031)?
- Is code marked as illustrative or executed with its environment and result (FR-008, FR-009)?

Verification:

- **Paper:** open the exact cited section, sentence or equation. If the available
  fetch tool cannot read a PDF, use an available HTML version or PDF extraction.
  Corroborate image-based pseudocode with official code. Record disagreements
  between paper and implementation with both contexts, even for `>` versus `≥`.
- **Cited section:** a true claim attributed to the wrong section remains
  unsupported until the citation is corrected.
- **Code:** read the cited file at its commit and line numbers.
- **Documentation:** consult the cited version, such as OpenCV 4.13.
- **Numerical calculation:** recalculate it. `examples/pilot_math.py` contains
  existing pilot calculations; use a temporary file for a new exploratory check.

| Verdict | Meaning | Next step |
| --- | --- | --- |
| Confirmed | The passage makes the same claim under the same conditions | None |
| Imprecise | Missing condition or overly strong wording | Correct the nuance |
| False | The source or calculation contradicts the claim | Correct the reference, then cards |
| Unsupported | The cited passage does not establish the claim | Find the right passage or remove the claim |
| Not verifiable | Source inaccessible or paywalled | Record the limitation; do not confirm |

## Relevance to senior engineering

The learner has five years of CV experience, knows ML/DL and semantic
segmentation, and prioritizes classical methods, matching, calibration,
registration, tracking and detection.

- Does the card train a useful mechanism, reasoning, choice, diagnosis or evaluation?
- Should a senior recall it without documentation? A lookup value needs a
  reasoning role (128 = 4×4×8 explains SIFT's descriptor) or a frequent-error
  prevention role (Hamming distance for ORB).
- Is there one objective and a matching family?
- Does another card already test the same expected answer?
- Does it teach a vision-specific concept rather than generic DL material (FR-001)?
- Is the industrial case plausible and labelled as project reasoning rather than a published result?

## Gradability

- Does the question stand alone without opening the reference?
- Does the front avoid revealing the answer through a keyword, title or source extract?
- Is the expected answer a finite set of verifiable points? Optional explanation
  details must not become mandatory recall criteria.
- Are blocking errors plausible misconceptions about task, coordinate frame
  or assumption, rather than absurd mistakes?
- Does a comparison serve one coherent objective?
- Does the answer meet the 180-lexical-word threshold checked by
  `scripts/learning_path.py` and the inventory? There is no upper limit;
  length alone does not establish quality.
- Can the expected answer still be graded without hesitation? If it contains
  too many objectives, propose a complementary card instead of making it vague.

## Answer development

A detailed explanation helps reconstruct the answer and check whether it applies:

- explain the mechanism instead of stating only a conclusion;
- follow an interpreted example or constructed calculation with assumptions and units;
- identify assumptions and limitations relevant to the objective;
- include a discriminating check for a decision or diagnosis.

Avoid paraphrasing the expected answer, repeating another card's diagnostic
paragraph, collecting unrelated facts or presenting a project calculation or
protocol as a published result.

## Clarity

Applies to every mode, at the learner's request of 2026-11-17: notions were
too complicated and intermediate steps were missing. A card is reviewed alone
on the phone, so it must be readable without the reference.

- Is every acronym and symbol used outside a formula defined in the card at its
  first use, or in a **Key terms** rubric placed second? Method, dataset and
  library names count as acronyms when their expansion helps (RANSAC: random
  sample consensus).
- Does every numerical result show formula → substitution → result, with each
  intermediate value (IDF1 $=2\,\mathrm{IDTP}/(2\,\mathrm{IDTP}+\mathrm{IDFP}+\mathrm{IDFN})=26/(26+3+3)$,
  not only $26/32$)?
- Does the reasoning avoid skipped steps? Each numbered step performs one
  operation, and a conclusion follows from the steps shown.
- Does the back follow intuition → steps → formula → limits: Expected answer,
  optional Key terms, Further explanation (plain-language mechanism), one step
  rubric, optional Limits, Blocking errors?
- Are there at most six bold rubrics? Advanced side derivations, alternative
  readings and historical remarks belong to the reference, not the card.
- Does the card rely on a notion that no earlier card or prerequisite teaches?
  Complete the reference's prerequisites and propose a bridge card.

`docs/revues/2026-11-17-clarity/checks/clarity_metrics.py` reports rubric
count and order and lists acronyms that a card does not appear to define. It is
a heuristic: read each flagged token.

## Consistency

- Do the card, reference and related topics agree? Use `rg` for shared concepts
  such as IoU, residuals, thresholds and coordinate frames.
- Are notation, units and variables consistent with the reference?
- Do the English header family and stable `famille::` tag correspond?
- Does `Source` link to the canonical reference and an HTTPS source with a section,
  line or commit?
- Are version-dependent claims dated?
- Does the format follow the [card template](format-carte.md)?

## Warning signals

| Signal | Why it needs attention | Check |
| --- | --- | --- |
| “Guaranteed”, “invariant”, “always”, “optimal” | Guarantees need conditions | Exact source conditions |
| Universal threshold (0.5, 0.7, 0.8, etc.) | Thresholds depend on data and protocol | Origin and validation |
| Quantitative claim without protocol, variant or hardware | Results may be incomparable | Measurement conditions (FR-013) |
| Code claimed as executed | A result needs evidence | Environment and actual output |
| Front includes the answer's key term | Recall becomes recognition | Question context |
| Two questions in one card | Ambiguous grading | Split or unify the objective |
| Expected answer requires an optional detail | Unfair failure | Move it to the explanation |
| Source lacks a section, line or commit | Claim is difficult to verify | Exact passage |
| Approximation presented as equality | Incorrect interpretation | Approximation conditions |
| Implicit coordinate frame, unit or origin | Calculation errors | Data contract (FR-031) |
| Library defect treated as method property | Method/implementation confusion | Separate scientific source (FR-036) |
| Missing or misplaced reference link | Orphaned card | Wikilink and domain |
| Heading, table, blockquote or stray `$` in a field | Package conversion fails | Inventory conversion anomaly |
| Paraphrase used to lengthen an answer | Review cost without information | Contribution of each paragraph |
| Unlabelled constructed calculation or proposed ablation | Confusion with measured results | Number origin and execution evidence |
| Result given without its calculation | The learner cannot rebuild it | Formula, substitution and each intermediate value |
| Acronym or symbol undefined in the card | The card does not stand alone | Definition at first use or in Key terms |
| More than six rubrics or an aside between steps | The main line of reasoning is lost | Move the aside to the reference |

## Severity

- **Blocking:** scientific or numerical error; ungradable answer; front reveals
  the answer; contradiction with the reference.
- **Important:** misleading omission or overly strong wording; unsupported claim;
  multiple objectives; duplicate; important implicit data contract; answer below
  the threshold or filled with irrelevant text.
- **Minor:** wording, harmless notation inconsistency, vague but accurate reference
  or an improvable link.
