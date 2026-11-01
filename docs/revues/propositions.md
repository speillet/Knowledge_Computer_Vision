# Card proposal register

This register tracks proposals from card reviews (`revue-cartes`) through the
learner's decision. A proposal remains pending until accepted, rejected or
deferred. See the [report conventions](../../.agents/skills/revue-cartes/references/rapports.md#proposal-register)
for statuses and formatting.

Baseline on 2026-10-30: the four priority proposals in the
[2026-10-20 overview](2026-10-20/00-bilan.md) had not received a decision.
Older reports contain other proposals. Each new pass brings its subject's
proposals into this register after checking whether they have already been
implemented (for example, DLT became CV-SVD-005 and CV-SVD-006).

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P-CV-FUSION-01 | CV-FUSION | Check NIS and biased residuals | Distinguish small residuals from consistent covariance | Evaluation | 1 card, 3 criteria | [Gamse et al., §§2.2.2 and 3.4](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/) | pending |
| P-CV-SE3-01 | CV-SE3 | Transport covariance with the adjoint | Avoid mixing uncertainty coordinate frames | Reasoning | 1 card, 3 criteria | [Solà et al., §II-H](https://arxiv.org/abs/1812.01537) | pending |
| P-CV-SEGMENTATION-01 | CV-SEGMENTATION | Calculate PQ for a small matching example | Make the panoptic metric operational | Evaluation | 1 card, TP/FP/FN and mean IoU | [Kirillov et al., §4](https://arxiv.org/abs/1801.00868) | pending |
| P-CV-METRIQUES-TEMPS-01 | CV-METRIQUES-TEMPS | Calculate an ID switch's effect on IDF1 | Move from a qualitative distinction to a worked example | Reasoning | 1 card on a short sequence | [Ristani et al., identity metrics](https://arxiv.org/abs/1609.01775) | pending |
