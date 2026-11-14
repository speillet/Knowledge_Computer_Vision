# Review — Exposure, noise, color and sampling — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 10 to revision 11. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note for the photometric and sampling side of
acquisition. Shutters and timestamps stay in
[CV-CAPTEURS](../../../vault/20-acquisition-images/references/22-capteurs-horodatage.md)
and other modalities in
[CV-IMAGERIES](../../../vault/20-acquisition-images/references/23-imageries-specialisees.md);
the note links to them.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ACQUISITION-001 | Blur $800\times0.005=4$ px and $t_e\le1.25$ ms recomputed: confirmed (project kinematics). Source line cited EMVA §§2.1, 2.4, 2.6–2.7 for the blur calculation, which EMVA does not contain: imprecise citation. French decimal comma in the expected answer; "standardized observation", "assumes a unique and neglectful optical direction" obscured the model's assumptions | Reasoning: convert speed and exposure into image blur and invert it into a budget | 2 expected criteria; 378 → 388 lexical words | Notation aligned with the reference ($v\,t_{exp}$, box blur) | Minor | Expected-answer decimal fix; language fixes; Source now cites EMVA §1.2 eq. 1 and §2.1 eq. 6 and labels the blur formula as project kinematics |
| CV-ACQUISITION-002 | SNR independent of $K$ except quantization and the $\sqrt2$/2 regimes: confirmed (EMVA §2.6 eqs. 21–22); halved electron range at doubled gain: confirmed as a deduction from eq. 5 and §2.7 (clipping at $2^k-1$ before full well). Numbers 8.9, 13.3, 3.54, 5.77 recomputed. Expected answer said "photonic noise", "reading noise" and "reduces the dynamics" (French *dynamique* = dynamic range); explanation said "the gain tends towards $\sqrt2$", ambiguous with camera gain | Comparison: separate brightness from SNR, blur and saturation | 3 expected criteria; 490 → 497 lexical words | Consistent with reference worked example A | Minor | Meaning-restoring fix of the expected answer; language fixes; Source given exact equations |
| CV-ACQUISITION-003 | Prefilter before decimation and folded frequency 0.8 → 0.2 cyc/px: confirmed (Parmar et al. §3.2, §6.1; recomputed). "Configurations evaluated in 2022" imprecise: OpenCV 4.5.5 `cv2.resize`, TensorFlow 2.0 and PyTorch 1.9 `F.interpolate` with default flags (§6.3). "Resize 0.24 enables antialiasing by default, unlike its older versions" imprecise: before 0.17 PIL inputs were already antialiased, tensors were not by default (torchvision 0.24 `Resize`). "Controlled discounts", "image string", "adding increases" (augmentations), "not a real movement" obscured meaning | Diagnosis: separate sampling artifacts from model errors | 2 expected criteria; 423 → 444 lexical words | Reference example C gives the leakage of each prefilter | Minor | Precision of versions and antialias default; language fixes; Source: unreachable OpenCV tutorial replaced by `imgproc.hpp` at 4.13.0 |
| CV-ACQUISITION-004 | sRGB inverse $((c+0.055)/1.055)^{2.4}$ above 0.04045 and 0.5 → 0.214: confirmed (sRGB B.1; recomputed). Expected answer ended "in the actual received string" (French *chaîne* = pipeline). "An entire passage can clip values" (*passage en entier* = conversion to integers), "drive chain" (*chaîne d'entraînement* = training pipeline), "paintings", "re-compliance" | Practice: verify an input contract with a known stimulus | 1 expected criterion list (6 items); 368 → 372 lexical words | Reference now states the OpenCV `imread` contract (BGR, 8-bit, EXIF orientation) | Minor | Meaning-restoring fix of the expected answer; language fixes; Source adds `imgcodecs.hpp` at 4.13.0 |

Expected-answer changes (meaning-restoring language fixes, no change of recall
objective):

- CV-ACQUISITION-001: "About 4 px: 800 × 0,005." → "About 4 px: 800 × 0.005."
- CV-ACQUISITION-002: "doubling light doubles photoelectrons and increases SNR: by
  a factor of $\sqrt2$ when photonic noise dominates, up to 2 when reading noise
  dominates; longer exposure also increases motion blur. Double the gain multiplies
  signal and noise already acquired: excluding quantization noise, the SNR does not
  change, and the maximum numerical value is reached with half the electrons, which
  reduces the dynamics. The gain does not create photonic information and does not
  repair saturation." → "Doubling the light doubles the photoelectrons and
  increases the SNR: by a factor of $\sqrt2$ when photon shot noise dominates, up
  to 2 when read noise dominates; a longer exposure also increases motion blur.
  Doubling the gain multiplies the signal and the noise already acquired: excluding
  quantization noise, the SNR does not change, and the maximum digital value is
  reached with half the electrons, which reduces the dynamic range. The gain does
  not create photon information and does not repair saturation."
- CV-ACQUISITION-004: "… exposure and saturation in the actual received string." →
  "… exposure and saturation in the pipeline that actually feeds the model."

## Reference findings

Claims of revision 10 checked against their passages:

- EMVA noise model with $\sigma_d^2$ in e⁻² and $\sigma_q^2=1/12$ DN² (§2.4,
  eqs. 13–14) and SNR eq. 21: confirmed; $K$ cancels except through quantization
  (§2.6): confirmed; $\sqrt2$ and factor-2 regimes (eq. 22): confirmed.
- "A stronger gain reaches the maximum numerical value with fewer electrons, hence a
  reduced saturation capacity (§2.7)": confirmed as a deduction (eq. 5 and the
  §2.7 statement that saturation capacity is set by clipping at $2^k-1$ before
  full well); the condition "when the ADC limit binds" was missing and is now stated.
- "Nyquist requires less than half the sampling for a band-limited signal":
  garbled; replaced by Shannon's Theorem 1 (no frequency above $W$, samples
  $1/(2W)$ apart) and its pixel-grid reading (0.5 cyc/px).
- Parmar et al. aliasing in OpenCV, TensorFlow and PyTorch versus adaptive PIL
  filters: confirmed (§1, §3.2, §6.3), now with versions.
- `torchvision.transforms.Resize` 0.24 `antialias=True` default introduced in 0.17:
  confirmed, with the PIL/tensor nuance added.
- No scientific error found in revision 10. The body was shallow (595 words, one
  paragraph per section) and contained mistranslations that obscured meaning:
  "Stage" (scene), "quantification" (quantization), "photonic" (photon shot),
  "reading noise" (read noise), "opposite the adaptive filters" (against), "fault
  change to 0.17" (default change), "material results" (hardware results),
  "Question of work", "Reference Response", "Proposed Reproducible Investigation",
  "the check training/inference coherence", and French decimal commas.

New claims verified for revision 11 (main ones):

- EMVA 1288: assumptions 1–4 of §1.2, including debayering, denoising and sharpening
  as processing that breaks the white-noise assumption and the exclusion of EMCCD
  and intensified cameras; eq. 1 (radiant exposure), eqs. 2–6 (quantum efficiency,
  practical photon formula eq. 4, linear signal model), eq. 15 (photon transfer),
  eqs. 16–19 (two-frame mean and variance, $\sqrt{2/(NM)}$ uncertainty, 0.14% for a
  megapixel), eqs. 23–28 (ideal sensor, saturation capacity below full well,
  sensitivity threshold, dynamic range), eqs. 29–30 and §3.2 (dark current; no
  doubling-temperature model in Release 4), §4 and §4.1 (DSNU, PRNU, four types of
  nonuniformity).
- Healey and Kondepudy: CCD model $D=(KI+N_{DC}+N_S+N_R)A+N_Q$ with Poisson shot
  noise, read noise, quantization of variance $q^2/12$, per-site gain $K$ of mean 1,
  no blooming (§II-B, eqs. 2–6); sensor-level aliasing for high-frequency patterns
  (§III); two-image difference (§IV); uncorrected variance proportional to $I^2$
  versus shot-noise variance proportional to $I$ after correction, and the need for
  a linear response (§V).
- Shannon 1949, §II, Theorem 1.
- Parmar et al. §6.1: non-adaptive kernels reduce to a 2-tap average (even factors)
  or a delta (odd factors); adaptive bilinear gives $\{1,3,3,1\}/8$ at $r=2$.
- sRGB: A.2 (display gamma approximately 2.2), A.8 (forward curve, threshold
  0.0031308, scaling by $2^{bit\,depth}-1$), B.1 (inverse, threshold 0.04045).
- Bayer 1976: luminance elements at half of the positions, chrominance in
  alternating rows.

Implementation notes recorded in the reference (FR-036): OpenCV's header calls
`INTER_AREA` "moire'-free", whereas for a factor of 2 it is a 2×2 box average that
still passes 31% of a 0.4 cyc/px component as an alias (constructed example C);
Parmar et al. tested OpenCV 4.5.5, and in 4.13.0 `INTER_LINEAR` at exactly factor 2
is internally replaced by that area average (`resize.cpp` L4009–L4012).

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 595 → 4,435. About
1,000 tokens are tables, the pseudocode and the Mermaid diagram. The length comes
from three linked mechanisms (photon noise, motion blur, sampling) plus the data
contract; shutter and modality depth is linked, not restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Raw versus rendered output contracts (types, ranges, Bayer mosaic, sRGB scaling), OpenCV `imread` contract, coordinate and unit conventions, role for photometric, geometric and learned stages |
| Intuition | Shallow | Developed | Photon counting, exposure as a time window, grid as a sampler, encoded values are not light; constructed conveyor illustration; Mermaid diagram of the acquisition chain |
| Prerequisites | Shallow (one link) | Developed | Links to CV-FILTRES, CV-CAPTEURS, CV-IMAGERIES, CV-FIABILITE; probability background |
| Assumptions | Absent (merged with problem) | Developed | EMVA linear-model assumptions, no blooming, uniform motion, band limitation; observability (clipping, aliasing, blur zeros, single rendered image); degenerate cases |
| Procedure | Shallow | Developed | Eight-step acquisition design and check pseudocode with the purpose of each step |
| Mathematics | Shallow | Developed | EMVA eqs. 1–6, 13–15, 20–30 with units; Healey–Kondepudy model; PRNU signal dependence; motion-blur box and its zeros; sampling theorem and decimation; sRGB curve; worked examples A (blur, photons, gain), B (photon transfer and PRNU bias), C (prefilter leakage) |
| Parameters | Shallow | Developed | Seven-row table (exposure, illumination, gain, ADC depth, transfer curve, temperature, resize); interactions; tuning order |
| Properties | Shallow | Developed | Gain invariance and its limit, shot-noise bound, heteroscedastic noise, fixed patterns, irreversibility of aliasing, non-linearity of encoded values, sparse color sampling |
| Cost and implementation | Shallow | Developed | Data-rate formula and constructed example; OpenCV 4.13 `imread`, `resize`, `INTER_AREA`, `pyrDown`, Bayer codes; torchvision 0.24 `Resize`; Parmar versions; execution status |
| Evaluation | Shallow | Developed | EMVA characterization protocol; proposed baseline and exposure-for-illumination variation with confounds; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (light, exposure, gain, raw data, prefilter, shutter, modality); industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/21-exposition-bruit-echantillonnage.py`](checks/21-exposition-bruit-echantillonnage.py)
(21 checks): blur budget; SNR 19.4, 8.93 and 8.94; top-code electrons 7,990 and
1,997.5; irradiance 1.7 µW/cm² (EMVA eq. 4); 120.7 e⁻ for SNR 10 (eq. 25);
$\sigma_q/K=0.577$ e⁻; photon-transfer variances 106.3 and 506.3 DN², slope 0.5,
$\sigma_d^2=25$; PRNU-biased slope 0.62; $\sqrt{2/NM}$; PRNU/shot crossover at
10,000 and 40,000 e⁻; aliasing 0.8 → 0.2; prefilter responses at 0.4, 0.25 and
0.1 cyc/px; zeros of a 4 px box; sRGB 0.214 and 0.735 with round trip; 6 and
4 Gbit/s; the card values of CV-ACQUISITION-002.

## Applied corrections

- [Reference](../../../vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md),
  revision 10 → 11: body rewritten and deepened as above; appendices given the same
  language fixes as the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Physical reading and built example" →
  "Physical reading and constructed example", "Proposed Reproducible Investigation"
  → "Proposed reproducible investigation", "Example built frequency" →
  "Constructed frequency example", decimal commas); sources split into scientific
  and implementation sources; closing provenance line replaced. Front matter
  unchanged except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/20-acquisition-images/21-exposition-bruit-echantillonnage.md):
  three expected answers fixed as quoted above. Other language fixes in the
  explanations and blocking errors: "adds up the successive positions" → "sums";
  "to aim at the most one pixel of displacement" → "to keep the displacement during
  exposure to at most one pixel"; "standardized observation" → "normalized
  observation"; "assumes a unique and neglectful optical direction, noise and
  saturation" → "assumes a single motion direction and neglects optics, noise and
  saturation"; "Mix ms and s or conclude to a universal PSF" → "Mixing ms and s, or
  treating this box blur as a universal point spread function (PSF)"; "only plays
  by the quantification" → "enters only through the quantization term"; "the gain
  tends towards $\sqrt2$" → "the improvement tends towards $\sqrt2$"; "controlled
  discounts on calibration target" → "controlled downscalings of a calibration
  target"; "image string" → "image pipeline"; "adding increases" → "adding
  augmentations"; "not a real movement" → "not a real change in the scene";
  "an entire passage can clip values" → "a conversion to integers can clip values";
  "drive chain" → "training pipeline"; "re-compliance" → "realigning the pipeline";
  French decimal commas. Source lines given exact EMVA equations, OpenCV 4.13.0
  header links and the precise Parmar and torchvision scope. Questions, IDs,
  objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for
`Parmar`, `antialias`, `EMVA`, `photonic`, `0,04045`).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run). The 2026-10-23 proposals for a photon-transfer card and an
inspection-sizing card were not retained by the learner; they are not repeated.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-ACQUISITION-01 | CV-ACQUISITION | Explain why one fixed gray-level threshold gives different false-alarm rates in dark and bright regions, from $\sigma_y^2=K^2\sigma_d^2+\sigma_q^2+K(\mu_y-\mu_{y.dark})$, and name a remedy (threshold scaled by the local noise model) | Signal-dependent noise is developed in the reference but untested; it affects defect and edge thresholds | Understanding (absent family); Properties | 1 card, 3 criteria | [EMVA 1288 §2.4 eq. 15](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf); [Healey and Kondepudy §V](https://doi.org/10.1109/34.276126) |
| P-CV-ACQUISITION-02 | CV-ACQUISITION | Compute the fraction of a 0.4 cyc/px component that survives as an alias after a 2×2 area average versus an adaptive bilinear prefilter at $r=2$, and choose a resize method | No card trains the quantitative effect of the prefilter width that CV-ACQUISITION-003 only names | Reasoning; Mathematics, worked example C | 1 card, 3 criteria (alias at 0.2; responses 0.31 and 0.03; adaptive width) | [Parmar et al. §6.1](https://arxiv.org/abs/2104.11222); [OpenCV 4.13.0 `resize.cpp` L4009–L4041](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/resize.cpp#L4009-L4041) |

No defective question was found.

## Sources

Scientific sources, opened at the passages listed:

- EMVA 1288 Linear 4.0, [PDF](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf)
  (text extracted with `pdftotext`): §1.2, §2.1 (eqs. 2–6), §2.4 (eqs. 13–15),
  §2.5 (eqs. 16–19), §2.6 (eqs. 20–23), §2.7 (eqs. 24–28), §3.1–3.2 (eqs. 29–31),
  §4 and §4.1.
- Healey and Kondepudy 1994, read in the copy at
  [cs.nyu.edu](https://cs.nyu.edu/~fergus/drafts/Healey94.pdf) (published version,
  DOI 10.1109/34.276126): abstract, §II-A and §II-B (eqs. 1–6), §III (aliasing
  paragraph), §IV (eqs. 24–31, 41), §V (correction paragraph), §VII-C.
- Shannon 1949, read in the Proc. IEEE 1998 "Classic Paper" reprint mirrored at
  [web.cs.miami.edu](https://web.cs.miami.edu/home/burt/learning/Csc524.092/docs/shannonpaper.pdf):
  §II, Theorem 1.
- Parmar, Zhang and Zhu, [ar5iv HTML of arXiv 2104.11222](https://ar5iv.labs.arxiv.org/html/2104.11222):
  §1, §3.2, §6.1, §6.3.
- W3C, [How to interpret the sRGB color space](https://www.w3.org/Graphics/Color/srgb)
  (served as PDF): A.1–A.8 and B.1.
- Bayer, [US patent 3,971,065](https://patents.google.com/patent/US3971065A/en):
  abstract and detailed description (first 100,000 characters of the page).

Implementation sources (official code at tag 4.13.0 and versioned documentation):

- [`opencv/modules/imgcodecs/include/opencv2/imgcodecs.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgcodecs/include/opencv2/imgcodecs.hpp): L68–L85, L323–L386.
- [`opencv/modules/imgproc/include/opencv2/imgproc.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/include/opencv2/imgproc.hpp): L249–L270, L555–L556, L754–L824, L2419–L2455, L3194–L3214.
- [`opencv/modules/imgproc/src/resize.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/resize.cpp): L3960–L4045.
- [torchvision 0.24 `Resize`](https://docs.pytorch.org/vision/0.24/generated/torchvision.transforms.Resize.html): `antialias` and `interpolation` parameters.

Failed accesses and limits:

- docs.opencv.org/4.13.0 (Image Pyramids tutorial): HTTP 403 in this pass, as for the
  other subjects; the link is retained in the reference as not re-read.
- Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed.: the PDF download
  form requires a name and an e-mail address; not submitted, so the book was not
  consulted and is not cited.
- Edmund Optics resolution note: not retried; retained as unverified and not used
  for any claim.
- Context7 was not available in this session (see the scope record); official
  versioned code and documentation replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/21-exposition-bruit-echantillonnage.py` | 21 checks passed |
| `git diff --check -- vault/20-acquisition-images/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/20-acquisition-images/21-exposition-bruit-echantillonnage.md` | 4 cards, 388, 497, 444 and 372 words, no anomaly |
| Protected-field comparison with the pre-edit copy | No protected-field error: card headings, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` unchanged; reference front matter identical except `revision: 10` → `11`; H1 and per-card headings unchanged |
| Local links and anchors under `vault/20-acquisition-images` | 0 errors |

No camera, OpenCV call or resize was executed; the proposed baseline and variation
are protocols, not results. The Mermaid diagram and tables were not rendered in
Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is
agent self-review, without independent scientific validation or measurement of
learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-ACQUISITION revision 11, CV-ACQUISITION-001 to -004, corrections listed above,
Agent Claude Code self-review, to republish with `paquet-anki`) and the proposal
register (P-CV-ACQUISITION-01, P-CV-ACQUISITION-02).
