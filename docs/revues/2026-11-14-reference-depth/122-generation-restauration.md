# Review — VAEs, GANs and diffusion for generation and restoration — 2026-11-14

## Overview

3 cards audited in `approfondir` mode; the canonical reference body was deepened from
revision 7 to revision 8 at its declared awareness depth (`profondeur: reperage`).
Highest severity per card before correction: 0 blocking, 1 important, 2 minor, 0 with
no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DIFFUSION-001 | Training learns a denoiser at random noise levels; sampling chains it: confirmed (DDPM eq. 4, eq. 14, Algorithms 1–2); DDIM shows the same training objective admits other samplers (abstract, §1). $\hat x_0$ inversion of eq. 4 correct. "current DDPM parameterization" (usual), "loyalty", "exit" mistranslated | Understanding of a common confusion | 2 criteria; 362 → 364 words | Aligned with the reference appendix | Minor | Language fixes; DDIM added to the Source |
| CV-DIFFUSION-002 | Latent diffusion trades spatial cost against reconstruction error: confirmed (LDM §3.1, §4.1). Missing condition for this objective: the authors' own statement that the $f=4$ autoencoder can bottleneck fine-grained pixel accuracy (§5) and the $f$ 4–16 finding (§4.1). "business loyalty", "reserved references" mistranslated | Comparison of a design tradeoff | 2 criteria; 356 → 400 words | Aligned | Minor | Sourced limitation added to the further explanation; language fixes; Source fixed |
| CV-DIFFUSION-003 | Plausibility is not fidelity; detail in the null space of $H$ is unobservable: consistent with Blau and Michaeli (Theorems 1–2). Expected answer lacked the colon after **Expected answer**, a card-format defect; "keep the crude" mistranslated *raw image* | Diagnosis of a dangerous restoration | 2 criteria; 289 → 296 words | Aligned | Important (format defect in the expected answer and meaning-obscuring term) | Colon restored; language fixes; perception–distortion source added |

Expected-answer changes:

- CV-DIFFUSION-001 (language): "de-noise rule" → "denoising rule".
- CV-DIFFUSION-003 (format, requested by the coordinator): `**Expected answer** Visual
  plausibility …` → `**Expected answer**: Visual plausibility …`; text unchanged.

## Reference findings

Revision 7 claims checked: the forward marginal, $\bar\alpha_t$ and the remark that $t$
indexes a noise level are correct (DDPM eq. 4); the 2026-10-30 $\hat x_0$ inversion is
correct. Imprecisions: "fewer steps do not have a universal effect" lacked the DDIM
fact that samplers can be changed without retraining; "Self-encoder" (autoencoder),
"de-noise", "lens promotes plausibility" (objective). No numerical error found.

New verified content: VAE lower bound (§2.2 eq. 3, §2.4); GAN value function,
optimal discriminator, global optimum $-\log4$ at $p_g=p_{\text{data}}$, collapse
warning (§6); DDPM data scaling to $[-1,1]$, $L_{\text{simple}}$ and its
down-weighting of small $t$, $T=1000$, linear $\beta$ from $10^{-4}$ to 0.02,
Algorithms 1–2; DDIM same objective and 10–50× faster sampling; LDM perceptual and
adversarial autoencoder losses, KL or VQ regularization, $f=H/h$, concatenation or
cross-attention conditioning, LDM-{4–16} finding and §5 limitations; perception–distortion
Definition 3, Theorems 1–2 and Example 1; FID eq. 6.

## Reference depth

Body word counts (whitespace tokens, front matter excluded, H1 included, before the
first per-card appendix): 337 → 2,073. The length follows the note's awareness depth.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Generation versus restoration with $y=Hx+n$; data scaling and latent shapes; seed dependence; pipeline role |
| Intuition | Shallow | Developed | Four mechanisms; constructed perception–distortion illustration |
| Prerequisites | Shallow (one link) | Developed | Links to CV-SVD, CV-ACQUISITION, CV-METRIQUES-APPLIQUEES |
| Assumptions | Shallow | Developed | Training distribution, degradation model, non-invertibility (Theorem 1), autoencoder fidelity, degenerate cases |
| Procedure | Shallow | Developed | DDPM Algorithms 1–2 and a restoration-for-inspection procedure with purposes |
| Mathematics | Shallow | Developed | VAE bound, GAN objective and optimum, DDPM eq. 4 and 14, schedule, LDM shapes, perception–distortion function, null-space example, PSNR and FID; worked examples A–D |
| Parameters | Shallow (list) | Developed | Table with sourced effects; tuning approach |
| Properties | Shallow | Developed | Scope of each guarantee; stochastic versus deterministic sampling |
| Cost and implementation | Shallow | Developed | Network evaluations, DDIM, $f^2$, GAN comparison, execution status |
| Evaluation | Shallow | Developed | Baseline with defect metrics; 8 seeds per input as the controlled variation; limits |
| Failure modes and diagnosis | Shallow (one sentence) | Developed | Five-row symptom table |
| Alternatives and sources | Shallow | Developed | Conditional choices, industrial uses labelled as project reasoning, sources split |

Constructed examples are recomputed by
[`checks/122-generation-restauration.py`](checks/122-generation-restauration.py) (8
checks): $\bar\alpha_T\approx4.0\times10^{-5}$, SNR below 1 at $t=260$, $\hat x_0$
inversion and error amplification 0.34 at $t=500$; Gaussian perception–distortion
(MSE 0.5 with KL 0.153 against MSE 0.586 with KL 0); a null-space detail invisible after
2× averaging; 64× fewer latent positions at $f=8$; PSNR 34.15 dB at RMS error 5.

## Applied corrections

- [Reference](../../../vault/120-generatif-multimodal/references/122-generation-restauration.md),
  revision 7 → 8: body rewritten; appendix language fixes identical to the card fixes
  ("Question of work" → "Working question", "Reference Response" → "Reference answer"
  with its missing colon, "Example of check" → "Example check", "Why Can Clarity
  Deceive?" → "Why sharpness can deceive", "the crude" → "the raw image", "current"
  → "usual", "poorly observed kernel" → "poorly observed null space (kernel) of $H$");
  sources split; closing line replaced.
- [Cards](../../../vault/120-generatif-multimodal/122-generation-restauration.md):
  expected-answer changes above; one sourced limitation added to the further
  explanation of 002; language fixes and blocking errors ("Assimilate the forward
  process…" → "Equating the forward noising process with the whole generation
  procedure", "Supposing compression without consequence on fidelity" → "Assuming that
  compression has no consequence for fidelity", "Validate a dimensional measurement on a
  prettier image only" → "Validating a dimensional measurement on a prettier image
  alone"); Source lines given sections and new primary sources. IDs, questions,
  objectives, families, tags and deck unchanged.

No other subject's card repeats a corrected claim.

## Proposals

To register as `pending` (register not edited in this pass):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-DIFFUSION-01 | CV-DIFFUSION | Design an evaluation showing whether a restored defect is determined by the measurement: several seeds per input, consistency $H\hat x\approx y$, and defect metrics against an acquired reference | No evaluation card; the cards explain the risk but not how to measure it | Evaluation | 1 card, 3 criteria | [Blau and Michaeli, Theorems 1–2](https://arxiv.org/abs/1711.06077); [DDPM, Algorithm 2](https://arxiv.org/html/2006.11239v2) |

No defective question was found. Objective lines "to protect an industrial
observation" and "locate the latent diffusion" are awkward but protected.

## Sources

Scientific sources: VAE §2.2–2.4 (PDF v11); GAN eq. 1, §4.1, §6 (PDF v1); DDPM eq. 4,
§3.3–3.4, Algorithms 1–2, §4 and Appendix B schedule line (HTML v2); DDIM abstract,
§1 (HTML v4); LDM §3.1–3.3, §4.1, §5 (HTML v2); Blau and Michaeli Definition 3,
Theorems 1–2, Example 1 (PDF v4); FID eq. 6 (PDF v6). French pre-migration text from
commit `b7142bb^` for "brut" and "fidélité".

Implementation sources: none; no library API is claimed. Context7 unavailable.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | Fails only on files of other subjects in progress (`132-tracking-trajectoires.md`, `45-recalage-ecc.md`); no error in this subject's files |
| `python3 scripts/learning_path.py` | OK, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/122-generation-restauration.py` | 8 checks passed |
| `git diff --check` on the two subject files | No whitespace error |
| Inventory of the card file | 3 cards, 364 / 400 / 296 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical (25); front matter identical except `revision`; H1 and `### CV-…` headings unchanged; `$` balanced |

No generator was executed; the protocol is proposed. Obsidian and AnkiDroid rendering
are unverified. Agent self-review, without independent validation or measured learner
proficiency. Export status: **to republish with `paquet-anki`**.

For the coordinator: `Suivi-pilote.md` entry — 2026-11-14, CV-DIFFUSION revision 8,
cards 001–003, corrections above, Agent Claude Code self-review, to republish with
`paquet-anki`; proposal P-CV-DIFFUSION-01.
