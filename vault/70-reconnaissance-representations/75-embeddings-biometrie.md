# Flashcards — Biometric recognition, ArcFace and PAD

reference note: [[70-reconnaissance-representations/references/75-embeddings-biometrie|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-BIOMETRIE-001

Objective: Distinguish between identity and presentation. Family: comparison. Provenance: agent.

START
CV-Pilote
ID: CV-BIOMETRIE-001
Question: Does an ArcFace embedding that separates identities well prove that a presentation is genuine?
Reponse: **Expected answer**: No: the identity comparison and PAD have separate targets and evaluation data.

**Further explanation**: Measure each component in the real system; a high identity score can also come from a reproduction.

**Difference of Targets**: Recognition compares an acquisition to a reference identity. Presentation detection seeks to distinguish certain types of acquisition or attack according to another protocol. A reproduction can retain a very close appearance of identity without being an authentic presentation.

**Constructed example**: A sharp photo can produce an embedding close to that of the person; this proximity answers a question of appearance, not the physical presence of that person at the time of acquisition. Define and evaluate the two outputs with adapted data, and then integrate them into the system. A correct face detection also does not resolve identity verification. The subject remains a technical contract of perception and evaluation; no conformity, certification or guarantee of resistance to any presentation is deduced from the embedding model alone.

**What the Margin Learns**: In ArcFace, class weights and normalized features give logits proportional to $\cos\theta_j$; for the target class during learning, an angular margin uses $\cos(\theta_y+m)$. This constraint pushes the separation of identities in the learned space. It does not provide a label on the materiality of a photographic presentation or on screen. At the inference, the score between two embeddings and the decision PAD therefore remain different outputs. If combined, evaluate their dependence and acquisition failures on common trials: naively multiplying two scores does not give a validated system probability.

**Identity similarity and presentation validity can disagree**: A high-quality photograph of an enrolled person can preserve identity cues while being an attack presentation. An identity embedding may correctly recognize those cues without solving the distinct presentation-validity task. A proposed system evaluation therefore separates bona fide matches, impostor matches and the defined attack types, then assesses the combined decision policy. A low identity error rate alone supplies no measured error rate for attacks absent from that benchmark.

**Blocking errors**: Deducing liveness from facial similarity.
Source: [[70-reconnaissance-representations/references/75-embeddings-biometrie|Full reference]]; [Deng et al., ArcFace, angular margin objective](https://arxiv.org/abs/1801.07698); [Ngan et al. 2023, NISTIR 8491, summary PAD](https://www.nist.gov/publications/face-analysis-technology-evaluation-fate-part-10-performance-passive-software-based); [Deng et al., ArcFace, §III-A, angular margin; binomial bound and system reasoning constructed](https://arxiv.org/html/1801.07698v4), see 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-BIOMETRIE-001 provenance::agent pole::E
END

## CV-BIOMETRIE-002

Objective: Choose an operating point. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-BIOMETRIE-002
Question: Why is EER insufficient for a system operating at a threshold with very low FMR?
Reponse: **Expected answer**: It describes a balance point that may differ significantly from the target threshold; measure FNMR and other errors at the required point.

**Further explanation**: Specify data, acquisition and subgroups; an average does not give the whole curve.

**Reading the curve**: Moving the threshold simultaneously changes wrongly accepted comparisons and wrongly rejected identities. The EER refers to an equality of these rates in a given protocol; a product aimed at a very low rate of false correspondence generally works elsewhere on the curve.

**Proposed evaluation**: set the threshold on setting data, then measure the rate of false non-matches at the level of FMR targeted on an independent test. Record acquisition quality, population, enrollment, and set size; examine subgroups and statistical uncertainty when relevant. Capture failures still add events at the system level. A good average value does not predict all operating conditions. The operating point and the comparison units must remain visible for two recognition results to be interpretable.

**Amount of evidence**: Under a simplified model of $n$ independent non-matte comparisons with probability of false correspondence $p$, observing zero error has probability $(1-p)^n$. The unilateral upper limit of 95% is then $1-0,05^{1/n}$, approximately $3/n$ for large $n$. Zero error on 1 000 comparisons thus remains compatible with a rate of around 0,003, and does not demonstrate a target of $10^{-6}$. Comparisons sharing the same identities are not necessarily independent; the uncertainty must respect the protocol. This constructed analysis explains why an excellent EER and a small test do not characterize the distribution tails at the target threshold.

**Low prevalence changes the fraction of accepted errors**: For genuine-attempt prevalence $\pi$, the fraction of accepted attempts that are false matches is $(1-\pi)FMR/[\pi(1-FNMR)+(1-\pi)FMR]$ under this constructed binary decision model. It differs from FMR, whose denominator is nonmate attempts. Thus the same matcher operating point can produce different accepted-error composition under a different traffic mix. Report the deployment scenario and uncertainty at the required threshold instead of relying on EER alone.

**Blocking errors**: Assimilate EER and performance to any threshold.
Source: [[70-reconnaissance-representations/references/75-embeddings-biometrie|Full reference]]; [NIST FRTE 1:1, definitions FMR/FNMR, consulted on 2026-10-20](https://pages.nist.gov/frvt/html/frvt11.html); comparison of operating points deduced from the error curve; [Deng et al., ArcFace, §III-A, angular margin; binomial bound and system reasoning constructed](https://arxiv.org/html/1801.07698v4), consulted the 2026-10-30. Added reasoning: project deduction; consulted passages are recorded in the canonical reference for 2026-11-08.
Tags: cv::pilote cv::d07 famille::evaluation cv_id::CV-BIOMETRIE-002 provenance::agent pole::E
END
