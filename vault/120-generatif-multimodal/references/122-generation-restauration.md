---
id: CV-DIFFUSION
type: comparaison
domaine: d12
poles: [A, D, E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 9
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d12]
---
# VAEs, GANs and diffusion for generation and restoration

This awareness-level comparison note covers three families of generative models and
their use for image restoration. Its central point for a vision engineer is the output
contract: a generative model returns a plausible sample, not a measurement, and a
restored image can look sharper while being less faithful to what the sensor observed.

## Problem and data contract

**Generation** draws an image from a learned distribution, possibly conditioned on a
class, a text or another image. **Restoration** estimates an image $x$ from a degraded
observation $y$, often modelled as $y=Hx+n$ with $H$ a blur, a downsampling or a mask
and $n$ noise; a generative restorer samples from, or approximates, the distribution
of $x$ given $y$.

**Data contract.** DDPM scales 8-bit images from $\{0,\dots,255\}$ linearly to
$[-1,1]$ [Ho et al., §3.3]. Latent diffusion encodes an RGB image
$x\in\mathbb R^{H\times W\times3}$ into $z=\mathcal E(x)\in\mathbb R^{h\times w\times c}$
with downsampling factor $f=H/h=W/w$ and decodes $\tilde x=\mathcal D(\mathcal E(x))$
[Rombach et al., §3.1]. Values are normalized intensities without a radiometric
unit; the inverse mapping, gamma and clipping must be stated before any measurement.
Outputs depend on the random seed and the sampler: the same input can give different
images.

**Pipeline role.** Synthetic data and augmentation, inpainting and display
enhancement, defect synthesis for training detectors, and denoising or super-resolution
for viewing. Metrology and acceptance decisions must keep the raw measurement as
evidence.

## Intuition

- **VAE**: an encoder maps an image to a distribution over a latent code and a decoder
  maps codes back; training maximizes a lower bound on the data likelihood
  [Kingma and Welling, §2.2–2.4].
- **GAN**: a generator maps noise to images and a discriminator tries to tell them
  from real ones; their minimax game has its global optimum when the generated and
  data distributions coincide [Goodfellow et al., §3–4.1].
- **Diffusion**: a fixed forward process adds Gaussian noise in many small steps; a
  network learns to predict the added noise, and generation starts from pure noise and
  denoises step by step [Ho et al., §2–3].
- **Latent diffusion**: a perceptual autoencoder first compresses the image, then
  diffusion runs on the smaller latent grid [Rombach et al., §3.1–3.2].

*Illustration (constructed example, recomputed by checks/122-generation-restauration.py).*
In Blau and Michaeli's Example 1 setting, $Y=X+N$ with $X\sim\mathcal N(0,1)$,
$N\sim\mathcal N(0,1)$ and a linear estimator $\hat X=aY$. The minimum-MSE estimator
($a=0.5$) has MSE 0.5 but a distribution that is too narrow (KL 0.153 from the true
one). Forcing the right distribution ($a=0.707$) raises the MSE to 0.586, about 17%
more. Looking right and being accurate are different objectives even in one dimension.

## Prerequisites and competencies

**Required prerequisites**: [vault conventions](../../01-Parcours/Pre-requis.md).
Useful: least squares and null spaces in
[CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md),
noise and sampling in
[CV-ACQUISITION](../../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md),
inspection metrics in
[CV-METRIQUES-APPLIQUEES](../../130-evaluation-fiabilite/references/134-metriques-applications.md).
**Target competencies**: explain the mechanism, compare under constraints, interpret a
measurement and diagnose a failure. The level is awareness; not all variants mentioned
are detailed.

## Assumptions, observability and degenerate cases

- **Training distribution.** The model reproduces the regularities of its training
  data; a rare defect absent from them is unlikely to be restored faithfully.
- **Degradation model.** Restoration needs a known $H$ or paired training data that
  match the real degradation; a mismatch produces confident artefacts.
- **Non-invertible degradation.** When $H$ removes high frequencies, details in its
  null space are not observable: in Example C below, $x$ and $x+\delta$ give the same
  measurement. Blau and Michaeli prove that, for a non-invertible degradation, no
  distortion measure is "stably distribution preserving" [Theorem 1]: low distortion
  does not generally imply natural-looking output [§4].
- **Autoencoder fidelity (latent diffusion).** Structures smaller than the latent cell,
  or not preserved by $\mathcal D(\mathcal E(x))$, cannot be recovered by the diffusion
  stage; the authors note that their $f=4$ autoencoder can become a bottleneck for
  tasks requiring fine-grained pixel accuracy [Rombach et al., §5].
- **Degenerate cases.** Very few sampling steps with a sampler designed for many,
  clipping of values outside $[-1,1]$, and an unconditional model used as a restorer.

## Procedure

```text
DDPM training (Ho et al., Algorithm 1)
  repeat: x0 ~ data; t ~ Uniform{1..T}; eps ~ N(0, I)
          gradient step on || eps - eps_theta( sqrt(abar_t) x0 + sqrt(1 - abar_t) eps, t ) ||^2

DDPM sampling (Algorithm 2)
  xT ~ N(0, I)
  for t = T..1: z ~ N(0, I) if t > 1 else 0
      x_{t-1} = ( x_t - (1 - alpha_t) / sqrt(1 - abar_t) * eps_theta(x_t, t) ) / sqrt(alpha_t) + sigma_t z

Restoration for inspection (project procedure)
  keep raw y; restore x_hat with a stated model, sampler, steps and seed
  check consistency H(x_hat) ~ y; measure defects on x_hat against an independent reference
```

Purpose. Training visits one random noise level per example; sampling chains $T$
network evaluations. The two share weights but not procedure, which is why DDIM can
reuse a DDPM-trained network with a different, shorter sampler [Song et al., §1,
§4.2]. Keeping $y$ and checking $H\hat x\approx y$ separates what was measured from
what was filled in, although consistency does not validate details in the null space.

## Mathematics, conventions and units

**VAE.** For data $x$, latent $z$, encoder $q_\phi(z\mid x)$ and decoder
$p_\theta(x\mid z)$, the variational lower bound is
$\mathcal L=-D_{KL}(q_\phi(z\mid x)\,\|\,p_\theta(z))+\mathbb E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]$,
optimized with the reparameterization trick [Kingma and Welling, eq. 3, §2.4].

**GAN.** $\min_G\max_D V(D,G)=\mathbb E_{x\sim p_{\text{data}}}[\log D(x)]+\mathbb E_{z\sim p_z}[\log(1-D(G(z)))]$
[Goodfellow et al., eq. 1]. For a fixed $G$ the optimal discriminator is
$D^*(x)=p_{\text{data}}(x)/(p_{\text{data}}(x)+p_g(x))$, and the criterion reaches its
global minimum $-\log4$ if and only if $p_g=p_{\text{data}}$ [Proposition 1, Theorem 1].
The authors warn that the generator must not be trained too much without updating the
discriminator, otherwise it can collapse many $z$ to the same $x$ [§6].

**DDPM.** With $\alpha_t=1-\beta_t$ and $\bar\alpha_t=\prod_{s\le t}\alpha_s$,
the forward marginal is [Ho et al., eq. 4]

$$q(x_t\mid x_0)=\mathcal N\big(x_t;\sqrt{\bar\alpha_t}\,x_0,\,(1-\bar\alpha_t)I\big),$$

so $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\,\epsilon$ with
$\epsilon\sim\mathcal N(0,I)$; $t$ indexes the noise level, not a single transition.
Training minimizes
$L_{\text{simple}}=\mathbb E_{t,x_0,\epsilon}\|\epsilon-\epsilon_\theta(x_t,t)\|^2$
[eq. 14], which down-weights small-$t$ terms relative to the variational bound
[§3.4]. The paper uses $T=1000$ and a linear schedule from $\beta_1=10^{-4}$ to
$\beta_T=0.02$ [§4]. Inverting eq. 4 gives the clean-image estimate
$\hat x_0=(x_t-\sqrt{1-\bar\alpha_t}\,\epsilon_\theta)/\sqrt{\bar\alpha_t}$.

*Worked example A (constructed, recomputed by the check script).* With that schedule,
$\bar\alpha_T\approx4.0\times10^{-5}$, so the signal weight at $t=T$ is about 0.0064;
the signal-to-noise ratio $\bar\alpha_t/(1-\bar\alpha_t)$ falls below 1 at $t=260$. At
$t=500$, $\bar\alpha_t=0.079$ and an error of 0.1 in the predicted noise becomes an
error of $0.1\sqrt{(1-\bar\alpha_t)/\bar\alpha_t}=0.34$ in $\hat x_0$: estimates of the
clean image from high noise levels are unreliable, which is why sampling refines them
over many steps.

**Latent diffusion.** The autoencoder is trained with a perceptual loss and a
patch-based adversarial objective to avoid the blur of pure $L_1$ or $L_2$ losses, and
regularized either by a slight KL penalty or by vector quantization [§3.1]. Diffusion
then runs on $z$ with $h\,w=HW/f^2$ positions; conditioning uses concatenation or
cross-attention [§3.3]. *Example D:* $f=8$ on a $512\times512$ image gives a
$64\times64$ latent, 64 times fewer positions, and a 6 px wide crack spans less than
one latent cell.

**Perception–distortion.** For a distortion $\Delta$ and a divergence $d$ between
distributions, $P(D)=\min_{p_{\hat X\mid Y}} d(p_X,p_{\hat X})$ subject to
$\mathbb E[\Delta(X,\hat X)]\le D$; if $d$ is convex in its second argument, $P(D)$ is
monotonically non-increasing and convex [Blau and Michaeli, Definition 3, Theorem 2]:
below some distortion, better perceptual quality can only be bought with more
distortion.

*Example C (constructed).* With $H$ averaging adjacent pairs of a 1-D profile
$x=(10,12,30,31,12,11)$, the alternating detail $\delta=(1,-1,1,-1,1,-1)$ satisfies
$H\delta=0$, so $x$ and $x+\delta$ give the same $y=(11,30.5,11.5)$. A generator chooses
between them by prior, not by evidence.

*Example E (constructed, recomputed by the 2026-11-16 check script; CV-DIFFUSION-003).*
A sensor pixel averages 4 high-resolution columns, and a dark crack of width $w\le4$ px
and depth $a$ lies inside one cell: the pixel drops by $aw/4$. A dip of 10 grey levels
fits $(w,a)=(1,40)$, $(2,20)$ and $(4,10)$, and a 1 px crack at any of the 4 positions,
all with $H\hat x=y$ exactly; the measurement fixes $aw=40$ grey levels·px, not the
width. The MMSE estimate is the posterior mean, "an average over all possible
explanations", which yields blurry reconstructions [Blau and Michaeli, §3.1]: with the
three widths equally likely and left-aligned, it is $(23.3,10,3.3,3.3)$, none of the
candidates. A sampler returns one sharp candidate per seed, so a width that varies
across seeds while $H\hat x\approx y$ holds is undetermined by the data.

**Metrics.** PSNR $=10\log_{10}(\mathrm{MAX}^2/\mathrm{MSE})$, for example 34.15 dB for
an RMS error of 5 grey levels on an 8-bit scale (constructed). FID is the Fréchet
distance between Gaussians fitted to Inception features of real and generated images,
$\|m-m_w\|_2^2+\mathrm{Tr}(C+C_w-2(CC_w)^{1/2})$ [Heusel et al., eq. 6]. PSNR measures
distortion; FID measures distribution mismatch; neither measures a defect's width.

## Parameters and tuning

| Parameter | Effect | What to watch |
| --- | --- | --- |
| Noise schedule and $T$ | Signal-to-noise ratio along the chain | Example A; schedules are tied to the training run |
| Sampler and number of steps | Cost, determinism and sample quality | DDIM samples 10× to 50× faster than DDPM with the same trained network [Song et al., abstract] |
| Seed | Which plausible solution is produced | Vary seeds to expose what the measurement does not determine |
| Conditioning strength | Agreement with the condition against diversity | Check consistency with $y$, not only appearance |
| Downsampling factor $f$ and regularization | Cost against detail preservation | LDM-4 to LDM-16 balanced efficiency and quality on ImageNet; large $f$ stalled quality [Rombach et al., §4.1] |
| Resolution and tiling | Memory and seams | Seams and repeated textures at tile borders |

Tuning approach (project method): fix the checkpoint, conditioning and preprocessing;
measure the autoencoder alone on critical structures first; then sweep sampler steps
and seeds on held-out pairs with an acquired high-resolution reference, recording
defect metrics and the seed-to-seed spread.

## Properties and limits of guarantees

- The GAN optimum $p_g=p_{\text{data}}$ holds in the space of arbitrary functions with
  enough capacity [Goodfellow et al., §4]; it says nothing about restoring a
  particular image.
- The VAE objective is a lower bound; DDPM's $L_{\text{simple}}$ is a reweighted bound
  that favours sample quality [Ho et al., §3.4].
- Diffusion sampling is stochastic in DDPM; DDIM can make it deterministic given
  $x_T$ [Song et al., §1].
- Restoration quality and fidelity trade off (perception–distortion); a sharper output
  is not evidence of a better estimate of the scene.
- Latent diffusion inherits the autoencoder's reconstruction limits [§5].

## Cost and implementation

DDPM sampling needs $T=1000$ network evaluations per sample [§4]; DDIM reduces the
number of steps [Song et al.]; latent diffusion reduces spatial positions by $f^2$ but
its sequential sampling remains slower than a GAN's single forward pass
[Rombach et al., §5]. Memory grows with resolution and attention layers. No generator
was executed for this note, and no library API is described.

## Evaluation and controlled variation

**Protocol (proposed, not executed).** Held-out pairs of degraded inputs and
independently acquired high-resolution references with annotated defects.

- *Baseline*: bicubic interpolation and the learned restorer with one seed, measuring
  PSNR, a perceptual or distribution metric, defect recall, false defects and defect
  width error against the reference.
- *Controlled variation*: the same learned restorer and inputs with 8 seeds per input,
  everything else fixed.
- *Reading*: a defect whose presence or width changes across seeds is not determined by
  the measurement (Example C); report the spread next to the averages.

**Measurement limits.** PSNR favours blurred outputs and FID needs many images and
says nothing about one defect; perceptual improvements can hide the modification of a
small critical structure; synthetic training data must be evaluated against real
distributions.

## Failure modes and diagnosis

| Symptom | Possible causes | Discriminating check | Conditional remedy |
| --- | --- | --- | --- |
| A crack disappears or appears after super-resolution | Detail in the null space of $H$; prior of the generator | Compare several seeds and the raw image; check $H\hat x\approx y$ | Keep the raw image as evidence; use a physical reference or better acquisition |
| Small defects lost before any diffusion | Autoencoder compression | Measure $\mathcal D(\mathcal E(x))$ alone on defect crops | Smaller $f$, pixel-space model or no generative step |
| Output varies between runs | Stochastic sampler, unfixed seed | Fix seed, compare samplers | Record seed and sampler; deterministic sampler if needed |
| Repeated or identical samples | GAN mode collapse | Diversity across $z$ | Training changes or another family |
| Good PSNR, defects blurred | Distortion-optimal estimator averages solutions | Defect width and contrast metrics | Task-specific metric; accept the tradeoff explicitly |

## Alternatives and applications

- Prefer a classical restoration with an explicit model (deconvolution, denoising,
  interpolation) when measurements must remain traceable.
- Prefer better acquisition (optics, exposure, resolution) when a detail is below the
  sampling limit; no model recovers it reliably.
- Use generative models for synthetic training data, inpainting for display, or
  defect synthesis, with evaluation against real data.

Industrial uses (project reasoning): generating rare defect variants to train a
detector, validated on real defects; enhancing images for human viewing while
archiving the raw image used for decisions.

## Guided reasoning and proposed checks

These constructed cases develop conditional distributions and restoration fidelity. They explain or test reasoning; no image, video or hardware result is claimed as measured. Method properties remain tied to the sources below.

### Case linked to CV-DIFFUSION-001

**Working question**: Why are training and sampling different operations in a diffusion model?

**Reference answer**: Training learns a denoising rule under a noise distribution; sampling uses this rule in a procedure to produce an output.

**Decomposition of the process**: During learning, we build noisy examples at selected levels and optimize a prediction target according to the formulation. In sampling, weights are used in a sequence of operations to transform a condition and noise into output. The data viewed and decisions made at these two moments differ.

**Example check**: Keep the weights and conditioning fixed, then compare several numbers of steps and seeds on a defined set. Measure cost, diversity and fidelity to the condition rather than concluding from a single favorable image. The marginal forward process at a noise level is not the entire reverse generation procedure. A likely output may fill in unobserved details; it does not become a physical measurement because the training has converged. For a restoration task, the retention of critical information must therefore be evaluated separately.

### Case linked to CV-DIFFUSION-003

**Working question**: Super-resolution makes an image sharp but changes a crack. Why is this a defect in an inspection system?

**Reference answer**: Visual plausibility is not fidelity to critical observation; the model can suppress or invent a structure.

**Why sharpness can deceive**: Multiple detailed images can be compatible with low-resolution observation. The model uses its learned regularities to choose a plausible reconstruction. This decision can create a credible texture without matching the actual crack present.

**Proposed validation**: Keep the raw image and, if possible, a reference acquired with an adapted resolution, then measure preservation, width and location of defects. Compare with a simple restoration with explicit assumptions and examine errors on rare cases. Do not replace the proof of acquisition with a more convincing generated image. An improvement in perceptual score or overall reconstruction may mask the modification of a small but critical structure. The choice depends on the objective: producing an illustration and measuring a crack do not require the same fidelity. No generator is executed in this case, which is used to reason on the output contract.

**Source consulted for this pass**: [Latent Diffusion Models](https://arxiv.org/html/2112.10752v2), §3, latent space and conditioning. The remaining developments are in the [flashcards](../122-generation-restauration.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are constructed cases under stated assumptions; protocols remain proposals until a test is recorded.

### CV-DIFFUSION-001

**Situation**: Why are training and sampling different operations in a diffusion model?

**Noise target**: In the usual DDPM parameterization, draw a level $t$ and a noise $\epsilon$, build $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$, then minimize an error in predicting this noise. With this convention, an estimate of the clean image can be written $\hat x_0=(x_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(x_t,t))/\sqrt{\bar\alpha_t}$. This relationship alone is not a complete sampler: transitions, variances, levels traveled and conditioning remain to be defined. Other settings predict another target. Naming the one used avoids applying an output interpretation formula to the wrong tensor.

### CV-DIFFUSION-002

**Situation**: What tradeoff is introduced by performing diffusion in an autoencoder's latent space?

**Spatial size check**: If the encoder reduces each image dimension by a factor of $f$, the latent grid has about $HW/f^2$ positions, with a different number of channels. This reduction alone does not predict time savings, as decoder, attention and iterations have their own costs. Writing $\tilde x=D(E(x))$ and comparing $x$ with $\tilde x$ isolates the reconstruction of the autoencoder before diffusion. Evaluate specifically the structures smaller than the effective compression support. A good average reconstruction can preserve the large shapes while modifying a rare detail that the product precisely seeks to measure.

### CV-DIFFUSION-003

**Situation**: Super-resolution makes an image sharp but changes a crack. Why is this a defect in an inspection system?

**Non-unique inverse problem**: If the acquisition is $y=Hx+n$, multiple high-resolution $x$ images can produce almost the same $y$ when $H$ loses high frequencies. For a detail $\delta$ such that $H\delta\simeq0$, $x$ and $x+\delta$ are difficult to distinguish from the measurement. The generative model then chooses with its learned preferences, without proof that the crack added or removed is real. Consistency $H\hat x\simeq y$ is useful but insufficient to validate the details lying in the poorly observed null space (kernel) of $H$. This derivation explains why keeping the raw measurement and a physical reference remains essential for inspection.

**Passages consulted for these developments**: [Ho et al., DDPM](https://arxiv.org/html/2006.11239v2), Algorithms 1–2 and §3.2, noise prediction; the algebraic inversion is the project's; [Rombach et al., Latent Diffusion](https://arxiv.org/html/2112.10752v2), §3.1, compression and reconstruction; the spatial size relation and the inverse-problem argument are project deductions.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-DIFFUSION-001 — Fewer sampling steps change an inference procedure

Training may sample individual noise levels to learn a denoiser, while generation repeatedly calls it according to a solver and schedule. Reducing sampling steps changes numerical approximation, latency and possibly output quality without necessarily changing the learned weights. A proposed comparison fixes checkpoint, conditioning, resolution and random seeds while varying the sampler. A training loss at sampled noise levels is not a direct measurement of final generation fidelity.

### CV-DIFFUSION-002 — The autoencoder gives a separate distortion baseline

Before attributing a lost scratch to latent diffusion, inspect $D(E(x))$ for the same input under the autoencoder alone. If the critical structure is already absent, the representation introduces an information bottleneck before iterative generation. A proposed evaluation measures that reconstruction on defect size and contrast, then adds the denoising stage. More sampling iterations cannot be assumed to recover a detail the representation did not preserve.

Consulted foundations: [DDPM](https://arxiv.org/html/2006.11239v2): Algorithms 1–2 and §3 noise-prediction training versus reverse sampling; [Latent Diffusion](https://arxiv.org/html/2112.10752v2): §3.1 perceptual compression and §3.2 latent generation.

## Sources and flashcards

### Scientific sources

- [Kingma and Welling 2014, VAE](https://arxiv.org/abs/1312.6114): §2.2 eq. 3 (lower bound), §2.4 (reparameterization).
- [Goodfellow et al. 2014, GAN](https://arxiv.org/abs/1406.2661): eq. 1, §4.1 Proposition 1 and Theorem 1, §6 (collapse warning).
- [Ho et al. 2020, DDPM](https://arxiv.org/html/2006.11239v2): eq. 4, §3.3 data scaling, §3.4 eq. 14, Algorithms 1–2, §4 schedule; also the [NeurIPS version](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html).
- [Song et al. 2021, DDIM](https://arxiv.org/html/2010.02502v4): abstract and §1, same training objective and faster sampling.
- [Rombach et al. 2022, Latent Diffusion](https://arxiv.org/html/2112.10752v2): §3.1–3.3, §4.1 (downsampling factors), §5 limitations.
- [Blau and Michaeli 2018, The perception–distortion tradeoff](https://arxiv.org/abs/1711.06077): §3.1 (MMSE estimate as posterior mean, blurry reconstructions, Fig. 4), Theorem 1, Definition 3, Example 1, Theorem 2.
- [Heusel et al. 2017, FID](https://arxiv.org/abs/1706.08500): eq. 6.

### Implementation sources

None: no library API or code is described in this awareness-level note.

### Related flashcards and references

- [Flashcards](../122-generation-restauration.md): CV-DIFFUSION-001 to 003.
- [CV-ANOMALIES](../../70-reconnaissance-representations/references/73-patchcore-padim.md) for inspection without generation; [CV-METRIQUES-APPLIQUEES](../../130-evaluation-fiabilite/references/134-metriques-applications.md) for inspection metrics.

Drafted by agent, 2026-10-18. Revision 8, 2026-11-14: body deepened and language corrected by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-14-reference-depth/122-generation-restauration.md).
Revision 9, 2026-11-16: example E (crack width under pixel averaging, MMSE profile, seed check)
added while deepening CV-DIFFUSION-003, by Agent Claude Code (`revue-cartes`, self-review); see the [subject report](https://github.com/speillet/Knowledge_Computer_Vision/blob/main/docs/revues/2026-11-16-card-depth/122-generation-restauration.md).
