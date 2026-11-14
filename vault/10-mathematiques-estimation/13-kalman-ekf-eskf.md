# Flashcards — Kalman, EKF, UKF and ESKF for sensor fusion

reference note: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-FUSION-001

Objective: distinguish filter variants. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-001
Question: How do EKF, UKF and ESKF differ, without ranking them by absolute accuracy?
Reponse: **Expected answer**: The EKF linearizes models and measurements around the current estimate. The UKF propagates $2n+1$ sigma-points selected deterministically through nonlinear functions, without Jacobian. The ESKF integrates a nonlinear nominal state and estimates a small error around it, with the prediction and correction equations of an EKF applied to this error. These names therefore describe choices that combine, not three exclusive categories.

**Further explanation**: According to Julier and Uhlmann, the unscented transform computes the mean to a higher order of accuracy than the EKF, and the covariance to the same order. The result depends on the model, noise, initialization, and time consistency; an algorithm label is not a universal ranking.

**Design choice**: Begin with the state representation, the nonlinearity of the observations and the acceptable cost. The selected filter must be evaluated on consistent innovations and trajectory errors. A better local approximation of propagation does not correct a bad extrinsic, a wrong association or an offset clock; these defects belong to the model and the data.

**Common computational basis**: in an EKF approximation, $x^-=f(x^+,u)$ and $P^-=FP^+F^T+Q$, then $K=P^-H^T(HP^-H^T+R)^{-1}$. $F$ and $H$ are the Jacobians of dynamics and measurement; $Q$ and $R$ describe their uncertainties in the stated coordinates and time step. We correct with innovation, by solving a system to calculate the gain rather than an explicit inverse. The UKF replaces some of these linearizations by the propagation of weighted points; the ESKF changes the coordinates in which the small correction is estimated. A truly multimodal distribution, like two possible visual associations, is not rendered unimodal by this change of calculation.

**Curvature can change the propagated mean**: Constructed scalar example: let $x$ have mean zero and variance one, and propagate $f(x)=x^2$. The true output mean is one, whereas an EKF-style first-order mean propagation gives $f(0)=0$. Sigma points that reproduce the input second moment give weighted mean one for this quadratic. This illustrates one benefit of nonlinear moment propagation without ranking filters universally: other functions, noise models and computational budgets still require evaluation, and error-state coordinates address a different representation choice.

**Blocking errors**: saying that the UKF is always better or that the ESKF removes nonlinearity.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Solà, §5.2, §6.1, equation 278, and Appendix E, equations 439 – 440](https://arxiv.org/abs/1711.02508); [Julier and Uhlmann 1997, SPIE 3068, §3, equations 12 – 14](https://doi.org/10.1117/12.280797); [Solà, Quaternion kinematics, §§5–6, state, correction and reset; Appendix E, noise integration](https://arxiv.org/html/1711.02508v1), consulted 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::comprehension cv_id::CV-FUSION-001 provenance::agent pole::B pole::C
END

## CV-FUSION-002

Objective: Interpret a normalized innovation. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-002
Question: In a filter, $\nu$ is the innovation, defined as measurement minus prediction, and $S$ is its positive-definite covariance. What does $\nu^TS^{-1}\nu$ measure in an innovation check?
Reponse: **Expected answer**: this is the squared measurement–prediction deviation weighted by its uncertainty, a unitless squared Mahalanobis distance. If the model, Gaussian noises and $S$ are correct, it follows a $\chi^2$ distribution with $m$ degrees of freedom, $m$ being the measurement dimension. A measurement is therefore rejected beyond a chosen quantile, for example $\chi^2_{3,0.95}\approx7.81$.

**Further explanation**: DeepSORT thus excludes associations beyond the 95% quantile for a four-dimensional measurement, 9.4877. The threshold depends on $m$ and the accepted risk, not on units. Libraries differ in what they call the Mahalanobis distance: FilterPy 1.4.5 returns its square root, which must be compared with $\sqrt{9.4877}\approx3.08$. A rejection signals a gap between prediction, stochastic model and observation, without saying which is involved; it also does not prove the identity of the right object. Too often high or low values on a sequence signal an over- or under-trusting filter.

**Reading the gate**: The test removes associations that are too incompatible with the assumed uncertainty. It does not necessarily select a single association among the eligible ones. A filter that is too uncertain can accept many candidates; an overconfident filter can reject the right measurement. The assignment and statistical calibration therefore remain two separate controls.

**Calculation without an inverse and selection effect**: if $S=LL^T$, solving $Le=\nu$ and then computing $e^Te$ gives the score. For independent measurements of fixed dimensions, its nominal expectation is $m$, before selection. On the other hand, keeping only observations that have passed the gating artificially reduces the average observed; it can no longer be naively compared to $m$ to conclude that the covariance is too large. Similarly, testing multiple candidates and then retaining the best changes the distribution. Check noise consistency on reference observations and account for rejected ones. A succession of innovations of the same sign also reveals a temporal structure that a histogram of norms can mask.

**Whitened innovation direction matters**: For innovation covariance $S=\operatorname{diag}(1,100)$ in squared measurement units, innovations $(3,0)^T$ and $(0,3)^T$ have scores 9 and 0.09. The same Euclidean error is surprising along one axis and expected along the other. This constructed example makes the covariance ellipse operational. Even a plausible score does not establish correct association: unrelated candidates can fall within the gate, especially when uncertainty is large.

**Blocking errors**: confusing a large pixel residual with a large statistical inconsistency; applying the same threshold regardless of the measurement dimension.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Gamse et al. 2014, §2.2.2, equations 5 – 10, and §3.4.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/); [Wojke et al. 2017, DeepSORT, §2.2](https://arxiv.org/abs/1703.07402); [FilterPy 1.4.5, `mahalanobis`, L1124–L1135](https://github.com/rlabbe/filterpy/blob/1.4.5/filterpy/kalman/kalman_filter.py#L1124-L1135); quantiles recalculated by the project; [Solà, Quaternion kinematics, §§5–6, state, correction and reset; Appendix E, noise integration](https://arxiv.org/html/1711.02508v1), consulted 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-FUSION-002 provenance::agent pole::B pole::C
END

## CV-FUSION-003

Objective: Preserve the ESKF covariance. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-003
Question: In a camera–IMU ESKF, orientation covariance drops almost to zero after every correction. Subsequent measurements are rejected by gating or barely change the state. Which reset error should be investigated first, and what is the correct treatment?
Reponse: **Expected answer**: Look for a zeroing of $P$ at the moment the mean error is injected and then reset. The reset changes only the reference point of the error, not the available information: we set $\hat{\delta x}\leftarrow0$ but $P\leftarrow GPG^T$, with $G$ the reset Jacobian.

**Further explanation**: In the local angular error convention of Solà, $R_{\text{true}}=R_{\text{nom}}\operatorname{Exp}(\delta\theta)$, $G$ is equal to the identity except on the orientation block $G_\theta\approx I-[\hat{\delta\theta}/2]_\times$ in the first order. Taking $G\approx I$ neglects this small coordinate correction, without cancelling $P$. A global error convention requires its own Jacobian. To distinguish this from an $R$ that is too small, look at when $P$ drops: at the reset, the reset is at fault; during the update, the measurement weighting is. A zero covariance declares a fictitious perfect knowledge.

**Geometric intuition**: After injection, the same uncertainty is described around a new nominal state. Re-centering a distribution does not make it a point mass. Testing the correction and reset separately on a known small perturbation helps locate the fault, keeping all correlations between orientation and other variables.

**Also preserve correlations**: If the error is split into $\theta$ orientation and other $a$ variables, the reset transforms $P_{\theta a}$ into $G_\theta P_{\theta a}$ and $P_{a\theta}$ into $P_{a\theta}G_\theta^T$, not just the $P_{\theta\theta}$ block. These terms can transfer information from a visual observation to position, velocity or bias at the next correction. Erroneously canceling them changes the filter. A constructed check consists of comparing the distribution of small perturbations before and after injection in their respective coordinates: the numerical description changes, while the physical states represented must remain close. Testing the reset separately avoids confusing it with the legitimate reduction of uncertainty due to measurement.

**A zero correction gives a reset identity test**: When the injected orientation correction is exactly zero, the reset Jacobian must reduce to the identity and the reset alone must preserve $P$. This is distinct from the preceding measurement update, which may legitimately reduce uncertainty. Separate these two operations when inspecting a trace. For nonzero corrections, the first-order sign of the skew term depends on whether the orientation error is local or global; copying it across conventions changes the represented distribution.

**Blocking errors**: equating a reset of the representation with a disappearance of uncertainty.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Solà, §6.3, equations 285 – 288](https://arxiv.org/abs/1711.02508); symptom and discriminant test proposed by the project; [Solà, Quaternion kinematics, §§5–6, state, correction and reset; Appendix E, noise integration](https://arxiv.org/html/1711.02508v1), consulted 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-FUSION-003 provenance::agent pole::B pole::C
END

## CV-FUSION-004

Objective: Handle timing and missing data. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-004
Question: The camera drops from 30 to 10 frames/s with variable latency, while the IMU stays at 200 Hz. Which timing contract must sensor fusion respect?
Reponse: **Expected answer**: propagate state and covariance IMU sample by IMU sample, with the actual $\Delta t$ between timestamps, because each covariance term depends on it. Apply each camera measurement at its acquisition time, not its reception time. Distinguish a missing measurement from a zero measurement.

**Further explanation**: on a step $\Delta t$, Solà propagates the dynamic term by an exponential; the IMU measurement noise contributes in $\Delta t^2$, the bias random walks in $\Delta t$. The $\Delta t^2$ term assumes per-sample standard deviations: a datasheet noise density $\sigma_c$ first converts to $\sigma_c/\sqrt{\Delta t}$, so the variance actually grows as $\sigma_c^2\Delta t$. A code that propagates once per frame with a frozen $\Delta t$, or ignores lost IMU samples, therefore predicts poor covariance. A delayed image is processed with a state buffer and re-propagation from its acquisition time, or explicitly rejected. Check clocks, delays and order of receipt before retuning the gain.

**Constructed case**: An image received late may correspond to a state already overtaken by several IMU integrations. Correcting it as if it were current conflates motion and delay. Keeping the capture time allows a correction applied to the right state followed by re-propagation, with an explicit policy for measurements that are too old.

**Do not mix density and discrete variance**: for a position–velocity state subjected to a continuous white acceleration of spectral density $q$, the ideal integration gives $Q_d=q\begin{bmatrix}\Delta t^3/3&\Delta t^2/2\\\Delta t^2/2&\Delta t\end{bmatrix}$. If we assume instead a constant random acceleration on each interval, of variance $\sigma_a^2$, the block becomes $\sigma_a^2\begin{bmatrix}\Delta t^4/4&\Delta t^3/2\\\Delta t^3/2&\Delta t^2\end{bmatrix}$. These two analytical cases describe different noises; reusing the same numerical value in the other model is wrong. The powers of $\Delta t$ are therefore not chosen by copying a matrix: they come from the noise model and its integration, with their units.

**Latency can dominate the nominal observation rate**: Constructed example: at a constant angular speed of $90^\circ$/s, applying a camera update 50 ms late as though it were current introduces a $4.5^\circ$ temporal mismatch. Increasing the camera rate does not remove that mismatch. A delayed-state update or replay must also account for correlations with intervening IMU propagation. The required history length follows the observed latency distribution; a single mean delay is inadequate when jitter produces occasional much older measurements.

**Blocking errors**: implicitly keeping a constant step despite varying intervals; timestamping an image at reception.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Solà, §5.4.2, equations 262 – 265, and Appendix E, equations 438 – 440](https://arxiv.org/abs/1711.02508); [Kalibr wiki, IMU Noise Model, discrete-time conversions](https://github.com/ethz-asl/kalibr/wiki/IMU-Noise-Model); time contract and treatment of delays proposed by the project; [Solà, Quaternion kinematics, §§5–6, state, correction and reset; Appendix E, noise integration](https://arxiv.org/html/1711.02508v1), consulted 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-FUSION-004 provenance::agent pole::B pole::C
END

## CV-FUSION-005

Objective: Justify the error-state formulation. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-005
Question: When fusing IMU and camera measurements with quaternion orientation, why estimate a small error around an integrated nominal state rather than the complete state in an EKF?
Reponse: **Expected answer**: the orientation error is minimal, three parameters for three degrees of freedom: we avoid the redundancy of the quaternion and the risk of singular covariance related to its norm constraint. The error remains small and close to the origin, far from the singularities of parameterization: the linearization remains valid, the products of the second order are negligible and the Jacobians simple. Its dynamics are slow, the rapid dynamics being integrated in the nominal state: corrections can happen less often than IMU predictions.

**Further explanation**: the nominal state integrates the IMU measurements without noise terms. The filter predicts the Gaussian law of the error, corrects it upon the arrival of another measurement, injects it into the nominal state and then resets it to zero (CV-FUSION-003). The ESKF does not remove the non-linearity of the measurement model: it limits the region where the linearization is made.

**Intuition**: The nominal state carries the important movement, while the error describes a local neighborhood. The small size of the error justifies a local approximation only as long as the estimate remains close to reality. A bad initialization or a long absence of measurement may leave this domain; keeping a normalized quaternion does not alone establish the consistency of the filter.

**Example of a minimum error state**: A nominal inertial state can hold position $p$, velocity $v$, quaternion $q$, accelerometer bias $b_a$ and gyro bias $b_g$. This represents 16 stored components, but an error of dimension 15 when the orientation uses three local coordinates and gravity is known. A typical correction injects $p\leftarrow p+\delta p$, $v\leftarrow v+\delta v$, $R\leftarrow R\operatorname{Exp}(\delta\theta)$, then the additive biases. The IMU measures a specific force and angular velocity, not directly a position: you have to remove the biases, express the acceleration in the correct coordinate frame and handle gravity according to the model. The exact size and content change if one also estimates gravity or calibration.

**Small errors are a maintained condition**: An error-state representation is a local approximation, so small errors must be maintained by initialization, prediction and timely corrections. A severely wrong initial orientation or a long visual outage can invalidate the linearization even though the nominal quaternion stays normalized. Normalize the representation and assess innovation consistency as different checks. Neither minimal coordinates nor a unit quaternion guarantees that the estimated attitude is near the true attitude.

**Blocking errors**: believing that the ESKF removes all nonlinearity; thinking that the filter directly estimates the complete state.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Solà, Quaternion kinematics, §5.1 and §5.2](https://arxiv.org/abs/1711.02508); [Solà, Quaternion kinematics, §§5–6, state, correction and reset; Appendix E, noise integration](https://arxiv.org/html/1711.02508v1), consulted 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-FUSION-005 provenance::agent pole::B pole::C
END

## CV-FUSION-006

Objective: stabilizing the covariance update. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-006
Question: After thousands of Kalman filter updates, Cholesky factorization of $P$ fails or a variance becomes negative, although the models appear correct. Which implementation issue should be checked, and which update form mitigates it?
Reponse: **Expected answer**: the simple form $P\leftarrow(I-KH)P$ is not guaranteed to remain symmetric or positive definite in finite arithmetic: rounding accumulates. Prefer the Joseph form $P^+=(I-KH)P^-(I-KH)^T+KRK^T$. $P^-$ is the covariance before correction, $H$ is the measurement Jacobian, $K$ is the gain and $R$ is the measurement noise covariance. If $P^-$ and $R$ are symmetric positive semi-definite and the measurement and prediction errors independent, this sum of quadratic terms is positive semi-definite in exact arithmetic. It mitigates the numerical risk without guaranteeing strict positivity in finite precision. The subtraction $P^--KSK^T$, with $S=HP^-H^T+R$, even theoretically equivalent for the optimal gain, remains subject to cancellation. Monitor symmetry and smaller eigenvalue of $P$ over runtime.

**Further explanation**: Solà, who denotes the measurement covariance $V$, gives the simplest form and notes its poor numerical stability. Symmetrizing with $(P+P^T)/2$ hides the asymmetry without correcting a negative eigenvalue. OpenCV 4.13.0's `KalmanFilter::correct` uses the simple form, whereas FilterPy 1.4.5 uses the Joseph form, which also remains valid for a non-optimal gain. To distinguish: a progressive drift with fixed models refers to arithmetic; a $Q$ or a $R$ not positive definite, or poorly sized, refers to the configuration.

**Origin of the Joseph form**: if the error before measurement is $e^-$ and the measurement noise $n$, the linear correction gives $e^+=(I-KH)e^- -Kn$. Taking the covariance and assuming their independence, the two cross terms vanish and we obtain the Joseph form. If measurement and prediction share the same information, these terms are no longer automatically zero: the stability of the algebraic form does not validate the statistical hypothesis. A square-root alternative propagates a covariance factor rather than $P$ directly; it improves the numerical properties in its frame, but requires a consistent implementation of prediction, correction, and reset. Adding an arbitrary diagonal at each failure can hide an invalid model.

**Symmetry repair is not positivity repair**: For a numerically asymmetric covariance, $(P+P^T)/2$ restores symmetry but can retain negative eigenvalues. Conversely, a valid positive-semidefinite covariance may be singular, so strict Cholesky can fail without a negative variance. Check the intended rank, eigenvalue scale and state constraints before adding diagonal jitter. Joseph form reduces cancellation in the update; it does not repair duplicated measurements, invalid noise covariances or an inconsistent error-state reset.

**Blocking errors**: retuning $Q$ or $R$ to hide the problem without examining the update form; assuming that $(I-KH)P$ always remains positive definite in finite precision.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Solà, Quaternion kinematics, §6.1, equations 274 – 276 and note 26](https://arxiv.org/abs/1711.02508); [Chin/JPL 2023, §III-A, equation 14](https://ipnpr.jpl.nasa.gov/progress_report/42-233/42-233A-orig.pdf); [OpenCV 4.13.0, `kalman.cpp` L106–L132](https://github.com/opencv/opencv/blob/4.13.0/modules/video/src/kalman.cpp#L106-L132); [FilterPy 1.4.5, `KalmanFilter.update`](https://github.com/rlabbe/filterpy/blob/1.4.5/filterpy/kalman/kalman_filter.py#L491-L565); discriminating test proposed by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-FUSION-006 provenance::agent pole::B pole::C
END
