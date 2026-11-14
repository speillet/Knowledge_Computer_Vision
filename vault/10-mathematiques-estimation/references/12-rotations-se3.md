---
id: CV-SE3
type: methode
domaine: d01
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 11
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# SO(3), SE(3) and transformation conventions

This method note covers how rotations and rigid poses are represented, composed,
inverted, perturbed, differentiated and compared, and how libraries encode them. Its
practical goal is a pose that means the same thing on both sides of every interface:
calibration to tracking, estimator to renderer, C++ optimizer to Python evaluation.
The Lie-group tools are presented at the depth that pose estimation, calibration and
fusion need, following Solà et al.'s "micro Lie theory".

## Problem and data contract

**Task.** Map points and directions between named coordinate frames; compose and
invert rigid transformations; parameterize small rotation or pose increments for
optimization and filtering; propagate their uncertainty; and measure the difference
between two orientations or poses.

**Inputs and their contracts.**

- A rotation $R\in SO(3)$: a $3\times3$ real matrix with $R^TR=I$ and $\det R=+1$, in
  double precision, orthonormal only up to rounding after many compositions.
- A translation $t\in\mathbb R^3$ in metres (or the unit of the scene model).
- A pose written $T_{ab}=(R_{ab},t_{ab})$, or as the $4\times4$ matrix
  $\begin{bmatrix}R_{ab}&t_{ab}\\0&1\end{bmatrix}$, which maps coordinates expressed in
  frame $b$ to coordinates in frame $a$: $p_a=R_{ab}p_b+t_{ab}$. Setting $p_b=0$ shows
  that $t_{ab}$ is the origin of $b$ expressed in $a$, and the columns of $R_{ab}$ are
  the axes of $b$ expressed in $a$ (project deductions from the definition).
- Alternative rotation encodings: a unit quaternion (four numbers whose order and
  algebra must be stated), a rotation vector $\theta u$ in radians (OpenCV `rvec`,
  $3\times1$), or Euler angles with a stated axis sequence and unit.
- Tangent increments: $\delta\theta\in\mathbb R^3$ (rad) for rotations, a 6-vector for
  poses whose block order ($[\rho,\theta]$ or $[\theta,\rho]$) and side (right/local or
  left/global) must be stated; covariances on those increments are $3\times3$ or
  $6\times6$ with units rad², m·rad and m².

**Outputs.** Transformed points (metres), composed or inverted poses, increments and
Jacobians in a declared tangent convention, covariances transported to the frame where
they are used, and error measures (a geodesic angle in radians, a translation error in
metres in a stated frame).

**Role in a pipeline.** Every geometric module exchanges poses: extrinsic and hand–eye
calibration ([CV-MULTICALIB](../../50-calibration-geometrie/references/55-calibration-multicapteurs.md),
[CV-HANDEYE](../../50-calibration-geometrie/references/57-calibration-hand-eye.md)),
PnP and relative pose ([CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md)),
bundle adjustment ([CV-BA](../../50-calibration-geometrie/references/54-bundle-adjustment.md)),
visual-inertial odometry ([CV-VIO](../../60-vision-3d/references/63-slam-vio.md)),
filters ([CV-FUSION](13-kalman-ekf-eskf.md)) and pose graphs
([CV-FACTEURS](14-graphes-facteurs.md)). Upstream modules must deliver, with each pose,
its target and source frames, timestamp, units and encoding; downstream modules
assume the same. A homogeneous matrix does not state its own meaning: two valid
matrices that differ by an inverse or an axis convention both pass numerical sanity
checks.

## Intuition

Three ideas carry most of the subject.

1. **Indices cancel.** Writing every pose as $T_{\text{to},\text{from}}$ makes
   composition a bookkeeping exercise: $T_{ac}=T_{ab}T_{bc}$ is valid because the inner
   indices match, and $T_{ba}=T_{ab}^{-1}$ swaps them. Most pose bugs are a missing
   inverse or a product in the wrong order that this notation exposes.
2. **Rotations live on a curved space.** Adding two rotation matrices does not give a
   rotation. Small changes are made in a flat tangent space of three numbers and wrapped
   onto the group by the exponential map, either after the current rotation, in its own
   (local) frame, or before it, in the global frame. The two choices are equally valid
   and related by the adjoint; mixing them silently produces Jacobians and covariances
   expressed in the wrong frame.
3. **A rotation about one point moves every other point.** For poses, an angular
   increment at one frame induces a translation at any frame with a lever arm. The
   adjoint of $SE(3)$ contains this lever-arm term explicitly.

### Worked example A: lever arm of a camera on an IMU

Constructed example, recomputed by checks/12-rotations-se3.py. A camera $c$ is rigidly
mounted on an IMU body $b$ with $R_{bc}=I$ and $t_{bc}=(0.5,0,0)^T$ m. Perturb the body
pose on the right by a yaw of 0.01 rad (0.57°), $\xi_b=(\rho,\theta)=(0,(0,0,0.01))$.
The camera pose changes by $\xi_c=\mathrm{Ad}_{T_{cb}}\xi_b$ with $T_{cb}=T_{bc}^{-1}$:
its rotation increment is the same 0.01 rad, and its translation increment is
$[-t_{bc}]_\times\theta=(0,0.005,0)$ m, i.e. 5 mm along the camera's $y$ axis. The
exact displacement of the camera origin agrees to first order; the remaining
second-order term is 25 µm. A yaw uncertainty of 0.01 rad on the body therefore
implies 5 mm of camera-position uncertainty, a cross term that a block-by-block
rotation of the covariance would miss.

## Prerequisites and competencies

**Required prerequisites**: [vault conventions](../../01-Parcours/Pre-requis.md);
orthogonal matrices, cross products and skew-symmetric matrices, the matrix
exponential, and first-order covariance propagation $\Sigma_y\approx J\Sigma_xJ^T$.
Useful links:

- Jacobians, Gauss–Newton and covariance of an estimate: [CV-SVD](11-moindres-carres-svd.md);
- camera extrinsics and the pinhole model: [CV-ZHANG](../../50-calibration-geometrie/references/52-calibration-zhang.md), [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md);
- error-state filtering on rotations: [CV-FUSION](13-kalman-ekf-eskf.md);
- poses as graph variables and gauge freedom: [CV-FACTEURS](14-graphes-facteurs.md);
- timestamps attached to poses: [CV-CAPTEURS](../../20-acquisition-images/references/22-capteurs-horodatage.md).

**Target competencies**: compose and invert named poses, choose and state a
perturbation convention, transport Jacobians and covariances between conventions,
convert between library encodings with tests that discriminate errors, and measure
rotation errors with a parameterization-independent metric.

## Assumptions, observability and degenerate cases

- **Right-handed frames.** REP 103 states that "all systems are right handed"; a
  matrix with determinant $-1$ is a reflection, not a pose, and no rotation converts
  between a right- and a left-handed frame.
- **Orthonormality is numerical.** Products of many rotations drift away from $SO(3)$;
  re-projection onto the group is needed (see Mathematics).
- **First-order perturbations.** Jacobians and the tangent-space Gaussian
  $\mathcal N(\bar X,\Sigma)$ rely on $f(X\oplus\tau)\approx f(X)\oplus J\tau$ for small
  $\tau$ [Solà et al., eq. 43, §II-H]. Uncertainties of tens of degrees make
  first-order transport inaccurate (project deduction).
- **Logarithm range.** The rotation angle from the trace lies in $[0,\pi]$. The matrix
  logarithm $\theta(R-R^T)^\vee/(2\sin\theta)$ [eq. 135] has a vanishing denominator at
  $\theta=0$ (handled by a small-angle expansion) and at $\theta=\pi$, where
  $R=R^T$ and the axis must be recovered from $R+I$, with an inherent sign ambiguity
  (project deduction from eq. 135).
- **Double cover.** $q$ and $-q$ represent the same rotation; the quaternion logarithm
  needs $w\ge0$ to return an angle in $[0,\pi]$ [Solà et al., App. B, eq. 133].
- **Euler singularities.** For the ZYX sequence, at a pitch of ±90° yaw and roll act
  about the same axis and only their difference (or sum) is defined (worked example D).
- **Same time instant.** Composing $T_{wb}(t_1)$ with $T_{bc}$ and a measurement taken
  at $t_2$ assumes no motion in between; timestamps belong to the pose contract.
- **Observability.** Conventions do not create information: a monocular relative pose
  has an unknown scale, and a pose graph without an anchor has a free global frame
  (see CV-EPIPOLAIRE and CV-FACTEURS).

## Procedure

```text
1. name frames:      every pose is T_<to><from> with (to, from, time, unit)
2. convention card:  pose direction; quaternion order (wxyz | xyzw) and algebra
                     (Hamilton | JPL); perturbation side (right/local | left/global);
                     tangent block order ([rho, theta] | [theta, rho]); angle unit;
                     Euler sequence if any
3. boundaries only:  parse external encodings into one internal form; emit at exits
4. boundary tests:   identity; quarter turns mapping e_x -> e_y, e_y -> e_z, e_z -> e_x;
                     a translated point; two non-commuting rotations composed; round trip
5. compose/invert:   (R, t) blocks; re-orthonormalize R when drift exceeds a tolerance
6. differentiate:    perturb on the declared side; check Jacobians by finite differences
                     applied on the same side and in the same frame
7. transport:        Jacobians and covariances to another side or frame with the adjoint
8. evaluate:         geodesic angle and translation error in a stated frame
```

Purpose of the steps. *Naming* turns composition errors into visible index mismatches.
The *convention card* records the four quaternion choices of Solà (component order,
algebra, active or passive function, direction of the operator) [Quaternion
kinematics, §3.1] plus the two choices that matter for optimization (side and block
order). *Converting at the boundaries only* keeps one convention inside the code.
*Boundary tests* must discriminate: a quarter turn about $z$ distinguishes the
component order (read in the wrong order it becomes a turn about $x$), a non-commuting
pair distinguishes the multiplication order, and a translated point distinguishes
$T$ from $T^{-1}$; an identity or a round trip alone can pass with a shared error.
*Finite-difference checks* only validate a Jacobian against the convention used to
perturb. *Transport* keeps uncertainty consistent with the frame of its consumer.

## Mathematics, conventions and units

### Composition and inversion

With $p_a=R_{ab}p_b+t_{ab}$, composition and inversion are [Solà et al., eq. 170–171]

$$T_{ac}=T_{ab}T_{bc}=(R_{ab}R_{bc},\;t_{ab}+R_{ab}t_{bc}),\qquad T_{ab}^{-1}=(R_{ab}^T,\;-R_{ab}^Tt_{ab}) .$$

The translation $t_{bc}$, expressed in $b$, is rotated into $a$ before the addition.
For two camera poses given in the world, $T_{c_1c_2}=T_{wc_1}^{-1}T_{wc_2}$, whose
translation $R_{wc_1}^T(t_{wc_2}-t_{wc_1})$ is the baseline expressed in camera 1, not a
difference of world coordinates. A homogeneous direction $[d^T,0]^T$ receives the
rotation but not the translation. Translations keep length units; rotation increments
are in radians.

### Exponential map and tangent increments

For a rotation of angle $\theta$ about the unit axis $u$, the exponential map (Rodrigues
formula) and its inverse are [App. B-A, eq. 134–135]

$$R=\operatorname{Exp}(\theta u)=I+\sin\theta\,[u]_\times+(1-\cos\theta)[u]_\times^2,\qquad
\theta=\arccos\frac{\operatorname{tr}(R)-1}{2},$$

where $[u]_\times$ is the skew-symmetric matrix with $[u]_\times v=u\times v$. `Exp` takes a
vector of $\mathbb R^3$; `exp` takes the skew matrix $[\theta u]_\times$. Increments are
applied on the right or on the left [§II-E, eq. 25–28]:

$$X\oplus{}^X\tau=X\operatorname{Exp}({}^X\tau)\quad(\text{local}),\qquad
{}^E\tau\oplus X=\operatorname{Exp}({}^E\tau)\,X\quad(\text{global}).$$

Solà et al. use local (right) perturbations by default [§II-E]. The derivative of the
rotation action with a right perturbation is $\partial(Rp)/\partial\theta=-R[p]_\times$
[eq. 150]; with a left perturbation it is $-[Rp]_\times$, and both describe the same
point change once $\delta\theta_G=R\,\delta\theta_L$ (project derivation, consistent with
eq. 139).

### Adjoint, Jacobians and covariance transport

Local and global increments are related by the adjoint,
${}^E\tau=\mathrm{Ad}_X\,{}^X\tau$ [§II-F, eq. 29–32], with [eq. 139 and 175]

$$\mathrm{Ad}_R=R\ \ \text{on }SO(3),\qquad
\mathrm{Ad}_T=\begin{bmatrix}R&[t]_\times R\\0&R\end{bmatrix}\ \ \text{on }SE(3)\ \text{for}\ \tau=(\rho,\theta).$$

Consequently a Jacobian with respect to a local increment equals the global one times
the adjoint, $J_L=J_G\,\mathrm{Ad}_X$ ($J_L=J_GR$ on $SO(3)$), and covariances transform as
${}^E\Sigma=\mathrm{Ad}_X\,{}^X\Sigma\,\mathrm{Ad}_X^T$ [eq. 54]. A global specification is
sometimes natural: Solà et al.'s example is an orientation known up to rotations in the
horizontal plane, ${}^E\Sigma=\operatorname{diag}(\sigma_\phi^2,\sigma_\theta^2,\infty)$
[§II-H]. General propagation through $f$ uses $\Sigma_Y\approx J\Sigma_XJ^T$ with
Jacobians defined on the manifold [eq. 55]. Worked example A applies the $SE(3)$ adjoint
to a lever arm.

### $SE(3)$ exponential versus composite parameterizations

The $SE(3)$ exponential of $\tau=(\rho,\theta)$ is [App. D-B, eq. 172–174]

$$\operatorname{Exp}(\tau)=\begin{bmatrix}\operatorname{Exp}(\theta)&V(\theta)\rho\\0&1\end{bmatrix},\qquad
V(\theta)=I+\frac{1-\cos\theta}{\theta^2}[\theta]_\times+\frac{\theta-\sin\theta}{\theta^3}[\theta]_\times^2 ,$$

so $\rho$ is *not* the translation: $SE(3)$ moves along a screw, translating and rotating
simultaneously. Solà et al. contrast it with $T(3)\times SO(3)$, whose right plus adds
$R\,p$ to the translation, and with the composite $\langle\mathbb R^3,SO(3)\rangle$, which
adds $p$ in the global frame and lets rotation and translation not interact [§IV].
*Worked example B (constructed, recomputed by checks/12-rotations-se3.py)*: for
$\rho=(1,0,0)$ m and a quarter turn $\theta=(0,0,\pi/2)$, $V(\theta)\rho=(2/\pi,2/\pi,0)\approx(0.637,0.637,0)$
m, the 0.900 m chord of a quarter circle of arc length 1 m, whereas the
$T(3)\times SO(3)$ step translates by $(1,0,0)$ m. For an optimizer step from $\tau=0$
the first two charts share their Jacobians, because $V(\theta)=I+O(\theta)$; the
composite chart differs at first order, because its translation increment is global
instead of local (project deduction from §IV).

### Quaternions

A Hamilton unit quaternion $q=(w,v)$ encodes $\operatorname{Exp}(\theta u)=(\cos\frac\theta2,\,u\sin\frac\theta2)$,
rotates vectors by $x'=q\,x\,q^*$ and corresponds to the matrix of eq. 138
[App. B-A, B-B, eq. 132–138]. Its logarithm is $2v\arctan(\|v\|,w)/\|v\|$; flipping $q$
to $-q$ when $w<0$ keeps the angle in $[0,\pi]$ [eq. 133]. The angle between $q$ and the
identity in $\mathbb R^4$ is half the rotation angle [Quaternion kinematics, §2.4.6,
eq. 110–112], hence the relative rotation angle $\theta=2\arccos|\langle q_1,q_2\rangle|$,
whose absolute value absorbs the double cover (project derivation). Hamilton and JPL
differ in all four binary choices except the active/passive one: component order,
algebra ($ij=k$ versus $ij=-k$), and whether right-to-left products mean
local-to-global or global-to-local [Quaternion kinematics, §3.1, eq. 140–143, Table 2].
Storing the scalar last, as Eigen does, does not make a quaternion JPL if the other
three choices are Hamilton's [§3.1.1]. Interpolation between orientations uses
$q(t)=q_0\otimes\operatorname{Exp}(t\operatorname{Log}(q_0^*\otimes q_1))$, or
$R(t)=R_0\operatorname{Exp}(t\operatorname{Log}(R_0^TR_1))$ for matrices [§2.7, eq. 124–128].

### Projection onto $SO(3)$

A noisy or linear estimate $M$ (from a DLT, Zhang's closed form or a drifted product) is
projected with the SVD $M=U\Sigma V^T$: $R=U\,\operatorname{diag}(1,1,s)\,V^T$ with $s=-1$
when $\det U\det V<0$ and $s=1$ otherwise, which is the determinant correction of
Umeyama's method as implemented in Eigen 3.4 [`Umeyama.h` L136–L143]. Without the
correction, $UV^T$ can be a reflection.

### Worked example C: precision of the angle formulas

Constructed example, recomputed by checks/12-rotations-se3.py. For a rotation of
$10^{-8}$ rad about $z$, $(\operatorname{tr}R-1)/2$ rounds to exactly 1 in double
precision and the arccos formula returns 0; at $10^{-6}$ rad it is off by about
$4\cdot10^{-5}$ relative. The form $\theta=\operatorname{atan2}(\tfrac12\|(R-R^T)^\vee\|,\,(\operatorname{tr}R-1)/2)$,
or $2\operatorname{atan2}(\|v\|,|w|)$ for a quaternion, recovers $10^{-8}$ rad to machine
precision. This matters for finite-difference Jacobian checks, whose steps are often
near $10^{-8}$.

## Parameters and tuning

The "parameters" of this subject are conventions; they are decided and documented,
not tuned. A tuning approach is therefore not applicable; it is replaced by the
convention card and the discriminating tests of the procedure.

| Convention | Options | Where libraries fix it | What a mismatch does | Discriminating test |
| --- | --- | --- | --- | --- |
| Pose direction | $T_{wc}$ (camera→world) or $T_{cw}$ (world→camera) | OpenCV `solvePnP`: `rvec`, `tvec` bring model points into the camera frame | Inverse pose: camera centre at $t$ instead of $-R^Tt$ | Project a known point; recover the centre as $-R^Tt$ |
| Quaternion order | $(w,x,y,z)$ or $(x,y,z,w)$ | Eigen constructor $w$ first, storage $[x,y,z,w]$; SciPy scalar last by default; Ceres `QuaternionManifold` $[w,x,y,z]$ | A different rotation, often about another axis | Quarter turn about $z$ maps $e_x$ to $e_y$ |
| Quaternion algebra and direction | Hamilton or JPL | Hamilton in Eigen, ROS and Ceres [Quaternion kinematics, §3.1] | Inverse rotation, wrong composition order | Compose two non-commuting quarter turns |
| Perturbation side | Right (local) or left (global) | Solà et al. right by default; Ceres `QuaternionManifold` left product | Jacobians and covariances in another frame | Same physical perturbation, compare transformed points |
| Tangent block order | $[\rho,\theta]$ or $[\theta,\rho]$ | Solà et al. and Sophus $[\rho,\theta]$; GTSAM `Pose3` $[\omega,v]$ | Covariance blocks swapped; adjoint transposed by blocks | Perturb only the rotation and see which block responds |
| Tangent scale | Full angle or half angle | Ceres quaternion tangent is half the rotation vector | Steps and covariances off by a factor 2 or 4 | A tangent step of norm $\delta$ rotates by $\delta$ or $2\delta$ |
| Camera axes | OpenCV $x$ right, $y$ down, $z$ forward; OpenGL looks along $-z$, $y$ up; ROS body $x$ forward, $y$ left, $z$ up | Library documentation | Scene upside down or behind the camera | A point in front must stay in front |

Numerical settings are the only tunable quantities: the angle below which Exp, Log and
Jacobians switch to Taylor expansions (GTSAM's `ComputeQforExpmapDerivative` defaults
`nearZeroThreshold` to $10^{-5}$ [Pose3.h L221–L222]; Sophus 1.22.10 takes its small-angle
branch when $\theta^2<(10^{-10})^2$ in double precision [so3.hpp L282]), and the
frequency of re-orthonormalization. Test them with angles from $10^{-10}$ to $\pi$ and
with long chains of compositions.

## Properties and limits of guarantees

- **Group structure.** Composition is associative, has an identity and cheap inverses,
  and is not commutative; $SO(3)$ and $SE(3)$ have 3 and 6 degrees of freedom.
- **Bi-invariant error angle.** Because $\operatorname{tr}(R_1^TQ^TQR_2)=\operatorname{tr}(R_1^TR_2)$
  and $\operatorname{tr}(Q^TR_1^TR_2Q)=\operatorname{tr}(R_1^TR_2)$, the geodesic angle is
  unchanged when both rotations are expressed in another frame, on either side (project
  derivation). It does not depend on the parameterization.
- **Jacobians.** Left and right Jacobians of $SO(3)$ satisfy $J_l=J_r^T$ [eq. 147] and
  tend to $I$ for small angles; first-order transport is exact only for linear maps.
- **Representations.** A matrix has 9 numbers and no singularity; a unit quaternion has 4
  numbers, no singularity and a double cover; a rotation vector has 3 numbers and wraps at
  $\pi$; Euler angles have 3 numbers, 24 conventions (REP 103) and singular
  configurations. Zhou et al. show that every representation of 3-D rotations in a real
  Euclidean space of four or fewer dimensions is discontinuous, including quaternions and
  Euler angles, while 5-D and 6-D continuous representations exist [Zhou et al. 2019,
  abstract]; this matters when a network regresses rotations.
- **Charts.** $SE(3)$ and $T(3)\times SO(3)$ give different poses for the same finite
  6-vector (worked example B); they agree only to first order at the origin.

## Cost and implementation

Computational cost is rarely the constraint (project counts): composing $(R,t)$ costs
36 multiplications against 64 for a full $4\times4$ product; a quaternion product costs
16; rotating a vector costs 9 multiplications with a matrix. Storage is 9, 4 or 3 numbers
for a matrix, a quaternion or a rotation vector. Renormalizing a quaternion costs one
division, while a drifted matrix needs an SVD or Gram–Schmidt step. The real cost drivers
are interface errors, which affect every downstream sensor, and the evaluation of Exp,
Log and Jacobians near their singular angles.

### Implementation contracts

Read in the cited versions; no library call was executed for this note, and the worked
examples were recomputed with the Python standard library only.

- **OpenCV 4.13.0** [calib3d.hpp]: the pinhole model divides by $Z_c$, so visible points
  have $Z_c>0$, and with pixel rows increasing downwards $Y_c$ points down (L94–L118 plus
  project deduction); `Rodrigues` converts between a rotation vector (radians, norm =
  angle) and a matrix, and its optional Jacobian is $3\times9$ or $9\times3$, a derivative
  of matrix entries, not a Lie Jacobian (L681–L707); `solvePnP` returns `rvec` and `tvec`
  that bring points "from the model coordinate system to the camera coordinate system"
  (L1031–L1032).
- **Eigen 3.4**: `Quaternion(w, x, y, z)` takes the scalar first while "internally the
  coefficients are stored in the following order: [x, y, z, w]"; `umeyama` applies the
  determinant correction [`Umeyama.h` L136–L143].
- **SciPy 1.18.0**: `Rotation.from_quat` assumes scalar-last order unless
  `scalar_first=True`, normalizes its input and represents active rotations; only a listed
  subset of operations preserves the double cover.
- **Ceres 2.2.0**: `QuaternionManifold` stores a Hamilton quaternion as $[w,x,y,z]$ and
  defines $\boxplus(x,\Delta)=\exp(\Delta)\otimes x$, a *left* product, with
  $\exp(\Delta)=[\cos\|\Delta\|,\ \sin\|\Delta\|\,\Delta/\|\Delta\|]$, so a tangent step of norm
  $\|\Delta\|$ rotates by $2\|\Delta\|$; `EigenQuaternionManifold` is the same manifold
  for Eigen's $[x,y,z,w]$ memory layout [nnls_modeling.rst L1567–L1645;
  manifold.cc L27–L60].
- **GTSAM 4.2**: `Pose3` tangent vectors are ordered $[\omega,v]$, rotation first;
  `AdjointMap` returns $\begin{bmatrix}R&0\\ {[t]_\times}R&R\end{bmatrix}$ in that order;
  `Retract` uses the exponential map when `GTSAM_POSE3_EXPMAP` is set (default `ON`),
  otherwise a rotation retraction plus an added translation [Pose3.h L138–L160,
  L206–L236; Pose3.cpp L57–L63, L211–L223; HandleGeneralOptions.cmake L19].
- **Sophus 1.22.10**: `SE3::log` returns $[\upsilon,\omega]$, translation part first
  [se3.hpp L237–L254].
- **ROS REP 103**: right-handed frames; body $x$ forward, $y$ left, $z$ up; `_optical`
  frames $z$ forward, $x$ right, $y$ down; quaternions preferred and Euler angles
  "generally discouraged due to having 24 'valid' conventions".
- **OpenGL `gluLookAt`**: maps the reference point to the negative $z$ axis and the up
  vector to $+y$; from OpenCV camera axes this is $M=\operatorname{diag}(1,-1,-1)$, a
  half-turn about $x$ with determinant $+1$, applied as $T^{gl}_{wc}=T^{cv}_{wc}M_h$ or
  $T^{gl}_{cw}=M_hT^{cv}_{cw}$ with $M_h=\operatorname{diag}(1,-1,-1,1)$.

## Evaluation and controlled variation

**Metrics.** For orientations, the geodesic angle of the residual rotation
$R^T\hat R$, $\theta=\arccos\frac{\operatorname{tr}(R^T\hat R)-1}{2}\in[0,\pi]$, computed with
the atan2 form near zero; for poses, the pose error $T^{-1}\hat T$ reported as an angle
and a translation norm in a stated frame; distributions (median, high quantiles,
maximum) rather than a mean alone, because a few reversed orientations can hide in a
small average. Trajectory metrics after alignment (absolute and relative trajectory
errors) belong to [CV-VIO](../../60-vision-3d/references/63-slam-vio.md).

**Controlled variation executed by the project on 2026-10-23, outside the repository**
(NumPy 2.2.6, SciPy 1.13.1; recomputed with the standard library by
checks/12-rotations-se3.py). Baseline: component-wise difference of ZYX Euler angles.
Varied factor: the measure only, with identical rotations. Prediction: divergence near
a pitch of 90°. Result: $(30°,89.9°,0°)$ and $(0°,89.9°,-30°)$ differ by 30° on two Euler
angles but by 0.052° in geodesic angle; $q$ and $-q$ are at Euclidean distance 2 for a
zero rotation. Constructed cases, not system measurements.

**Proposed boundary-test protocol (not executed).** Baseline: an interface that passes
identity and round-trip tests. Controlled variation: inject one convention error at a
time (scalar-first read as scalar-last, Hamilton read as JPL, $T_{wc}$ read as $T_{cw}$,
left read as right perturbation) and record which test of the procedure fails. Expected
result (hypothesis): the round trip catches none of them, the quarter-turn test catches
the order error, the non-commuting pair the algebra error, and the projected point the
inversion. Measurement: a pass/fail matrix per test and per injected error.

**Measurement limits.** Ground-truth orientations come with their own frame alignment
(hand–eye or motion-capture calibration) and time offset, which add to the measured
error. Symmetric objects need an evaluation that minimizes over their symmetry group,
which should not be applied to camera orientation. A mean angle over a sequence mixes
bias and noise.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| Reprojection correct at rest, wrong once the platform rotates | Extrinsic inverted, or applied on the wrong side | Recompute the camera centre $-R^Tt$; compose with a pure rotation and compare | Name every pose $T_{\text{to,from}}$; fix the inverse at the boundary |
| Quaternion of unit norm but a rotation about the wrong axis | Scalar-first versus scalar-last order | Quarter turn about $z$ must map $e_x$ to $e_y$ | Convert at the boundary; never reorder inside the code |
| Rotations compose correctly in one order only | Hamilton versus JPL, or active versus passive | Compose two non-commuting quarter turns in both libraries | Convert the algebra, not only the storage order |
| Jacobians pass finite differences in each library but disagree | Left versus right perturbation; block order; half-angle tangent | Apply the same physical perturbation and compare point changes | Transport with the adjoint; reorder blocks; rescale by 2 |
| Covariance looks too small in position after transport | Rotation applied block by block, lever arm forgotten | Compare with $\mathrm{Ad}_T\Sigma\mathrm{Ad}_T^T$ (worked example A) | Use the full adjoint |
| Scene upside down or behind the camera in the renderer | OpenCV versus OpenGL axes; single-axis flip | A point in front must stay in front; $\det M=+1$ | $M=\operatorname{diag}(1,-1,-1)$ on the correct side |
| Error angle 0 for small but non-zero errors, or NaN | arccos of a rounded or out-of-range trace | Compare with the atan2 form (worked example C) | Clamp the argument; use atan2 or the quaternion form |
| Large Euler-angle errors on an almost correct pose | Gimbal lock near pitch ±90° | Geodesic angle of $R^T\hat R$ | Report geodesic angles; avoid Euler angles in interfaces |
| Rotation matrix with $\det=-1$ after a fit | SVD projection without determinant correction | Check $\det R$ | $R=U\operatorname{diag}(1,1,\det(UV^T))V^T$ |
| Same 6-vector gives different poses in two libraries | $SE(3)$ exponential versus $T(3)\times SO(3)$ or composite charts | Apply a step with a large rotation (worked example B) | Exchange poses, not increments; or document the chart |

## Alternatives and applications

Conditional choices:

- **Prefer rotation matrices or $(R,t)$ blocks** for composition and point
  transformation, and as the internal canonical form when performance is not critical.
- **Prefer unit quaternions** for storage, interpolation and renormalization, with the
  four convention choices written down.
- **Prefer tangent increments** ($\delta\theta$ or a 6-vector with a declared side and
  block order) for optimization, filtering and covariances.
- **Prefer Euler angles** only for human-facing display or for interfaces that impose
  them, never for averaging or error measurement.
- **Prefer a continuous 6-D or 5-D representation** when a network regresses a
  rotation, following Zhou et al.
- **Prefer exchanging poses rather than increments** between libraries whose charts
  differ, and transport covariances with the adjoint of the consumer's convention.

Industrial uses (project reasoning, not published results): camera–IMU and
camera–LiDAR extrinsics passed between a calibration tool and a fusion stack;
robot-mounted cameras where hand–eye results feed a controller; augmented-reality
overlays where an OpenCV pose drives an OpenGL renderer; multi-camera inspection cells
where each camera's pose is re-expressed in the part frame.

## Guided reasoning and proposed checks

These constructed cases develop the composition of coordinate frames and left/right perturbations. They explain or test reasoning; no image, video or hardware result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-SE3-001

**Working question**: For two images, a SLAM system provides poses $T_{wc_1}$ and $T_{wc_2}$ that map camera coordinates into the world frame: $p_w=T_{wc_i}\,p_{c_i}$. Which transformation expresses a point known in camera 2 coordinates in camera 1 coordinates?

**Reference answer**: $T_{c_1c_2}=T_{wc_1}^{-1}T_{wc_2}=T_{c_1w}T_{wc_2}$: go back from $c_2$ to the world, then from the world to $c_1$. The adjacent indices must coincide ($c_1w$ then $wc_2$); the composition is not commutative.

**Constructed example**: with two identical orientations and centers offset on a world axis, the origin point of the second camera must appear at the same offset in the first. Turning only the first camera then makes it necessary to express this shift in its axes. This simple test reveals a translation added in the wrong coordinate frame, which a seemingly valid multiplication of matrices can pass.

### Case linked to CV-SE3-005

**Working question**: To evaluate an estimated orientation $\hat R$ against ground truth $R$, one report compares Euler angles component by component and another compares quaternions. Which measure should be used instead, and why can both direct comparisons mislead?

**Reference answer**: measure the angle of the residual rotation $R^T\hat R$: $\theta=\arccos\frac{\operatorname{tr}(R^T\hat R)-1}{2}$, independent of parameterization. Euler angles depend on convention and are singular: near a pitch of 90°, large yaw and roll differences compensate each other. $q$ and $-q$ represent the same rotation: their components can be at Euclidean distance 2 for a zero error; for unit quaternions, use $\theta=2\arccos|\langle q_1,q_2\rangle|$.

**Reading the score**: The angular error measures the relative rotation required to align the orientations, not their distance to a particular angle origin. Keep radians and degrees explicit in the calculation and report, and then examine the distribution of errors instead of a single average.

**Source consulted for this pass**: [Solà et al., micro Lie theory](https://arxiv.org/html/1812.01537v9), §II, perturbations and uncertainties; Appendix D, SE(3). The other developments are in the [flashcards](../12-rotations-se3.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-SE3-001

**Situation**: For two images, a SLAM system provides poses $T_{wc_1}$ and $T_{wc_2}$ that map camera coordinates into the world frame: $p_w=T_{wc_i}\,p_{c_i}$. Which transformation expresses a point known in camera 2 coordinates in camera 1 coordinates?

**Calculation by blocks**: a homogeneous pose is written $T=\begin{bmatrix}R&t\\0&1\end{bmatrix}$, with $R\in SO(3)$, $t\in\mathbb R^3$ and homogeneous points $[p^T,1]^T$. Its inverse uses $R^T$ and $-R^Tt$. For the two poses of the question, the relative rotation is $R_{wc_1}^TR_{wc_2}$ and the translation is $R_{wc_1}^T(t_{wc_2}-t_{wc_1})$. The latter is the movement between centers re-expressed in camera 1, not just a difference in world coordinates. A homogeneous direction vector has a last zero coordinate and must not receive this translation. This check distinguishes applying a pose to a point from applying it to a direction.

### CV-SE3-002

**Situation**: Given $p_c=Rp_w+t$, how do you recover the camera center in world coordinates?

**From pixel to world ray**: After removing the distortion, a homogeneous pixel $\tilde u$ defines a camera direction proportional to $K^{-1}\tilde u$, where $K$ is the intrinsic matrix. In world coordinates, the ray is written as $p_w(\lambda)=C_w+\lambda R^TK^{-1}\tilde u$, with a scale convention for $\lambda$. The center is its origin, the inverse rotation orients its direction and the depth remains unknown on a single view. This calculation shows the distinct role of the three elements: $t$ participates in the localization of the camera, $R$ in the change of axes and $K$ in the geometry in pixels. None of these elements alone provide the depth of a point.

### CV-SE3-003

**Situation**: Two implementations of the same cost parameterize rotation increments with a small vector $\delta\theta$ and obtain different Jacobians, both verified by finite differences. Which convention can explain this, how are the two related, and which should you choose?

**Complete extension to poses**: by ordering increment $\xi=(\rho,\phi)$, translation then rotation, the adjoint of $T=(R,t)$ is $\operatorname{Ad}_T=\begin{bmatrix}R&[t]_\times R\\0&R\end{bmatrix}$, where $[t]_\times a=t\times a$. Switching from a right perturbation to the equivalent left perturbation uses $\xi_G=\operatorname{Ad}_T\xi_L$. A covariance follows $P_G=\operatorname{Ad}_TP_L\operatorname{Ad}_T^T$ in this local approximation. The cross block reflects the fact that a small rotation around another origin also induces a displacement. A simple block-by-block rotation would forget this lever arm effect. The translation/rotation conventions must accompany the matrix to avoid swapping its blocks.

### CV-SE3-004

**Situation**: A camera–IMU extrinsic calibration is passed between libraries as a unit quaternion and translation. Reprojection becomes incorrect even though the quaternion norm is 1. Which conventions should be checked, and which test distinguishes them?

**Representation check**: A unit quaternion describes a rotation, but its multiplication is noncommutative. In Hamilton convention, an angle $\theta$ around a unit axis $a$ is represented, scalar first, by $(\cos(\theta/2),a\sin(\theta/2))$. This writing makes it possible to build a verifiable quarter turn without converting ambiguous Euler angles. A convention conversion must address the order, signs and meaning of application in a consistent way: swapping the four numbers is not always enough. Testing the three basis axes in turn and a translated point verifies the whole transformation; normalization does not repair either an inversion of pose or an incompatible product convention.

### CV-SE3-005

**Situation**: To evaluate an estimated orientation $\hat R$ against ground truth $R$, one report compares Euler angles component by component and another compares quaternions. Which measure should be used instead, and why can both direct comparisons mislead?

**More robust near-zero calculation**: From a unit relative quaternion in a stated convention, $q_{rel}=(w,v)$, the principal angle can be written as $\theta=2\operatorname{atan2}(\|v\|_2,|w|)\in[0,\pi]$. This form uses the vector part when the arccos becomes sensitive to rounding near 1. The absolute value handles the double cover, without erasing a true rotation error. Check that the two orientations express the same coordinate frame and the same direction before forming the relative rotation. For aggregations, report also quantiles and extreme cases: a low average error can hide some completely reversed orientations. These expressions give radians; explicitly convert only for display to degrees.

### CV-SE3-006

**Situation**: A camera pose estimated with OpenCV is passed to an OpenGL renderer and a ROS node. The rendered scene appears upside down or behind the camera. Which axis conventions should be compared, and which transformation relates OpenCV and OpenGL?

**Change of bases on both sides**: if $p'_c=B_c p_c$ and $p'_w=B_w p_w$, then a world matrix→camera becomes $T'_{cw}=B_cT_{cw}B_w^{-1}$, using homogeneous matrices $4\times4$. The core example changes only the camera basis: $B_w=I$, hence the multiplication on the left. Changing the world frame also requires the second factor. This general rule avoids applying an "OpenGL conversion" without specifying which base changes. Camera coordinate conventions alone do not define clip space projection, depth buffer direction, or the origin of the framebuffer pixels: these additional contracts must be checked separately in the render.

**Passages consulted for these developments**: [Solà et al., micro Lie theory](https://arxiv.org/html/1812.01537v9), §II-F, adjoint; §II-H, covariances; appendices B and D; [Solà, Quaternion kinematics](https://arxiv.org/html/1711.02508v1), §§2.4 and 3.1, quaternion and conventions.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-SE3-001 — Composition checked by a round trip

Use a constructed case with $R_{wc_1}=R_z(90^\circ)$, $t_{wc_1}=0$, $R_{wc_2}=I$ and $t_{wc_2}=(1,0,0)^T$ m. Camera 2's origin has coordinates $(0,-1,0)^T$ m in camera 1. Mapping it back with $T_{wc_1}$ must recover $(1,0,0)^T$ m. Nonzero translation and nonidentity rotation expose order errors that two identity poses cannot reveal.

### CV-SE3-002 — The optical center does not project to an image pixel

At $C_w=-R^Tt$, the camera-space point is exactly zero. Its perspective projection requires division by $Z_c=0$ and is undefined. Therefore verify the center using the rigid transform before perspective division, rather than checking a pixel coordinate. Conversely, a point on a viewing ray with positive camera depth projects correctly, but different depths share that pixel. This separates a valid pose-inversion test from an invalid projection test at the optical center.

### CV-SE3-003 — The same perturbation produces the same point change

For $y=Rp$ and a right perturbation, the first-order change is $\delta y=-R[p]_\times\delta\theta_L$. Under a left perturbation it is $\delta y=-[Rp]_\times\delta\theta_G$. Substituting $\delta\theta_G=R\delta\theta_L$ makes the two identical. A finite-difference test should therefore perturb the same physical rotation before comparing outputs. Equal numeric increment components in different frames generally represent different motions.

### CV-SE3-004 — A round trip can preserve a shared mistake

Two conversion routines that apply the same mistaken inverse can pass a round-trip test while both disagree with the sensor contract. Include an independently constructed axis-angle example, such as the Hamilton active rotation $q=(\sqrt2/2,0,0,\sqrt2/2)$ taking $e_x$ to $e_y$. Then compose two rotations about different axes. This second check exposes multiplication-order differences that testing one quaternion and its inverse may leave invisible.

### CV-SE3-005 — Symmetry belongs to the evaluation contract

The geodesic angle compares coordinate-frame orientations. If an object is physically indistinguishable after a half-turn, the raw angle may penalize an equivalent object pose; evaluating that application requires minimizing over its declared symmetry group. Do not silently apply this quotient to camera orientation, where a reversed optical axis is usually a real error. Parameterization invariance and task-specific symmetry invariance are separate properties of an evaluation measure.

### CV-SE3-006 — Handedness and visibility are separate tests

The matrix $M=\operatorname{diag}(1,-1,-1)$ preserves lengths and handedness because $M^TM=I$ and $\det M=1$. A camera-space point $(0,0,2)^T$ becomes $(0,0,-2)^T$: it remains in front according to each convention, despite the sign change of depth. A single-axis reflection also preserves lengths, so checking distances alone misses a handedness error. Use an oriented basis and a point with positive source-camera depth.

Consulted foundations: [Solà et al., micro Lie theory](https://arxiv.org/html/1812.01537): §II-F adjoint, §II-H covariance and appendices B/D group operations.

## Sources and flashcards

### Scientific sources

- [Solà, Deray and Atchuthan, A micro Lie theory for state estimation in robotics, arXiv 1812.01537v9](https://arxiv.org/html/1812.01537v9): §II-E eq. 25–28 (right and left plus and minus), §II-F eq. 29–34 and the $SE(3)$ adjoint example, §II-G eq. 41–43 and the rotation-action example, §II-H eq. 51–55 (covariances on manifolds), §IV ($SE(n)$ versus $T(n)\times SO(n)$ versus composites), App. B eq. 131–151 ($S^3$ and $SO(3)$), App. D eq. 168–183 ($SE(3)$).
- [Solà, Quaternion kinematics for the error-state Kalman filter, arXiv 1711.02508v1](https://arxiv.org/html/1711.02508v1): §2.4.6 eq. 110–112 (double cover), §2.7 eq. 124–128 (SLERP), §3.1 eq. 140–143 and Table 2 (Hamilton versus JPL), §3.1.1 (component order, Eigen).
- [Zhou, Barnes, Lu, Yang and Li 2019, On the Continuity of Rotation Representations in Neural Networks, arXiv 1812.07035](https://arxiv.org/abs/1812.07035): abstract (discontinuity in four or fewer dimensions; continuous 5-D and 6-D representations).

### Implementation sources

- [OpenCV 4.13.0, `modules/calib3d/include/opencv2/calib3d.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L94-L118): pinhole model (L94–L118), `Rodrigues` (L681–L707), `solvePnP` `rvec` and `tvec` (L1031–L1032).
- [Eigen 3.4, `Quaternion` class](https://libeigen.gitlab.io/eigen/docs-3.4/classEigen_1_1Quaternion.html): constructor argument order and storage order; [Eigen 3.4.0, `Umeyama.h`](https://gitlab.com/libeigen/eigen/-/blob/3.4.0/Eigen/src/Geometry/Umeyama.h#L136-L143): determinant correction (L136–L143).
- [SciPy 1.18.0, `Rotation.from_quat`](https://docs.scipy.org/doc/scipy-1.18.0/reference/generated/scipy.spatial.transform.Rotation.from_quat.html): scalar-last default, `scalar_first`, normalization, double-cover subset.
- [Ceres Solver 2.2.0, `docs/source/nnls_modeling.rst`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/docs/source/nnls_modeling.rst): `QuaternionManifold` and `EigenQuaternionManifold` (L1567–L1645); [`internal/ceres/manifold.cc`](https://github.com/ceres-solver/ceres-solver/blob/2.2.0/internal/ceres/manifold.cc#L27-L60): `QuaternionPlusImpl` (L27–L60).
- [GTSAM 4.2, `gtsam/geometry/Pose3.h`](https://github.com/borglab/gtsam/blob/4.2/gtsam/geometry/Pose3.h): `Expmap`, `AdjointMap` (L138–L160), `ChartAtOrigin`, `ComputeQforExpmapDerivative`, `wedge` (L206–L236); [`Pose3.cpp`](https://github.com/borglab/gtsam/blob/4.2/gtsam/geometry/Pose3.cpp): `AdjointMap` (L57–L63), `ChartAtOrigin::Retract` (L211–L223); [`cmake/HandleGeneralOptions.cmake`](https://github.com/borglab/gtsam/blob/4.2/cmake/HandleGeneralOptions.cmake#L19): `GTSAM_POSE3_EXPMAP` default (L19).
- [Sophus 1.22.10, `sophus/se3.hpp`](https://github.com/strasdat/Sophus/blob/1.22.10/sophus/se3.hpp#L237-L254): `SE3::log` ordering (L237–L254); [`sophus/so3.hpp`](https://github.com/strasdat/Sophus/blob/1.22.10/sophus/so3.hpp#L282): small-angle branch (L282).
- [REP 103, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst): Coordinate Frame Conventions, Axis Orientation, Suffix Frames, Rotation Representation.
- [Khronos, gluLookAt, Description](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml): retained from the 2026-10-23 pass, not re-read.

### Related flashcards and references

- [Flashcards](../12-rotations-se3.md): CV-SE3-001 to CV-SE3-006.
- Consumers of these conventions: [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md), [CV-BA](../../50-calibration-geometrie/references/54-bundle-adjustment.md), [CV-MULTICALIB](../../50-calibration-geometrie/references/55-calibration-multicapteurs.md), [CV-HANDEYE](../../50-calibration-geometrie/references/57-calibration-hand-eye.md), [CV-VIO](../../60-vision-3d/references/63-slam-vio.md), [CV-FUSION](13-kalman-ekf-eskf.md), [CV-FACTEURS](14-graphes-facteurs.md).

The constructed cases are reasoning of the project; no image, video or hardware result is claimed as measured.

Drafted by agent, 2026-10-18. Revisions 3 and 4: self-review `revue-cartes` by Agent Claude Code on 2026-10-23, corrections and enrichments accepted by the learner, without independent validation. Revision 11, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/12-rotations-se3.md).
