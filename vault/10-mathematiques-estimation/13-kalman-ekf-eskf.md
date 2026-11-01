# Flashcards — Kalman, EKF, UKF and ESKF for sensor fusion

reference note: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-FUSION-001

Objective: distinguish filter variants. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-001
Question: How do EKF, UKF and ESKF differ, without ranking them by absolute accuracy?
Reponse: **Expected answer**: The EKF linearizes models and measurements around the current estimate. The UKF propagates $2n+1$ sigma-points selected deterministically through nonlinear functions, without Jacobian. The ESKF integrates a nonlinear nominal state and estimates a small error around it, with the prediction and correction equations of a EKF applied to this error. These names therefore describe choices that combine, not three exclusive categories.

**Further explanation**: According to Julier and Uhlmann, the unscented transform calculates the mean with an order of precision greater than the EKF, but the covariance with the same order. The result depends on the model, noise, initialization, and time consistency; an algorithm label is not a universal ranking.

**Choice of design**: Begin with the representation of state, non-linearity of observations, and acceptable cost. The selected filter must be evaluated on consistent innovations and trajectory errors. A better local approximation of propagation does not correct a bad extrinsic, false association, or offbeat clock; these defects belong to the model and the data.

**Common Basis of Calculation**: in an approximation EKF, $x^-=f(x^+,u)$ and $P^-=FP^+F^T+Q$, then $K=P^-H^T(HP^-H^T+R)^{-1}$. $F$ and $H$ are the Jacobians of dynamics and measurement; $Q$ and $R$ describe their uncertainties in the coordinates and no time announced. We correct with innovation, by solving a system to calculate the gain rather than an explicit inverse. The UKF replaces some of these linearizations by the propagation of weighted points; the ESKF changes the coordinates in which the small correction is estimated. A truly multimodal distribution, like two possible visual associations, is not rendered unimodal by this change of calculation.

**Blocking errors**: say that UKF is always better or that ESKF removes nonlinearity.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Solà, §5.2, §6.1, equation 278, and Appendix E, equations 439 – 440](https://arxiv.org/abs/1711.02508); [Julier and Uhlmann 1997, SPIE 3068, §3, equations 12 – 14](https://doi.org/10.1117/12.280797); [Solà, Quaternion kinematics, §§5 – 6, status, correction and reset; Appendix E, noise integration](https://arxiv.org/html/1711.02508v1), see 2026-10-30.
Tags: cv::pilote cv::d01 famille::comprehension cv_id::CV-FUSION-001 provenance::agent pole::B pole::C
END

## CV-FUSION-002

Objective: interpret a standardized innovation. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-002
Question: In a filter, $\nu$ is the innovation, defined as measurement minus prediction, and $S$ is its positive-definite covariance. What does $\nu^TS^{-1}\nu$ measure in an innovation check?
Reponse: **Expected answer**: this is the square of the measurement/prediction deviation weighted by its uncertainty, a Mahalanobis distance without unity. If the model, Gaussian noises and $S$ are correct, it follows a law of $\chi^2$ to $m$ degrees of freedom, $m$ being the dimension of the measurement. We therefore reject a measure beyond a chosen quantile, for example $\chi^2_{3;0{,}95}\approx7{,}81$.

**Further explanation**: DeepSORT thus excludes associations beyond the quantile to 95% for a measurement of dimension 4, or 9,4877. The threshold depends on $m$ and the accepted risk, not units. A rejection signals a gap between prediction, stochastic model and observation, without saying which is involved; it also does not prove the identity of the right object. Too often high or low values on a sequence signal an over- or under-trusting filter.

**Reading the Gatting**: The test removes associations that are too incompatible with the assumed uncertainty. It does not necessarily select a single association among the eligible ones. A filter that is too uncertain can accept many candidates; an overconfident filter can reject the right measure. The assignment and statistical calibration therefore remain two separate controls.

**Non-reverse calculation and selection effect**: if $S=LL^T$, solve $Le=\nu$ and then calculate $e^Te$ gives the score. For independent measurements of fixed dimensions, its nominal expectation is $m$, before selection. On the other hand, keeping only observations that have passed the gating artificially reduces the average observed; it can no longer be naively compared to $m$ to conclude a too great covariance. Similarly, testing multiple candidates and then retaining the best changes the distribution. Check noise consistency on baseline observations and consider releases. A succession of innovations of the same sign also reveals a temporal structure that a histogram of norms can mask.

**Blocking errors**: confuse large residual in pixels and large statistical inconsistency; apply the same threshold regardless of the size of the measurement.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Gamse et al. 2014, §2.2.2, equations 5 – 10, and §3.4.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/); [Wojke et al. 2017, DeepSORT, §2.2](https://arxiv.org/abs/1703.07402); quantiles recalculated by the project; [Solà, Quaternion kinematics, §§5 – 6, status, correction and reset; Appendix E, noise integration](https://arxiv.org/html/1711.02508v1), consult the 2026-10-30.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-FUSION-002 provenance::agent pole::B pole::C
END

## CV-FUSION-003

Objective: preserve the covariance ESKF. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-003
Question: In a camera–IMU ESKF, orientation covariance drops almost to zero after every correction. Subsequent measurements are rejected by gating or barely change the state. Which reset error should be investigated first, and what is the correct treatment?
Reponse: **Expected answer**: Look for a reset of $P$ at the time the average error is injected and then reset. The reset changes only the reference point of the error, not the available information: on pose $\hat{\delta x}\leftarrow0$ but $P\leftarrow GPG^T$, with $G$ the Jacobian of the reset.

**Further explanation**: In the local angular error convention of Solà, $R_{vrai}=R_{nom}\operatorname{Exp}(\delta\theta)$, $G$ is equal to the identity except on the orientation block $G_\theta\approx I-[\hat{\delta\theta}/2]_\times$ in the first order. Taking $G\approx I$ neglects this small coordinate correction, without cancelling $P$. A global error convention requires its own Jacobian. To differentiate a $R$ too small, look where falls $P$: at the moment of the reset, it is the reset; during the update, it is the weighting of the measurements. A zero covariance declares a fictitious perfect knowledge.

**Geometric Intuition**: After injection, the same uncertainty is described around a new nominal state. Refocusing a distribution does not make it punctual. Testing the correction and reset separately on a known small perturbation helps locate the fault, keeping all correlations between orientation and other variables.

**Also preserve correlations.**: If the error is split into $\theta$ orientation and other $a$ variables, the reset transforms $P_{\theta a}$ into $G_\theta P_{\theta a}$ and $P_{a\theta}$ into $P_{a\theta}G_\theta^T$, not just the $P_{\theta\theta}$ block. These terms can transfer information from a visual observation to position, speed, or bias at the next correction. Erroneously canceling them changes the filter. A constructed check consists of comparing the distribution of small perturbations before and after injection in their respective coordinates: the numerical description changes, while the physical states represented must remain close. Testing the reset separately avoids confusing it with the legitimate reduction of uncertainty due to measurement.

**Blocking errors**: assimilating representation reset and disappearance of uncertainty.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Solà, §6.3, equations 285 – 288](https://arxiv.org/abs/1711.02508); symptom and discriminant test proposed by the project; [Solà, Quaternion kinematics, §§5 – 6, status, correction and reset; Appendix E, noise integration](https://arxiv.org/html/1711.02508v1), consult the 2026-10-30.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-FUSION-003 provenance::agent pole::B pole::C
END

## CV-FUSION-004

Objective: Processing time and missing data. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-004
Question: The camera drops from 30 to 10 frames/s with variable latency, while the IMU stays at 200 Hz. Which timing contract must sensor fusion respect?
Reponse: **Expected answer**: propagate state and covariance sample IMU per sample, with the actual $\Delta t$ between timestamps, because each term of covariance depends on it. Apply each camera measurement at its moment of acquisition, no reception. Distinguish between lack of measurement and zero measurement.

**Further explanation**: on a step $\Delta t$, Solà propagates the dynamic term by an exponential; the measurement noise IMU contributes to this in $\Delta t^2$, the random steps of the biases in $\Delta t$. A code that propagates once per frame with a frozen $\Delta t$, or ignores lost IMU samples, therefore predicts poor covariance. A delayed image is processed by state buffer and re-propagation from its moment of acquisition, or explicitly rejects itself. Check clocks, delays and order of receipt before retouching the gain.

**Constructed case**: An image received late may correspond to a state already exceeded by several IMU integrations. Correcting it as if it were current conflates motion and delay. Keeping the capture time allows to consider a correction to the good condition and then a repropagation, with an explicit policy for measures too old.

**Do not mix density and discrete variance**: for a position – speed state subjected to a continuous white acceleration of spectral density $q$, the ideal integration gives $Q_d=q\begin{bmatrix}\Delta t^3/3&\Delta t^2/2\\\Delta t^2/2&\Delta t\end{bmatrix}$. If we assume instead a constant random acceleration on each interval, of variance $\sigma_a^2$, the block becomes $\sigma_a^2\begin{bmatrix}\Delta t^4/4&\Delta t^3/2\\\Delta t^3/2&\Delta t^2\end{bmatrix}$. These two analytical cases describe different noises; replacing one with the other with an unchanged numerical value is false. The powers of $\Delta t$ are therefore not chosen by copying a matrix: they come from the noise model and its integration, with their units.

**Blocking errors**: implicitly maintain a constant step despite different intervals; date an image when it is received.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Solà, §5.4.2, equations 262 – 265, and Appendix E, equations 438 – 440](https://arxiv.org/abs/1711.02508); time contract and treatment of delays proposed by the project; [Solà, Quaternion kinematics, §§5 – 6, status, correction and reset; Appendix E, noise integration](https://arxiv.org/html/1711.02508v1), consulted the 2026-10-30.
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-FUSION-004 provenance::agent pole::B pole::C
END

## CV-FUSION-005

Objective: justify the formulation at the state of error. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-005
Question: When fusing IMU and camera measurements with quaternion orientation, why estimate a small error around an integrated nominal state rather than the complete state in an EKF?
Reponse: **Expected answer**: the orientation error is minimal, three parameters for three degrees of freedom: we avoid the redundancy of the quaternion and the risk of singular covariance related to its norm constraint. The error remains small and close to the origin, far from the singularities of parameterization: the linearization remains valid, the products of the second order are negligible and the Jacobians simple. Its dynamics are slow, the rapid dynamics being integrated in the nominal state: corrections can happen less often than predictions IMU.

**Further explanation**: the nominal state integrates the noise-free IMU measurements. The filter predicts the Gaussian law of the error, corrects it upon the arrival of another measurement, injects it into the nominal state and then resets it to zero (CV-FUSION-003). The ESKF does not remove the non-linearity of the measurement model: it limits the area where one linearizes.

**Intuition for follow-up**: The nominal state carries the important movement, while the error describes a local neighborhood. The small size of the error justifies a local approximation only as long as the estimate remains close to reality. A bad initialization or a long absence of measurement may leave this domain; keeping a normal quaternion does not alone establish the consistency of the filter.

**Example of a minimum error state**: A nominal inertial state can hold position $p$, speed $v$, quaternion $q$, accelerometer bias $b_a$ and gyro bias $b_g$. This represents 16 stored components, but an error of dimension 15 when the orientation uses three local coordinates and the gravity is known here. A typical correction injects $p\leftarrow p+\delta p$, $v\leftarrow v+\delta v$, $R\leftarrow R\operatorname{Exp}(\delta\theta)$, then the additive biases. The IMU measures a specific force and angular velocity, not directly a position: you have to remove the biases, express the acceleration in the correct coordinate frame and process the gravity according to the model. The exact size and content change if one also estimates gravity or calibration.

**Blocking errors**: believe that the ESKF removes all non-linearity; think that the filter directly estimates the complete state.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Solà, Quaternion kinematics, §5.1 and §5.2](https://arxiv.org/abs/1711.02508); [Solà, Quaternion kinematics, §§5 – 6, status, correction and reset; Appendix E, noise integration](https://arxiv.org/html/1711.02508v1), see 2026-10-30.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-FUSION-005 provenance::agent pole::B pole::C
END

## CV-FUSION-006

Objective: stabilizing the covariance update. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-FUSION-006
Question: After thousands of Kalman filter updates, Cholesky factorization of $P$ fails or a variance becomes negative, although the models appear correct. Which implementation issue should be checked, and which update form mitigates it?
Reponse: **Expected answer**: the simple form $P\leftarrow(I-KH)P$ is neither symmetric nor positive definite in finite arithmetic: rounding accumulates. Prefer the form of Joseph $P^+=(I-KH)P^-(I-KH)^T+KRK^T$. $P^-$ is the covariance before correction, $H$ is the measurement Jacobian, $K$ is the gain and $R$ is the measurement noise covariance. If $P^-$ and $R$ are positive semi-definite symmetric and independent measurement and prediction errors, this sum of quadratic terms is positive semi-definite in exact arithmetic. It mitigates digital risk without guaranteeing strict positivity in finite precision. The subtraction $P^--KSK^T$, with $S=HP^-H^T+R$, even theoretically equivalent for the optimal gain, remains subject to cancellation. Monitor symmetry and smaller eigenvalue of $P$ over runtime.

**Further explanation**: Solà, which scores $V$ as the measuring covariance, gives the simplest shape and signals its poor numerical stability. Symmetrize $(P+P^T)/2$ hides the asymmetry without correcting a negative eigenvalue. To distinguish: a progressive drift with fixed models refers to arithmetic; a $Q$ or a $R$ not positive definite, or poorly sized, refers to the configuration.

**Origin of Joseph**: if the error before measurement is $e^-$ and the measurement noise $n$, the linear correction gives $e^+=(I-KH)e^- -Kn$. Taking the covariance and assuming their independence, the two crossed terms cancel each other out and we find the sum of Joseph. If measurement and prediction share the same information, these terms are no longer automatically zero: the stability of the algebraic form does not validate the statistical hypothesis. A square-root alternative propagates a covariance factor rather than $P$ directly; it improves the numerical properties in its frame, but requires a consistent implementation of prediction, correction, and reset. Adding an arbitrary diagonal to each failure can hide an invalid template.

**Blocking errors**: retouch $Q$ or $R$ to hide the problem without looking at the shape of update; assume that $(I-KH)P$ always remains positive definite in finite precision.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Full reference]]; [Solà, Quaternion kinematics, §6.1, equations 274 – 276 and note 26](https://arxiv.org/abs/1711.02508); [Chin/JPL 2023, §III-A, equation 14](https://ipnpr.jpl.nasa.gov/progress_report/42-233/42-233A-orig.pdf); discriminatory test proposed by the project.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-FUSION-006 provenance::agent pole::B pole::C
END
