# Learning contract for reference notes and flashcards

**Status**: proposal based on confirmed choices, to be tested in the pilot.

## Learner profile and language

Explanations target an engineer who already knows ML/DL foundations. They focus
on vision-specific models, assumptions, geometry, representations, parameters,
protocols, tradeoffs and failure modes. Revisit a general concept when it is
needed to explain a concrete problem.

All prose is in English, following the learner's request of 2026-10-31.
Retain original method names, acronyms and code identifiers. Define important
terms when first introduced and use them consistently. Historical paths,
metadata keys, tags and Anki schema names remain stable for compatibility.

## Reference note contract

Each validated reference note covers the entries below. Mark and justify an
inapplicable entry rather than filling it artificially.

| Section | Expected content |
| --- | --- |
| Problem | Need, task, inputs/outputs and role in a pipeline |
| Intuition | Mechanism, illustration or useful example |
| Prerequisites | Required knowledge and links to fill a gap |
| Assumptions | Applicability conditions, observability and degenerate cases |
| Procedure | Steps, purpose of each step and useful pseudocode |
| Mathematics | Explained equations, conventions, symbols and relevant dimensions/units |
| Parameters | Effects, interactions, sensitivity and a tuning approach |
| Properties | Invariances, approximations and limits of guarantees |
| Cost and implementation | Complexity or cost drivers; explained code and execution status |
| Evaluation | Protocol, metrics, relevant data and measurement limitations |
| Failure modes and diagnosis | Symptoms, possible causes, discriminating checks and conditional remedies |
| Alternatives and sources | Conditional comparisons, industrial applications, primary sources and related flashcards |

Reference notes may be long. Subsections, diagrams and links must make details
accessible without requiring a complete linear reading during every review.

Adapt this contract to the note type: problem, method, comparison,
metric/protocol or pipeline. Concepts need not all be presented as algorithms.
Required sections depend on the depth and competencies stated in the inventory;
justify any inapplicable section.

Where relevant, specify input/output coordinate frames, shapes and data types,
value ranges, color conventions, units and normalization. Trace resolution
changes, cropping, padding and coordinate transformations through to the output.
Make frame-rate assumptions and access to future frames explicit.

## Flashcard contract

A flashcard contains:

- A stable pedagogical ID and a parent reference note.
- One explicit recall objective and a question family.
- A contextualized question understandable without opening the reference note.
- A direct answer followed by useful explanations.
- Relevant validity conditions, limitations or counterexamples.
- Criteria for deciding whether the learner's answer is satisfactory.
- Sources and a link to further detail in the reference note.
- Its domain, family and the career tracks served by its reference note,
  exported as tags to track mastery by domain and career track in Anki.
- Authorship provenance: learner, agent or mixed.

Answers may contain paragraphs, equations, lists, diagrams and code. Length
follows explanatory needs. A comparison can constitute one coherent objective;
several independent questions within a card need redesign. No uniform number
of cards per method, word ceiling or review-time ceiling is imposed.

**Editorial choice confirmed on 2026-10-24**: the learner requests long cards
for every subject. Each answer develops the mechanism, a worked example or
reasoning sequence, and assumptions or limitations relevant to its objective.
`python3 scripts/learning_path.py` flags answers below 180 lexical words
(`re.findall(r'\w+', Reponse)`). This threshold identifies overly brief answers
in this project; it does not measure understanding or quality, impose a ceiling
or justify filler. The expected answer remains the grading rule even when the
full explanation is long.

Keep the direct answer visible at the beginning of the back. Organize details
by purpose: mechanism, reasoning, limitations and example. Do not reveal the
answer on the front through a title or source extract.

### Expected answer and further explanation

The back has three elements:

- **Expected answer**: the points required to satisfy the stated objective.
- **Further explanation**: useful details, derivations, examples and connections
  retained in the detailed answer without requiring recitation at every review.
- **Blocking errors**: misconceptions that invalidate the answer, such as
  confusing the task, coordinate frame or a decisive assumption.

An answer is satisfactory when it covers all required points without a blocking
error. Missing an optional detail is not a recall failure. If the expected
answer becomes too composite to grade unambiguously, add focused cards while
retaining a detailed synthesis card. The number of required points depends on
the objective; there is no uniform quota.

## Card families

These prompts illustrate the design; their educational answers are not yet written.

| Family | Objective | Example prompt |
| --- | --- | --- |
| Understanding | Explain a method and its assumptions | Describe the ORB pipeline and each component's role |
| Mathematical reasoning | Interpret or reconstruct a relationship | Explain reprojection error and its conventions |
| Algorithmic procedure | Follow steps and explain their purpose | Describe one robust-estimation iteration and its acceptance criterion |
| Comparison and decision | Choose under explicit constraints | Compare SIFT and ORB for matching under a compute budget |
| Diagnosis | Distinguish possible causes of failure | Investigate an unstable homography despite many matches |
| Practice | Understand a code extract or parameter setting | Relate the matcher to the descriptor representation |
| Evaluation | Interpret a measurement and its blind spots | Explain what a tracking score supports |
| System design | Propose a complete pipeline under constraints | Design inspection on a production line, from requirements to validation |

Cover relevant families without multiplying redundant questions. Cloze and
reversed cards are optional; add them only for an identified purpose and verify
them with the selected note template. English family labels map to the stable
internal tag values documented in the flashcard template.

## Practice and transfer

For a priority family, content must connect:

1. A simple reference case or baseline, with assumptions and expected result.
2. A controlled variation: noise, scale, occlusion, threshold, frame rate,
   initialization or another relevant factor.
3. A reasoned prediction of the effect of that variation.
4. An observation or measurement, followed by an explanation of any discrepancy.

An experiment may be small and targeted. It need not retrain every network or
require a separate exercise platform. An analytical case is acceptable when
explicitly identified as such.

Transfer-validation scenarios must differ from already worked examples. For
each of the six pilot families — matching, calibration/geometry, tracking,
detection, classical segmentation and 3D registration — prepare two scenarios
with reference answers: one method-selection case and one diagnosis in a
different context.

Grade suitability for the task, assumptions/conventions, justification,
a discriminating check and limits of the conclusion. Satisfy every applicable
criterion and justify any inapplicability.

Incidents from the learner's project work provide realistic cases. Anonymize
them, retain no confidential data and apply the same grading criteria.

## Assessing card usefulness

The learning pilot records a first attempt and delayed recall in another
session, on dates chosen by the learner. No optimal interval or memory
performance is assumed.

Select the sample before observing results. Cover every pilot family and each
card type produced; retain its composition and limitations. Do not remove
failed cards from the sample after testing.

For each tested card, record performance against its expected answer, review
time, ambiguity, perceived overload, answer-revealing cues and required
changes. An ungradable question, scientific error or essential information
revealed on the front prevents editorial validation until corrected.

Keep recall and transfer results separate: reciting a familiar explanation
does not by itself demonstrate diagnosis of a new scene.

Use measured times to estimate daily workload for the first production batch.
Do not impose a ceiling in advance. If the learner finds the workload excessive,
options include splitting overly composite cards, spacing comparison and
diagnosis cards further apart in a dedicated deck, or reducing cards per note.

## Equations, code and illustrations

- Introduce symbols near their first use.
- Define coordinate frames, transformation direction, dimensions and relevant units.
- Explain the purpose and conditions of equations.
- Include necessary derivations in the reasoning; detailed calculations may
  live in a linked explanation.
- Distinguish pseudocode, illustrative extracts and executed examples.
  Identify unexecuted examples instead of claiming verified results.
- For executable examples, state relevant dependencies/versions, inputs,
  expected results and useful reproducibility conditions.
- Use library calls to illuminate the algorithm; a call alone does not explain it.
- Give each visual a caption, explanatory purpose and source. Retain required
  reuse conditions and source files.

## Sources, review and corrections

Source algorithmic properties in relevant primary papers or reference works.
Tie implementation-specific claims to official documentation or code and its
version. Distinguish these levels: a library's output does not justify a
general property.

Record disagreements between sources with the variants and conditions being
compared. An unresolved central claim remains uncertain and prevents validation
of its reference note.

Each review records its date, author or reviewer, sources examined, limitations
and corrections. Label self-review explicitly; do not present it as independent
validation. A scientific correction identifies affected cards and checks them
again before publication of their new version.

### Authorship and ownership of learning

Each reference note and flashcard records whether the learner, an agent or both
authored it. Check an agent-authored central claim against the precise cited
passage; the presence of a citation alone is insufficient.

Reading generated content is not equivalent to producing it. The generation
effect ([Slamecka and Graf, 1978](https://doi.org/10.1037/0278-7393.4.6.592))
shows better retention for learner-generated information than for information
only read in simple verbal tasks. Its applicability to reformulated technical
flashcards is not established here. The division of authoring work remains an
open specification decision.

## Editorial review checklist

1. Are the problem and recall objective explicit?
2. Are assumptions, conventions and limitations verifiable?
3. Are explanations consistent, and does each source support the associated claim?
4. Do comparisons give conditional reasons?
5. Are the criteria sufficient to grade an answer?
6. Do cards provide complementary perspectives without unnecessary duplication?
7. Does content remain readable and complete after export?

Passing this review is separate from personal mastery and technical export success.

## Educational basis and limits of inference

[Roediger and Karpicke](https://psychnet.wustl.edu/memory/wp-content/uploads/2018/04/Roediger-Karpicke-2006_PsychSci.pdf)
study retrieval practice and delayed retention of prose passages. Their work
supports retrieval practice for detailed content without establishing an optimal
flashcard length or certifying professional expertise.

The combination of complete reference notes and cards with explicit objectives
is a design choice suited to the request. The pilot will assess its depth,
readability and ease of grading.
