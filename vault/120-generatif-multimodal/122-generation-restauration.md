# Flashcards — VAEs, GANs and diffusion for generation and restoration

reference note: [[120-generatif-multimodal/references/122-generation-restauration|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::120-generatif-multimodal

## CV-DIFFUSION-001

Objective: Separate training and sampling. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-DIFFUSION-001
Question: Why are training and sampling different operations in a diffusion model?
Reponse: **Expected answer**: Training learns a denoising rule under a noise distribution; sampling uses this rule in a procedure to produce an output.

**Further explanation**: The choice of sampler, number of steps and conditioning changes cost and results without making the output true by definition.

**Decomposition of the process**: During learning, we build noisy examples at selected levels and optimize a prediction target according to the formulation. In sampling, weights are used in a sequence of operations to transform a condition and noise into output. The data viewed and decisions made at these two moments differ.

**Example check**: Keep the weights and conditioning fixed, then compare several numbers of steps and seeds on a defined set. Measure cost, diversity and fidelity to the condition rather than concluding from a single favorable image. The marginal forward process at a noise level is not the entire reverse generation procedure. A likely output may fill in unobserved details; it does not become a physical measurement because the training has converged. For a restoration task, the retention of critical information must therefore be evaluated separately.

**Noise target**: In the usual DDPM parameterization, draw a level $t$ and a noise $\epsilon$, build $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$, then minimize an error in predicting this noise. With this convention, an estimate of the clean image can be written $\hat x_0=(x_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(x_t,t))/\sqrt{\bar\alpha_t}$. This relationship alone is not a complete sampler: transitions, variances, levels traveled and conditioning remain to be defined. Other settings predict another target. Naming the one used avoids applying an output interpretation formula to the wrong tensor.

**Fewer sampling steps change an inference procedure**: Training may sample individual noise levels to learn a denoiser, while generation repeatedly calls it according to a solver and schedule. Reducing sampling steps changes numerical approximation, latency and possibly output quality without necessarily changing the learned weights. A proposed comparison fixes checkpoint, conditioning, resolution and random seeds while varying the sampler. A training loss at sampled noise levels is not a direct measurement of final generation fidelity.

**Blocking errors**: Equating the forward noising process with the whole generation procedure.
Source: [[120-generatif-multimodal/references/122-generation-restauration|Full reference]]; [Ho et al., DDPM, eq. 4, §3.4 eq. 14 and Algorithms 1–2: noise-prediction training versus iterative sampling](https://arxiv.org/html/2006.11239v2); [Song et al., DDIM, abstract and §1: same training objective, different and faster sampler](https://arxiv.org/html/2010.02502v4). The inversion for the clean-image estimate is a project derivation.
Tags: cv::pilote cv::d12 famille::comprehension cv_id::CV-DIFFUSION-001 provenance::agent pole::A pole::D pole::E
END

## CV-DIFFUSION-002

Objective: Situate latent diffusion. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-DIFFUSION-002
Question: What tradeoff is introduced by performing diffusion in an autoencoder's latent space?
Reponse: **Expected answer**: Reduce the spatial cost of the process at the cost of a compressed representation and its reconstruction error.

**Further explanation**: Also assess what the autoencoder can lose, including small defects, and not just the denoiser. The latent diffusion authors note that even their $f=4$ autoencoder can become a bottleneck for tasks requiring fine-grained pixel accuracy, and found factors between 4 and 16 a good balance for ImageNet generation, with larger factors limiting the achievable quality.

**Two possible sources of loss**: The autoencoder transforms the image into a more compact representation, and then the generative process acts in this space. A detail poorly preserved by the first transformation can be difficult to preserve afterwards, even if the latent noise removal works according to its purpose.

**Proposed ablation**: First compare the raw image to its autoencoder reconstruction without adding the diffusion process. Examine small defects and useful boundaries, and then introduce generation under the same condition. Measure perceptual quality and application fidelity separately, with held-out references. This separation locates the origin of a degradation and avoids assigning everything to the sampler. The compression targets a tradeoff between computation and representation; its relevance depends on what the application must keep. An inconspicuous loss for a general scene can be decisive for a scratch or fine measurement.

**Spatial size check**: If the encoder reduces each image dimension by a factor of $f$, the latent grid has about $HW/f^2$ positions, with a different number of channels. This reduction alone does not predict time savings, as decoder, attention and iterations have their own costs. Writing $\tilde x=D(E(x))$ and comparing $x$ with $\tilde x$ isolates the reconstruction of the autoencoder before diffusion. Evaluate specifically the structures smaller than the effective compression support. A good average reconstruction can preserve the large shapes while modifying a rare detail that the product precisely seeks to measure.

**The autoencoder gives a separate distortion baseline**: Before attributing a lost scratch to latent diffusion, inspect $D(E(x))$ for the same input under the autoencoder alone. If the critical structure is already absent, the representation introduces an information bottleneck before iterative generation. A proposed evaluation measures that reconstruction on defect size and contrast, then adds the denoising stage. More sampling iterations cannot be assumed to recover a detail the representation did not preserve.

**Blocking errors**: Assuming that compression has no consequence for fidelity.
Source: [[120-generatif-multimodal/references/122-generation-restauration|Full reference]]; [Rombach et al., Latent Diffusion, §§3.1–3.2: perceptual compression and latent diffusion; §4.1: downsampling factors; §5: reconstruction as a bottleneck for fine-grained accuracy](https://arxiv.org/html/2112.10752v2). The spatial size relation is a project deduction.
Tags: cv::pilote cv::d12 famille::comparaison cv_id::CV-DIFFUSION-002 provenance::agent pole::A pole::D pole::E
END

## CV-DIFFUSION-003

Objective: Protect an industrial observation. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-DIFFUSION-003
Question: Super-resolution makes an image sharp but changes a crack. Why is this a defect in an inspection system?
Reponse: **Expected answer**: Visual plausibility is not fidelity to critical observation; the model can suppress or invent a structure.

**Further explanation**: Compare with the reference data and keep the raw image; choose a measurement adapted to the defect.

**Why sharpness can deceive**: Multiple detailed images can be compatible with low-resolution observation. The model uses its learned regularities to choose a plausible reconstruction. This decision can create a credible texture without matching the actual crack present.

**Proposed validation**: Keep the raw image and, if possible, a reference acquired with an adapted resolution, then measure preservation, width and location of defects. Compare with a simple restoration with explicit assumptions and examine errors on rare cases. Do not replace the proof of acquisition with a more convincing generated image. An improvement in perceptual score or overall reconstruction may mask the modification of a small but critical structure. The choice depends on the objective: producing an illustration and measuring a crack do not require the same fidelity. No generator is executed in this case, which is used to reason on the output contract.

**Non-unique inverse problem**: If the acquisition is $y=Hx+n$, multiple high-resolution $x$ images can produce almost the same $y$ when $H$ loses high frequencies. For a detail $\delta$ such that $H\delta\simeq0$, $x$ and $x+\delta$ are difficult to distinguish from the measurement. The generative model then chooses with its learned preferences, without proof that the crack added or removed is real. Consistency $H\hat x\simeq y$ is useful but insufficient to validate the details lying in the poorly observed null space (kernel) of $H$. This derivation explains why keeping the raw measurement and a physical reference remains essential for inspection.

**Blocking errors**: Validating a dimensional measurement on a prettier image alone.
Source: [[120-generatif-multimodal/references/122-generation-restauration|Full reference]]; constructed case of the project: fidelity to a crack versus plausibility; [Blau and Michaeli, The perception–distortion tradeoff, Theorem 1 and Theorem 2: for non-invertible degradations, low distortion and natural appearance conflict](https://arxiv.org/abs/1711.06077); [Rombach et al., Latent Diffusion, §3.1 and §5: compression and its fine-detail limit](https://arxiv.org/html/2112.10752v2).
Tags: cv::pilote cv::d12 famille::diagnostic cv_id::CV-DIFFUSION-003 provenance::agent pole::A pole::D pole::E
END
