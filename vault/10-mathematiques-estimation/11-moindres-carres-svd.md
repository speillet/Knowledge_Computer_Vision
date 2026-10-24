# Moindres carrés, SVD et conditionnement — cartes

Fiche : [[10-mathematiques-estimation/references/11-moindres-carres-svd|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-SVD-001

Objectif : distinguer résidu et identifiabilité. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-001
Question: Une estimation linéaire $\hat x=\arg\min_x\|Ax-b\|_2$ a un résidu très faible, mais $\hat x$ change fortement quand les mesures $b$ sont légèrement perturbées. Avec la SVD fine $A=U\Sigma V^T$ de rang colonne plein, quelle relation explique qu'un bon ajustement ne garantisse pas des paramètres fiables ?
Reponse: **Noyau attendu** : $\delta\hat x=V\Sigma^{-1}U^T\delta b=\sum_i\frac{u_i^T\delta b}{\sigma_i}v_i$ : la perturbation est amplifiée par $1/\sigma_i$ le long du vecteur singulier droit $v_i$. Réciproquement, déplacer $x$ de $t\,v_i$ ne change $Ax$ que de $|t|\,\sigma_i$ en norme : si $\sigma_i$ est petite, les paramètres bougent sans que le résidu change. Un petit résidu ne prouve donc pas l'identifiabilité ; il faut inspecter les petites valeurs singulières et $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$.

**Approfondissement** : cas exécuté par le projet : deux colonnes qui diffèrent de $10^{-3}$ donnent $\sigma_2\approx10^{-3}$ ; perturber $b$ de $10^{-3}$ selon $u_2$ déplace $\hat x$ d'une norme 1 selon $v_2\approx(1,-1)/\sqrt2$, résidu toujours nul. Ceres montre le même effet sur la covariance : $(J^TJ)^{-1}$ atteint $\pm2\cdot10^{14}$ pour un jacobien presque singulier. $\kappa_2$ dépend des unités des colonnes : mettre les paramètres à l'échelle avant de conclure.

**Erreurs bloquantes** : assimiler petit résidu et paramètres fiables ; attribuer la sensibilité aux grandes valeurs singulières ; confondre les directions de paramètres $v_i$ et de mesures $u_i$.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Ceres, Covariance Estimation, Rank of the Jacobian et `min_reciprocal_condition_number` (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) ; relation dérivée de la SVD par le projet.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-SVD-001 provenance::agent pole::B pole::C
END

## CV-SVD-002

Objectif : choisir QR ou équations normales. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-002
Question: Pour résoudre $\min_x\|Ax-b\|_2$ avec $A$ de rang colonne plein, quand préférer une factorisation QR ou SVD de $A$, et quand les équations normales $A^TAx=A^Tb$ résolues par Cholesky restent-elles un choix défendable ?
Reponse: **Noyau attendu** : former $A^TA$ élève le conditionnement au carré, $\kappa_2(A^TA)=\kappa_2(A)^2$, et fait perdre environ deux fois plus de chiffres significatifs. QR, ou SVD plus précise mais plus lente et utile pour diagnostiquer le rang, s'impose dès que $A$ est mal conditionnée, même modérément. Les équations normales sont en général les plus rapides, surtout pour $A$ haute et étroite : elles restent défendables si $A$ est bien conditionnée après mise à l'échelle, et les grands problèmes creux comme le bundle adjustment les exploitent par Cholesky creux et complément de Schur.

**Approfondissement** : ordre de grandeur : avec $\kappa_2(A)=10^6$, environ 6 des 16 chiffres de la double précision sont menacés avec QR, 12 avec les équations normales. Ceres conseille `DENSE_QR` pour les petits problèmes denses et `SPARSE_SCHUR` pour les BA à milliers de caméras. Factoriser puis résoudre : l'inverse explicite est inutile.

**Lecture pour un projet** : choisir le solveur après avoir examiné rang, échelles et structure creuse. Un temps de résolution inférieur ne compense pas des paramètres devenus inutilisables. Comparer aussi la stabilité lorsque les observations sont légèrement perturbées, avec le même objectif et les mêmes unités.

**Erreurs bloquantes** : dire que deux formulations mathématiquement équivalentes sont numériquement identiques ; exclure les équations normales en toute circonstance, y compris pour un BA creux.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Triggs et al. 2000, §4.3, QR et équations normales](https://inria.hal.science/inria-00548290) ; [Eigen 5.0.1-dev, Solving linear least squares systems, Using normal equations (consulté le 2026-10-23)](https://libeigen.gitlab.io/eigen/docs-nightly/group__LeastSquares.html) ; [Ceres, Solving Non-linear Least Squares, Linear Solvers et Schur complement trick (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_solving.html).
Tags: cv::pilote cv::d01 famille::comparaison cv_id::CV-SVD-002 provenance::agent pole::B pole::C
END

## CV-SVD-003

Objectif : pondérer des résidus hétérogènes. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-003
Question: Un objectif de calibration additionne une erreur pixel et une erreur en mètres. Comment éviter un poids dicté par les unités ?
Reponse: **Noyau attendu** : Définir la covariance $C$ des résidus, supposée définie positive, puis les blanchir : avec $C=LL^T$, utiliser $L^{-1}r$. Sa norme au carré est $r^TC^{-1}r$, sans dimension et pondérée par l’incertitude.

**Approfondissement** : Changer mètres en millimètres ne doit pas changer arbitrairement la solution. Exemple calculé par le projet : $r_{px}=0{,}8$ px avec $\sigma_{px}=0{,}5$ px, $r=3$ mm avec $\sigma=2$ mm. La somme brute des carrés vaut 0,64 en mètres et 9,64 en millimètres : l'unité choisit quel terme domine. La somme blanchie vaut 4,81 dans les deux cas. Vérifier modèle de bruit et corrélations ; une perte robuste éventuelle s'applique ensuite au résidu blanchi.

**Interprétation** : le blanchiment exprime chaque écart relativement au bruit que le modèle lui attribue. Un résidu de deux pixels peut être banal avec une incertitude de dix pixels et surprenant avec une incertitude de 0,1 pixel. Les termes hors diagonale de $C$ comptent si les observations sont corrélées : diviser chaque composante par son écart-type n'est alors pas un blanchiment complet. Une pondération choisie pour obtenir une belle solution ne devient pas automatiquement un modèle de bruit justifié.

**Erreurs bloquantes** : Additionner les valeurs brutes puis interpréter leur somme comme une vraisemblance.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Ceres, Covariance Estimation, Introduction et Rank of the Jacobian (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html).
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-SVD-003 provenance::agent pole::B pole::C
END

## CV-SVD-004

Objectif : distinguer outliers et rang déficient. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-004
Question: Après RANSAC, une transformation estimée sur un large consensus change notablement d'une exécution ou d'un sous-ensemble d'inliers à l'autre. Quels contrôles départagent des outliers restés parmi les inliers et une configuration presque dégénérée ?
Reponse: **Noyau attendu** : des outliers résiduels se voient dans les résidus des inliers, avec une queue près du seuil ; retirer ces points ou resserrer le seuil stabilise l'estimation. Une quasi-dégénérescence se voit dans la géométrie des inliers, alignés, concentrés ou presque coplanaires selon le modèle, et dans une petite valeur singulière après normalisation : la solution varie selon une même direction même sur des inliers propres. Le rejet d'outliers ne crée pas les contraintes manquantes : seules une meilleure couverture ou un modèle plus contraint corrigent ce second cas.

**Approfondissement** : cas publié : avec un plan dominant, un échantillon de sept correspondances dont au moins cinq vérifient une homographie donne une géométrie épipolaire compatible avec tout le plan ; d'où un large consensus pour une matrice fondamentale mal déterminée (Chum, Werner et Matas 2005). Pour un système homogène $Lh=0$, c'est l'avant-dernière valeur singulière qui doit rester nettement non nulle.

**Contrôle proposé** : conserver les mêmes observations, réajuster sur plusieurs sous-ensembles et visualiser la direction de variation des paramètres. Comparer ensuite une meilleure répartition spatiale plutôt qu'un simple quota plus élevé. Les deux causes peuvent coexister : corriger les outliers ne valide pas encore la géométrie restante.

**Erreurs bloquantes** : supposer qu'un estimateur robuste corrige une géométrie dégénérée ; conclure à des outliers dès qu'une solution est instable.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Chum, Werner et Matas 2005, résumé et théorème du plan dominant](https://dspace.cvut.cz/bitstream/10467/9495/1/2005-Two-view-geometry-estimation-unaffected-by-dominant-plane.pdf) ; [Hartley 1997, §4, rôle de $d_1/d_8$](https://doi.org/10.1109/34.601246) ; [Ceres, Covariance Estimation, Rank of the Jacobian (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) ; tests discriminants proposés par le projet.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-SVD-004 provenance::agent pole::B pole::C
END

## CV-SVD-005

Objectif : dérouler une estimation DLT. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-005
Question: Décris l'estimation linéaire (DLT) d'une homographie $H$ à partir de $n\ge4$ correspondances de points : quel système construit-on, quelle contrainte impose-t-on et quel vecteur retient-on comme solution ?
Reponse: **Noyau attendu** : chaque correspondance fournit deux équations linéaires homogènes en les neuf coefficients $h$ de $H$ ; on les empile en $Lh=0$, avec $L\in\mathbb R^{2n\times9}$. $H$ n'étant défini qu'à un facteur près, on minimise $\|Lh\|$ sous $\|h\|=1$, ce qui exclut $h=0$. La solution est le vecteur singulier droit de $L$ associé à la plus petite valeur singulière, c'est-à-dire le vecteur propre de $L^TL$ de plus petite valeur propre.

**Approfondissement** : ce coût algébrique n'a pas de sens physique : Zhang s'en sert pour initialiser, puis minimise l'erreur de reprojection par Levenberg-Marquardt. Pour $F$, chaque correspondance donne une équation et il en faut au moins huit ; on impose ensuite le rang 2 en annulant la plus petite valeur singulière de $F$. Normaliser les coordonnées avant de construire $L$.

**Interprétation du minimum** : la contrainte de norme élimine la solution triviale, mais ne donne pas une unité physique au résidu algébrique. Une bonne initialisation linéaire doit donc être contrôlée dans l'espace où le produit est utilisé, par exemple avec des distances de reprojection sur des points réservés.

**Erreurs bloquantes** : retenir le vecteur de la plus grande valeur singulière ; résoudre $Lh=0$ par moindres carrés sans contrainte ; croire que la DLT minimise l'erreur de reprojection.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Zhang 1998, MSR-TR-98-71, §3.2 et annexe A](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) ; [Hartley 1997, §§2.2–2.3](https://doi.org/10.1109/34.601246).
Tags: cv::pilote cv::d01 famille::algorithme cv_id::CV-SVD-005 provenance::agent pole::B pole::C
END

## CV-SVD-006

Objectif : relier normalisation et conditionnement de la DLT. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-006
Question: Pourquoi une DLT construite sur des coordonnées pixel brutes, de l'ordre de $10^3$, est-elle mal conditionnée, et quelle normalisation proposée par Hartley y remédie ?
Reponse: **Noyau attendu** : une ligne de la matrice mélange des termes de l'ordre de 1, des coordonnées de l'ordre de $10^3$ et des produits de l'ordre de $10^6$ ; les entrées de $L^TL$ s'étalent sur une douzaine d'ordres de grandeur et le vecteur solution devient très sensible au bruit. Pour chaque image séparément, translater les points pour amener leur centroïde à l'origine, puis les mettre à l'échelle de façon isotrope pour une distance moyenne de $\sqrt2$ ; estimer $\hat H$ sur ces points, puis dénormaliser : $H=T'^{-1}\hat HT$. La solution algébrique n'étant pas invariante à ces transformations, la normalisation change l'estimateur, pas seulement les arrondis.

**Approfondissement** : Hartley mesure un conditionnement amélioré d'environ $10^8$ sur la paire « house ». Cas exécuté par le projet : avec 50 points répartis sur 1920×1080, $\sigma_1/\sigma_8$ passe de $8\cdot10^6$ à 4 mais l'erreur reste vers 0,2 px ; avec 20 points dans un carré de 200 px, l'erreur médiane sur l'image passe d'environ 1000 px à 28 px. La normalisation ne crée pas la couverture manquante. Pour $F$ : $F=T'^T\hat FT$.

**Erreurs bloquantes** : oublier la dénormalisation ; présenter la normalisation comme un simple arrondi sans effet sur la solution ; croire qu'elle compense une mauvaise répartition des points.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Hartley 1997, §§3–5 et 7.3.1](https://doi.org/10.1109/34.601246) ; [Zhang 1998, annexe A](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) ; calcul exécuté par le projet.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-SVD-006 provenance::agent pole::B pole::C
END

## CV-SVD-007

Objectif : situer Gauss-Newton et Levenberg-Marquardt. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-007
Question: Pour raffiner une calibration en minimisant une erreur de reprojection non linéaire, que calcule une itération de Gauss-Newton, comment Levenberg-Marquardt la rend-elle plus sûre, et quelle condition ces deux méthodes exigent-elles ?
Reponse: **Noyau attendu** : Gauss-Newton linéarise les résidus autour de l'estimée courante, $r(x+\delta)\approx r(x)+J\delta$, et résout le moindres carrés linéaire $J^TJ\delta=-J^Tr$ : il approche le hessien par $J^TJ$, ce qui suppose des résidus petits ou un modèle presque linéaire. Levenberg-Marquardt amortit le pas, $(J^TJ+\lambda D^TD)\delta=-J^Tr$ : $\lambda$ augmente quand la baisse prédite du coût ne se réalise pas, ce qui raccourcit le pas vers la descente de gradient, et diminue sinon vers Gauss-Newton. Les deux sont locales : elles exigent une initialisation proche, en général une solution linéaire comme la DLT ou la solution fermée de Zhang.

**Approfondissement** : Ceres présente LM comme une région de confiance de rayon $\mu$, doublé si la baisse réelle suit la prédiction et divisé par deux sinon ; $D$ est souvent la racine de la diagonale de $J^TJ$. Le système se résout comme en CV-SVD-002, par QR, Cholesky ou Schur. Quand les termes négligés ne le sont pas, Gauss-Newton converge beaucoup plus lentement.

**Erreurs bloquantes** : croire que LM trouve le minimum global quelle que soit l'initialisation ; confondre amortissement et perte robuste ; dire que Gauss-Newton utilise le hessien exact.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Triggs et al. 2000, §§4.2–4.3](https://inria.hal.science/inria-00548290) ; [Ceres, Solving Non-linear Least Squares, Trust Region Methods et Levenberg-Marquardt (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_solving.html) ; [Zhang 1998, §3.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf).
Tags: cv::pilote cv::d01 famille::comprehension cv_id::CV-SVD-007 provenance::agent pole::B pole::C
END

## CV-SVD-008

Objectif : régler l'échelle d'une perte robuste. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-008
Question: Dans Ceres, on ajoute une `HuberLoss(a)` ou une `CauchyLoss(a)` à des blocs de résidus de reprojection. Sur quelle quantité agit la perte et comment choisir $a$, selon que les résidus sont en pixels ou blanchis ?
Reponse: **Noyau attendu** : la perte $\rho$ s'applique à $s=\|f\|^2$, la norme au carré du bloc de résidus ; elle imite le coût quadratique pour les petits résidus et réduit le poids des grands. L'échelle $a$ a l'unité de la norme du résidu, $\rho(s,a)=a^2\rho(s/a^2)$ : en pixels pour des résidus en pixels, en écarts-types pour des résidus blanchis. On la choisit d'après le bruit attendu des inliers.

**Approfondissement** : Huber reste quadratique jusqu'à $\|f\|=a$ puis croît linéairement ; Cauchy vaut $a^2\log(1+s/a^2)$. Le poids $\rho'(s)$ décroît en $1/\|f\|$ pour Huber et en $1/\|f\|^2$ pour Cauchy. Exemple du projet, avec un bruit d'inliers de 0,5 px : $a=1$ en pixels commence à réduire les résidus au-delà de $2\sigma$, $a=1$ en blanchi dès $1\sigma$. La perte raffine autour d'une initialisation : elle ne remplace pas RANSAC face à de nombreux outliers, ni un modèle juste quand toutes les observations sont affectées.

**Erreurs bloquantes** : exprimer $a$ comme un seuil sur la norme au carré ; croire qu'une perte robuste rejette les outliers quelle que soit l'initialisation.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Ceres, Modeling Non-linear Least Squares, LossFunction (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html) ; [Triggs et al. 2000, §3.3](https://inria.hal.science/inria-00548290) ; exemple chiffré du projet.
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-SVD-008 provenance::agent pole::B pole::C
END

## CV-SVD-009

Objectif : interpréter une covariance d'estimation. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-009
Question: Après un ajustement par moindres carrés non linéaires, on lit l'incertitude des paramètres dans $(J^TJ)^{-1}$, avec $J$ le jacobien à la solution. Sous quelles conditions cette lecture est-elle valable, et que ne mesure-t-elle pas ?
Reponse: **Noyau attendu** : il faut des résidus blanchis, de covariance identité, et un $J$ de rang colonne plein ; la matrice obtenue est alors la dispersion locale de l'estimée, qui n'approche sa covariance qu'asymptotiquement. Si $J$ est déficient en rang (jauge, paramètre non observable), $J^TJ$ n'est pas inversible : fixer la jauge, reparamétrer ou utiliser une pseudo-inverse. Elle ne mesure ni un biais de modèle, comme une distorsion mal modélisée, ni l'effet d'outliers : elle suppose modèle et bruit corrects.

**Approfondissement** : Triggs et al. jugent l'approximation asymptotique bien moins sûre pour les petits problèmes de géométrie et les réseaux faibles. Par défaut, Ceres échoue sur un jacobien déficient (`Compute()` renvoie faux) ; `DENSE_SVD` calcule une pseudo-inverse pour les problèmes petits ou moyens. Un jacobien presque singulier donne des variances absurdes, d'où `min_reciprocal_condition_number`. Les termes hors diagonale révèlent des paramètres que les données ne séparent pas (CV-ZHANG-006).

**Décision proposée** : confronter les intervalles annoncés à des répétitions ou des perturbations contrôlées, en conservant jauge et unités. Une faible dispersion autour d'une solution biaisée reste compatible avec une mauvaise précision. Séparer donc incertitude locale, variation entre acquisitions et adéquation du modèle physique.

**Erreurs bloquantes** : lire $(J^TJ)^{-1}$ sans blanchiment ni contrôle du rang ; prendre une faible variance pour une preuve d'exactitude du modèle.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Ceres, Covariance Estimation, Introduction, Gauge Invariance, Rank of the Jacobian et Covariance::Options (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) ; [Triggs et al. 2000, §3.1](https://inria.hal.science/inria-00548290).
Tags: cv::pilote cv::d01 famille::evaluation cv_id::CV-SVD-009 provenance::agent pole::B pole::C
END
