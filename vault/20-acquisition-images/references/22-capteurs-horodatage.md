---
id: CV-CAPTEURS
type: methode
domaine: d02
poles: [B, C, E, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 6
prerequis: ["CV-SE3"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d02]
---
# Sensors, rolling shutter and synchronization

## Problem, data and assumptions

Link images, measurements IMU, LiDAR, radar or ToF to the same time and explicit coordinate frames. A frame, a LiDAR scan and an inertial measurement are not instantaneous observations of the same duration.

## Prerequisites and competencies

**Required prerequisites**: [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Distinguish capture time, integration time, read and packet arrival. The rolling shutter shifts the lines; a rotating scan samples directions at distinct times. Hardware trigger and clock synchronization should be measured, not assumed.

## Mathematics, conventions and units

With speed $v$ in m/s and delay $\Delta t$ in s, an apparent shift of the order of $v\Delta t$ appears in uniform translation. Rotation adds an effect dependent on the lever arm and depth. LiDAR/ToF infer a propagation distance; Doppler radar provides a radial velocity, not directly the full velocity vector 3D.

## Parameters and properties

Record clock origin, offset, drift, latency, frequency and time per point/line. A fixed extrinsic pose does not always correct a time delay. A short exposure alone does not remove the rolling shutter.

## Cost and implementation

Deskew and interpolation require movement and timestamps; their accuracy depends on these models. No ROS 2 or drivers are running; check formats and QoS before a real example.

## Evaluation and controlled variation

Analytical case: at 2 m/s and 50 ms difference, provide 0,10 m translation shift. check separately time and extrinsic on stationary sequences, then moving sequences.

## Failure modes and diagnosis

Obstacles break out especially in turns: compare data at the same time, deskew, extrinsic and sense of transformations. Immobility can mask an offset.

## Alternatives and applications

Global shutter, triggered sensors, time correction or rolling shutter model according to cadence and movement; no sensor is ideal for all conditions.

## Guided reasoning and proposed checks

These constructed cases develop separate exposure time, reading and synchronization. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-CAPTEURS-001

**Question of work**: Is a very short exposure sufficient to eliminate all rolling-shutter distortion?

**Reference Response**: No: it reduces blur per line, but the lines can still represent different moments.

**Decomposition of the phenomenon**: Exposure describes how long a line accumulates light; reading time determines the offset between lines. A moving scene can therefore produce individually sharp lines but taken at different positions. In a constructed example, a vertical calibration target that moves horizontally may appear inclined, with no marked blur on its edges.

**Proposed verification**: compare immobility, translation and rotation, and then vary exposure and playback time separately when the hardware allows. If the shortening of the exposure improves the sharpness without removing the inclination, the two effects have been well distinguished. A global shutter changes the capture simultaneity; it does not guarantee a fairly short exposure or a good synchronization with another sensor. The projection model used for calibration must remain compatible with the actual acquisition.

### Case linked to CV-CAPTEURS-004

**Question of work**: Why can a radar Doppler measurement not directly replace a 3D Cartesian velocity?

**Reference Response**: It constrains the radial component relative to the sensor according to its measurement model.

**Model of measurement**: if $\hat r$ is the unit vector of the sensor towards the target and $v_{rel}$ its relative speed in the same coordinate frame, the ideal measurement constrains $v_r=\hat r^Tv_{rel}$, with a sign convention to be announced. It is a scalar projection. Any component orthogonal to $\hat r$ can change without changing this instantaneous measurement.

**Constructed example**: A target that crosses the side of the field can have a high velocity and a low radial component at a given moment. To conclude that it is immobile would therefore be unjustified. To find more components, exploit other directions, several moments or other sensors with an explicit dynamic model. If the wearer moves, his own movement contributes to the relative speed. A merger must address this contribution and measurement uncertainty, rather than copying the Doppler scalar into three axes.

**Documentary reference for this pass**: [Basler, Electronic Shutter Types](https://docs.baslerweb.com/electronic-shutter-types), global and rolling shutter. The other developments are in the [flashcards](../22-capteurs-horodatage.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-CAPTEURS-001

**Situation**: Is a very short exposure sufficient to eliminate all rolling-shutter distortion?

**Time model by line**: write $t(y)=t_0+y\tau_r$, where $y$ is the line index, $\tau_r$ is the offset between exposure starts in seconds per line, and $t_0$ is the offset of the first line. For a constant horizontal translation $v_{px}$, the offset between first and last line is approximately $v_{px}(H-1)\tau_r$, with $H$ the height. It depends on the total scan time, distinct from the local drag $|v_{px}|t_e$. It is an ideal built-in model: reading direction, overlay modes and timestamp definition vary depending on the camera. Even a global shutter can transmit its lines successively while having exposed the pixels simultaneously.

### CV-CAPTEURS-002

**Situation**: Two sensors observe an object moving at 2 m/s with a 50 ms time offset. What is the approximate spatial error under uniform translation?

**Moving to an image measurement**: under perspective projection $u=f_xX/Z+c_x$, a small time error gives $\Delta u\approx f_x(v_XZ-Xv_Z)\Delta t/Z^2$. Here $X,Z$ are the camera coordinates in meters, $v_X,v_Z$ their derivatives in m/s, $f_x$ is in pixels and $c_x$ the main point. The derivative is local and here ignores the rotation; it shows why 0,10 m error world does not correspond to a universal number of pixels. For a target in the center, at 10 m, with $f_x=1000$ px and a transverse movement of 2 m/s, 50 ms give about 10 px. The sign depends on the relative movement and the direction of the shift.

### CV-CAPTEURS-003

**Situation**: Track C — diagnosis: camera–LiDAR obstacles appear doubled during turns but aligned at rest. How should this be investigated?

**Chain of transformations to be explained**: if $T_{AB}$ transforms B to A, a point LiDAR $p_L$ acquired at $t_L$ can be brought to the camera of $t_C$ by $p_C=T_{CW}(t_C)T_{WL}(t_L)p_L$ in homogeneous coordinates. Under rigid mounting and consistent clocks, the fixed extrinsics are composed with the time-dependent poses. Implicitly replacing $t_L$ with $t_C$ removes the movement to be compensated and creates a structured error, especially in rotation or at great distance. The deskew requires the time of each point, an interpolated pose and an announced reference time. If objects move independently of the vehicle, the ego movement alone is not enough to make them static.

### CV-CAPTEURS-004

**Situation**: Why can a radar Doppler measurement not directly replace a 3D Cartesian velocity?

**Elemental Observability**: for $H=\hat r^T$, the scalar measurement $z=Hv_{rel}+\epsilon$ constrains only one direction of a vector with three components. Its zero space has two dimensions: adding an orthogonal velocity to $\hat r$ leaves $z$ unchanged. A Cartesian velocity becomes conceivable with several independent directions and a model linking their observations to the same movement; three quasi-parallel measurements can remain very poorly conditioned. A rotation of coordinate frame gives $v'=Rv$ and $P'=RPR^T$ for a covariance $P$ and an exact rotation $R$. It re-expresses the available information without creating the two missing components; the uncertainty of the calibration may need to be added separately.

**Passages consulted for these developments**: [Basler, Electronic Shutter Types](https://docs.baslerweb.com/electronic-shutter-types), Global and Rolling Shutter; [Zhang and Singh, LOAM](https://www.roboticsproceedings.org/rss10/p07.pdf), §§II and V, acquisition and distortion of movement; [TI TIDUF01](https://www.ti.com/lit/ug/tiduf01/tiduf01.pdf), §2.4.9, radial velocity.

## Sources and flashcards

- [Zhang and Singh 2014, LOAM, §§II and V, motion distortion correction](https://www.roboticsproceedings.org/rss10/p07.pdf).
- [Texas Instruments, TIDUF01 (2021), §2.4.9](https://www.ti.com/lit/ug/tiduf01/tiduf01.pdf).

The offset calculation is kinematic and the camera – LiDAR case is built by the project; Forster supports inertial preintegration, not Doppler measurement.

- [Basler, electronic shutter types](https://docs.baslerweb.com/electronic-shutter-types).
- [Forster, IMU preintegration §§IV – VI](https://dellaert.github.io/files/Forster16tro.pdf).
- [Related flashcards](../22-capteurs-horodatage.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
