"""Recompute the constructed examples of CV-PIPELINE (reference 141-contrats-profiling-video).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/141-contrats-profiling-video.py
Inputs: ITU-R BT.601-7 sec. 2.5 and BT.709-6 items 3.2-3.4 (coefficients, 8-bit quantization);
OpenCV 4.13.0 modules/imgproc/doc/colors.markdown L74-L76 (YUV 4:2:0 -> RGB formula) and
resize.cpp L1133 / L4101 (nearest and bilinear source-index mapping); GStreamer queue defaults
(200 buffers, 10485760 bytes, 1 s); Yates and Kaul, arXiv 1608.08622v2, eq. (8) (M/M/1 FCFS
average age); Dean and Barroso 2013 (fan-out to 100 servers). All scenarios are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def int_itu(x):
    """ITU INT(): fractions of 0.5 and above round up."""
    return math.floor(x + 0.5)


checks = 0

# --- Example A: queue growth, leaky queues and Little's law ---------------------
lam, mu = 240.0, 200.0  # arrivals and service in frames/s
backlog_10s = (lam - mu) * 10
# Check 1: with no drop, the backlog grows by 40 frames/s: 400 frames after 10 s,
# i.e. 2 s of waiting for a frame that arrives then (backlog / service rate).
assert backlog_10s == 400 and close(backlog_10s / mu, 2.0)
checks += 1


def simulate_leaky(lam, mu, cap, policy, horizon=60.0, warmup=10.0):
    """Deterministic arrivals every 1/lam, deterministic service 1/mu, one server.

    The queue holds at most `cap` waiting frames (the frame in service is not counted).
    policy 'downstream' drops the oldest waiting frame when full (GStreamer leaky=downstream);
    policy 'upstream' drops the arriving frame (leaky=upstream).
    Returns (mean wait of frames served after warm-up, drop fraction after warm-up).
    """
    queue = []           # arrival times of waiting frames
    server_free = 0.0
    waits, arrivals, drops = [], 0, 0
    n = int(horizon * lam)
    for i in range(n):
        t = i / lam
        # serve every frame that can start before this arrival
        while queue and max(server_free, queue[0]) <= t:
            start = max(server_free, queue[0])
            a = queue.pop(0)
            if a >= warmup:
                waits.append(start - a)
            server_free = start + 1.0 / mu
        counted = t >= warmup
        arrivals += counted
        if len(queue) < cap:
            queue.append(t)
        elif policy == "downstream":
            queue.pop(0)
            queue.append(t)
            drops += counted
        else:
            drops += counted
    return sum(waits) / len(waits), drops / arrivals


w_down, d_down = simulate_leaky(lam, mu, 10, "downstream")
w_up, d_up = simulate_leaky(lam, mu, 10, "upstream")
# Check 2: at saturation both leaky policies drop 1 - mu/lam = 1/6 of the arrivals.
assert close(d_down, 1 / 6, 2e-3) and close(d_up, 1 / 6, 2e-3)
checks += 1
# Check 3: dropping the oldest frame bounds the wait near the fluid value C/lam = 41.7 ms
# (simulated 39.4 ms), dropping the newest near C/mu = 50 ms (simulated 47.7 ms); both are
# bounded, unlike the 2 s of the no-drop case, and dropping the oldest gives the fresher output.
assert close(w_down, 0.0394, 5e-4) and close(w_up, 0.0477, 5e-4) and w_down < w_up
assert close(w_down, 10 / lam, 3e-3) and close(w_up, 10 / mu, 3e-3)
checks += 1
# Check 4: Little's law used as a cross-check: 48 frames in flight on average at
# 240 frames/s means a mean time in system of 0.2 s.
assert close(48 / 240, 0.2)
checks += 1

# --- Example B: age of information ---------------------------------------------
L, X = 0.050, 30.0  # constant latency (s) and periodic output rate (outputs/s)
# Check 5: the age sawtooth goes from L to L + 1/X: mean 66.7 ms, peak 83.3 ms.
assert close(L + 1 / (2 * X), 0.06667, 1e-4) and close(L + 1 / X, 0.08333, 1e-4)
# ... and halving the output rate to 15/s raises the peak age to 116.7 ms at the same latency.
assert close(L + 1 / 15, 0.11667, 1e-4)
# A detection 100 ms old on a conveyor moving at 0.5 m/s is 50 mm behind the part.
assert close(0.5 * 0.100, 0.050)
checks += 1


def aoi_fcfs(rho):
    """Average age times mu for an M/M/1 FCFS queue, Yates and Kaul eq. (8)."""
    return 1 + 1 / rho + rho ** 2 / (1 - rho)


best = min((aoi_fcfs(r / 10000), r / 10000) for r in range(100, 9990))
# Check 6: eq. (8) is minimized near rho = 0.53 (paper: rho* ~ 0.53), at about 3.48 service times.
assert close(best[1], 0.53, 0.01) and close(best[0], 3.48, 0.01)
checks += 1
# Check 7: at rho = 0.9 the average age is about 10.2 service times, three times the optimum.
assert close(aoi_fcfs(0.9), 10.211, 1e-3)
checks += 1

# --- Example C: percentiles are not additive ----------------------------------


def quantile(dist, p):
    """Smallest x with P(X <= x) >= p for a discrete distribution {value: prob}."""
    acc = 0.0
    for v in sorted(dist):
        acc += dist[v]
        if acc >= p - 1e-12:
            return v
    raise ValueError


def convolve(d1, d2):
    out = {}
    for a, pa in d1.items():
        for b, pb in d2.items():
            out[a + b] = out.get(a + b, 0.0) + pa * pb
    return out


stage_a = {10: 0.98, 40: 0.02}
sum_a = convolve(stage_a, stage_a)
# Check 8: two independent stages with 2% spikes: p99 per stage 40 ms, sum of p99s 80 ms,
# but p99 of the sum is 50 ms (summing overestimates).
assert quantile(stage_a, 0.99) == 40 and quantile(sum_a, 0.99) == 50
checks += 1
stage_b = {10: 0.995, 100: 0.005}
sum_b = convolve(convolve(stage_b, stage_b), stage_b)
# Check 9: three independent stages with 0.5% spikes: p99 per stage 10 ms, sum 30 ms,
# but P(sum <= 30) = 0.995^3 = 0.985 < 0.99, so p99 of the sum is 120 ms (summing underestimates).
assert quantile(stage_b, 0.99) == 10 and close(sum_b[30], 0.985075, 1e-6)
assert quantile(sum_b, 0.99) == 120
checks += 1
comonotonic = {30: 0.995, 300: 0.005}  # the three stages spike together
# Check 10: when stages are slow together (comonotonic), quantiles add: 10 + 10 + 10 = 30.
assert quantile(comonotonic, 0.99) == 30
checks += 1
# Check 11: fan-in. With a 1% chance of being late per input, a decision waiting for 8 inputs
# is late 7.7% of the time; for 100 inputs 63% (Dean and Barroso's example).
assert close(1 - 0.99 ** 8, 0.0773, 1e-4) and close(1 - 0.99 ** 100, 0.634, 1e-3)
checks += 1
# Check 12: one minute at 30 frames/s gives 1,800 latencies, only 18 of them above the p99.
assert 30 * 60 == 1800 and 1800 // 100 == 18
checks += 1

# --- Example D: throughput, overlap and batching ------------------------------
stages_ms = [4, 3, 10, 2]  # decode, preprocess, inference, postprocess (one worker each)
# Check 13: run serially, one frame takes 19 ms (52.6 frames/s); pipelined, the 10 ms stage
# bounds throughput at 100 frames/s while one frame still needs at least 19 ms.
assert sum(stages_ms) == 19 and close(1000 / sum(stages_ms), 52.63, 0.01)
assert close(1000 / max(stages_ms), 100.0)
checks += 1
# Check 14: forming a batch of 8 from a steady 240 frames/s makes the first frame wait 29.2 ms.
assert close((8 - 1) / 240, 0.02917, 1e-4)
checks += 1

# --- Example E: data volumes and queue limits ---------------------------------
W, H = 1920, 1080
nv12 = W * H * 3 // 2
bgr = W * H * 3
fp32 = 3 * 640 * 640 * 4
# Check 15: bytes per frame and per second at 240 frames/s.
assert nv12 == 3_110_400 and nv12 * 240 == 746_496_000
assert bgr == 6_220_800 and bgr * 240 == 1_492_992_000
assert fp32 == 4_915_200 and fp32 * 240 == 1_179_648_000
checks += 1
# Check 16: GStreamer queue defaults expressed in 1080p frames at 30 frames/s:
# 10 MiB holds 3.37 NV12 frames, 1 s holds 30 frames, 200 buffers hold 6.7 s.
assert close(10485760 / nv12, 3.371, 1e-3) and close(200 / 30, 6.667, 1e-3)
checks += 1

# --- Example F: colour matrix and range mismatch --------------------------------


def encode_709(r, g, b):
    """BT.709-6 items 3.2-3.4: non-linear R'G'B' in [0, 1] -> 8-bit limited-range Y'CbCr."""
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    cb = (b - y) / 1.8556
    cr = (r - y) / 1.5748
    return int_itu(219 * y + 16), int_itu(224 * cb + 128), int_itu(224 * cr + 128)


def clip8(x):
    return max(0, min(255, int_itu(x)))


def decode_opencv_601(y, u, v):
    """OpenCV 4.13.0 colors.markdown L74-L76 (BT.601, limited range)."""
    yy = 1.164 * (y - 16)
    return (clip8(yy + 1.596 * (v - 128)),
            clip8(yy - 0.813 * (v - 128) - 0.391 * (u - 128)),
            clip8(yy + 2.018 * (u - 128)))


# Check 17a: the colour-difference divisors are 2(1 - K): 1.772 and 1.402 for BT.601
# (K_B = 0.114, K_R = 0.299), 1.8556 and 1.5748 for BT.709 (K_B = 0.0722, K_R = 0.2126).
assert close(2 * (1 - 0.114), 1.772, 1e-9) and close(2 * (1 - 0.299), 1.402, 1e-9)
assert close(2 * (1 - 0.0722), 1.8556, 1e-9) and close(2 * (1 - 0.2126), 1.5748, 1e-9)
# Check 17: OpenCV's constants are BT.601 rescaled for limited range: 1.164 = 255/219,
# 1.596 = 1.402 * 255/224, 2.018 = 1.772 * 255/224 (to 3 decimals).
assert close(255 / 219, 1.164) and close(1.402 * 255 / 224, 1.596) and close(1.772 * 255 / 224, 2.017, 1e-3)
checks += 1
red = encode_709(1, 0, 0)
# Check 18: BT.709 red is coded (63, 102, 240); decoded with the BT.601 formula it becomes (233, 0, 2).
assert red == (63, 102, 240) and decode_opencv_601(*red) == (233, 0, 2)
checks += 1
green = encode_709(0.2, 0.8, 0.2)
# Check 19: a saturated green (51, 204, 51) comes back as (63, 231, 56): +27 on G.
assert decode_opencv_601(*green) == (63, 231, 56)
checks += 1
grey = encode_709(0.5, 0.5, 0.5)
# Check 20: grey has Cb = Cr = 128, so any matrix returns R = G = B: a grey chart cannot detect
# a matrix mismatch.
assert grey[1:] == (128, 128) and len(set(decode_opencv_601(*grey))) == 1
checks += 1
# Check 21: reading limited-range data as full range maps black to 16 and white to 235,
# compressing contrast to 219/255 = 0.859.
assert close(219 / 255, 0.859)
checks += 1

# --- Example G: letterbox and resize conventions --------------------------------
src_w, src_h, dst = 1920, 1080, 640
r = min(dst / src_w, dst / src_h)
new_w, new_h = round(src_w * r), round(src_h * r)
pad_x, pad_y = (dst - new_w) / 2, (dst - new_h) / 2
# Check 22: 1920x1080 -> 640x640 letterbox: r = 1/3, content 640x360, 140 px bands top and bottom.
assert close(r, 1 / 3) and (new_w, new_h) == (640, 360) and (pad_x, pad_y) == (0, 140)
# ... so 1 - 360/640 = 43.75% of the model input is padding.
assert close(1 - new_h / dst, 0.4375)
checks += 1
box = (100, 200, 300, 400)  # x1, y1, x2, y2 in model-input pixels (continuous edge coordinates)
inv = ((box[0] - pad_x) / r, (box[1] - pad_y) / r, (box[2] - pad_x) / r, (box[3] - pad_y) / r)
# Check 23: the inverse maps the box to (300, 180, 900, 780) in source pixels;
# forgetting the padding shifts y by 140 / r = 420 px.
assert all(close(a, b) for a, b in zip(inv, (300, 180, 900, 780))) and close(pad_y / r, 420)
checks += 1
scale = 3.0  # OpenCV scale_x = src / dst for a 3x downscale
dx = 5
linear_src = (dx + 0.5) * scale - 0.5   # resize.cpp L4101
nearest_src = math.floor(dx * scale)    # resize.cpp L1133
# Check 24: bilinear samples source index 3*dx + 1, nearest samples 3*dx: a mask resized with
# INTER_NEAREST is offset by (scale - 1) / 2 = 1 source pixel from the image.
assert close(linear_src - nearest_src, (scale - 1) / 2) and close(linear_src - nearest_src, 1.0)
checks += 1

print(f"CV-PIPELINE checks: {checks} groups passed")
