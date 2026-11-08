---
id: CV-BIOMETRIE
type: comparaison
domaine: d07
poles: [E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 7
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# Biometric recognition, ArcFace and PAD

## Problem, data and assumptions

Compare visual identities according to a protocol, without confusing verification 1:1, identification 1:N and presentation detection. Entries: acquisitions and embeddings; outputs: scores/decisions conditioned to the threshold. This reference note does not establish any regulatory compliance.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

ArcFace learns an angular separation of identity representations. An embedding comparison does not automatically detect a photo, screen, or other attack by presentation; PAD is another problem with its protocol.

## Mathematics, conventions and units

FMR/FNMR describe comparison errors below a threshold; FAR/FRR system also depend on procedure and acquisition failures. An EER is a balancing point of a protocol, not the result of very low false acceptance rates. Similarities remain dependent on the domain.

## Parameters and properties

Qualify populations, quality, enrolment, threshold and data; evaluate subgroups and acquisition conditions. A PAD standard reference must be versioned in a dedicated study; no certification is inferred from a model.

## Cost and implementation

Encode, search, and maintain the gallery have different costs between 1:1 and 1:N. No real face or biometric system executed.

## Evaluation and controlled variation

Proposed variation: quality/pose then gallery size separately. Measure at business threshold and intervals according to protocol, not just a global accuracy or EER.

## Failure modes and diagnosis

Good average score but failures on a condition: stratify acquisition and comparison, inspect threshold and data. A correct face detection does not attest to identity or liveness.

## Alternatives and applications

Verification, identification, quality and PAD require separate outputs and references; documenting generalization limits.

## Guided reasoning and proposed checks

These built cases develop verification, identification and point of exploitation. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-BIOMETRIE-001

**Question of work**: Does an ArcFace embedding that separates identities well prove that a presentation is genuine?

**Reference Response**: No: the identity comparison and PAD have separate targets and evaluation data.

**Difference of Targets**: Recognition compares an acquisition to a reference identity. Presentation detection seeks to distinguish certain types of acquisition or attack according to another protocol. A reproduction can retain a very close appearance of identity without being an authentic presentation.

**Constructed example**: A sharp photo can produce an embedding close to that of the person; this proximity answers a question of appearance, not the physical presence of that person at the time of acquisition. Define and evaluate the two outputs with adapted data, and then integrate them into the system. A correct face detection also does not resolve identity verification. The subject remains a technical contract of perception and evaluation; no conformity, certification or guarantee of resistance to any presentation is deduced from the embedding model alone.

### Case linked to CV-BIOMETRIE-002

**Question of work**: Why is EER insufficient for a system operating at a threshold with very low FMR?

**Reference Response**: It describes a balance point that may differ significantly from the target threshold; measure FNMR and other errors at the required point.

**Reading the curve**: Moving the threshold simultaneously changes wrongly accepted comparisons and wrongly rejected identities. The EER refers to an equality of these rates in a given protocol; a product aimed at a very low rate of false correspondence generally works elsewhere on the curve.

**Proposed evaluation**: set the threshold on setting data, then measure the rate of false non-matches at the level of FMR targeted on an independent test. Record acquisition quality, population, enrollment, and set size; examine subgroups and statistical uncertainty when relevant. Capture failures still add events at the system level. A good average value does not predict all operating conditions. The operating point and the comparison units must remain visible for two recognition results to be interpretable.

**Documentary reference for this pass**: [NIST, FRTE 1:1 Verification](https://pages.nist.gov/frvt/html/frvt11.html), presentation of the evaluation check and errors. The other developments are in the [flashcards](../75-embeddings-biometrie.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-BIOMETRIE-001

**Situation**: Does an ArcFace embedding that separates identities well prove that a presentation is genuine?

**What the Margin Learns**: In ArcFace, class weights and normalized features give logits proportional to $\cos\theta_j$; for the target class during learning, an angular margin uses $\cos(\theta_y+m)$. This constraint pushes the separation of identities in the learned space. It does not provide a label on the materiality of a photographic presentation or on screen. At the inference, the score between two embeddings and the decision PAD therefore remain different outputs. If combined, evaluate their dependence and acquisition failures on common trials: naively multiplying two scores does not give a validated system probability.

### CV-BIOMETRIE-002

**Situation**: Why is EER insufficient for a system operating at a threshold with very low FMR?

**Amount of evidence**: Under a simplified model of $n$ independent non-matte comparisons with probability of false correspondence $p$, observing zero error has probability $(1-p)^n$. The unilateral upper limit of 95% is then $1-0,05^{1/n}$, approximately $3/n$ for large $n$. Zero error on 1 000 comparisons thus remains compatible with a rate of around 0,003, and does not demonstrate a target of $10^{-6}$. Comparisons sharing the same identities are not necessarily independent; the uncertainty must respect the protocol. This constructed analysis explains why an excellent EER and a small test do not characterize the distribution tails at the target threshold.

**Passages consulted for these developments**: [Deng et al., ArcFace](https://arxiv.org/html/1801.07698v4), §III-A, angular margin; binomial bound and system reasoning constructed.

## Worked reasoning and boundary cases — 2026-11-08

The following are constructed project deductions and proposed checks, not
new empirical results. Each extends an existing recall objective; the concise
expected answer on its card remains the grading target.

### CV-BIOMETRIE-001 — Identity similarity and presentation validity can disagree

A high-quality photograph of an enrolled person can preserve identity cues while being an attack presentation. An identity embedding may correctly recognize those cues without solving the distinct presentation-validity task. A proposed system evaluation therefore separates bona fide matches, impostor matches and the defined attack types, then assesses the combined decision policy. A low identity error rate alone supplies no measured error rate for attacks absent from that benchmark.

### CV-BIOMETRIE-002 — Low prevalence changes the fraction of accepted errors

For genuine-attempt prevalence $\pi$, the fraction of accepted attempts that are false matches is $(1-\pi)FMR/[\pi(1-FNMR)+(1-\pi)FMR]$ under this constructed binary decision model. It differs from FMR, whose denominator is nonmate attempts. Thus the same matcher operating point can produce different accepted-error composition under a different traffic mix. Report the deployment scenario and uncertainty at the required threshold instead of relying on EER alone.

Consulted foundations: [ArcFace](https://arxiv.org/html/1801.07698v4): §III-A normalized identity embeddings and angular margin; [NIST FRTE 1:1](https://pages.nist.gov/frvt/html/frvt11.html): verification operating points, FMR and FNMR.

## Sources and flashcards

- [Ngan et al. 2023, NISTIR 8491, summary PAD](https://www.nist.gov/publications/face-analysis-technology-evaluation-fate-part-10-performance-passive-software-based)

- [ArcFace, objective and evaluation](https://arxiv.org/abs/1801.07698).
- [NIST FRTE 1:1, FMR/FNMR](https://pages.nist.gov/frvt/html/frvt11.html).
- [Related flashcards](../75-embeddings-biometrie.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
