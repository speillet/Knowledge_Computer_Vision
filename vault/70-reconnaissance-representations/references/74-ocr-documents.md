---
id: CV-OCR
type: comparaison
domaine: d07
poles: [E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 5
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# OCR and document understanding

## Problem, data and assumptions

Extract text, read order and structure according to separate outputs. Entries: pages/images with resolution and language; outputs: characters, words, boxes, fields or structure. An exact text in the wrong order may be unusable.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Detect regions/lines then recognize: CRNN/CTC is a sequential reference, TrOCR a transformative approach. LayoutLM combines text and layout; Donut studies extraction without a separate OCR engine. These names do not refer to the same interface.

## Mathematics, conventions and units

The classic CER is $(S+D+I)/N$ for $N>0$ reference characters, with substitutions, deletions, and edit inserts. The classic WER applies the same logic to words. OCR-D also describes a standardized variant $(S+D+I)/(S+D+I+C)$, where $C$ counts the correct characters, and uses this bounded variant in its benchmarks; do not assimilate their scores to the classic convention adopted here. Unicode normalization, case, spaces and segmentation change the protocol; the score can exceed 1 if the insertions are numerous.

## Parameters and properties

DPI, rotation, languages, cutting, lexicon, tokenization and reading order. Distinguish line detection error, recognition, assembly and extraction of a field.

## Cost and implementation

Cost of rendering, detection, crops and generation; large documents require pagination and limits. No OCR performed and no linguistic performance claimed.

## Evaluation and controlled variation

Baseline: clean page and reference text, then blur/rotate controlled. Measure CER/WER and field/structure accuracy; an overall character score can hide a false critical amount.

## Failure modes and diagnosis

Readable text but mixed columns: check detection and read order. Numerical errors: analyze business cost and resolution data, without claiming that a fluid generation is correct.

## Alternatives and applications

Specialized OCR or multimodal pipeline depending on output, data and constraints; retain visual evidence and protocol of essential fields.

## Guided reasoning and proposed checks

These constructed cases develop OCR chain, standardization and metric adapted to the document. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-OCR-001

**Question of work**: Why is a good CER insufficient to validate invoice extraction?

**Reference Response**: CER measures the editing of characters according to a protocol; order of reading, association of fields and accuracy of amounts are other outputs.

**Example of Business Difference**: An invoice can contain almost all the correct characters while associating the amount of a row with the wrong reference, or by reversing two columns. A small error on a critical figure can also count little in the overall CER of a long document.

**Proposed contract**: set separately transcription, reading order, boxes, keys and expected values, with a reference suitable for each. Keep normalization rules for spaces, cases, and numbers in the assessment. Measure accuracy of critical fields, fully correct documents, and human verification rate at the selected threshold. A linguistically plausible generation must still match the source image. The validation of the product therefore concerns the information actually used by the downstream process; it is not deduced from the single character recognition score or the legible aspect of the reconstructed text.

### Case linked to CV-OCR-003

**Question of work**: Individual lines are recognized correctly, but the output interleaves columns. Which component should be examined?

**Reference Response**: Detection/layout and assembly of the reading order, before the character recognizer.

**Breakdown of the pipeline**: Boxes or regions determine which lines are sent for recognition; their structure then determines how texts are assembled. A recognizer can be exact on each crop and the final document can be fake because these crops are traversed in the wrong order.

**Test construit**: Retain line transcripts and replace only the order or assembly with a reference annotation. If the document becomes correct again, the diagnosis is about layout or reading rather than characters. Test columns, tables, inserts and inclined lines with the same normalization rules. Check the links between fields and values, because a plausible order is not always enough to extract the business structure. This approach locates responsibility before choosing additional annotations or training for a component that does not address the cause.

**Documentary reference for this pass**: [OCR-D, Evaluation](https://ocr-d.de/en/spec/ocrd_eval.html), definitions, alignment and normalization of errors. The other developments are in the [flashcards](../74-ocr-documents.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-OCR-001

**Situation**: Why is a good CER insufficient to validate invoice extraction?

**Example of weighting**: A document of 2 000 characters with a substitution on the total amount may have a CER of 0,05% and remain unusable for accounting processing. A field metric can compare the numerical value after a predicted normalization of separators, currencies, and decimals; a document metric can require all the correct critical fields. Also keep the raw string and image region allows to distinguish recognition error, field association and normalization. Arithmetic checks between lines, taxes and totals provide additional consistency, without proving that a plausible value actually corresponds to that printed.

### CV-OCR-002

**Situation**: Can CER exceed 100%, and under which conditions?

**Calculation of distance**: Dynamic programming uses $D_{i,j}=\min(D_{i-1,j}+1,D_{i,j-1}+1,D_{i-1,j-1}+\mathbf1[a_i\ne b_j])$, with $D_{i,0}=i$ and $D_{0,j}=j$ edges. It looks for the minimum editing cost, not a simple count of different fixed-position characters. To aggregate several pages, the ratio $\sum_k(S_k+D_k+I_k)/\sum_kN_k$ weights by reference length, while the average of CER per page weights the pages as well. Both answer different questions. Defining Unicode units and processing empty references before this calculation avoids incompatible score comparisons.

### CV-OCR-003

**Situation**: Individual lines are recognized correctly, but the output interleaves columns. Which component should be examined?

**Model of order**: represent regions as nodes and relationships "must be read before" as edges allows to explain a partial order. Topological sorting produces a compatible order if these constraints are cycle-free; column rules, arrays, and inserts determine edges, not the confidence of the recognizer. A simple global sorting by height can intertwine two well-detected columns. To locate the fault, successively compare reference regions, reference transcriptions and reference order by replacing only one output at a time. This ablation identifies what each component brings to the final document error.

**Passages consulted for these developments**: [OCR-D](https://ocr-d.de/en/spec/ocrd_eval.html), Text Evaluation, distance from Levenshtein, CER/WER; examples and built order model.

## Sources and flashcards

- [CRNN, method](https://arxiv.org/abs/1507.05717).
- [TrOCR](https://arxiv.org/abs/2109.10282).
- [LayoutLM](https://arxiv.org/abs/1912.13318).
- [Donut](https://arxiv.org/abs/2111.15664).
- [OCR-D, evaluation](https://ocr-d.de/en/spec/ocrd_eval.html).
- [Related flashcards](../74-ocr-documents.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
