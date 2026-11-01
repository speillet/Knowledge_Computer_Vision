# Conventions and useful reminders

**Provenance**: agent. These reminders give local conventions; the canonical reference notes of estimation and geometry develop their mechanisms. The [Senior Course](Parcours-senior.md) commands the subjects and their prerequisites.

## Read a flashcard

Hide the back, produce a response, and then compare to the **expected answer**. An answer is satisfactory if it covers this kernel without **Error Blocker**. The further explanation explains more without imposing an integral recitation. Writing, exporting and personal mastery are followed separately.

## Images and coordinates

A grayscale image is marked $I[y,x]$, with height $H$ and width $W$. Geometric coordinates are $(x,y)$; indexing an array is usually `[y, x]`. The origin is at the top left and $y$ descends into the driver examples. A color image is not automatically RGB: the tables loaded by OpenCV are usually BGR.

The boxes are continuous, in pixels, in the form $(x_1,y_1,x_2,y_2)$, with $x_2>x_1$ and $y_2>y_1$. Their area is worth $(x_2-x_1)(y_2-y_1)$, without `+1`. A COCO `xywh` annotation instead provides $(x,y,w,h)$. A standardized box must be put back in the same coordinate frame before IoU. After resize/crop/padding, also transform the points, boxes and intrinsics concerned. A measurement in another resolution does not automatically keep the same threshold in pixels.

## Homogeneous points and projection

An image point $(x,y)$ can be represented by $\tilde x=[x,y,1]^T$. Two homogeneous vectors that differ only by a non-zero factor represent the same point. For $c\ne0$, $\pi([a,b,c]^T)=[a/c,b/c]^T$. The symbol $\sim$ means this equality to one factor; it does not mean an equality of Euclidean coordinates.

An ideal perspective projection is written $s\tilde x=K[R\mid t]\tilde X_w$, with $X_c=RX_w+t$. $R$ goes from the world to the camera, $t$ is expressed in the coordinate frame camera and in the unit chosen for the scene. $K$ turns normalized camera coordinates into pixels; distortion is an additional step. Reference: [Zhang, §2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf).

## Distance, correspondence and estimation

A detector locates points; a descriptor represents their vicinity; a matcher proposes pairs; a geometric check tests their consistency. A nearest neighbor is not necessarily the same physical structure. The distance must correspond to the representation: Euclidean for the classic SIFT, Hamming for ORB with two-point binary tests. See [SIFT](../40-features-matching/references/41-sift.md), [ORB](../40-features-matching/references/42-orb.md).

An estimator minimizes a chosen residual. A robust estimate tolerates a portion of incompatible observations; it does not repair a false physical model. See [RANSAC](../50-calibration-geometrie/references/51-ransac-homographie.md).

## Kalman and assignment

A linear Kalman filter represents the estimated state and its covariance. It predicts with a motion model, then corrects with a measurement and its noise. The gain reflects their relative uncertainty; it does not choose the identity of the measured object. Assignment is the separate problem that associates measures and tracks, with possible unassociated observations.

In the scalar case, $K=P^-/(P^-+R)$, $u^+=u^-+K(z-u^-)$ and $P^+=(1-K)P^-$. $u^-,z,u^+$ are here positions in pixels; $P^-,R,P^+$ are variances in square pixels; $K$ is without unit. These relationships assume a linear model and appropriate noise assumptions. They illustrate the correction, not the entire [SORT](../110-tracking-association/references/111-sort.md) tracker. Reference: [SORT, §3.2](https://arxiv.org/abs/1602.00763).

## Prerequisites and thematic links

A prerequisite is necessary to understand the main reasoning. A thematic link gives a useful connection without imposing a reading order. The [Senior Course](Parcours-senior.md) gives a complete order, controlled on the 60 reference notes, with passing criteria and three integrations. The concepts of IoU precede NMS and SORT; the basics of filtering precede association. This does not require mastering all the AP to understand Kalman or all the ESKF to start SORT. The numbers of the files rank the themes, without imposing this learning order.
