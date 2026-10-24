---
id: CV-FUSION
type: methode
domaine: d01
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 5
prerequis: ["CV-SE3"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# Kalman, EKF, UKF et ESKF pour la fusion

## Problème, données et hypothèses

Fusionner mesures et prédictions horodatées en représentant leurs incertitudes. Entrées : modèle d'état, mesures, bruit et timestamps ; sortie : état estimé et covariance. Les incertitudes supposées et les associations conditionnent la cohérence du résultat.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SE3](12-rotations-se3.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Kalman linéaire alterne prédiction et correction. EKF linéarise les modèles. UKF propage $2n+1$ sigma-points déterministes à travers les fonctions non linéaires, sans jacobienne ; sa moyenne a un ordre de précision supérieur à l'EKF, sa covariance le même ordre (Julier et Uhlmann 1997, §3, équations 12–14). ESKF sépare état nominal et petite erreur tangentielle. Chez Solà, l'erreur suit la prédiction d'un EKF (annexe E, équations 439–440), et sa correction utilise la jacobienne d'un EKF classique composée avec celle de l'erreur (§6.1, équation 278). Ce n'est donc pas une alternative mutuellement exclusive à EKF. Corriger l'erreur puis l'injecter dans la pose exige aussi un reset cohérent de covariance.

Solà (§5.1) justifie la formulation à état d'erreur par quatre propriétés. L'erreur d'orientation est minimale, ce qui évite la redondance du quaternion et le risque de covariance singulière lié à sa contrainte. L'erreur opère près de l'origine, loin des singularités de paramétrisation, ce qui garde la linéarisation valide. Elle reste petite, si bien que ses produits du second ordre sont négligeables. Sa dynamique est lente, la dynamique rapide étant intégrée dans l'état nominal : les corrections peuvent venir moins souvent que les prédictions. Le cycle (§5.2) : intégrer l'état nominal sans bruit, prédire la loi de l'erreur, la corriger à l'arrivée d'une mesure non IMU, l'injecter, puis la remettre à zéro.

## Mathématiques, conventions et unités

L'innovation est $\nu=z-h(x^-)$, de covariance $S=HP^-H^T+R$ dans l'EKF. Avec $S$ définie positive, le score $\nu^TS^{-1}\nu$ est sans unité, puisque $S$ porte les unités de $\nu$. Si l'innovation est gaussienne, centrée, blanche et de covariance $S$, il suit une loi du $\chi^2$ à $m$ degrés de liberté, $m$ étant le nombre d'observations (Gamse et al. 2014, §2.2.2, équations 7–10). Un rejet au-delà de $\chi^2_{m;1-\alpha}$ signale un écart dans la prédiction, le modèle stochastique ou l'observation, sans dire lequel. Quantiles à 95 % recalculés : 3,84 ($m=1$), 5,99 ($m=2$), 7,81 ($m=3$), 9,49 ($m=4$). DeepSORT utilise 9,4877 pour une mesure de dimension 4 (§2.2). Raisonnement du projet : des scores trop souvent élevés sur une séquence signalent un filtre surconfiant, trop souvent faibles un filtre sous-confiant.

$P^-=FP^+F^T+Q$ utilise le pas de temps réel. Sur un pas $\Delta t$, Solà montre trois dépendances différentes (annexe E, équation 440) : le terme dynamique est exponentiel, le bruit de mesure IMU contribue en $\Delta t^2$, les perturbations comme les marches aléatoires des biais en $\Delta t$. Les covariances d'impulsion le traduisent : $\sigma_{\tilde a_n}^2\Delta t^2I$ pour la vitesse, $\sigma_{a_w}^2\Delta t\,I$ pour le biais accéléromètre (§5.4.2, équations 262–265). Propager échantillon IMU par échantillon avec le $\Delta t$ réel, et appliquer une mesure caméra à son instant d'acquisition, sont donc des conditions de cohérence ; le traitement des retards par tampon et re-propagation est une proposition du projet. Dans l'ESKF, après injection, $\hat{\delta x}\leftarrow0$ et $P\leftarrow GPG^T$ selon la jacobienne de reset $G$ (Solà, §6.3, équations 285–288). Pour l’erreur angulaire locale $R_{vrai}=R_{nom}\operatorname{Exp}(\delta\theta)$ de Solà, $G_\theta\approx I-[\hat{\delta\theta}/2]_\times$ au premier ordre ; les autres blocs diagonaux sont identitaires. $G\approx I$ néglige le changement de coordonnées pour une petite correction ; une erreur angulaire globale demande une jacobienne différente. Remettre l'erreur moyenne à zéro ne remet pas l'incertitude à zéro.

## Paramètres et propriétés

Choisir état, fréquence, Q/R, traitement des biais, délais et mesure absente. Un bruit artificiellement petit donne une confiance excessive. UKF ne garantit pas de réparer toute non-linéarité, distribution multimodale ou mauvais modèle.

## Coût et implémentation

L'état et la fréquence dominent les produits matriciels ; la cohérence temporelle prime sur une promesse de fréquence. Aucune implémentation complète de filtre n'est fournie ; l'exemple scalaire exécuté du premier lot illustre seulement une correction.

Forme de la mise à jour de covariance. La soustraction $P^+=P^--KSK^T$, avec $S=HP^-H^T+R$, reste vulnérable aux arrondis. Chin/JPL 2023 (§III-A, équation 14) privilégie la forme de Joseph $P^+=(I-KH)P^-(I-KH)^T+KRK^T$. $P^-$ désigne la covariance avant correction, $K$ le gain, $H$ la jacobienne de mesure et $R$ sa covariance de bruit. Sous indépendance des erreurs de prédiction et de mesure et avec $P^-,R$ semi-définies positives, la somme de termes quadratiques préserve la semi-définie positivité en arithmétique exacte ; elle réduit le risque numérique mais n’offre pas de garantie absolue en flottants. Surveiller symétrie, valeurs propres et conditionnement ; une factorisation Cholesky exige la positivité stricte. Une implémentation square-root peut être comparée si nécessaire. Symétriser $(P+P^T)/2$ ne corrige pas à elle seule une valeur propre négative. Les symptômes et tests sont des diagnostics proposés par le projet.

## Évaluation et variation contrôlée

Variation proposée : augmenter R en conservant mesure/prédiction ; la correction doit suivre moins fortement la mesure. Vérifier ensuite l'innovation sur séquences réservées ; une covariance faible seule n'atteste pas la précision réelle.

## Échecs et diagnostic

Deux capteurs en désaccord : comparer horodatage, extrinsèques, unités, biais et corrélations avant de diminuer R. Des innovations systématiquement biaisées suggèrent autre chose qu'un bruit blanc accru.

## Alternatives et usages

Filtrage pour faible latence ; lissage/graphes pour réestimer plusieurs états. Une mesure redondante corrélée ne doit pas être comptée deux fois comme information indépendante.

## Sources et cartes

- [Gamse et al. 2014, Statistical Process Control of a Kalman Filter Model, §2.2.2, équations 5–10, et §3.4.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/).
- [Julier et Uhlmann 1997, A New Extension of the Kalman Filter to Nonlinear Systems, SPIE 3068, §3, équations 12–14](https://doi.org/10.1117/12.280797) : sigma-points, ordre de précision, absence de jacobienne. Version de l'éditeur payante ; texte lu sur une copie de cours hébergée par Berkeley. L'article de 2004 aux Proceedings of the IEEE, cité auparavant, n'a pas été lu.
- [Wojke, Bewley et Paulus 2017, DeepSORT, §2.2](https://arxiv.org/abs/1703.07402) : seuil $\chi^2$ à 95 % en dimension 4.

- [Solà, Quaternion kinematics for the error-state Kalman filter](https://arxiv.org/abs/1711.02508) : §5.1 avantages de l'ESKF, §5.2 principe, §5.4.2 équations 262–265, §6.1 équations 274–278 et note 26, §6.3 équations 285–288, annexe E équations 438–440.
- [Chin/JPL 2023, stabilité numérique et forme de Joseph, §III-A](https://ipnpr.jpl.nasa.gov/progress_report/42-233/42-233A-orig.pdf).
- [Cartes associées](../13-kalman-ekf-eskf.md) : CV-FUSION-001 à 006.

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet. Révisions 3 et 4 : auto-revue `revue-cartes` par Agent Claude Code le 2026-10-23, corrections puis enrichissements acceptés par l'apprenant, sans validation indépendante.
