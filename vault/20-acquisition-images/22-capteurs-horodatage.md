# Flashcards — Sensors, rolling shutter and synchronization

reference note: [[20-acquisition-images/references/22-capteurs-horodatage|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-CAPTEURS-001

Objective: Separate exposure and readout in a rolling shutter. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-CAPTEURS-001
Question: Is a very short exposure sufficient to eliminate all rolling-shutter distortion?
Reponse: **Expected answer**: No: it reduces blur per line, but the lines can still represent different moments.

**Further explanation**: Measure readout time, motion and shutter type; test a global shutter or correct with a rolling-shutter model.

**Decomposition of the phenomenon**: Exposure describes how long a line accumulates light; readout time determines the offset between lines. A moving scene can therefore produce individually sharp lines taken at different positions. In a constructed example, a vertical calibration target that moves horizontally may appear inclined, with no marked blur on its edges.

**Proposed verification**: compare a static scene, translation and rotation, then vary exposure and readout time separately when the hardware allows. If shortening the exposure improves sharpness without removing the inclination, the two effects have been separated. A global shutter changes the simultaneity of capture; it does not guarantee a short enough exposure or good synchronization with another sensor. The projection model used for calibration must remain compatible with the actual acquisition.

**Per-row time model**: write $t(y)=t_0+y\tau_r$, where $y$ is the row index, $\tau_r$ is the offset between exposure starts in seconds per row, and $t_0$ is the exposure-start time of the first row. For a constant horizontal translation $v_{px}$, the offset between the first and last rows is approximately $v_{px}(H-1)\tau_r$, with $H$ the height. It depends on the total readout time, distinct from the local blur $|v_{px}|t_e$. It is an idealized constructed model: readout direction, overlapping modes and timestamp definition vary between cameras. Even a global shutter can transmit its rows successively after exposing all pixels simultaneously.

**Short exposure can coexist with large skew**: Constructed example: a sensor has a 20 ms first-to-last-row exposure-start offset and uses 0.1 ms exposure. At 1000 px/s horizontal image motion, each row has only 0.1 px blur, while top-to-bottom displacement is about 20 px. The image can therefore look locally sharp and globally sheared. Reducing exposure further does little to this shear; changing the readout timing or modeling per-row pose addresses a different part of the acquisition process.

**Blocking errors**: Confusing the sharpness of each row with the simultaneity of the whole image.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Full reference]] ; [Basler, Electronic Shutter Types, Rolling Shutter (v138, 2026-11-12)](https://docs.baslerweb.com/electronic-shutter-types#rolling-shutter) ; [Meingast et al. 2005, §2 (exposure adds blur, not geometric distortion)](https://arxiv.org/abs/cs/0503076) ; [Oth et al. 2013, §1 (line delay)](https://openaccess.thecvf.com/content_cvpr_2013/papers/Oth_Rolling_Shutter_Camera_2013_CVPR_paper.pdf). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::comparaison cv_id::CV-CAPTEURS-001 provenance::agent pole::B pole::C pole::E pole::F
END

## CV-CAPTEURS-002

Objective: estimate a spatial time lag. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-CAPTEURS-002
Question: Two sensors observe an object moving at 2 m/s with a 50 ms time offset. What is the approximate spatial error under uniform translation?
Reponse: **Expected answer**: 0.10 m, before rotation and estimation effects.

**Further explanation**: The calculation helps distinguish a timing error from spatial noise; state the assumed clock and motion.

**Calculation and interpretation**: first convert 50 ms to 0.050 s, then apply $\Delta x=v\Delta t$. The result measures the distance traveled during the capture gap; it is neither a variance nor a constant calibration error. If the speed doubles, this term doubles in the stated model. If the object is still, the same delay can become invisible in this check.

**Use in diagnostics**: compare the order of magnitude obtained with the observed deviation before refining an extrinsic. A shift that varies with speed is compatible with a time problem. This does not prove that the clock is the only cause: also check which instant the timestamp represents and whether the latency is constant. To express the offset in pixels, the depth, the relative motion and the projection model are still needed.

**From world error to image error**: under perspective projection $u=f_xX/Z+c_x$, a small time error gives $\Delta u\approx f_x(v_XZ-Xv_Z)\Delta t/Z^2$. Here $X,Z$ are camera coordinates in meters, $v_X,v_Z$ their derivatives in m/s, $f_x$ is in pixels and $c_x$ is the principal point. The derivative is local and ignores rotation here; it shows why a 0.10 m world error does not correspond to a universal number of pixels. For a target at the image centre at 10 m, with $f_x=1000$ px and a transverse motion of 2 m/s, 50 ms give about 10 px. The sign depends on the relative motion and the direction of the offset.

**Offset and drift need different corrections**: Model the clocks locally as $t_B=a t_A+b$: $b$ is offset and $a-1$ is fractional drift. A constructed 20 ppm drift accumulates 12 ms over ten minutes, corresponding to 24 mm at 2 m/s. A one-time offset calibration cannot remove this accumulating discrepancy. Record the time span of synchronization validation, and distinguish clock error from variable packet delivery latency before interpreting an apparent extrinsic shift.

**Blocking errors**: Applying this translation model to a rotating scene without further assumptions.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Full reference]]; [Rehder 2018, ETH doctoral thesis, §3.1 (clock synchronization versus temporal offsets; jitter, skew and delay)](https://doi.org/10.3929/ethz-b-000334970); kinematic calculation $v\Delta t$ and clock model of the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::raisonnement cv_id::CV-CAPTEURS-002 provenance::agent pole::B pole::C pole::E pole::F
END

## CV-CAPTEURS-003

Objective: Separate calibration and timing errors. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-CAPTEURS-003
Question: Track C — diagnosis: camera–LiDAR obstacles appear doubled during turns but aligned at rest. How should this be investigated?
Reponse: **Expected answer**: Check clock offsets and drift, the time of each scan point, deskewing, then the extrinsic calibration in a common coordinate frame. Compare static sequences with controlled motions.

**Further explanation**: Motion makes a timing defect visible; the spatial calibration can also be wrong. Measure residuals as a function of speed and rotation before choosing a correction.

**Discriminating reasoning**: An extrinsic describes a fixed spatial transformation; a timing defect associates observations taken at different poses. A compensating translation can make one turn coincide while degrading the opposite turn. Deskewing brings the points of a scan back to a common time using an estimated motion: it only works correctly if its timestamps and its model are consistent.

**Constructed protocol**: record a static scene seen by the vehicle when stationary, in translation and then in rotation in both directions. Plot the residuals against the time within the scan and the angular speed. Compare a time correction alone, a spatial correction alone and their combination, on a held-out sequence. A good alignment at a standstill constrains some spatial errors, but does not validate the timing chain or all geometric configurations.

**Explicit chain of transformations**: if $T_{AB}$ maps coordinates from B to A, a LiDAR point $p_L$ acquired at $t_L$ can be brought into the camera frame at $t_C$ by $p_C=T_{CW}(t_C)T_{WL}(t_L)p_L$ in homogeneous coordinates. Under rigid mounting and consistent clocks, the fixed extrinsics are composed with the time-dependent poses. Implicitly replacing $t_L$ with $t_C$ ignores the motion that must be compensated and creates a structured error, especially in rotation or at long range. Deskewing requires the time of each point, an interpolated pose and a stated reference time. If objects move independently of the vehicle, ego-motion alone is not enough to make them static.

**Turning exposes a lever-arm timing error**: For rigid-body angular velocity $\omega$ and sensor lever arm $\ell$, the sensor velocity includes $\omega\times\ell$. A time error then induces an approximate displacement $(\omega\times\ell)\Delta t$ even when the body origin translates little. This explains why a calibration can look correct at rest and fail during turns. Use opposite turn directions and different speeds in a proposed check: timing-induced error changes with motion, while a fixed rigid-transform error follows another pattern.

**Blocking errors**: Compensating permanently with a fixed translation without examining the timestamps.

**Grading criteria for the case**: explicit task and constraints, stated assumptions, justified choice, discriminating check, limits of the conclusion. Constructed case, without field observation.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Full reference]]; [Zhang and Singh 2014, LOAM, §III and §V-C, motion distortion correction](https://www.roboticsproceedings.org/rss10/p07.pdf); [Rehder 2018, ETH doctoral thesis, §3.3.1 eqs. 3.2–3.4 (time offset observable through motion)](https://doi.org/10.3929/ethz-b-000334970); camera–LiDAR investigation constructed by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-CAPTEURS-003 provenance::agent pole::B pole::C pole::E pole::F cas_pole::C::diagnostic
END

## CV-CAPTEURS-004

Objective: interpret the output of sensors. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-CAPTEURS-004
Question: Why can a radar Doppler measurement not directly replace a 3D Cartesian velocity?
Reponse: **Expected answer**: It constrains the radial component relative to the sensor according to its measurement model.

**Further explanation**: Transform coordinate frames and compensate ego-motion, then fuse other observations for the unmeasured components. Covariances must follow the transformation.

**Measurement model**: if $\hat r$ is the unit vector from the sensor towards the target and $v_{rel}$ its relative velocity in the same coordinate frame, the ideal measurement constrains $v_r=\hat r^Tv_{rel}$, with a sign convention to be stated. It is a scalar projection. Any component orthogonal to $\hat r$ can change without changing this instantaneous measurement.

**Constructed example**: A target crossing the field of view laterally can have a high velocity and a low radial component at a given moment. Concluding that it is stationary would therefore be unjustified. To recover more components, exploit other directions, several instants or other sensors with an explicit dynamic model. If the carrier platform moves, its own motion contributes to the relative velocity. A fusion filter must handle this contribution and the measurement uncertainty, rather than copying the Doppler scalar into three axes.

**Elementary observability**: for $H=\hat r^T$, the scalar measurement $z=Hv_{rel}+\epsilon$ constrains only one direction of a vector with three components. Its null space has two dimensions: adding a velocity orthogonal to $\hat r$ leaves $z$ unchanged. A Cartesian velocity becomes recoverable with several independent directions and a model linking their observations to the same motion; three nearly parallel measurements can remain very poorly conditioned. A change of coordinate frame gives $v'=Rv$ and $P'=RPR^T$ for a covariance $P$ and an exact rotation $R$. It re-expresses the available information without creating the two missing components; the uncertainty of the calibration may need to be added separately.

**Radial speed depends on relative motion**: A static wall can have nonzero measured Doppler when the radar platform moves. With line-of-sight unit vector $\hat r$, the ideal translational term is $\hat r^T(v_{target}-v_{sensor})$, with sign set by the sensor contract. Compensating ego motion requires the sensor velocity at its lever arm and measurement time. A zero Doppler value therefore does not prove a stationary object, and a nonzero value does not by itself prove independent object motion.

**Blocking errors**: Taking a radial velocity for the three components of the motion.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Full reference]] ; [Texas Instruments, TIDUF01 (2021), §2.4.9 (relative radial velocity, ego-motion fit)](https://www.ti.com/lit/ug/tiduf01/tiduf01.pdf). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::comprehension cv_id::CV-CAPTEURS-004 provenance::agent pole::B pole::C pole::E pole::F
END
