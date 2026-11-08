---
id: CV-FUSION
type: methode
domaine: d01
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 9
prerequis: ["CV-SE3"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# Kalman, EKF, UKF and ESKF for sensor fusion

## Problem, data and assumptions

Merge time-stamped measurements and predictions by representing their uncertainties. Inputs: state model, measurements, noise and timestamps; output: estimated state and covariance. The supposed uncertainties and associations condition the consistency of the result.

## Prerequisites and competencies

**Required prerequisites**: [CV-SE3](12-rotations-se3.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Kalman linear alternates prediction and correction. EKF linearizes the models. UKF propagates $2n+1$ sigma-deterministic points through nonlinear functions, without Jacobian; its mean has an order of precision greater than EKF, its covariance the same order (Julier and Uhlmann 1997, §3, equations 12 – 14). ESKF separates nominal state and small tangential error. At Solà, the error follows the prediction of a EKF (Appendix E, equations 439 – 440), and its correction uses the Jacobian of a classical EKF composed with that of the error (§6.1, equation 278). This is not a mutually exclusive alternative to EKF. Correcting the error and then injecting it into the pose also requires a consistent covariance reset.

Solà (§5.1) justifies the error-state formulation with four properties. The orientation error is minimal, which avoids the redundancy of the quaternion and the risk of singular covariance related to its constraint. The error operates near the origin, far from the parameterization singularities, which keeps the linearization valid. It remains small, so that its second-order products are negligible. Its dynamics are slow, the rapid dynamics being integrated in the nominal state: corrections can come less often than predictions. The cycle (§5.2): integrate the nominal state without noise, predict the law of error, correct it at the arrival of a non-IMU measurement, inject it, then reset it to zero.

## Mathematics, conventions and units

The innovation is $\nu=z-h(x^-)$, of covariance $S=HP^-H^T+R$ in the EKF. With $S$ set positive, the $\nu^TS^{-1}\nu$ score is unitless, since $S$ carries the units of $\nu$. If the innovation is Gaussian, centered, white and covariance $S$, it follows a law of $\chi^2$ to $m$ degrees of freedom, $m$ being the number of observations (Gamse et al. 2014, §2.2.2, equations 7 – 10). A rejection beyond $\chi^2_{m;1-\alpha}$ signals a deviation in prediction, stochastic model, or observation, without saying which. Quantiles at 95 % recalculated: 3,84 ($m=1$), 5,99 ($m=2$), 7,81 ($m=3$), 9,49 ($m=4$). DeepSORT uses 9,4877 for a dimension measurement 4 (§2.2). Reasoning the project: too often high scores on a sequence signal an overconfident filter, too often low a subtrust filter.

$P^-=FP^+F^T+Q$ uses real-time step. On a step $\Delta t$, Solà shows three different dependencies (Appendix E, equation 440): the dynamic term is exponential, the measurement noise IMU contributes in $\Delta t^2$, the disturbances as the random steps of the biases in $\Delta t$. Pulse covariances translate it: $\sigma_{\tilde a_n}^2\Delta t^2I$ for speed, $\sigma_{a_w}^2\Delta t\,I$ for accelerometer bias (§5.4.2, equations 262 – 265). Spreading sample IMU per sample with the actual $\Delta t$, and applying a camera measurement at its acquisition time, are therefore conditions of consistency; the processing of delays by buffer and re-propagation is a proposal of the project. In ESKF, after injection, $\hat{\delta x}\leftarrow0$ and $P\leftarrow GPG^T$ according to reset Jacobian $G$ (Solà, §6.3, equations 285 – 288). For the local angular error $R_{vrai}=R_{nom}\operatorname{Exp}(\delta\theta)$ from Solà, $G_\theta\approx I-[\hat{\delta\theta}/2]_\times$ at first order; the other diagonal blocks are identical. $G\approx I$ neglects the change of coordinates for a small correction; a global angular error requires a different Jacobian. Resetting the average error to zero does not reset the uncertainty to zero.

## Parameters and properties

Choose Status, Frequency, Q/A, Bias Processing, Delay, and Absent Measure. Artificially small noise gives excessive confidence. UKF does not guarantee to repair any non-linearity, multimodal distribution or bad model.

## Cost and implementation

State and frequency dominate matrix products; temporal consistency takes precedence over a frequency promise. No complete filter implementation is provided; the scalar example executed in the first batch only illustrates a correction.

Form of covariance update. The $P^+=P^--KSK^T$ subtraction, with $S=HP^-H^T+R$, remains vulnerable to rounding. Chin/JPL 2023 (§III-A, equation 14) favors the form of Joseph $P^+=(I-KH)P^-(I-KH)^T+KRK^T$. $P^-$ denotes the covariance before correction, $K$ the gain, $H$ the measurement Jacobian and $R$ its noise covariance. Under the independence of prediction and measurement errors and with $P^-,R$ semi-definite positive, the sum of quadratic terms preserves the semi-definite positivity in exact arithmetic; it reduces the numerical risk but does not offer an absolute guarantee in floats. Monitoring symmetry, eigenvalues, and conditioning; a Cholesky factorization requires strict positivity. A square-root implementation can be compared if necessary. Symmetrize $(P+P^T)/2$ does not correct a negative eigenvalue on its own. Symptoms and tests are diagnoses offered by the project.

## Evaluation and controlled variation

Proposed variation: increase R while retaining measurement/prediction; correction should follow less strongly the measurement. Then check the innovation on reserved sequences; a low covariance alone does not attest to the actual accuracy.

## Failure modes and diagnosis

Two sensors disagree: compare timestamp, extrinsic, units, bias and correlations before decreasing R. Systematically biased innovations suggest something other than increased white noise.

## Alternatives and applications

Filtering for low latency; smoothing/graphs to re-estimate multiple states. A correlated redundant measurement should not be counted twice as independent information.

## Guided reasoning and proposed checks

These built cases develop innovations, covariance and reset of the ESKF. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-FUSION-001

**Question of work**: How do EKF, UKF and ESKF differ, without ranking them by absolute accuracy?

**Reference Response**: The EKF linearizes models and measurements around the current estimate. The UKF propagates $2n+1$ sigma-points selected deterministically through nonlinear functions, without Jacobian. The ESKF integrates a nonlinear nominal state and estimates a small error around it, with the prediction and correction equations of a EKF applied to this error. These names therefore describe choices that combine, not three exclusive categories.

**Choice of design**: Begin with the representation of state, non-linearity of observations, and acceptable cost. The selected filter must be evaluated on consistent innovations and trajectory errors. A better local approximation of propagation does not correct a bad extrinsic, false association, or offbeat clock; these defects belong to the model and the data.

### Case linked to CV-FUSION-005

**Question of work**: When fusing IMU and camera measurements with quaternion orientation, why estimate a small error around an integrated nominal state rather than the complete state in an EKF?

**Reference Response**: the orientation error is minimal, three parameters for three degrees of freedom: we avoid the redundancy of the quaternion and the risk of singular covariance related to its norm constraint. The error remains small and close to the origin, far from the singularities of parameterization: the linearization remains valid, the products of the second order are negligible and the Jacobians simple. Its dynamics are slow, the rapid dynamics being integrated in the nominal state: corrections can happen less often than predictions IMU.

**Intuition for follow-up**: The nominal state carries the important movement, while the error describes a local neighborhood. The small size of the error justifies a local approximation only as long as the estimate remains close to reality. A bad initialization or a long absence of measurement may leave this domain; keeping a normal quaternion does not alone establish the consistency of the filter.

**Documentary reference for this pass**: [Solà, Quaternion kinetics for the error-state Kalman filter](https://arxiv.org/html/1711.02508v1), §6.3, injection and reset error. The other developments are in the [flashcards](../13-kalman-ekf-eskf.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-FUSION-001

**Situation**: How do EKF, UKF and ESKF differ, without ranking them by absolute accuracy?

**Common Basis of Calculation**: in an approximation EKF, $x^-=f(x^+,u)$ and $P^-=FP^+F^T+Q$, then $K=P^-H^T(HP^-H^T+R)^{-1}$. $F$ and $H$ are the Jacobians of dynamics and measurement; $Q$ and $R$ describe their uncertainties in the coordinates and no time announced. We correct with innovation, by solving a system to calculate the gain rather than an explicit inverse. The UKF replaces some of these linearizations by the propagation of weighted points; the ESKF changes the coordinates in which the small correction is estimated. A truly multimodal distribution, like two possible visual associations, is not rendered unimodal by this change of calculation.

### CV-FUSION-002

**Situation**: In a filter, $\nu$ is the innovation, defined as measurement minus prediction, and $S$ is its positive-definite covariance. What does $\nu^TS^{-1}\nu$ measure in an innovation check?

**Non-reverse calculation and selection effect**: if $S=LL^T$, solve $Le=\nu$ and then calculate $e^Te$ gives the score. For independent measurements of fixed dimensions, its nominal expectation is $m$, before selection. On the other hand, keeping only observations that have passed the gating artificially reduces the average observed; it can no longer be naively compared to $m$ to conclude a too great covariance. Similarly, testing multiple candidates and then retaining the best changes the distribution. Check noise consistency on baseline observations and consider releases. A succession of innovations of the same sign also reveals a temporal structure that a histogram of norms can mask.

### CV-FUSION-003

**Situation**: In a camera–IMU ESKF, orientation covariance drops almost to zero after every correction. Subsequent measurements are rejected by gating or barely change the state. Which reset error should be investigated first, and what is the correct treatment?

**Also preserve correlations.**: If the error is split into $\theta$ orientation and other $a$ variables, the reset transforms $P_{\theta a}$ into $G_\theta P_{\theta a}$ and $P_{a\theta}$ into $P_{a\theta}G_\theta^T$, not just the $P_{\theta\theta}$ block. These terms can transfer information from a visual observation to position, speed, or bias at the next correction. Erroneously canceling them changes the filter. A constructed check consists of comparing the distribution of small perturbations before and after injection in their respective coordinates: the numerical description changes, while the physical states represented must remain close. Testing the reset separately avoids confusing it with the legitimate reduction of uncertainty due to measurement.

### CV-FUSION-004

**Situation**: The camera drops from 30 to 10 frames/s with variable latency, while the IMU stays at 200 Hz. Which timing contract must sensor fusion respect?

**Do not mix density and discrete variance**: for a position – speed state subjected to a continuous white acceleration of spectral density $q$, the ideal integration gives $Q_d=q\begin{bmatrix}\Delta t^3/3&\Delta t^2/2\\\Delta t^2/2&\Delta t\end{bmatrix}$. If we assume instead a constant random acceleration on each interval, of variance $\sigma_a^2$, the block becomes $\sigma_a^2\begin{bmatrix}\Delta t^4/4&\Delta t^3/2\\\Delta t^3/2&\Delta t^2\end{bmatrix}$. These two analytical cases describe different noises; replacing one with the other with an unchanged numerical value is false. The powers of $\Delta t$ are therefore not chosen by copying a matrix: they come from the noise model and its integration, with their units.

### CV-FUSION-005

**Situation**: When fusing IMU and camera measurements with quaternion orientation, why estimate a small error around an integrated nominal state rather than the complete state in an EKF?

**Example of a minimum error state**: A nominal inertial state can hold position $p$, speed $v$, quaternion $q$, accelerometer bias $b_a$ and gyro bias $b_g$. This represents 16 stored components, but an error of dimension 15 when the orientation uses three local coordinates and the gravity is known here. A typical correction injects $p\leftarrow p+\delta p$, $v\leftarrow v+\delta v$, $R\leftarrow R\operatorname{Exp}(\delta\theta)$, then the additive biases. The IMU measures a specific force and angular velocity, not directly a position: you have to remove the biases, express the acceleration in the correct coordinate frame and process the gravity according to the model. The exact size and content change if one also estimates gravity or calibration.

### CV-FUSION-006

**Situation**: After thousands of Kalman filter updates, Cholesky factorization of $P$ fails or a variance becomes negative, although the models appear correct. Which implementation issue should be checked, and which update form mitigates it?

**Origin of Joseph**: if the error before measurement is $e^-$ and the measurement noise $n$, the linear correction gives $e^+=(I-KH)e^- -Kn$. Taking the covariance and assuming their independence, the two crossed terms cancel each other out and we find the sum of Joseph. If measurement and prediction share the same information, these terms are no longer automatically zero: the stability of the algebraic form does not validate the statistical hypothesis. A square-root alternative propagates a covariance factor rather than $P$ directly; it improves the numerical properties in its frame, but requires a consistent implementation of prediction, correction, and reset. Adding an arbitrary diagonal to each failure can hide an invalid template.

**Passages consulted for these developments**: [Solà, Quaternion kinematics](https://arxiv.org/html/1711.02508v1), §§5 – 6, status, correction and reset; Appendix E, noise integration; [Chin/JPL 2023](https://ipnpr.jpl.nasa.gov/progress_report/42-233/42-233A-orig.pdf), §III-A, Joseph shape; square-root sections.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-FUSION-001 — Curvature can change the propagated mean

Constructed scalar example: let $x$ have mean zero and variance one, and propagate $f(x)=x^2$. The true output mean is one, whereas an EKF-style first-order mean propagation gives $f(0)=0$. Sigma points that reproduce the input second moment give weighted mean one for this quadratic. This illustrates one benefit of nonlinear moment propagation without ranking filters universally: other functions, noise models and computational budgets still require evaluation, and error-state coordinates address a different representation choice.

### CV-FUSION-002 — Whitened innovation direction matters

For innovation covariance $S=\operatorname{diag}(1,100)$ in squared measurement units, innovations $(3,0)^T$ and $(0,3)^T$ have scores 9 and 0.09. The same Euclidean error is surprising along one axis and expected along the other. This constructed example makes the covariance ellipse operational. Even a plausible score does not establish correct association: unrelated candidates can fall within the gate, especially when uncertainty is large.

### CV-FUSION-003 — A zero correction gives a reset identity test

When the injected orientation correction is exactly zero, the reset Jacobian must reduce to the identity and the reset alone must preserve $P$. This is distinct from the preceding measurement update, which may legitimately reduce uncertainty. Separate these two operations when inspecting a trace. For nonzero corrections, the first-order sign of the skew term depends on whether the orientation error is local or global; copying it across conventions changes the represented distribution.

### CV-FUSION-004 — Latency can dominate the nominal observation rate

Constructed example: at a constant angular speed of $90^\circ$/s, applying a camera update 50 ms late as though it were current introduces a $4.5^\circ$ temporal mismatch. Increasing the camera rate does not remove that mismatch. A delayed-state update or replay must also account for correlations with intervening IMU propagation. The required history length follows the observed latency distribution; a single mean delay is inadequate when jitter produces occasional much older measurements.

### CV-FUSION-005 — Small errors are a maintained condition

An error-state representation is a local approximation, so small errors must be maintained by initialization, prediction and timely corrections. A severely wrong initial orientation or a long visual outage can invalidate the linearization even though the nominal quaternion stays normalized. Normalize the representation and assess innovation consistency as different checks. Neither minimal coordinates nor a unit quaternion guarantees that the estimated attitude is near the true attitude.

### CV-FUSION-006 — Symmetry repair is not positivity repair

For a numerically asymmetric covariance, $(P+P^T)/2$ restores symmetry but can retain negative eigenvalues. Conversely, a valid positive-semidefinite covariance may be singular, so strict Cholesky can fail without a negative variance. Check the intended rank, eigenvalue scale and state constraints before adding diagonal jitter. Joseph form reduces cancellation in the update; it does not repair duplicated measurements, invalid noise covariances or an inconsistent error-state reset.

Consulted foundations: [Solà, quaternion kinematics](https://arxiv.org/html/1711.02508v1): §5 error-state formulation, §6.3 reset, Appendix E noise integration.

## Sources and flashcards

- [Gamse et al. 2014, Statistical Process Control of a Kalman Filter Model, §2.2.2, equations 5 – 10, and §3.4.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/).
- [Julier and Uhlmann 1997, A New Extension of the Kalman Filter to Nonlinear Systems, SPIE 3068, §3, Equations 12 – 14](https://doi.org/10.1117/12.280797): sigma-points, precision order, absence of Jacobian. Paid publisher version; text read on a course copy hosted by Berkeley. 2004's previously cited article at the Proceedings of the IEEE has not been read.
- [Wojke, Bewley and Paulus 2017, DeepSORT, §2.2](https://arxiv.org/abs/1703.07402): threshold $\chi^2$ to 95% in dimension 4.

- [Solà, Quaternion kinetics for the error-state Kalman filter](https://arxiv.org/abs/1711.02508) : §5.1 Benefits of theESKF, §5.2 principe, §5.4.2 Equations 262–265, §6.1 Equations 274–278 and note 26, §6.3 Equations 285–288Appendix E Equations 438–440.
- [Chin/JPL 2023, digital stability and Joseph shape, §III-A](https://ipnpr.jpl.nasa.gov/progress_report/42-233/42-233A-orig.pdf).
- [Related flashcards](../13-kalman-ekf-eskf.md): CV-FUSION-001 to 006.

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project. Revisions 3 and 4: self-review `revue-cartes` by Agent Claude Code on 2026-10-23, corrections and enrichments accepted by the learner, without independent validation.
