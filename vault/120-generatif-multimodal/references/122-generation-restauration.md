---
id: CV-DIFFUSION
type: comparaison
domaine: d12
poles: [A, D, E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 7
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d12]
---
# VAEs, GANs and diffusion for generation and restoration

## Problem, data and assumptions

Generate or restore an image according to a goal distinct from the physical measurement. Inputs: noise/conditioning or degraded image; output: plausible image under model. An added texture can be visually credible and factually false.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

VAE learns a probabilistic latent space; GAN opposes generation and discrimination; diffusion learns a de-noise in a noisy process. Latent diffusion moves this process into the space of an autoencoder; compression becomes part of the compromise.

## Mathematics, conventions and units

A sample of the marginal forward at the $t$ level can be written as $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$, $\epsilon\sim\mathcal N(0,I)$, with $\bar\alpha_t=\prod_{s=1}^{t}(1-\beta_s)$ and $\beta_s$ the noise variance of each transition. This is not an elementary transition since $x_{t-1}$; $t$ indexes the noise level. The training and the sampling procedure are distinct. The units depend on the normalized representation, not an implicit physical radiometric scale.

## Parameters and properties

Data, conditioning, noise levels, sampler, steps, guidance and seed. Variants change; fewer steps do not have a universal effect on quality and fidelity. A conditioned exit does not guarantee the preservation of all observed details.

## Cost and implementation

Self-encoder, resolutions and generation iterations dominate cost/memory. No generator executed, no synthetic image presented as actual measurement.

## Evaluation and controlled variation

Baseline: classic restoration adapted to noise, then learned model with references not degraded if available. Vary degradation level and measure defect fidelity, not just overall perceptual quality.

## Failure modes and diagnosis

A defect disappears after super-resolution: check that the lens promotes plausibility rather than preservation. Keep raw image and proof related to the useful measure.

## Alternatives and applications

Generating for synthesis/assisted annotation according to validation; explicit measurement model for metrology. Synthetic data must be evaluated against actual distributions.

## Guided reasoning and proposed checks

These constructed cases develop conditional distribution and restoration fidelity. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-DIFFUSION-001

**Question of work**: Why are training and sampling different operations in a diffusion model?

**Reference Response**: Training learns a de-noise rule under a noise distribution; sampling uses this rule in a procedure to produce an output.

**Decomposition of the process**: During learning, we build noisy examples at selected levels and optimize a prediction target according to the formulation. In sampling, weights are used in a sequence of operations to transform a condition and noise into output. The data viewed and decisions made at these two moments differ.

**Example of check**: maintain weight and conditioning, then compare multiple steps and seeds on a defined set. Measure cost, diversity and loyalty to the condition rather than conclude from a single favorable image. The marginal forward at a noise level is not the entire reverse generation procedure. A likely exit may fill in unobserved details; it does not become a physical measurement because the training has converged. For a restoration task, the retention of critical information must therefore be evaluated separately.

### Case linked to CV-DIFFUSION-003

**Question of work**: Super-resolution makes an image sharp but changes a crack. Why is this a defect in an inspection system?

**Reference Response** Visual plausibility is not fidelity to critical observation; the model can suppress or invent a structure.

**Why Can Clarity Deceive?**: Multiple detailed images can be compatible with low-resolution observation. The model uses its learned regularities to choose a plausible reconstruction. This decision can create a credible texture without matching the actual crack present.

**Proposed Validation**: preserve the crude and, if possible, a reference acquired with an adapted resolution, then measure preservation, width and location of defects. Compare to a simple restoration with explicit assumptions and examine errors on rare cases. Do not replace the proof of acquisition with a more convincing generated image. An improvement in perceptual score or overall reconstruction may mask the modification of a small but critical structure. The choice depends on the objective: producing an illustration and measuring a crack do not require the same fidelity. No generator is executed in this case, which is used to reason on the output contract.

**Documentary reference for this pass**: [Latent Diffusion Models](https://arxiv.org/html/2112.10752v2), §3, latent space and conditioning. The other developments are in the [flashcards](../122-generation-restauration.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-DIFFUSION-001

**Situation**: Why are training and sampling different operations in a diffusion model?

**Noise target**: In the current DDPM parameterization, draw a level $t$ and a noise $\epsilon$, build $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$, then minimize an error in predicting this noise. With this convention, an estimate of the clean image can be written $\hat x_0=(x_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(x_t,t))/\sqrt{\bar\alpha_t}$. This relationship alone is not a complete sampler: transitions, variances, levels traveled and conditioning remain to be defined. Other settings predict another target. Naming the one used avoids applying an output interpretation formula to the wrong tensor.

### CV-DIFFUSION-002

**Situation**: What tradeoff is introduced by performing diffusion in an autoencoder's latent space?

**Spatial size check**: If the encoder reduces each image dimension by a factor of $f$, the latent grid has about $HW/f^2$ positions, with a different number of channels. This reduction alone does not predict time savings, as decoder, attention and iterations have their own costs. Note $\tilde x=D(E(x))$ and compare $x$ to $\tilde x$ isolates the reconstruction of the autoencoder before diffusion. Specially evaluate structures smaller than the effective compression support. A good average reconstruction can preserve the large shapes while modifying a rare detail that the product precisely seeks to measure.

### CV-DIFFUSION-003

**Situation**: Super-resolution makes an image sharp but changes a crack. Why is this a defect in an inspection system?

**Non-unique inverse problem**: If the acquisition is $y=Hx+n$, multiple high-resolution $x$ images can produce almost the same $y$ when $H$ loses high frequencies. For a detail $\delta$ such as $H\delta\simeq0$, $x$ and $x+\delta$ are difficult to distinguish from the measurement. The generative model then chooses with its learned preferences, without proof that the crack added or removed is real. Consistency $H\hat x\simeq y$ is useful but insufficient to validate the details of the poorly observed kernel. This derivation explains why keeping the raw measurement and a physical reference remains essential for inspection.

**Passages consulted for these developments**: [Ho et al., DDPM](https://arxiv.org/html/2006.11239v2), Algorithm 1 – 2 and §3.2, noise prediction; algebraic reversal of the project; [Rombach et al., Latent Diffusion](https://arxiv.org/html/2112.10752v2), §3.1, compression and reconstruction; spatial balance and inverse problem deduced.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-DIFFUSION-001 — Fewer sampling steps change an inference procedure

Training may sample individual noise levels to learn a denoiser, while generation repeatedly calls it according to a solver and schedule. Reducing sampling steps changes numerical approximation, latency and possibly output quality without necessarily changing the learned weights. A proposed comparison fixes checkpoint, conditioning, resolution and random seeds while varying the sampler. A training loss at sampled noise levels is not a direct measurement of final generation fidelity.

### CV-DIFFUSION-002 — The autoencoder gives a separate distortion baseline

Before attributing a lost scratch to latent diffusion, inspect $D(E(x))$ for the same input under the autoencoder alone. If the critical structure is already absent, the representation introduces an information bottleneck before iterative generation. A proposed evaluation measures that reconstruction on defect size and contrast, then adds the denoising stage. More sampling iterations cannot be assumed to recover a detail the representation did not preserve.

### CV-DIFFUSION-003 — Measurement consistency does not imply unique reconstruction

For an acquisition operator with a nontrivial nullspace, $H(x+\delta)=Hx$ whenever $H\delta=0$. A reconstructed crack difference in that nullspace can satisfy the same low-resolution observation. Validate task-critical geometry against independent high-resolution measurements and keep original observations available. A visually sharp result or small re-degradation error alone does not establish which of several measurement-consistent structures was physically present.

Consulted foundations: [DDPM](https://arxiv.org/html/2006.11239v2): Algorithms 1–2 and §3 noise-prediction training versus reverse sampling; [Latent Diffusion](https://arxiv.org/html/2112.10752v2): §3.1 perceptual compression and §3.2 latent generation.

## Sources and flashcards

- [VAE, summary and §2](https://arxiv.org/abs/1312.6114): latent model and variational inference.
- [GAN, summary](https://arxiv.org/abs/1406.2661): Adversarial generator/discriminator learning.

- [DDPM, process and objective](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html).
- [Latent Diffusion Models](https://arxiv.org/abs/2112.10752).
- [Related flashcards](../122-generation-restauration.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
