# flashcards Review Grid

Detailed criteria for skill step 2. They take over the pedagogical contract (`specs/001-cv-knowledge-base/learning-design.md`) and the requirements FR-007 to FR-016, FR-031, FR-032 and FR-036 of the spec.

1. [Exactitude](#exactitude)
2. [Relevance to a senior profile](#relevance-to-a-senior-profile)
3. [Corrigibility](#corrigibility)
4. [Consistency](#consistency)
5. [Warning signals](#warning-signals)
6. [Severity](#severity)

## Exactitude

- Is each central statement supported by **the Cited Passage**, and not just by the document in general?
- Do the general properties (article) and implementation features (documentation or code, with version or commit) each have their source (FR-036)?
- Are guarantees, approximations, hypotheses and empirical results distinguished (FR-011)?
- Is a threshold, score or cost accompanied by its protocol, variant or hardware (FR-013)?
- Does each equation define its symbols, conventions, validity conditions and units (FR-007)?
- Is the data contract explicit: coordinate frame, origin of coordinates, normalization, effect of a resize, a crop or a padding (FR-031)?
- Is the status of the code clear: illustrative, or executed with its environment and result (FR-008, FR-009)?

To check:

- **Article**: open the quoted section and reread the exact sentence or equation. WebFetch does not read text from arXiv PDFs; use HTML version `https://ar5iv.labs.arxiv.org/html/<identifiant>`. The pseudocode is often an image: corroborate it with the official code. A contradiction between the article and an implementation, even on a boundary like `>` versus `≥`, is recorded with both contexts, not resolved in silence.
- **Cited section**: A true statement attributed to the wrong section remains "unsupported" as long as the reference is not corrected.
- **Code**: consult the file at the commit cited, with the line numbers.
- **Documentation**: consult the quoted version (e.g. OpenCV 4.13).
- **Numerical calculation**: do it again. `examples/pilot_math.py` already contains driver calculations; a new calculation is done in a temporary file outside the repository.

| Verdict | Sens | Suite |
| --- | --- | --- |
| Confirmed | The passage says the same thing, under the same conditions. | Rien |
| Imprecise | True under an unspoken condition, or overly strong formulation | Correct the nuance |
| False | The passage or calculation contradicts the assertion | Correct reference note and then flashcards |
| Not supported | Perhaps true, but the source quoted does not say so. | Finding the right passage or removing the affirmation |
| Not verifiable | Inaccessible or Paid Source | Say it in the report; do not confirm it |

## Relevance to a senior profile

The learner has five years of experience in CV, masters ML/DL and semantic segmentation, and seeks to fill its gaps: classic methods, matching, calibration and registration, tracking, detection.

- Does the flashcard involve a useful mechanism, reasoning, choice, diagnosis or evaluation in a project?
- Should a senior know how to respond without looking? A value that is consulted in the documentation has no place in a flashcard, unless it serves a reasoning (128 = 4×4×8 explains the structure of the descriptor SIFT) or prevents a frequent error (Hamming standard for ORB).
- Is the goal unique and does the family fit the question?
- Does another flashcard of the subject already test the same kernel?
- Does the flashcard recall a general DL course instead of the vision specificity (FR-001)?
- Is the industrial case plausible and presented as a reasoning of the project, and not as a published result?

## Corrigibility

- Is the question understood without opening the reference note?
- Does the front avoid the key term, title, or source extract that gives the answer?
- Is the **expected answer** a finite set of verifiable points? A detail of the **further explanation** does not have to be necessary to succeed.
- Are **Blocking Errors**s plausible countersenses (confusion of task, coordinate frame or hypothesis), and not absurdities that no one would commit?
- Does a comparison form a single coherent objective, rather than two juxtaposed questions?
- Is the length reasonable for a recall? There is no ceiling. Report a much longer answer than the others of the subject, or a kernel too composite to be noted without hesitation.

## Consistency

- Does the flashcard agree with the reference note, and the reference note with the other subjects? Look for the concepts shared by `grep` (IoU, residual, threshold, coordinate frame...).
- Are the notations, units, and variable names those of the reference note?
- Does the `famille::` tag match the family of the header line? The inventory reports discrepancies.
- Does the `Source` field contain the wikilink to the reference note and an HTTPS source with its section, line or commit?
- Are statements that depend on a version or date dated?
- Does the format respect the [Model of flashcard](format-carte.md)?

## Warning signals

| Signal | Why it is Suspect | What to check |
| --- | --- | --- |
| “guarantee”, “invariant”, “always”, “optimal” | A guarantee is rare in vision | Exact conditions in the source |
| Threshold presented as universal (0,5, 0,7, 0,8...) | A threshold depends on the dataset and the protocol | Origin of the threshold and validation |
| Encryption without protocol, variant or hardware | It is not comparable | Measurement conditions (FR-013) |
| Code presented as executed | The result may have been invented | Environment and real output |
| Front containing the key word of the answer | Revision becomes recognition | Redrafting the context |
| Two questions in a flashcard | Ambiguous notation | Split or unify the goal |
| Core that requires an optional detail | Unfair failures | Move the detail to further explanation |
| Source without section, line or commit | Unverifiable Affirmation | Specify the passage |
| Approximation presented as equality | Countersense learned | Distinguish between “Approximate” and “Equal” |
| coordinate frame, unit or origin of implicit coordinates | Calculation error in project | Data contract (FR-031) |
| Failure of a library presented as property of the method | Confusion method/implementation | Separate scientific source (FR-036) |
| Link to reference note missing or different from the file | flashcard orphaned or misarranged | Wikilink and domain |

## Severity

- **Bloquant**: scientific or numerical error; answer impossible to note unambiguously; answer revealed on the front; contradiction with the reference note.
- **Important**: Overly strong wording or missing nuance that misleads; source that does not support assertion; double purpose; duplicate; implicit data contract where it counts.
- **Minor**: style, inconsistent notation without consequence, too vague but exact reference, improved link.
