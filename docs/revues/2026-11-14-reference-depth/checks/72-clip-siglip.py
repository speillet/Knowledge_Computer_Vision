"""Recompute the constructed examples of CV-CLIP (reference 72-clip-siglip).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/72-clip-siglip.py
Inputs: CLIP's learned temperature, initialized at 0.07 and clipped so logits are scaled by at most
100 (arXiv 2103.00020, Sec. 2.5), SigLIP's initialization t = exp(log 10) = 10 and b = -10
(arXiv 2303.15343v4, Sec. 3.2, Algorithm 1), OpenCLIP v3.3.0 ViT-B-32 embed_dim = 512.
Cosine values, vocabularies and index sizes are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def softmax(logits):
    m = max(logits)
    e = [math.exp(x - m) for x in logits]
    return [x / sum(e) for x in e]


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# --- Example A: a small cosine gap becomes a confident softmax -----------------
cos_a, cos_b = 0.30, 0.27
p_scale100 = softmax([100 * cos_a, 100 * cos_b])[0]
p_scale10 = softmax([10 * cos_a, 10 * cos_b])[0]
# Check 1: a 0.03 cosine gap gives 0.953 at logit scale 100 but 0.574 at scale 10.
assert close(p_scale100, 0.9526, 1e-4) and close(p_scale10, 0.5744, 1e-4)
# Check 2: CLIP's initial temperature 0.07 corresponds to a logit scale of ~14.3.
assert close(1 / 0.07, 14.286, 1e-3)

# --- Example B: the candidate set changes the normalized score ------------------
# Check 3: a logit gap of log 19 (~2.944) gives 0.95 whatever the absolute logits.
assert close(math.log(19), 2.944, 1e-3)
for offset in (-5.0, 0.0, 12.0):
    assert close(softmax([offset + math.log(19), offset])[0], 0.95, 1e-12)
# Check 4: adding a third candidate tied with the first lowers its score to 19/39 ~ 0.487.
assert close(softmax([math.log(19), 0.0, math.log(19)])[0], 19 / 39, 1e-12) and close(19 / 39, 0.4872, 1e-4)

# --- Example C: SigLIP scores at initialization --------------------------------
t, b = math.exp(math.log(10)), -10.0
scores = {c: sigmoid(t * c + b) for c in (1.0, 0.5, 0.0)}
# Check 5: at initialization a perfectly aligned pair scores 0.5, cosine 0.5 scores 0.0067,
# an orthogonal pair 4.5e-5: the bias sets the prior, not the presence probability at deployment.
assert close(scores[1.0], 0.5, 1e-12) and close(scores[0.5], 0.00669, 1e-5) and close(scores[0.0], 4.54e-5, 1e-6)
batch = 32_768
# Check 6: with a 32k batch each image has 1 positive and 32,767 negatives (positive rate 3.05e-5),
# the same order of magnitude as sigmoid(-10).
assert close(1 / batch, 3.05e-5, 1e-7) and 0.1 < (1 / batch) / scores[0.0] < 10

# --- Example D: prompt ensembling in embedding space ---------------------------
theta = math.radians(60)
u = (1.0, 0.0)
v = (math.cos(theta), math.sin(theta))
mean = ((u[0] + v[0]) / 2, (u[1] + v[1]) / 2)
# Check 7: the mean of two unit text embeddings 60 degrees apart has norm cos(30 deg) ~ 0.866,
# so it must be renormalized before cosine scoring.
assert close(math.hypot(*mean), math.cos(theta / 2), 1e-12) and close(math.hypot(*mean), 0.8660, 1e-4)
K, P, d = 1000, 80, 512
# Check 8: 1,000 classes x 80 prompts cached as 1,000 averaged vectors cost 512,000 multiply-adds per image,
# the same as a single prompt, instead of 40,960,000 without averaging.
assert K * d == 512_000 and K * P * d == 40_960_000

# --- Example E: retrieval index size ---------------------------------------------
n_images = 1_000_000
# Check 9: one million 512-d embeddings take 1.02 GB in float16 and 2.05 GB in float32.
assert n_images * d * 2 == 1_024_000_000 and n_images * d * 4 == 2_048_000_000

print("72-clip-siglip: 9 checks passed "
      f"(softmax 0.03 gap: {p_scale100:.3f} at scale 100, {p_scale10:.3f} at 10; third candidate 19/39; "
      f"SigLIP init scores {scores[1.0]:.2f}/{scores[0.5]:.4f}/{scores[0.0]:.1e})")
