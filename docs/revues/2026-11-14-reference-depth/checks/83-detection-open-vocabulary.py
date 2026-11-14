"""Recompute the constructed examples of CV-OPENVOC (reference 83-detection-open-vocabulary).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/83-detection-open-vocabulary.py
Rules come from GLIP (arXiv 2112.03857v2, Sec. 3.1: phrase probability = mean of token
probabilities), the official Grounding DINO code at commit 856dde2 (util/inference.py:
box kept if max token probability > box_threshold, label = tokens above text_threshold,
phrases2classes substring mapping), transformers v5.23.0 OWL-ViT post-processing (argmax over
queries, then sigmoid), OWL-ViT (arXiv 2205.06230v2, Sec. 3.1: tokens = max objects) and LVIS
(arXiv 1908.03195v2, Sec. 2.2-2.3: federated evaluation). All numbers are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


# --- Example A: token scores, phrase scores and label mapping ------------------
# One predicted box; tokens of the prompt "traffic light. car." after the tokenizer.
tokens = ["traffic", "light", ".", "car", "."]
probs = [0.60, 0.20, 0.05, 0.10, 0.02]          # sigmoid token probabilities for this box
glip_phrase = (probs[0] + probs[1]) / 2          # GLIP: mean over the phrase's tokens
gd_box_score = max(probs)                        # Grounding DINO: max over all tokens
# Check 1: GLIP scores the phrase "traffic light" 0.40; Grounding DINO scores the box 0.60.
assert close(glip_phrase, 0.40) and close(gd_box_score, 0.60)
checks += 1
box_threshold, text_threshold = 0.35, 0.25       # official demo defaults
kept = gd_box_score > box_threshold
label_tokens = [t for t, p in zip(tokens, probs) if p > text_threshold]
phrase = " ".join(label_tokens).replace(".", "").strip()
# Check 2: the box is kept, but only "traffic" passes text_threshold, so the label is a partial phrase.
assert kept and phrase == "traffic"
checks += 1


def phrases2classes(phrases, classes):
    """Official helper: first class name that is a substring of the phrase, else None."""
    out = []
    for ph in phrases:
        for c in classes:
            if c in ph:
                out.append(classes.index(c))
                break
        else:
            out.append(None)
    return out


# Check 3: the partial phrase "traffic" maps to no class, because "traffic light" is not a substring of it.
assert phrases2classes(["traffic"], ["traffic light", "car"]) == [None]
checks += 1
# Check 4: a box labelled "cart" is mapped to "car", which precedes it in the class list.
assert phrases2classes(["cart"], ["car", "cart"]) == [0]
checks += 1
# Check 5: with "cart" listed first, the same helper maps "cart" correctly: the mapping depends on order.
assert phrases2classes(["cart"], ["cart", "car"]) == [0]
assert phrases2classes(["car"], ["cart", "car"]) == [1]
checks += 1

# --- Example B: argmax labelling when a query is added (OWL-ViT post-processing) ------
logits_v0 = {"bolt": 2.0, "nut": -1.0}
logits_v1 = dict(logits_v0, **{"anchor bolt": 2.3})


def owl_label(logits):
    name = max(logits, key=logits.get)
    return name, sigmoid(logits[name])


lab0, s0 = owl_label(logits_v0)
lab1, s1 = owl_label(logits_v1)
# Check 6: with V0 the box is "bolt" at 0.881; adding one query relabels it "anchor bolt" at 0.909,
# although the per-query sigmoid of "bolt" is unchanged (independent sigmoids, argmax coupling).
assert lab0 == "bolt" and close(s0, 0.8808, 1e-4)
assert lab1 == "anchor bolt" and close(s1, 0.9089, 1e-4)
assert close(sigmoid(logits_v1["bolt"]), s0)
checks += 1

# --- Example C: LVIS federated counting for one category ----------------------
# Each detection of category "canoe": (image status, matched to a GT?)
#   P_exh: image in P_c, exhaustively annotated; P_non: in P_c with e_i^c false;
#   N: image in N_c (canoe known absent); U: image in neither set.
dets = [("P_exh", True), ("P_exh", False), ("P_non", True), ("P_non", False),
        ("N", False), ("U", False), ("U", False)]
tp = fp = ignored = 0
for status, matched in dets:
    if status == "U":
        ignored += 1                  # not evaluated (Sec. 2.2)
    elif matched:
        tp += 1
    elif status == "P_non":
        ignored += 1                  # no FP counted on non-exhaustive images (Sec. 2.3)
    else:
        fp += 1                       # P_exh unmatched or any detection on a negative image
# Check 7: of 7 detections, 2 are TPs, 2 FPs (one on a positive image, one on a negative image)
# and 3 are not counted.
assert (tp, fp, ignored) == (2, 2, 3)
checks += 1

# --- Example D: capacity and text-length limits ------------------------------------
# Check 8: OWL-ViT B/32 at 768 px has (768/32)^2 = 576 image tokens, hence at most 576 boxes;
# B/16 at 768 px gives 2304 and L/14 at 840 px 3600.
assert (768 // 32) ** 2 == 576 and (768 // 16) ** 2 == 2304 and (840 // 14) ** 2 == 3600
checks += 1
names, max_tokens, special = 1203, 256, 2
min_tokens = names * 2                         # at least one token per name plus one "." separator
chunks = math.ceil(min_tokens / (max_tokens - special))
# Check 9: the 1203 LVIS names need at least 2406 text tokens, so a 256-token caption must be
# split into at least 10 chunks, i.e. at least 10 forward passes of a fused model per image.
assert min_tokens == 2406 and chunks == 10
checks += 1

print(f"83-detection-open-vocabulary: {checks} checks passed")
