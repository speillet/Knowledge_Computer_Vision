# Flashcards — Sensors, rolling shutter and synchronization

reference note: [[20-acquisition-images/references/22-capteurs-horodatage|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-CAPTEURS-001

Objective: separate exhibition and reading rolling shutter. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-CAPTEURS-001
Question: Is a very short exposure sufficient to eliminate all rolling-shutter distortion?
Reponse: **Expected answer**: No: it reduces blur per line, but the lines can still represent different moments.

**Further explanation**: Measure playback time, movement and shutter type; test global shutter or correct.

**Decomposition of the phenomenon**: Exposure describes how long a line accumulates light; reading time determines the offset between lines. A moving scene can therefore produce individually sharp lines but taken at different positions. In a constructed example, a vertical calibration target that moves horizontally may appear inclined, with no marked blur on its edges.

**Proposed verification**: compare immobility, translation and rotation, and then vary exposure and playback time separately when the hardware allows. If the shortening of the exposure improves the sharpness without removing the inclination, the two effects have been well distinguished. A global shutter changes the capture simultaneity; it does not guarantee a fairly short exposure or a good synchronization with another sensor. The projection model used for calibration must remain compatible with the actual acquisition.

**Time model by line**: write $t(y)=t_0+y\tau_r$, where $y$ is the line index, $\tau_r$ is the offset between exposure starts in seconds per line, and $t_0$ is the offset of the first line. For a constant horizontal translation $v_{px}$, the offset between first and last line is approximately $v_{px}(H-1)\tau_r$, with $H$ the height. It depends on the total scan time, distinct from the local drag $|v_{px}|t_e$. It is an ideal built-in model: reading direction, overlay modes and timestamp definition vary depending on the camera. Even a global shutter can transmit its lines successively while having exposed the pixels simultaneously.

**Blocking errors**: Confound sharpness of each line and simultaneity of the whole image.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Full reference]] ; [Basler, Electronic Shutter Types, Rolling Shutter (v136, 2026-10-01)](https://docs.baslerweb.com/electronic-shutter-types#rolling-shutter).
Tags: cv::pilote cv::d02 famille::comparaison cv_id::CV-CAPTEURS-001 provenance::agent pole::B pole::C pole::E pole::F
END

## CV-CAPTEURS-002

Objective: estimate a spatial time lag. Family: reasoning. Provenance: agent.

START
CV-Pilote
ID: CV-CAPTEURS-002
Question: Two sensors observe an object moving at 2 m/s with a 50 ms time offset. What is the approximate spatial error under uniform translation?
Reponse: **Expected answer**: 0,10 m, before rotation and estimation effects.

**Further explanation**: The calculation is used to differentiate timing and spatial noise; announce the supposed clock and movement.

**Calculation and interpretation**: first convert 50 ms to 0,050 s, then apply $\Delta x=v\Delta t$. The result measures the distance traveled during the capture gap; it is neither a variance nor a constant calibration error. If the speed doubles, this term doubles in the advertised model. If the object is still, the same delay can become invisible in this check.

**Use in diagnostics**: compare the order of magnitude obtained with the observed deviation before refining an extrinsic. A shift that varies with speed is compatible with a time problem. This does not prove that the clock is the only cause: it is also necessary to check which moment represents the timestamp and if the latency is constant. To express the offset in pixels, we would still need the depth, the relative movement and the projection model.

**Moving to an image measurement**: under perspective projection $u=f_xX/Z+c_x$, a small time error gives $\Delta u\approx f_x(v_XZ-Xv_Z)\Delta t/Z^2$. Here $X,Z$ are the camera coordinates in meters, $v_X,v_Z$ their derivatives in m/s, $f_x$ is in pixels and $c_x$ the main point. The derivative is local and here ignores the rotation; it shows why 0,10 m error world does not correspond to a universal number of pixels. For a target in the center, at 10 m, with $f_x=1000$ px and a transverse movement of 2 m/s, 50 ms give about 10 px. The sign depends on the relative movement and the direction of the shift.

**Blocking errors**: Use this model for any rotating scene with no other assumptions.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Full reference]]; [Basler, Electronic Shutter Types, Rolling Shutter (v136, 2026-10-01)](https://docs.baslerweb.com/electronic-shutter-types#rolling-shutter); kinematic calculation $v\Delta t$ of the project.
Tags: cv::pilote cv::d02 famille::raisonnement cv_id::CV-CAPTEURS-002 provenance::agent pole::B pole::C pole::E pole::F
END

## CV-CAPTEURS-003

Objective: Calibration and time. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-CAPTEURS-003
Question: Track C — diagnosis: camera–LiDAR obstacles appear doubled during turns but aligned at rest. How should this be investigated?
Reponse: **Expected answer**: Check offsets/drift clocks, time per scan point, deskew then extrinsic in the same coordinate frame. Compare motionless sequences and controlled movements.

**Further explanation**: Motion makes a temporal defect visible; spatial calibration can also be false. Measure residuals according to speed and rotation before choosing a correction.

**Discriminant Reasoning**: An extrinsic describes a fixed spatial transformation; a temporal defect associates observations of different poses. A compensating translation can make a given turn coincide while degrading the opposite turn. The deskew brings the points of a scan back to a common time from an estimated movement: it only works correctly if its timestamps and its model are consistent.

**Protocol built**: record a static scene seen by the vehicle when stationary, in translation and then in rotation in both directions. Trace the residuals according to the time in the scan and the angular speed. Compare a time correction alone, a spatial correction alone and their combination, on a reserved sequence. A good alignment at a standstill constrains some spatial errors, but does not validate the time chain or all geometric configurations.

**Chain of transformations to be explained**: if $T_{AB}$ transforms B to A, a point LiDAR $p_L$ acquired at $t_L$ can be brought to the camera of $t_C$ by $p_C=T_{CW}(t_C)T_{WL}(t_L)p_L$ in homogeneous coordinates. Under rigid mounting and consistent clocks, the fixed extrinsics are composed with the time-dependent poses. Implicitly replacing $t_L$ with $t_C$ removes the movement to be compensated and creates a structured error, especially in rotation or at great distance. The deskew requires the time of each point, an interpolated pose and an announced reference time. If objects move independently of the vehicle, the ego movement alone is not enough to make them static.

**Blocking errors**: Fix permanently by fixed translation without examining the timestamps.

**Criteria for correction of the case**: explicit task and constraints, announced assumptions, justified choice, discriminating verification, limit of the conclusion. Case built, without field observation.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Full reference]]; [Zhang and Singh 2014, LOAM, §§II and V, motion distortion correction](https://www.roboticsproceedings.org/rss10/p07.pdf); camera survey – LiDAR built by the project.
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-CAPTEURS-003 provenance::agent pole::B pole::C pole::E pole::F cas_pole::C::diagnostic
END

## CV-CAPTEURS-004

Objective: interpret the output of sensors. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-CAPTEURS-004
Question: Why can a radar Doppler measurement not directly replace a 3D Cartesian velocity?
Reponse: **Expected answer**: It constrains the radial component relative to the sensor according to its measurement model.

**Further explanation**: Transform coordinate frames and ego movement, then merge other observations for unmeasured components. Covariances must follow the transformation.

**Model of measurement**: if $\hat r$ is the unit vector of the sensor towards the target and $v_{rel}$ its relative speed in the same coordinate frame, the ideal measurement constrains $v_r=\hat r^Tv_{rel}$, with a sign convention to be announced. It is a scalar projection. Any component orthogonal to $\hat r$ can change without changing this instantaneous measurement.

**Constructed example**: A target that crosses the side of the field can have a high velocity and a low radial component at a given moment. To conclude that it is immobile would therefore be unjustified. To find more components, exploit other directions, several moments or other sensors with an explicit dynamic model. If the wearer moves, his own movement contributes to the relative speed. A merger must address this contribution and measurement uncertainty, rather than copying the Doppler scalar into three axes.

**Elemental Observability**: for $H=\hat r^T$, the scalar measurement $z=Hv_{rel}+\epsilon$ constrains only one direction of a vector with three components. Its zero space has two dimensions: adding an orthogonal velocity to $\hat r$ leaves $z$ unchanged. A Cartesian velocity becomes conceivable with several independent directions and a model linking their observations to the same movement; three quasi-parallel measurements can remain very poorly conditioned. A rotation of coordinate frame gives $v'=Rv$ and $P'=RPR^T$ for a covariance $P$ and an exact rotation $R$. It re-expresses the available information without creating the two missing components; the uncertainty of the calibration may need to be added separately.

**Blocking errors**: Take a radial velocity for the three components of the movement.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Full reference]] ; [Texas Instruments, TIDUF01 (2021), §2.4.9](https://www.ti.com/lit/ug/tiduf01/tiduf01.pdf).
Tags: cv::pilote cv::d02 famille::comprehension cv_id::CV-CAPTEURS-004 provenance::agent pole::B pole::C pole::E pole::F
END
