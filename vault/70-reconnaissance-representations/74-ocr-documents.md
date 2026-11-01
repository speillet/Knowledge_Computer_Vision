# Flashcards — OCR and document understanding

reference note: [[70-reconnaissance-representations/references/74-ocr-documents|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-OCR-001

Objective: Separate recognition and structure. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-OCR-001
Question: Why is a good CER insufficient to validate invoice extraction?
Reponse: **Expected answer**: CER measures the editing of characters according to a protocol; order of reading, association of fields and accuracy of amounts are other outputs.

**Further explanation**: Evaluate each of the deliverables useful to the product with reference and standardization rules.

**Example of Business Difference**: An invoice can contain almost all the correct characters while associating the amount of a row with the wrong reference, or by reversing two columns. A small error on a critical figure can also count little in the overall CER of a long document.

**Proposed contract**: set separately transcription, reading order, boxes, keys and expected values, with a reference suitable for each. Keep normalization rules for spaces, cases, and numbers in the assessment. Measure accuracy of critical fields, fully correct documents, and human verification rate at the selected threshold. A linguistically plausible generation must still match the source image. The validation of the product therefore concerns the information actually used by the downstream process; it is not deduced from the single character recognition score or the legible aspect of the reconstructed text.

**Example of weighting**: A document of 2 000 characters with a substitution on the total amount may have a CER of 0,05% and remain unusable for accounting processing. A field metric can compare the numerical value after a predicted normalization of separators, currencies, and decimals; a document metric can require all the correct critical fields. Also keep the raw string and image region allows to distinguish recognition error, field association and normalization. Arithmetic checks between lines, taxes and totals provide additional consistency, without proving that a plausible value actually corresponds to that printed.

**Blocking errors**: Confounds near global text and correctly structured invoice.
Source: [[70-reconnaissance-representations/references/74-ocr-documents|Full reference]]; [OCR-D, Text Evaluation, CER and WER, Viewed on 2026-10-20](https://ocr-d.de/en/spec/ocrd_eval.html); invoice criteria proposed by the project.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-OCR-001 provenance::agent pole::E
END

## CV-OCR-002

Objective: Interpreting CER. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-OCR-002
Question: Can CER exceed 100%, and under which conditions?
Reponse: **Expected answer**: Yes: Inserts can exceed the number of reference characters in (S+D+I)/N.

**Further explanation**: Specify normalization, case N=0 and aggregation; this is not a simple proportion of false characters in the prediction.

**Analytical example**: A reference contains five characters; if the system produces these five characters followed by ten additional characters, an editing convention that has ten insertions gives a CER of $10/5=2$, or 200%. The denominator describes the reference length, not the output length.

**Interpretation of the Protocol**: A normalized variant can use another denominator and be bounded; it then measures a different quantity. Announce the convention before comparing two tools. Also define the case of an empty reference, Unicode normalization and inter-page aggregation. An average per page does not give documents the same weight as a ratio on all characters. These choices can change the apparent ranking without a change in the recognizer. The score remains an edit measure, and does not validate the reading order or the correct extraction of the amounts.

**Calculation of distance**: Dynamic programming uses $D_{i,j}=\min(D_{i-1,j}+1,D_{i,j-1}+1,D_{i-1,j-1}+\mathbf1[a_i\ne b_j])$, with $D_{i,0}=i$ and $D_{0,j}=j$ edges. It looks for the minimum editing cost, not a simple count of different fixed-position characters. To aggregate several pages, the ratio $\sum_k(S_k+D_k+I_k)/\sum_kN_k$ weights by reference length, while the average of CER per page weights the pages as well. Both answer different questions. Defining Unicode units and processing empty references before this calculation avoids incompatible score comparisons.

**Blocking errors**: Rotate arbitrarily to 1 without announcing another protocol.
Source: [[70-reconnaissance-representations/references/74-ocr-documents|Full reference]]; [OCR-D, Text Evaluation, CER and WER, Viewed on 2026-10-20](https://ocr-d.de/en/spec/ocrd_eval.html); classical convention with denominator N.
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-OCR-002 provenance::agent pole::E
END

## CV-OCR-003

Objective: locate a reading order defect. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-OCR-003
Question: Individual lines are recognized correctly, but the output interleaves columns. Which component should be examined?
Reponse: **Expected answer**: Detection/layout and assembly of the reading order, before the character recognizer.

**Further explanation**: Compare boxes and structure to the annotated document; a new recognition language does not correct this contract.

**Breakdown of the pipeline**: Boxes or regions determine which lines are sent for recognition; their structure then determines how texts are assembled. A recognizer can be exact on each crop and the final document can be fake because these crops are traversed in the wrong order.

**Test construit**: Retain line transcripts and replace only the order or assembly with a reference annotation. If the document becomes correct again, the diagnosis is about layout or reading rather than characters. Test columns, tables, inserts and inclined lines with the same normalization rules. Check the links between fields and values, because a plausible order is not always enough to extract the business structure. This approach locates responsibility before choosing additional annotations or training for a component that does not address the cause.

**Model of order**: represent regions as nodes and relationships "must be read before" as edges allows to explain a partial order. Topological sorting produces a compatible order if these constraints are cycle-free; column rules, arrays, and inserts determine edges, not the confidence of the recognizer. A simple global sorting by height can intertwine two well-detected columns. To locate the fault, successively compare reference regions, reference transcriptions and reference order by replacing only one output at a time. This ablation identifies what each component brings to the final document error.

**Blocking errors**: Retrain only the recognizer without checking the regions.
Source: [[70-reconnaissance-representations/references/74-ocr-documents|Full reference]]; [OCR-D, Text Evaluation, CER and WER, Viewed on 2026-10-20](https://ocr-d.de/en/spec/ocrd_eval.html); assembly diagnosis deduced by the project.
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-OCR-003 provenance::agent pole::E
END
