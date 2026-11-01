# Review –  Biometric recognition, ArcFace and PAD –  2026-10-30

## Overview

2 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BIOMETRIE-001 | Deduction/Assumption Cases; Documentary Context Below | What Margin Learns: Specifying the Existing Question | Finished core preserved; 186 → 293 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-BIOMETRIE-002 | Deduction/cases under assumptions; documentary context below; verified synthetic calculation | Amount of evidence: specifies the existing question | Finished core preserved; 186 → 299 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-BIOMETRIE](../../../vault/70-reconnaissance-representations/references/75-embeddings-biometrie.md); [flashcards](../../../vault/70-reconnaissance-representations/75-embeddings-biometrie.md). reference note modified before the flashcards.

- **CV-BIOMETRIE-001 –  What Margin Learns**: In ArcFace, class weights and normalized features give logits proportional to $\cos\theta_j$; for the target class during learning, an angular margin uses $\cos(\theta_y+m)$. This constraint pushes the separation of identities in the learned space. It does not provide a label on the materiality of a photographic presentation or on screen. At the inference, the score between two embeddings and the decision PAD therefore remain different outputs. If combined, evaluate their dependence and acquisition failures on common trials: naively multiplying two scores does not give a validated system probability.

- **CV-BIOMETRIE-002 –  Amount of evidence**: Under a simplified model of $n$ independent non-matte comparisons with probability of false correspondence $p$, observing zero error has probability $(1-p)^n$. The unilateral upper limit of 95% is then $1-0,05^{1/n}$, approximately $3/n$ for large $n$. Zero error on 1 000 comparisons thus remains compatible with a rate of around 0,003, and does not demonstrate a target of $10^{-6}$. Comparisons sharing the same identities are not necessarily independent; the uncertainty must respect the protocol. This constructed analysis explains why an excellent ERA and a small test do not characterize the distribution tails at the target threshold.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Deng et al., ArcFace](https://arxiv.org/html/1801.07698v4) –  §III-A, angular margin; binomial bound and system reasoning constructed. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
