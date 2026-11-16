# Review — Kalman, EKF, UKF and ESKF for sensor fusion — 2026-11-16

## Overview

Mode: `ajouter` for the accepted proposal P-CV-FUSION-01. One card added,
CV-FUSION-007; the six existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/13-kalman-ekf-eskf.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 10 → 11.

The card and its reference section were drafted on 2026-11-09 from `main` at `76fda5a`
and left uncommitted. Meanwhile #27 deepened the reference to revision 10. On
2026-11-16 the draft was reapplied on `main` at `6cef833`: the draft's own revision bump
and its stale source list were dropped in favour of the deepened reference, then the
section was verified again, aligned and completed as below.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-FUSION-007 | Gamse et al. list zero mean, whiteness, Gaussianity and the predicted covariance as properties of the innovation sequence, define the NIS (eq. 7) and test $H_0:\mathbb E(d_k)=0$ per epoch against $\chi^2_{m,1-\alpha}$, $m$ being the number of observations at the epoch (eq. 8–10): confirmed in §2.2.2. §3.4.2 applies $m=3$, $\alpha=0.05$, threshold 7.815, and checks normality with probability plots and reported means and standard deviations, without a whiteness test: confirmed. Whitening, the moment identity $\mathbb E\|e\|^2=\operatorname{tr}\operatorname{Cov}(e)+\|\mathbb E e\|^2$, the two traces, the periodicity of repeated B and the gate calculation (accepted mean 1.68 for a correct filter; 2.00 with 11.8% rejections when the true covariance is $1.4\,S$): project derivations, recomputed by the check script | Evaluation: judges competing innovation sequences instead of a single NIS value; trains the bias/variance trade-off hidden in a mean NIS and the selection bias of a gate. Distinct from CV-FUSION-002 (definition and gate of the NIS) | 3 expected criteria (mean NIS does not establish the model; A biased, B centred but four samples certify nothing; diagnostics on pre-gate innovations); 420 lexical words | Notation $\nu_k$, $S_k$, $m$ of the reference; worked example aligned with the card | Evaluation |

The front gives NIS = 2 for every epoch on purpose: the card asks what that equality
cannot establish, so stating it does not reveal the answer.

## Reference findings

- The "Innovation consistency" subsection still called P-CV-FUSION-01 pending. It now
  points to the CV-FUSION-007 worked example and states what a nominal mean NIS leaves
  open.
- The 2026-11-09 draft attributed "these model assumptions must be checked rather than
  inferred from a favorable average" to Gamse et al. §2.2.2 and §3.4.2. The paper lists
  the assumptions and checks normality, but does not make that statement and does not
  test whiteness. The sentence now separates what the paper states from the project's
  conclusion.
- The draft said that gating "changes its reference distribution" without quantifying
  it. A constructed gate example now shows that the mean of accepted NIS values can look
  nominal for an overconfident filter, while the rejection rate exposes it.
- The Gamse source entry said "quoted in the 2026-10-23 report, not re-read". It was
  re-read for this card; the entry now records the passages used.
- The upstream sentence "If the innovation is zero-mean, white, Gaussian with covariance
  $S$, it follows a $\chi^2$ distribution" states sufficient conditions and is kept; the
  worked example adds that whiteness is not needed for the one-epoch marginal law, only
  for sequence statistics.

## Applied corrections

- `vault/10-mathematiques-estimation/13-kalman-ekf-eskf.md`: CV-FUSION-007 appended
  (drafted 2026-11-09); objective capitalized like its siblings; constructed gate
  calculation added to the further explanation; source line names the check script.
- `vault/10-mathematiques-estimation/references/13-kalman-ekf-eskf.md`, revision
  10 → 11: section "Approved worked example — CV-FUSION-007 — 2026-11-09" (Gamse
  attribution corrected, gate example added); "Innovation consistency" pointer; Gamse
  source entry; CV-FUSION-007 listed under related flashcards; closing provenance line
  extended.

Correction log: no published statement was false. The misattribution was in the
unpublished 2026-11-09 draft and was fixed before delivery; the other changes are
pointers and traceability. No existing card repeats the draft sentence (search for
"favorable average" over `vault/`).

## Proposals

P-CV-FUSION-01: accepted by the learner on 2026-11-09, completed as CV-FUSION-007.
P-CV-FUSION-02 (IMU noise conversion) remains pending and is not affected.

## Sources

Scientific sources:

- Gamse, Nobakht-Ersi and Sharifi 2014, Statistical Process Control of a Kalman Filter
  Model, Sensors 14(10), [PMC4239867](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/):
  §2.2.2 (eq. 5–10, innovation properties, NIS, hypotheses and chi-square test) and the
  §3.4 subsection list, §3.4.2 (degrees of freedom, $\alpha$, 7.815, normal probability
  plots). Read through a fetch tool that returns short verbatim fragments and summaries,
  not the full text.

No implementation source is needed: the card makes no API claim.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 -I docs/revues/2026-11-09-four-proposals/checks/13-kalman-ekf-eskf.py` | 21 checks passed, including a seeded Monte Carlo cross-check of the gate formula |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/10-mathematiques-estimation/13-kalman-ekf-eskf.md` | 7 cards, no anomaly; CV-FUSION-007 420 lexical words |
| `git diff --check -- vault/10-mathematiques-estimation/` | No whitespace error |

The vault-wide checks are recorded in the [overview](00-bilan.md). The gate example
assumes Gaussian innovations with a correctly shaped but scaled covariance; other
mis-specifications change the numbers. No filter was run on camera or IMU data. Agent
self-review only; the Obsidian and AnkiDroid renderings of the card are not verified.
Export status: to republish with `paquet-anki`.
