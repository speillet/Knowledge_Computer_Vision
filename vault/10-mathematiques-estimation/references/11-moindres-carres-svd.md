---
id: CV-SVD
type: methode
domaine: d01
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 4
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# Moindres carrés, SVD et conditionnement

## Problème, données et hypothèses

Estimer des paramètres géométriques à partir d'observations bruitées. Entrées : $A\in\mathbb R^{m\times n}$, $b\in\mathbb R^m$ et leur contrat d'unités ; sortie : paramètres et diagnostic de rang. Un modèle linéarisé n'est valable que près de son point de développement. Des outliers nécessitent un traitement robuste distinct du choix du solveur.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Projeter les observations sur l'espace expliqué par le modèle ; résoudre par QR ou SVD, inspecter valeurs singulières et résidus, puis confronter la solution à des observations réservées. La SVD décompose les directions bien ou mal contraintes ; une petite erreur d'ajustement n'atteste pas l'identifiabilité.

## Mathématiques, conventions et unités

On minimise $\|Ax-b\|_2^2$. Si $A=U\Sigma V^T$ est la SVD fine à rang colonne plein, $\hat x=V\Sigma^{-1}U^Tb$, donc $\delta\hat x=\sum_i(u_i^T\delta b/\sigma_i)\,v_i$ : une perturbation des mesures est amplifiée par $1/\sigma_i$ le long du vecteur singulier droit $v_i$. Réciproquement, $\|A(t\,v_i)\|=|t|\,\sigma_i$ : le long d'une direction de petite valeur singulière, les paramètres peuvent bouger sans changer le résidu. Cette relation est une dérivation algébrique du projet. Le conditionnement $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$ dépend de l'échelle des colonnes, donc des unités des paramètres. À rang colonne plein, $\kappa_2(A^TA)=\kappa_2(A)^2$ : les équations normales amplifient le conditionnement. Pour un résidu $r$ et sa covariance $C$ définie positive, $r^TC^{-1}r$ est sans unité. Blanchir signifie former $L^{-1}r$ avec $C=LL^T$ ; la forme quadratique est sa norme au carré. Une covariance singulière impose de traiter les contraintes ou le sous-espace observable séparément ; mélanger pixels et mètres sans pondération modifie arbitrairement l'objectif.

## Système homogène, DLT et normalisation

L'estimation linéaire d'une homographie ou d'une matrice fondamentale s'écrit $Lh=0$, avec $h$ défini à un facteur près. Pour une homographie, chaque correspondance fournit deux équations linéaires en les neuf coefficients, d'où $L\in\mathbb R^{2n\times9}$ ; pour $F$, une équation par correspondance et au moins huit points. On minimise $\|Lh\|$ sous $\|h\|=1$ pour exclure la solution nulle ; la solution est le vecteur singulier droit de la plus petite valeur singulière, ou le vecteur propre minimal de $L^TL$ (Zhang 1998, annexe A ; Hartley 1997, §2.2). Pour $F$, on impose ensuite le rang 2 en annulant la plus petite valeur singulière : la matrice obtenue est la plus proche en norme de Frobenius (Hartley 1997, §2.3). Ce coût est algébrique, sans sens physique : Zhang l'utilise pour initialiser, puis minimise l'erreur de reprojection (§3.2).

Sur des pixels bruts, une ligne de $L$ mélange 1, des coordonnées de l'ordre de $10^3$ et des produits de l'ordre de $10^6$ ; Zhang note que $L$ est alors mal conditionnée. Hartley (§4) montre qu'un tel étalement rend le vecteur propre minimal très sensible au bruit, selon le rapport $d_1/d_8$. Sa normalisation (§5.1) traite chaque image séparément : translation du centroïde à l'origine, puis mise à l'échelle isotrope pour une distance moyenne de $\sqrt2$. On estime sur les points normalisés $\hat x=Tx$, $\hat x'=T'x'$, puis on dénormalise : $H=T'^{-1}\hat HT$, ou $F=T'^T\hat FT$ (§3). La solution des moindres carrés algébriques n'est pas invariante à ces transformations (§3) : normaliser change l'estimateur. Sur la paire « house », le conditionnement s'améliore d'environ $10^8$ (§7.3.1).

## Moindres carrés non linéaires et pertes robustes

Pour un résidu non linéaire $r(x)$ de jacobien $J$, Gauss-Newton linéarise $r(x+\delta)\approx r(x)+J\delta$ et résout $J^TJ\delta=-J^Tr$. Il remplace le hessien par $J^TJ$, approximation valable si les résidus sont petits ou le modèle presque linéaire ; sinon la convergence ralentit fortement (Triggs et al. 2000, §4.3). Levenberg-Marquardt amortit le pas : $(J^TJ+\lambda D^TD)\delta=-J^Tr$. $\lambda$ grandit quand la prédiction est mauvaise, ce qui raccourcit le pas vers la descente de gradient, et diminue sinon (§4.2). Ceres le formule en région de confiance de rayon $\mu$, doublé ou divisé par deux selon le rapport entre baisse réelle et baisse prédite ; $D$ est souvent la racine de la diagonale de $J^TJ$. Ces méthodes trouvent un minimum local : elles exigent une initialisation, linéaire ou fermée, dans le bon bassin.

Une perte robuste remplace la contribution $s=\|f\|^2$ d'un bloc par $\frac12\rho(s)$, avec $\rho(0)=0$ et $\rho'(0)=1$, pour imiter le coût quadratique près de zéro et réduire le poids des grands résidus. Avec l'échelle $a$, $\rho(s,a)=a^2\rho(s/a^2)$ : $a$ a l'unité de la norme du résidu. Ceres définit Huber, $\rho(s)=s$ pour $s\le1$ et $2\sqrt s-1$ au-delà, et Cauchy, $\rho(s)=\log(1+s)$. Leurs poids $\rho'(s)$ décroissent en $1/\|f\|$ et $1/\|f\|^2$, calcul du projet. Triggs et al. appliquent $\rho$ au résidu pondéré $\Delta z^TW\Delta z$, chaque groupe d'observations étant accepté ou réduit en bloc (§3.3). Ils notent aussi qu'une erreur touchant toutes les observations, comme un modèle de projection faux, ne se corrige pas par simple nettoyage des données. Une perte robuste ne fournit pas non plus l'initialisation : avec beaucoup d'outliers, un filtrage comme RANSAC la précède. Cette articulation est un raisonnement du projet.

## Incertitude des paramètres

Ceres donne $C(x^*)=(J^TJ)^{-1}$ comme covariance de l'estimée, sous deux hypothèses. Les résidus doivent avoir une covariance identité, ce que l'utilisateur obtient en évaluant $S^{-1/2}f$. $J$ doit être de rang colonne plein ; sinon la covariance est déficiente et donnée par la pseudo-inverse. En SfM, la reconstruction n'est définie qu'à une similitude près : cette jauge demande une SVD ou une inversion adaptée. L'algorithme par défaut, `SPARSE_QR`, ne traite pas un jacobien déficient : `Compute()` renvoie faux. `DENSE_SVD` le traite, pour des problèmes petits ou moyens. Triggs et al. (§3.1) rappellent que la dispersion n'approche la covariance de l'estimateur qu'asymptotiquement ; c'est bien moins sûr pour les petits problèmes de géométrie et les réseaux faibles. Cette covariance ne mesure ni biais de modèle ni outliers.

## Paramètres et propriétés

Centrer/mettre à l'échelle les variables, fixer la tolérance de rang et justifier une régularisation. Rang déficient, mauvais conditionnement et mauvaise adéquation physique sont trois diagnostics différents. Régulariser ajoute une hypothèse ; cela ne crée pas une observation.

## Coût et implémentation

SVD facilite le diagnostic de rang mais peut coûter davantage qu'un QR adapté. Eigen classe la SVD comme généralement la plus précise mais la plus lente. Il présente les équations normales comme en général les plus rapides, surtout pour $A$ haute et étroite, mais déconseillées dès que $A$ est même modérément mal conditionnée, car elles perdent environ deux fois plus de chiffres. Ordre de grandeur du projet : avec $\kappa_2(A)=10^6$, environ 6 des 16 chiffres de la double précision sont menacés avec QR, environ 12 avec les équations normales.

Les grands problèmes creux renversent l'arbitrage. Ceres recommande `DENSE_QR` pour les petits problèmes denses et prévient que `DENSE_NORMAL_CHOLESKY` peut échouer pour un jacobien mal conditionné. Pour le bundle adjustment, il forme pourtant les équations normales et élimine les points par complément de Schur : `DENSE_SCHUR` reste praticable jusqu'à quelques centaines de caméras, `SPARSE_SCHUR` vise des milliers. Mise à l'échelle des paramètres et préconditionnement y sont donc indispensables. Aucun appel Eigen/Ceres n'est exécuté ici ; éviter de matérialiser une inverse comme recette par défaut.

## Évaluation et variation contrôlée

Cas analytique : deux colonnes presque identiques donnent une direction peu contrainte. Perturber légèrement b en gardant A fixe : prédire une forte variation des paramètres dans cette direction, même si les résidus changent peu. Comparer QR/SVD et stabilité, pas seulement le coût minimal.

Calcul exécuté par le projet le 2026-10-23 hors du dépôt (Python 3.10.13, NumPy 2.2.6) : $A$ de trois lignes, de colonnes $(1,1,1)$ et $(1;1{,}001;0{,}999)$, a $\sigma_2\approx10^{-3}$ et $\kappa_2(A)\approx2{,}4\cdot10^3$. Une perturbation de $b$ de norme $10^{-3}$ alignée sur $u_2$ déplace $\hat x$ d'une norme 1,0 selon $v_2\approx(1,-1)/\sqrt2$ ; le résidu reste de l'ordre de $10^{-16}$. Ceres illustre le même phénomène avec $J=\begin{pmatrix}1&1\\1&1{,}0000001\end{pmatrix}$ : $(J^TJ)^{-1}$ a des termes d'environ $\pm2{,}05\cdot10^{14}$, résultat que la documentation juge inutilisable. Ce sont des cas construits, pas des mesures sur images.

Variation contrôlée de la DLT, exécutée dans le même environnement. Baseline : DLT d'homographie sur coordonnées pixel brutes. Facteur varié : la seule normalisation de Hartley, à données identiques. Le cas est construit : homographie connue proche de l'identité, bruit gaussien de 0,5 px, 200 tirages par configuration. Prédiction : forte baisse de $\sigma_1/\sigma_8$ dans tous les cas, gain de précision surtout quand les points sont loin de l'origine par rapport à leur étendue. Mesure : erreur médiane de transfert sur 200 points répartis dans toute l'image 1920×1080.

| Configuration | $\sigma_1/\sigma_8$ brut | normalisé | Erreur brute | normalisée |
| --- | --- | --- | --- | --- |
| 50 points sur toute l'image | $8{,}3\cdot10^6$ | 4,1 | 0,22 px | 0,20 px |
| 8 points sur toute l'image | $1{,}2\cdot10^7$ | 6,6 | 0,70 px | 0,67 px |
| 20 points dans un carré de 200 px | $1{,}4\cdot10^8$ | 3,5 | 1013 px | 28 px |

Lecture : en double précision, des points bien répartis tolèrent l'absence de normalisation ; des points concentrés loin de l'origine ne la tolèrent pas. Normaliser ne remplace pas la couverture : 28 px reste une extrapolation fragile. Limites : un seul modèle, un bruit isotrope, pas d'outliers, pas d'image réelle.

## Échecs et diagnostic

Des paramètres énormes avec petit résidu suggèrent ambiguïté, unités ou conditionnement. Inspecter spectre singulier et contraintes physiques ; injecter des mesures indépendantes avant de seulement augmenter le nombre d'itérations.

Après un estimateur robuste, deux causes d'instabilité se départagent. Des outliers restés parmi les inliers laissent une queue de résidus près du seuil ; les retirer stabilise l'estimation. Une quasi-dégénérescence tient à la géométrie des inliers, alignés, concentrés ou presque coplanaires selon le modèle : la solution varie le long d'une même direction même sur des inliers propres. Le rejet d'outliers n'y change rien ; seules une meilleure couverture ou un modèle plus contraint y remédient. Chum, Werner et Matas (2005) en donnent un cas : avec un plan dominant, un échantillon de sept correspondances dont au moins cinq vérifient une homographie produit une géométrie épipolaire compatible avec tout ce plan. Leur théorème explique pourquoi RANSAC échoue souvent sur la géométrie épipolaire en présence d'un plan dominant. Pour un système homogène $Lh=0$, la solution est portée par la plus petite valeur singulière : c'est l'avant-dernière qui doit rester nettement non nulle, ce que Hartley (1997, §4) exprime par le rapport $d_1/d_8$. Les tests de queue de résidus, de couverture et de rééchantillonnage sont des propositions du projet.

## Alternatives et usages

QR pour un problème bien posé, SVD pour diagnostic de rang et systèmes homogènes, solveur creux pour grandes reconstructions, estimation robuste contre outliers. Chaîne usuelle en géométrie : RANSAC sur un modèle minimal, DLT normalisée sur les inliers, puis Levenberg-Marquardt sur l'erreur géométrique avec une perte robuste, et enfin lecture de la covariance si le rang le permet. Le choix dépend des données et du système linéaire.

## Sources et cartes

- [Ceres, Covariance Estimation, Introduction et Rank of the Jacobian (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html).
- [Ceres, Modeling Non-linear Least Squares, Introduction (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html).

Ces documentations étayent les solveurs, le blanchiment et le traitement des outliers. Le cas de perturbation et le diagnostic de géométrie sont des raisonnements algébriques du projet ; ils ne constituent pas une expérience publiée.

- [Eigen 5.0.1-dev, Solving linear least squares systems, Using the SVD decomposition / Using normal equations (documentation consultée le 2026-10-23 ; l'ancienne adresse eigen.tuxfamily.org redirige ici)](https://libeigen.gitlab.io/eigen/docs-nightly/group__LeastSquares.html).
- [Ceres, Solving Non-linear Least Squares, Linear Solvers et Schur complement trick (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_solving.html).
- [Chum, Werner et Matas 2005, Two-View Geometry Estimation Unaffected by a Dominant Plane, CVPR, résumé](https://dspace.cvut.cz/bitstream/10467/9495/1/2005-Two-view-geometry-estimation-unaffected-by-dominant-plane.pdf) ; [DOI](https://doi.org/10.1109/CVPR.2005.354).
- [Hartley 1997, In Defense of the Eight-Point Algorithm, IEEE TPAMI 19(6)](https://doi.org/10.1109/34.601246) : §§2.2–2.3 solution linéaire et rang 2, §3 dénormalisation et non-invariance, §4 rapport $d_1/d_8$, §5.1 normalisation isotrope, §7.3.1 gain de conditionnement. Version de l'éditeur payante ; passages lus sur une copie universitaire.
- [Zhang 1998, A Flexible New Technique for Camera Calibration, MSR-TR-98-71](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) : §3.2 raffinement Levenberg-Marquardt après solution fermée, annexe A DLT et normalisation.
- [Triggs, McLauchlan, Hartley et Fitzgibbon 2000, Bundle Adjustment — A Modern Synthesis](https://inria.hal.science/inria-00548290) : §3.1 covariance asymptotique, §3.3 moindres carrés robustifiés, §4.2 contrôle du pas, §4.3 Gauss-Newton, QR et équations normales.
- [Ceres, Modeling Non-linear Least Squares, LossFunction (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html) : conditions sur $\rho$, Huber, Cauchy, échelle $a$.
- [Ceres, Covariance Estimation, Gauge Invariance et Covariance::Options (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) : jauge, `SPARSE_QR`, `DENSE_SVD`, `min_reciprocal_condition_number`.
- [Cartes associées](../11-moindres-carres-svd.md) : CV-SVD-001 à 009.

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet. Révisions 3 et 4 : auto-revue `revue-cartes` par Agent Claude Code le 2026-10-23, corrections puis enrichissements acceptés par l'apprenant, sans validation indépendante.
