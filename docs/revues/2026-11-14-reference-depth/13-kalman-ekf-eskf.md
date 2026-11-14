# Review — Kalman, EKF, UKF and ESKF for sensor fusion — 2026-11-14

## Overview

6 cards audited in `approfondir` mode; the canonical reference body was deepened from
revision 9 to revision 10. Highest severity per card before correction:
0 blocking, 4 important, 2 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The body of revision 9 held about 880 words: a sound summary of the ESKF motivation,
noise integration, reset and Joseph form, with one-sentence sections elsewhere and
several French remnants ("$R_{vrai}$", "on pose", "status" for *état*). The audit found
no false scientific claim in the reference, but four cards had an expected answer or
explanation that was overly strong, incomplete on a condition, or garbled.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FUSION-001 | EKF, UKF ($2n+1$ sigma points, no Jacobian) and ESKF descriptions: confirmed (Julier and Uhlmann §3, eq. 12–14; Solà §5.2, §6.1). "Mean to a higher order of accuracy than the EKF, covariance to the same order": confirmed (§3, property 1) | Understanding: variants as combinable choices | 3 criteria; 377 → 380 words | Aligned with the reference appendix | Minor | Language fixes ("a EKF", "offbeat clock", "Common Basis of Calculation") |
| CV-FUSION-002 | $\chi^2_m$ distribution of the NIS: confirmed (Gamse et al. §2.2.2, quoted 2026-10-23); quantiles recomputed (3.841, 5.991, 7.815, 9.488). Expected answer called $\nu^TS^{-1}\nu$ "a Mahalanobis distance without unity": imprecise, it is the *squared* Mahalanobis distance, and FilterPy 1.4.5's `mahalanobis` returns the root, so the distinction changes the gate | Reasoning: statistical meaning of a gate | 3 criteria; 397 → 421 words | Decimal commas; "Gatting" | Important | Expected answer corrected and language restored; explanation completed with the FilterPy root convention and its source |
| CV-FUSION-003 | Reset $\hat{\delta x}\leftarrow0$, $P\leftarrow GPG^T$, $G_\theta=I-[\tfrac12\hat{\delta\theta}]_\times$: confirmed (Solà §6.3, eq. 285–288, 294). Expected answer garbled: "a reset of $P$ at the time the average error is injected", "on pose" (French *on pose*, "we set") | Diagnosis: covariance collapse at reset | 2 criteria; 403 → 410 words | "$R_{vrai}$" in the explanation | Important | Meaning-restoring fix of the expected answer; language fixes |
| CV-FUSION-004 | Dependence of the covariance terms on $\Delta t$: confirmed (Solà §5.4.2 eq. 262–265, App. E eq. 440). Missing condition: the $\Delta t^2$ law holds for per-sample noise standard deviations; a datasheet density must first be converted ($\sigma_c/\sqrt{\Delta t}$, Kalibr), after which the variance grows as $\sigma_c^2\Delta t$. Expected answer said "at its moment of acquisition, no reception" | Practice: timing contract | 3 criteria; 413 → 439 words | Aligned | Important | Meaning-restoring fix of the expected answer; missing condition added to the explanation with its source |
| CV-FUSION-005 | Four ESKF properties: confirmed (Solà §5.1, re-read); nominal state integrated without noise terms (§5.2) | Reasoning: why an error state | 3 criteria; 425 → 421 words | Aligned | Minor | Language fixes ("predictions IMU", "normal quaternion", "speed") |
| CV-FUSION-006 | Solà note 26 says the simple form "is not guaranteed to be symmetric nor positive definite"; the card said it "is neither symmetric nor positive definite": overly strong. Joseph form and its derivation: confirmed (Chin §III-A, eq. 14); validity for a non-optimal gain: project deduction from the derivation, stated in FilterPy's code comment | Diagnosis: numerical covariance failure | 3 criteria; 404 → 433 words | Aligned | Important | Expected answer corrected; explanation completed with OpenCV 4.13.0 (simple form) and FilterPy 1.4.5 (Joseph form) contracts |

Expected-answer changes (old → new):

- CV-FUSION-002 (sourced precision and language): "a Mahalanobis distance without unity … follows a law of $\chi^2$ to $m$ degrees of freedom … We therefore reject a measure … $\chi^2_{3;0{,}95}\approx7{,}81$" → "a unitless squared Mahalanobis distance … follows a $\chi^2$ distribution with $m$ degrees of freedom … A measurement is therefore rejected … $\chi^2_{3,0.95}\approx7.81$".
- CV-FUSION-003 (meaning-restoring): "Look for a reset of $P$ at the time the average error is injected and then reset … on pose $\hat{\delta x}\leftarrow0$ … with $G$ the Jacobian of the reset" → "Look for a zeroing of $P$ at the moment the mean error is injected and then reset … we set $\hat{\delta x}\leftarrow0$ … with $G$ the reset Jacobian".
- CV-FUSION-004 (meaning-restoring): "sample IMU per sample … each term of covariance … at its moment of acquisition, no reception. Distinguish between lack of measurement and zero measurement" → "IMU sample by IMU sample … each covariance term … at its acquisition time, not its reception time. Distinguish a missing measurement from a zero measurement".
- CV-FUSION-005 (language): "less often than predictions IMU" → "less often than IMU predictions".
- CV-FUSION-006 (sourced correction, Solà §6.1 note 26): "is neither symmetric nor positive definite in finite arithmetic … Prefer the form of Joseph … If $P^-$ and $R$ are positive semi-definite symmetric and independent measurement and prediction errors … mitigates digital risk" → "is not guaranteed to remain symmetric or positive definite in finite arithmetic … Prefer the Joseph form … If $P^-$ and $R$ are symmetric positive semi-definite and the measurement and prediction errors independent … mitigates the numerical risk".
- CV-FUSION-001 (language): "a EKF" → "an EKF".

## Reference findings

Claims of revision 9 checked against their passages:

- Solà, Quaternion kinematics (arXiv 1711.02508v1, HTML): §5.1 four properties, §5.2
  cycle, §5.4.2 eq. 262–265 with units, §6.1 eq. 274–278 and note 26, §6.3 eq. 285–288
  and the remark that most implementations use $G=I_{18}$, Appendix E eq. 438–440:
  confirmed.
- Julier and Uhlmann 1997, §3 eq. 12–14 and properties 1–5: confirmed on the Berkeley
  course copy.
- Chin 2023, §III-A eq. 14: confirmed; the body also uses §I, §II eq. 5–10 (standard
  filter, optimal linear estimator equal to the conditional mean under Gaussian
  assumptions, round-off in the covariance difference) and the cost remark of §III-A.
- Imprecision found in the reference and corrected: the $\Delta t^2$ dependence of the IMU
  measurement-noise term was stated without its condition (per-sample standard
  deviations); the body now gives the density conversion (Kalibr) and worked example B.
- Language defects that obscured meaning in revision 9: "$R_{vrai}$", "on pose",
  "status, correction and reset" (state), "Quaternion kinetics", "pulse covariances"
  (impulse), "the disturbances as the random steps of the biases" (perturbations, bias
  random walks), "subtrust filter" (underconfident), "Choose Status, Frequency, Q/A…",
  "Question of work", "Reference Response", "Joseph shape", "the sum of Joseph",
  "invalid template" (model), "speed" (velocity), French decimal commas.

Implementation facts added and their relation to the papers (FR-036):

| Aspect | Paper | Implementation |
| --- | --- | --- |
| Covariance update | Solà note 26: simple form not guaranteed symmetric or positive definite; Chin eq. 14: Joseph form | OpenCV 4.13.0 `KalmanFilter::correct`: simple form $P^--KHP^-$ (kalman.cpp L128–L129); FilterPy 1.4.5 `update`: Joseph form (L554–L560) |
| Gain computation | $K=PH^TS^{-1}$ | OpenCV: `solve(..., DECOMP_SVD)`; FilterPy: explicit inverse of $S$ |
| Mahalanobis gate | $\nu^TS^{-1}\nu\sim\chi^2_m$ (Gamse et al.) | FilterPy `mahalanobis` returns $\sqrt{\nu^TS^{-1}\nu}$ (L1124–L1135) |
| IMU noise inputs | Solà: per-sample $\sigma_{\tilde a_n}$ [m/s²], $\sigma_{\tilde\omega_n}$ [rad/s]; random walks $\sigma_{a_w}$ [m/s²√s] | Kalibr: densities [unit/√Hz] with $\sigma_d=\sigma/\sqrt{\Delta t}$ and $\sigma_{bd}=\sigma_b\sqrt{\Delta t}$; static values optimistic, ×10 or more for low-cost MEMS |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 880 → 3,965. About
900 tokens are the two tables, the pseudocode and the Mermaid diagram.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow (two sentences) | Developed | Task; state components, units and dimensions (Solà eq. 266); inputs with rates and timestamps; outputs; pipeline roles and upstream/downstream contracts |
| Intuition | Partly developed (variant summary) | Developed | Inverse-variance weighting; worked example A (scalar update, recomputed); variant positioning; Mermaid diagram of the ESKF loop |
| Prerequisites | Shallow (one link) | Developed | Links to CV-SE3, CV-SVD, CV-CAPTEURS, CV-SORT, CV-VIO, CV-FACTEURS |
| Assumptions | Shallow | Developed | Noise model and optimality (Chin §II), linearization (Solà §5.1), unimodality, timing, observability (Solà §5.1, §6), degenerate cases |
| Procedure | Partly developed (cycle in prose) | Developed | ESKF pseudocode with buffer, gate, Joseph update, injection, reset and re-propagation; purpose of each step |
| Mathematics | Partly developed | Developed | KF/EKF equations (Chin eq. 5–8); NIS and quantiles; sigma-point equations and properties (Julier–Uhlmann eq. 12–14); error-state propagation and impulses (Solà eq. 262–271, App. E); density conversion with worked example B; constant-velocity $Q_d$; correction Jacobian, injection and reset (eq. 274–294); update forms with the non-optimal-gain example |
| Parameters | Shallow (one sentence) | Developed | Table of noise densities, random walks, $R$, $P_0$, gate, buffer, reset and update form with sources (Kalibr, Solà); tuning approach based on consistency |
| Properties | Shallow | Developed | Linear-Gaussian optimality, unscented accuracy, error-state properties, covariance forms, consistency versus accuracy |
| Cost and implementation | Partly developed (update forms) | Developed | Cost drivers with $n$, $m$ and rates; OpenCV 4.13.0, FilterPy 1.4.5 and Kalibr contracts; execution status |
| Evaluation | Shallow (one proposed variation) | Developed | Metrics; baseline and controlled variation (acquisition versus reception time) with hypothesis and confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow (two sentences) | Developed | Six conditional choices; industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/13-kalman-ekf-eskf.py`](checks/13-kalman-ekf-eskf.py) (13 checks): scalar
update (gain 0.8, 0.8 m, 0.8 m²) and the non-optimal gain (1.25 m² actual versus 2.0 and
2.75 m² reported); $\chi^2$ 95% quantiles for $m=1$–4 and the root-gate value 3.08; the
whitened-innovation example (9 and 0.09); the unscented mean of $x^2$; the factor 200
between the two constant-velocity noise models at 200 Hz; the gyroscope density conversion
($2.4\cdot10^{-3}$ rad/s, $1.45\cdot10^{-10}$ rad², $1.7\cdot10^{-4}$ rad after 1 s, 0.097° after
100 s, factor $\sqrt{200}$ if the conversion is forgotten); the 4.5° latency mismatch; the reset
of a covariance by $G$ for a 0.02 rad correction; the $2n^3$ propagation cost.

## Applied corrections

- [Reference](../../../vault/10-mathematiques-estimation/references/13-kalman-ekf-eskf.md),
  revision 9 → 10: body rewritten and deepened as above; the $\Delta t^2$ condition made
  explicit; mistranslations fixed in the body and in all three appendices ("Question of
  work", "Reference Response", "Documentary reference", "Quaternion kinetics", "Choice of
  design", "Common Basis of Calculation", "Non-reverse calculation", "consider releases",
  "Also preserve correlations.", "speed", "Origin of Joseph", "sum of Joseph", "invalid
  template", "Joseph shape", "status, correction and reset"); sources split into
  scientific and implementation sources; closing provenance line replaced. Front matter
  unchanged except `revision`; H1 and the six `### CV-FUSION-00N` headings kept.
- [Cards](../../../vault/10-mathematiques-estimation/13-kalman-ekf-eskf.md): the
  expected-answer changes above; explanations of CV-FUSION-002 (FilterPy root
  convention), CV-FUSION-004 (density conversion) and CV-FUSION-006 (OpenCV and FilterPy
  update forms) completed with their sources; language fixes in all explanations and
  blocking errors; Source lines "see" / "consult the" / "consulted the" → "consulted",
  "status" → "state". Questions, IDs, objectives, families, tags and target deck
  unchanged.

`rg` over `vault/` for "Joseph", "(I-KH)", "Mahalanobis" and "9.4877": the other files
that mention a Mahalanobis distance (CV-ASSOCIATION, CV-ANOMALIES, CV-HOMOGRAPHIE) state
no gate threshold on its square or root and make no claim about the covariance update
form. No change is needed outside this subject.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run). P-CV-FUSION-01 (NIS and biased residuals) remains pending and is not
duplicated; the reference now develops the NIS material it would test.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-FUSION-02 | CV-FUSION | Convert an IMU datasheet noise density and an Allan-deviation random walk into the discrete impulse covariances of an ESKF at a given IMU rate, and predict the effect of skipping the conversion | No card trains building $Q$ from sensor specifications; CV-FUSION-004 covers timing, not units | Practice; Mathematics, worked example B | 1 card, 3 criteria ($\sigma/\sqrt{\Delta t}$ and $\sigma_b\sqrt{\Delta t}$; impulse variance $\sigma^2\Delta t$; underestimate by $\sqrt{\text{rate}}$) | [Solà, §5.4.2 eq. 262–265 and App. E eq. 433–440](https://arxiv.org/html/1711.02508v1); [Kalibr wiki, IMU Noise Model](https://github.com/ethz-asl/kalibr/wiki/IMU-Noise-Model) |

## Sources

Scientific sources, opened at the passages listed:

- Solà, Quaternion kinematics, [arXiv HTML v1](https://arxiv.org/html/1711.02508v1):
  §5.1, §5.2, §5.4.2, §5.4.3, §6, §6.1 with note 26, §6.1.1, §6.2, §6.3, §6.3.1,
  Appendix E (eq. 425–440) and E.2.1 (eq. 454–459).
- Julier and Uhlmann 1997, [Berkeley course copy](https://www.cs.berkeley.edu/~pabbeel/cs287-fa13/optreadings/JulierUhlmann-UKF.pdf)
  (text extracted with `pdftotext`): §3, eq. 12–14 and properties 1–5.
- Chin 2023, [JPL IPN Progress Report 42-233](https://ipnpr.jpl.nasa.gov/progress_report/42-233/42-233A-orig.pdf):
  abstract, §I, §II (eq. 3–10), §III opening and §III-A (eq. 14).
- Gamse et al. 2014 and Wojke et al. 2017: not re-opened; their passages were quoted in
  the 2026-10-23 report and are used for the same details.

Implementation sources:

- OpenCV 4.13.0 `modules/video/src/kalman.cpp`: L60–L80, L82–L132.
- FilterPy 1.4.5 `filterpy/kalman/kalman_filter.py`: L491–L565, L1124–L1135.
- Kalibr wiki, [IMU Noise Model](https://github.com/ethz-asl/kalibr/wiki/IMU-Noise-Model),
  read from the wiki repository on 2026-11-14 (unversioned page).

Failed accesses and limits:

- Bar-Shalom's consistency tests (NEES) were not consulted; the normalized estimation
  error squared is presented as a project protocol derived from the Gaussian assumption.
- The Kalibr page is an unversioned wiki; its claims are labelled as tool documentation.
- Context7 was not available in this session (see the scope record); versioned official
  code replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/13-kalman-ekf-eskf.py` | 13 checks passed |
| `git diff --check -- vault/10-mathematiques-estimation/ <check scripts>` | No whitespace error |
| `inventaire_cartes.py vault/10-mathematiques-estimation/13-kalman-ekf-eskf.md` | 6 cards, 380 to 439 words, no anomaly; absent families: algorithm, comparison, evaluation, design |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 9` → `10`; six `### CV-FUSION-00N` headings unchanged; `$$` and code fences balanced |

No filter was run; the proposed baseline and variation are protocols, not results. The
Mermaid diagram, tables and display equations were not rendered in Obsidian, and AnkiDroid
rendering of the corrected cards is unverified. This is agent self-review, without
independent scientific validation or measurement of learner proficiency. Export status:
**to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-FUSION revision
10; CV-FUSION-002 squared-distance correction; CV-FUSION-004 density condition;
CV-FUSION-006 "not guaranteed" correction; CV-FUSION-003 meaning restored; Agent Claude
Code self-review; to republish with `paquet-anki`) and the proposal register
(P-CV-FUSION-02).
