# Review — Semantic, instance and panoptic segmentation — 2026-11-16

## Overview

Mode: `ajouter` for the accepted proposal P-CV-SEGMENTATION-01. One card added,
CV-SEGMENTATION-005; the four existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/93-semantique-instances-panoptique.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 8 → 9.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-SEGMENTATION-005 | Matching only at IoU strictly greater than 0.5, unique by Theorem 1 so that greedy and optimal matching agree (§4.1); PQ, SQ, RQ, eqs. 1–2, RQ as the F1 score, per-class computation then class average, equal weight of segments, SQ and RQ not independent (§4.2); void rule (prediction's void pixels removed before matching; unmatched predictions over the threshold not FPs) and group rule (§4.2); class averages with "PQ=SQ×RQ per class" (§6, Table 1 caption): confirmed in the arXiv v3 text. panopticapi at commit 7bb4655: same-category and non-crowd pairs only (L127–L130), union minus the prediction's void pixels (L132), `iou > 0.5` with no assignment step (L134–L138), crowd ground truth not an FN (L141–L149), unmatched prediction ignored when void plus same-category crowd pixels exceed half its area (L151–L163), per-category sums over all images, empty categories skipped, PQ, SQ and RQ averaged separately (L49–L73, L221–L224): confirmed. Pixel counts, the variants and the 2-pixel tie: project constructions, recomputed by the check script | Evaluation: computing PQ by hand exposes the conventions that change the number (strict threshold, void, category averaging) and what SQ and RQ diagnose. Distinct from CV-SEGMENTATION-001 (output contracts) and CV-SEGMENTATION-004 (limits of Dice); it does not train the aggregation level (P-CV-SEGMENTATION-02) or the instance-to-panoptic conversion (P-CV-SEGMENTATION-03) | 3 expected criteria (matching with TP, FP and FN; SQ, RQ and PQ for car, road and the category mean; what the decomposition says about the car errors); 631 lexical words | Notation of eq. 2 and worked example A of the reference; worked example A extended with the card's pixel-count version; tags `cv::d09`, `pole::A pole::E` match the reference | Evaluation |

The question gives the void pixels of $p_2$ and states that there is no crowd region,
because the computation needs them; it states neither the matching threshold, nor the
void rule, nor how categories are combined. One image is declared to be the whole
evaluation set, so per-image and dataset-level accumulation coincide and the card does
not encroach on P-CV-SEGMENTATION-02; the predictions are already a panoptic partition,
so no overlap resolution (P-CV-SEGMENTATION-03) is involved.

The card is longer than its siblings (631 against 279 to 382 lexical words) because it
carries the computation, the evaluator's void, crowd and averaging conventions, and the
non-independence of SQ and RQ, each with a recomputed number.

## Reference findings

Claims of revision 8 re-checked against §4.1–§4.2: strict IoU > 0.5, Theorem 1 and its
inequality, eqs. 1–2, RQ = F1, per-class averaging, equal weight of segments regardless
of area: confirmed. Worked example A (SQ 0.75, RQ 0.571, PQ 0.429, class mean 0.689):
confirmed; the 2026-11-14 script still passes.

- **Imprecise (minor).** The degenerate-case sentence said that unmatched predictions
  "mostly inside" a group region are not false positives. The paper restricts this to a
  group "of the same class" over the matching threshold (§4.2, "Group labels"), and
  panopticapi uses only the crowd segment of the prediction's category (L158–L159).
- **Incomplete (minor).** "Void pixels of the ground truth are removed from predicted
  segments before matching" gave only the first of the two void rules; the second,
  unmatched predictions with a void fraction over the matching threshold are not false
  positives (§4.2, "Void labels"), was missing.
- **Absent.** The note had no implementation source for PQ. panopticapi differs from the
  paper's wording in one respect: the paper states the void and group rules separately,
  while the code adds the two fractions before comparing with 0.5 (L155–L161). A 40-pixel
  prediction with 15 void and 10 same-category crowd pixels is therefore ignored by the
  code (25/40 > 0.5) although neither fraction alone exceeds 0.5 (check 11). The code
  keeps one crowd segment per category and image (the dictionary at L147 is overwritten);
  whether the COCO panoptic annotations ever hold two crowd segments of one category in
  an image was not checked. The comment at L140 reads "count false positives" above the
  loop that counts false negatives; it has no effect.
- **Absent.** Why the inequality is strict: a 2-pixel segment split into two 1-pixel
  predictions gives two pairs at exactly 0.5, so "≥ 0.5" loses uniqueness (project
  derivation from the proof of Theorem 1, check 12). The proof also holds for the
  void-adjusted IoU of the evaluator, since void pixels are outside every ground-truth
  segment (project derivation; randomized check 13).

## Applied corrections

- `vault/90-segmentation/93-semantique-instances-panoptique.md`: CV-SEGMENTATION-005
  appended. The four existing blocks, the header and the deck line are byte-identical to
  the pre-edit copy (the edited file equals that copy followed by the new block).
- `vault/90-segmentation/references/93-semantique-instances-panoptique.md`, revision
  8 → 9: degenerate-case crowd sentence restricted to the prediction's own class; the
  Panoptic quality section given the second void rule, the non-independence of SQ and RQ
  (§4.2), the strict-threshold tie and a paragraph of evaluator conventions with
  panopticapi line numbers; worked example A extended with the card's pixel-count version
  and its variants; the "Matching is unique" property qualified as strictly above 0.5;
  Kirillov §6 Table 1 caption and the panopticapi file added to the sources;
  CV-SEGMENTATION-005 listed under the related flashcards, with the location of both
  check scripts; closing provenance line extended. `statut: redige` and `provenance:
  agent` unchanged.

No existing card repeats the corrected claims (search for crowd, group region, void
pixel and `iscrowd` over `vault/`: the other matches concern the COCO detection
evaluator of CV-IOU-AP and CV-DETECTEURS).

## Proposals

P-CV-SEGMENTATION-01: accepted by the learner on 2026-11-09, completed as
CV-SEGMENTATION-005. The registered cost ("TP/FP/FN and mean IoU") is met with SQ, the
mean IoU of matched segments, and the card states that this mean alone is not PQ.
P-CV-SEGMENTATION-02 and P-CV-SEGMENTATION-03 remain pending and are not affected.

## Sources

Scientific sources:

- Kirillov, He, Girshick, Rother and Dollár, "Panoptic Segmentation",
  [arXiv 1801.00868v3](https://arxiv.org/abs/1801.00868) (10 Apr 2019): PDF downloaded
  from arxiv.org and its text extracted with pypdf 5.1.0. Passages read: §3 (format,
  void label, stuff and things, no overlap by construction), §4 opening, §4.1 with
  Theorem 1 and its proof, §4.2 with eqs. 1–2, "Void labels" and "Group labels", §4.3,
  §6 Table 1 and its caption, the "IoU threshold" and "SQ vs. RQ balance" paragraphs.

Implementation sources (Context7 is unavailable in this session):

- cocodataset/panopticapi `panopticapi/evaluation.py` at commit
  7bb4655548f98f3fedc07bf37e9040a992b054b0 (head of the default branch, 2021-06-18; the
  last commit touching this file is 5298a2c, 2019-08-05), GitHub raw, read in full
  (L1–L258); cited lines L49–L73, L78–L163, L178–L180, L221–L224.

No access failed. `pdftotext` is not installed in this environment, so the PDF text was
extracted with pypdf instead; the paper and the code were downloaded and read directly
rather than through a summarizing fetch.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 -I docs/revues/2026-11-09-four-proposals/checks/93-semantique-instances-panoptique.py` | 13 checks passed, including 3000 randomized instances |
| `python3 -I docs/revues/2026-11-14-reference-depth/checks/93-semantique-instances-panoptique.py` | 14 checks passed (worked examples A–C unchanged) |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 297 cards (shared tree, other agents' cards included) |
| `python3 scripts/learning_path.py` | OK: 60 references, 297 cards, 0 errors |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/90-segmentation/93-semantique-instances-panoptique.md` | 5 cards, no anomaly; CV-SEGMENTATION-005 631 lexical words |
| `git diff --check -- vault/90-segmentation/` | No whitespace error |

The check script re-implements the matching, FN, FP and averaging steps of panopticapi
with exact fractions on a joint histogram of segment ids that realizes the card's pixel
counts; panopticapi itself was not executed, and no PNG or JSON file was built. The
randomized check uses 1-D label sequences; it tests the uniqueness property, it does not
prove it. Agent self-review only, without independent scientific validation; the
Obsidian rendering and the AnkiDroid rendering of the card are not verified. Export
status: to republish with `paquet-anki`. The proposal register, the progress log, the
generated catalogue and the current-state counts are left to the coordinator.

For the correction log (to be entered by the coordinator): 2026-11-16, CV-SEGMENTATION
revision 9, CV-SEGMENTATION-005 added (P-CV-SEGMENTATION-01, accepted 2026-11-09).
Reference corrections: "unmatched predictions mostly inside [a group region] are not
false positives" → only those with more than half of their pixels in a group region of
their own class (Kirillov et al. §4.2, "Group labels"; panopticapi `evaluation.py` at
7bb4655 L155–L162); the void sentence completed with the second rule, unmatched
predictions with a void fraction over the matching threshold are not false positives
(§4.2, "Void labels"). Additions: panopticapi conventions (summed void and crowd fraction,
separately averaged PQ, SQ and RQ), the strict-threshold tie and the card's worked
example. No existing card repeats the corrected claims. Agent Claude Code, self-review;
checks as above; export status: to republish with `paquet-anki`.
