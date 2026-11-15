"""Recompute the constructed example of CV-FLANN-005 (reference 48-flann).

Stdlib only. Run with: python3 -I docs/revues/2026-11-15-accepted-proposals/checks/48-flann.py
Conventions checked against OpenCV 4.13.0 (modules/features2d/src/matchers.cpp):
- knnMatch(query, train, k) clones an empty matcher, adds `train` and matches through it
  (L589-L598; FlannBasedMatcher::clone L1389-L1405), so every call trains a new index.
- knnMatch(query, k) calls train() (L659); FlannBasedMatcher::train() rebuilds the whole
  flann::Index only when there is no index or descriptors were added (L1160-L1176).
The build and search times are project assumptions, not measurements.
"""

checks = 0
build = 1.0       # s, assumed index build for the 200,000-descriptor map
search = 0.020    # s, assumed search of one frame (1,000 queries) with the default budget
fps = 10
frames = 60 * fps


def one_shot(n_frames, search_s=search):
    """Per-call clone, add and train: the build is paid on every frame."""
    return n_frames * (build + search_s)


def reused(n_frames, rebuilds=1):
    """add once, train, then knnMatch(query, k): one build per rebuild."""
    return rebuilds * build + n_frames * search


# Check 1: per-call latency of the one-shot overload is 1.02 s; halving the search
# budget (search time halved) only brings it to 1.01 s, a 1% change.
assert abs(one_shot(1) - 1.02) < 1e-12 and abs(one_shot(1, search / 2) - 1.01) < 1e-12
assert abs((one_shot(1) - one_shot(1, search / 2)) / one_shot(1) - 0.0098) < 1e-4; checks += 1

# Check 2: one minute of video (600 frames) costs 612 s with the one-shot call,
# 10.2 times real time, against 13 s with a reused index: a factor of about 47.
assert frames == 600 and abs(one_shot(frames) - 612.0) < 1e-9
assert abs(one_shot(frames) / 60 - 10.2) < 1e-9
assert abs(reused(frames) - 13.0) < 1e-9 and abs(one_shot(frames) / reused(frames) - 47.08) < 5e-3
checks += 1

# Check 3: appending 5,000 descriptors once a minute triggers one full rebuild per
# minute: 13 s of work per minute, and a 1.02 s spike on the frame that pays it.
assert abs(reused(frames, rebuilds=1) - 13.0) < 1e-9 and abs(build + search - 1.02) < 1e-12
checks += 1

# Check 4: appending new descriptors on every frame rebuilds on every frame and
# brings back the one-shot cost.
assert abs(reused(frames, rebuilds=frames) - one_shot(frames)) < 1e-9; checks += 1

print(f"48-flann (CV-FLANN-005): {checks} checks passed")
