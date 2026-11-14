# Review — Sensors, rolling shutter and synchronization — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note on measurement instants, timestamps and
synchronization in multi-sensor rigs. Photometric exposure stays in
[CV-ACQUISITION](../../../vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md)
and spatial extrinsics in
[CV-MULTICALIB](../../../vault/50-calibration-geometrie/references/55-calibration-multicapteurs.md);
the note links to them.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CAPTEURS-001 | A short exposure reduces blur but not rolling-shutter skew: confirmed (Meingast et al. §2: a non-zero exposure gives "motion blur within the scanline, but has no geometric effects"; Basler: rows offset by `tRow`). "Playback time" (French *temps de lecture* = readout time) twice, "local drag" (blur), "ideal built-in model" obscured the mechanism | Comparison: separate exposure (blur) from readout (skew) | 1 criterion; 368 → 371 lexical words | Notation aligned with reference worked example A | Minor | Language fixes; Source adds Meingast §2 and Oth §1, Basler version updated to v138 |
| CV-CAPTEURS-002 | $2\times0.050=0.10$ m and 10 px at 10 m recomputed: confirmed (project kinematics). Decimal comma in the expected answer; "$c_x$ the main point" (principal point) altered a technical term. Source cited the Basler shutter page for a kinematic calculation and clock model it does not contain: unsupported citation | Reasoning: convert a time offset into world and image errors | 1 criterion; 373 → 370 lexical words | Consistent with reference worked example B | Minor | Expected-answer decimal fix; language fixes; Source replaced by Rehder §3.1 and labelled project kinematics |
| CV-CAPTEURS-003 | Investigation order (clocks, per-point time, deskew, then extrinsics; static versus motion): consistent with LOAM §III and §V-C and with Rehder §3.3.1 (offset information is carried by motion). Expected answer "Check offsets/drift clocks" was garbled; "Protocol built", "reserved sequence", "Criteria for correction of the case" | Diagnosis: separate timing from spatial calibration errors | 3 criteria; 415 → 422 lexical words | Transform convention $T_{AB}$ (B to A) matches the reference | Minor | Meaning-restoring fix of the expected answer; language fixes; Source given exact LOAM sections and Rehder §3.3.1 |
| CV-CAPTEURS-004 | Radar measures the radial component only: confirmed (TIDUF01 §2.4.9: radar "measures the relative radial velocity between the target and radar sensor"); null space of dimension 2: confirmed by construction. "If the wearer moves, his own movement", "A merger", "zero space", "Elemental Observability" obscured meaning | Understanding: interpret a sensor output under its measurement model | 1 criterion; 387 → 389 lexical words | Consistent with reference mathematics and example C | Minor | Language fixes; Source specifies the TIDUF01 passage |

Expected-answer changes (meaning-restoring language fixes, no change of recall
objective):

- CV-CAPTEURS-002: "0,10 m, before rotation and estimation effects." → "0.10 m,
  before rotation and estimation effects."
- CV-CAPTEURS-003: "Check offsets/drift clocks, time per scan point, deskew then
  extrinsic in the same coordinate frame. Compare motionless sequences and controlled
  movements." → "Check clock offsets and drift, the time of each scan point,
  deskewing, then the extrinsic calibration in a common coordinate frame. Compare
  static sequences with controlled motions."

Defective protected field (not edited; objective lines are invariants): the
objective of CV-CAPTEURS-001 reads "separate exhibition and reading rolling
shutter", a literal translation of *exposition* and *lecture*. Proposed wording:
"Separate exposure from readout in a rolling shutter." No defective question was
found.

## Reference findings

Claims of revision 7 checked against their passages:

- "A short exposure alone does not remove the rolling shutter": confirmed (Meingast
  et al. §2; Basler).
- "With speed $v$ and delay $\Delta t$, an apparent shift of the order of $v\Delta t$
  appears in uniform translation; rotation adds an effect dependent on the lever arm
  and depth": confirmed as kinematics; now derived for a rigid sensor.
- "Doppler radar provides a radial velocity, not directly the full velocity
  vector": confirmed (TIDUF01 §2.4.9).
- "LiDAR/ToF infer a propagation distance": confirmed for round-trip time
  $\tau=2d/c$ (TI SPYY005A eq. 4).
- "A fixed extrinsic pose does not always correct a time delay": confirmed as a
  deduction; Rehder's linearized residual (eqs. 3.2–3.4) shows that offset
  information comes from motion, and a constant-velocity offset can be absorbed by a
  translation.
- No scientific error found. The body was shallow (327 words) and contained
  mistranslations: "measurements IMU", "Obstacles break out especially in turns",
  "sense of transformations" (direction), "provide 0,10 m", "check separately time
  and extrinsic", "Question of work", "Reference Response", "Documentary reference",
  "Elemental Observability", "playback time", "wearer", "his own movement".

New claims verified for revision 8 (main ones):

- Rolling-shutter row timing $t=\bar t+v\,d$ and projection $u(t)=\pi(T(\bar t+vd)p)$
  (Oth et al. §3.2, eq. 6); line-delay definition and one-pose-per-row cost (§1); LED
  calibration as prior state of the art (§2; Meingast et al. §3); line delays
  137.7 µs (nominal 137.5, std 0.56 versus 3.12 µs for the LED method) on a BlueFOX
  camera (§5, Table 1) and 24.12 µs for an iPhone 4S at 1920×1080 (Table 3).
- Meingast et al. §2 eq. 1 (row index linear in time, sign by scan direction).
- LOAM: points received at different times distort the cloud (§I, Fig. 1);
  smooth-velocity assumption, released with an IMU (§III); linear interpolation of
  the pose within a sweep (§V-C, eq. 4).
- Rehder 2018: clock synchronization versus temporal calibration and three
  synchronization schemes, jitter, skew and delay (§3.1); mid-exposure measurement
  instant (§3.1, §3.4.8); offset estimation equations (§3.3.1, eqs. 3.2–3.4);
  offset slope 0.498 against exposure, theory 0.5 (§3.4.4, Fig. 3.7); compensation
  by advancing the trigger by half the exposure (§3.4.8, Fig. 3.15); offset
  precision of a few microseconds and the mid-exposure question (§1.1.4).
- RFC 5905: offset $\theta$ and delay $\delta$ formulas (§8); synchronization
  distance $\lambda=\epsilon+\delta/2$ as "the maximum error due to all causes" (§4).
- TI SPYY005A: $\tau=2d/c$ (eq. 4), $c/(2B)$ and 3.75 cm for 4 GHz (eq. 9),
  $v=\lambda\Delta\Phi/(4\pi T_c)$ (eq. 11), $v_{max}=\lambda/(4T_c)$ (eq. 12),
  $v_{res}=\lambda/(2T_f)$ with $T_f=NT_c$ (eq. 14).
- Basler (v138, 12 November 2026, page marked as a draft): global shutter exposes all
  rows together and reads them row by row; rolling shutter offsets rows by `tRow`;
  readout time "tRow x image ROI height"; Global Reset Release requires flash
  lighting; flash window from the start of exposure of the last row to the end of
  exposure of the first row (Line Source page).
- ROS 2 Jazzy messages: image stamp "should be acquisition time of image", optical
  frame axes, point-cloud stamp "time of sensor data acquisition".

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 327 → 3,854. About
900 tokens are tables, the pseudocode and the Mermaid diagram. The length comes from
four sensor types sharing one timing model and from the separation between
synchronization and temporal calibration; spatial calibration is linked to
CV-MULTICALIB rather than restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Measurement instant and frame as the output; per-sensor inputs with units; transform and image conventions; ROS 2 stamp contract and its silence on the instant; seven possible stamp meanings; pipeline consumers |
| Intuition | Shallow | Developed | Timing error as motion error; rows and sweeps as time series; exposure versus readout; synchronization versus calibration; constructed turning-car illustration; Mermaid diagram of the timing chain |
| Prerequisites | Shallow (one link) | Developed | CV-SE3 kept; links to CV-ACQUISITION, CV-ZHANG, CV-MULTICALIB, CV-FUSION |
| Assumptions | Absent | Developed | Constant line delay and scan direction, smooth motion, rigid mounting, path symmetry, constant offset; observability of offsets through motion; Doppler null space; flash window and velocity wrap-around |
| Procedure | Shallow | Developed | Seven-step timing-chain pseudocode with the purpose of each step |
| Mathematics | Shallow | Developed | NTP offset and delay with asymmetry derivation; clock model; rolling-shutter timing and flash window; rigid-motion error with range; pinhole image error; offset estimation equations; LOAM interpolation; range and FMCW velocity relations; worked examples A (skew), B (timing budget), C (radar limits) |
| Parameters | Shallow (list) | Developed | Eight-row table and a tuning order |
| Properties | Shallow | Developed | Skew independent of exposure; offset precision only with motion; asymmetry bound; interpolation limits; one Doppler component; static calibration does not validate timing |
| Cost and implementation | Shallow | Developed | Parameter cost of per-row poses; deskew cost; ROS 2 Jazzy message contracts; Basler readout and flash-window signals; execution status |
| Evaluation | Shallow | Developed | Published line-delay and offset protocols with their results and setups; proposed baseline and mid-exposure-stamp variation with a confound; measurement limits |
| Failure modes and diagnosis | Shallow (one sentence) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices for shutter, strobe, synchronization scheme, estimation model and sensor; industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/22-capteurs-horodatage.py`](checks/22-capteurs-horodatage.py) (16 checks):
26.0 ms readout and 26 px skew from Oth's line delay; flash-window existence; the
20 px / 0.1 px card case; 0.10 m and 0.52 m errors and their ratio; 12 ms and
24 mm drift; NTP bias of half the path asymmetry and the $\delta/2$ bound; mid-exposure
offsets 0.5–3.5 ms; LiDAR sweep 1.0 m and 1.05 m; 10 px image error against a
finite difference; radar $\lambda$, $v_{max}$, $v_{res}$ and velocity wrap; 3.75 cm
and 0.15 m; Doppler null space.

## Applied corrections

- [Reference](../../../vault/20-acquisition-images/references/22-capteurs-horodatage.md),
  revision 7 → 8: body rewritten and deepened as above; appendices given the same
  language fixes as the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Time model by line" → "Per-row time model",
  "Moving to an image measurement" → "From world error to image error", "Chain of
  transformations to be explained" → "Explicit chain of transformations",
  "Elemental Observability" → "Elementary observability", "Model of measurement" →
  "Measurement model"); sources split into scientific and implementation sources;
  closing provenance line replaced. Front matter unchanged except `revision`; H1 and
  per-card headings unchanged.
- [Cards](../../../vault/20-acquisition-images/22-capteurs-horodatage.md): two
  expected answers fixed as quoted above. Other language fixes: "playback time" →
  "readout time"; "local drag" → "local blur"; "ideal built-in model: reading
  direction, overlay modes" → "idealized constructed model: readout direction,
  overlapping modes"; "Confound sharpness of each line and simultaneity" →
  "Confusing the sharpness of each row with the simultaneity"; "announce the supposed
  clock and movement" → "state the assumed clock and motion"; "advertised model" →
  "stated model"; "main point" → "principal point"; "0,10 m error world" → "a 0.10 m
  world error"; "Discriminant Reasoning" → "Discriminating reasoning"; "Protocol
  built" → "Constructed protocol"; "reserved sequence" → "held-out sequence"; "time
  chain" → "timing chain"; "a point LiDAR … to the camera of $t_C$" → "a LiDAR point
  … into the camera frame at $t_C$"; "Fix permanently by fixed translation" →
  "Compensating permanently with a fixed translation"; "Criteria for correction of
  the case … Case built" → "Grading criteria for the case … Constructed case";
  "If the wearer moves, his own movement" → "If the carrier platform moves, its own
  motion"; "A merger" → "A fusion filter"; "zero space" → "null space"; French
  decimal commas. Source lines given exact sections; the unsupported Basler citation
  of CV-CAPTEURS-002 replaced. Questions, IDs, objectives, families, tags and target
  deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for
`playback`, `Doppler`, `rolling shutter`, `0,10 m`). CV-VIO, CV-MULTICALIB,
CV-ZHANG, CV-BA, CV-PIPELINE and CV-FLOT mention rolling shutter or timing
consistently with this note.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run). The 2026-10-18 proposal "Building a time error budget"
(design) remains in its report without a register entry; it is not repeated here.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-CAPTEURS-01 | CV-CAPTEURS | Explain why an image stamped at trigger time is offset by half its exposure from its measurement instant, why auto-exposure turns this into a varying offset, and name a hardware or software remedy | Stamp semantics, the most frequent hidden offset, are developed in the reference but untested | Diagnosis; Assumptions and Evaluation | 1 card, 3 criteria | [Rehder 2018, §3.4.4 Fig. 3.7 and §3.4.8](https://doi.org/10.3929/ethz-b-000334970) |
| P-CV-CAPTEURS-02 | CV-CAPTEURS | From four NTP timestamps, compute offset and round-trip delay, then the offset bias caused by unequal outbound and return delays and the $\delta/2$ bound | No card trains the synchronization step or its blind spot (path asymmetry) | Reasoning; Mathematics | 1 card, 3 criteria | [RFC 5905, §4 and §8](https://www.rfc-editor.org/rfc/rfc5905) |

## Sources

Scientific sources, opened at the passages listed:

- Meingast, Geyer and Sastry, [arXiv cs/0503076v1 PDF](https://arxiv.org/abs/cs/0503076):
  abstract, §1, §2 (eq. 1 and exposure assumption), §3 (Table 2).
- Oth et al., [CVPR 2013 open-access PDF](https://openaccess.thecvf.com/content_cvpr_2013/papers/Oth_Rolling_Shutter_Camera_2013_CVPR_paper.pdf):
  abstract, §1, §2, §3.2 (eq. 6), §5 (Tables 1–3).
- Zhang and Singh, [LOAM, RSS 2014 PDF](https://www.roboticsproceedings.org/rss10/p07.pdf):
  Fig. 1 caption, §II, §III, §V-C (eqs. 4–8).
- Rehder, [ETH doctoral thesis 2018](https://doi.org/10.3929/ethz-b-000334970),
  downloaded from the ETH Research Collection: §1.1.1, §1.1.4, §3.1, §3.3.1
  (eqs. 3.2–3.5), §3.4.4 (Fig. 3.7 caption), §3.4.8 (Fig. 3.15 caption).
- [RFC 5905](https://www.rfc-editor.org/rfc/rfc5905.txt): §4 (synchronization
  distance), §8 (on-wire protocol formulas and the negative-delay note).
- Iovescu and Rao, [TI SPYY005A](https://www.ti.com/lit/wp/spyy005a/spyy005a.pdf)
  (text extracted with `pdftotext`; the layered layout made extraction noisy, and
  equations 4, 9, 11, 12 and 14 were read from the extracted fragments).
- [TI TIDUF01](https://www.ti.com/lit/ug/tiduf01/tiduf01.pdf): §2.4.9.

Implementation sources:

- [Basler, Electronic Shutter Types](https://docs.baslerweb.com/electronic-shutter-types)
  and [Basler, Line Source](https://docs.baslerweb.com/line-source#flash-window),
  read with WebFetch (first 100,000 characters of each page; pages marked as draft).
- ROS 2 common_interfaces at commit
  [a941f14](https://github.com/ros2/common_interfaces/tree/a941f14bb318d8d904505ed935ccbb97f24a70a4)
  (Jazzy branch): `sensor_msgs/msg/Image.msg`, `sensor_msgs/msg/PointCloud2.msg`,
  `std_msgs/msg/Header.msg`.

Failed accesses and limits:

- IEEE 1588 (PTP): standard not openly available; not consulted. The note states the
  two-way principle from RFC 5905 and marks PTP-specific claims as unverified.
- Furgale, Rehder and Siegwart, IROS 2013: the author-hosted PDF returned HTTP 404;
  its content was read through Rehder's thesis, which incorporates it.
- Forster et al. (IMU preintegration): retained from earlier passes, not re-read and
  not used for any claim.
- Context7 was not available in this session.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | Fails only on `80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md` (another agent's in-progress file: "missing local link … $$"); no error in this subject's files |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/22-capteurs-horodatage.py` | 16 checks passed |
| `git diff --check -- vault/20-acquisition-images/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/20-acquisition-images/22-capteurs-horodatage.md` | 4 cards, 371, 370, 422 and 389 words, no anomaly |
| Protected-field comparison with the pre-edit copy | No protected-field error: card headings (including the `#cv-capteurs-003` link target), `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` unchanged; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged |
| Local links and anchors under `vault/20-acquisition-images` and `vault/01-Parcours` | 0 errors |

No sensor, synchronization or deskew code was executed; the proposed baseline and
variation are protocols, not results. The Mermaid diagram and tables were not
rendered in Obsidian, and AnkiDroid rendering of the corrected cards is unverified.
This is agent self-review, without independent scientific validation or measurement
of learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-CAPTEURS revision 8, CV-CAPTEURS-001 to -004, corrections listed above, Agent
Claude Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-CAPTEURS-01, P-CV-CAPTEURS-02).
