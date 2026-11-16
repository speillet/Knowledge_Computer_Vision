# Review — SO(3), SE(3) and transformation conventions — 2026-11-16

## Overview

Mode: `ajouter` for the accepted proposal P-CV-SE3-01. One card added, CV-SE3-007;
the six existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/12-rotations-se3.md)) and are
byte-for-byte unchanged.
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 11 → 12.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-SE3-007 | Covariance on the right tangent and its adjoint transport (§II-H eq. 51–54), the identity $X\operatorname{Exp}(\tau)X^{-1}=\operatorname{Exp}(\mathrm{Ad}_X\tau)$ (§II-F, derivation before eq. 29), $\mathrm{Ad}_{X^{-1}}=\mathrm{Ad}_X^{-1}$ and $\mathrm{Ad}_{XY}=\mathrm{Ad}_X\mathrm{Ad}_Y$ (eq. 33–34), composition Jacobians $\mathrm{Ad}_Y^{-1}$ and $I$ (eq. 65–66, 177–178), $SE(3)$ adjoint for $(\rho,\theta)$ (eq. 175), $SE(3)$ Exp with $V(\theta)$ (eq. 172–174) and the action Jacobian $[R,\ -R[p]_\times]$ (eq. 182): confirmed on arXiv 1812.01537v9. GTSAM 4.2 rotation-first order (`Pose3.h` L138–L141) and `translation` Jacobian $[0_3,R]$ (`Pose3.cpp` L308–L310): confirmed. Exactness of the transport, closed form $\rho_c=R_{bc}^T(\rho_b+\theta_b\times t_{bc})$, every number (2 mm, 5.39 mm, $\pm5\cdot10^{-5}$ m·rad, $\pm0.93$, factor 2.7, $(-0.025,4.99992,0)$ mm, world 5.39/2/5.39 mm, about 1 m on the global tangent) and the sign flip under $\mathrm{Ad}_{T_{bc}}$: project derivations, recomputed by the check script | Reasoning: computes a lever-arm covariance, interprets its coupling and separates a tangent translation from an origin displacement. Distinct from CV-SE3-003 (which side to perturb and why two Jacobians differ); does not compare $SE(3)$ and composite charts (pending P-CV-SE3-02) | 3 expected criteria (transport rule and numbers; meaning and sign of the coupling, loss in the copied covariance; frame of the translation block and its world reading); 607 lexical words, of which 396 outside formulas | Frames named $T_{\text{to,from}}$, block order $(\rho,\theta)$ and right increments as in the reference; worked example A extended with the same numbers | Reasoning |

The question states the pose direction, the side of the increment, the block order,
the units and an exact extrinsic, so each number has one value. It names neither the
adjoint nor the lever-arm term. The answer is longer than its siblings (387 to 445
lexical words) because the inline formulas count as words under the `\w+` convention
and because it carries the computation, its interpretation and the frame of the result.

## Reference findings

Worked example A and the covariance paragraph of Mathematics were checked against
§II-F, §II-H, §III-B and App. D. The adjoint, its use on the lever arm, the 5 mm first-order
increment and the 25 µm second-order remainder are correct (recomputed again here).
Two statements were imprecise:

- Worked example A said that a body yaw uncertainty of 0.01 rad "implies 5 mm of
  camera-position uncertainty". With a body position uncertainty, that 5 mm adds in
  variance, not in standard deviation: for 2 mm of body position the camera has
  $\sqrt{2^2+5^2}\approx5.39$ mm, not 7 mm. Minor; reworded.
- The assumption bullet said that large uncertainties make "first-order transport
  inaccurate". Transport through the adjoint by a known transformation is an exact linear
  map of the tangent vector, because $X\operatorname{Exp}(\tau)X^{-1}=\operatorname{Exp}(\mathrm{Ad}_X\tau)$
  for any $\tau$ (§II-F); only propagation through a nonlinear function (eq. 43, 55) and the
  reading of a tangent translation as a displacement ($V(\theta)\rho$, eq. 172) are first
  order. Minor; reworded. The check script confirms the identity on 400 random increments
  with rotations up to about 1.4 rad, with an identity and a rotated extrinsic.

No other statement of the reference was found to be wrong. The reference did not call
P-CV-SE3-01 pending, so no such text needed replacing.

Existing card not edited: the explanation of CV-SE3-003, copied in the reference's
"Additional technical explanations", says that $P_G=\operatorname{Ad}_TP_L\operatorname{Ad}_T^T$ holds "in
this local approximation". Read as "within the tangent-space Gaussian model", it is
correct. Read as "the transport is approximate", it is imprecise for the reason above.
The card was preserved as required in `ajouter` mode. A one-phrase clarification could be
made in a later `approfondir` pass.

## Applied corrections

- `vault/10-mathematiques-estimation/references/12-rotations-se3.md`, revision 11 → 12:
  worked example A, with the "5 mm" sentence reworded and a paragraph added for the
  card's covariance, coupling, conditional variance, wrong-direction sign test and
  world-axis reading. The "First-order perturbations" assumption bullet is reworded. A
  Mathematics paragraph covers exact rigid-attachment transport, the closed form, the
  identity Jacobian for an uncertain extrinsic, where approximation enters, and the global
  increment shared by body and camera. One failure-mode row covers a position–rotation
  correlation of the wrong sign. The scientific sources add §III-B eq. 61–66, and the
  implementation sources add GTSAM `translation` Jacobian L308–L310. CV-SE3-007 is
  listed under related flashcards, and the closing provenance line is extended. Front
  matter is unchanged except `revision`; `statut: redige` and `provenance: agent` are kept.
- `vault/10-mathematiques-estimation/12-rotations-se3.md`: CV-SE3-007 appended after
  CV-SE3-006. The first 21,289 bytes, the whole file at `HEAD` with its six blocks, are unchanged.
- `docs/revues/2026-11-09-four-proposals/checks/12-rotations-se3.py`: new stdlib
  recomputation script (11 checks).

No other vault card repeats either reworded statement. The search covered "first-order
transport", "5 mm of camera-position", "lever arm", "lever-arm" and `T_{cb}}` over `vault/`;
the other lever-arm passages concern hand–eye, ICP, timestamps and multi-sensor
calibration, and do not involve covariance transport.

For the correction log (to be entered by the coordinator): CV-SE3 revision 12, 2026-11-16;
CV-SE3-007 added from P-CV-SE3-01. Worked example A changed from "implies 5 mm of
camera-position uncertainty" to "adds, in quadrature, 5 mm of camera-position standard
deviation along $y$, correlated with the yaw", because the lever-arm term adds in
variance (2 mm and 5 mm give 5.39 mm, recomputed by
checks/12-rotations-se3.py of this pass). The assumption bullet changed from "first-order
transport inaccurate" to "first-order propagation inaccurate", with adjoint transport by a
known transformation kept exact (Solà et al., arXiv 1812.01537v9, §II-F derivation before
eq. 29, eq. 65, 177). A failure-mode row was added for a wrong-sign position–rotation
correlation from $\mathrm{Ad}_{T_{bc}}$. No existing card repeats either statement. Agent
Claude Code self-review, without independent validation; export status to republish with
`paquet-anki`.

## Proposals

P-CV-SE3-01: accepted by the learner on 2026-11-09, completed as CV-SE3-007. The register
row cites §II-H only; the card also rests on §II-F, §III-B and App. D, and its Source line
gives those passages. P-CV-SE3-02 (exponential versus chart differences between libraries)
remains pending and is not encroached: the card uses $V(\theta)$ only to separate a tangent
translation from the displacement of an origin, and compares no charts. No new proposal.

## Sources

Scientific sources:

- Solà, Deray and Atchuthan, "A micro Lie theory for state estimation in robotics",
  [arXiv HTML v9](https://arxiv.org/html/1812.01537v9), downloaded on 2026-11-16 and read
  as text with its LaTeX formulas: §II-E eq. 25–27 and footnote 3 (frame convention);
  §II-F, the derivation before eq. 29, eq. 29–34 and the $SE(3)$ adjoint example; §II-G
  eq. 41a–43 and the rotation-action example; §II-H eq. 51–55 and the horizontal-plane
  example; §III-B eq. 61–66; App. B eq. 139; App. D eq. 168–183.

Implementation sources (Context7 is unavailable in this session):

- GTSAM 4.2, GitHub raw at tag `4.2`: `gtsam/geometry/Pose3.h` L136–L162
  (canonical coordinates $[R_x,R_y,R_z,T_x,T_y,T_z]$, `AdjointMap` and `Adjoint`
  comments) and L284–L290; `gtsam/geometry/Pose3.cpp` L55–L63 (`AdjointMap` gives
  $[R\ 0;\ A\ R]$) and L308–L310 (`translation` Jacobian `Z_3x3, rotation().matrix()`).

No access failed. No library was executed. Claims of the reference outside this card's
scope (quaternion conventions, OpenCV, Eigen, SciPy, Ceres, Sophus, REP 103, `gluLookAt`)
were not re-read in this pass.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 -I docs/revues/2026-11-09-four-proposals/checks/12-rotations-se3.py` | 11 checks passed |
| `python3 -I docs/revues/2026-11-14-reference-depth/checks/12-rotations-se3.py` | 14 checks passed (earlier examples of the reference unchanged) |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 298 cards (shared tree, other agents' cards included) |
| `python3 scripts/learning_path.py` | OK: 60 references, 298 cards, 0 errors |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/10-mathematiques-estimation/12-rotations-se3.md` | 7 cards, no anomaly; CV-SE3-007 607 lexical words; next free ID CV-SE3-008 |
| `git diff --check -- vault/10-mathematiques-estimation/` | No whitespace error |
| `python3 scripts/sync_catalog.py --check` | 8 of 19 generated documents stale, expected after card additions; regeneration is left to the coordinator |

The check script uses exact fractions for the covariance numbers and floats for the
exponential, logarithm and finite-difference Jacobians. It verifies the identities on
random increments rather than proving them. The exactness of the transport assumes the
rotation increment stays within the principal branch of the logarithm ($|\theta|<\pi$),
which $\mathrm{Ad}$ preserves since $|R\theta|=|\theta|$. The scenario (IMU covariance, 0.5 m
arm, 100 m from the world origin) is a constructed project example, not a measured
system. Agent self-review only; no independent scientific validation. The Obsidian and
AnkiDroid rendering of the card and of the new reference passages is not verified.
Export status: to republish with `paquet-anki`. The proposal register, the progress log,
the generated catalogue and the counts are left to the coordinator.
