# Moindres carrés, SVD et conditionnement — cartes

Fiche : [[10-mathematiques-estimation/references/11-moindres-carres-svd|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-SVD-001

Objectif : distinguer résidu et identifiabilité. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-001
Question: Une estimation géométrique a un résidu très faible mais change fortement quand les pixels sont perturbés. Quel diagnostic numérique manque ?
Reponse: **Noyau attendu** : Inspecter rang et conditionnement : une direction peut être très mal contrainte malgré un bon ajustement.

**Approfondissement** : Les petites valeurs singulières identifient les combinaisons sensibles ; tester la stabilité sur perturbations et observations réservées.

**Erreurs bloquantes** : Assimiler petit résidu et paramètres fiables.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Ceres, Covariance Estimation, Introduction et Rank of the Jacobian (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html).
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-SVD-001 provenance::agent pole::B pole::C
END

## CV-SVD-002

Objectif : choisir QR ou équations normales. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-002
Question: Pourquoi éviter de résoudre systématiquement les moindres carrés par inversion de AᵀA ?
Reponse: **Noyau attendu** : Former $A^TA$ élève au carré le conditionnement spectral à rang plein ; QR ou SVD évitent cette amplification supplémentaire.

**Approfondissement** : Le choix doit aussi considérer taille et sparsité. Une inverse explicite n’est pas nécessaire pour résoudre le système.

**Erreurs bloquantes** : Dire que toute solution mathématiquement équivalente est numériquement identique.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Eigen, Using normal equations (consulté le 2026-10-18)](https://eigen.tuxfamily.org/dox/group__LeastSquares.html).
Tags: cv::pilote cv::d01 famille::comparaison cv_id::CV-SVD-002 provenance::agent pole::B pole::C
END

## CV-SVD-003

Objectif : pondérer des résidus hétérogènes. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-003
Question: Un objectif de calibration additionne une erreur pixel et une erreur en mètres. Comment éviter un poids dicté par les unités ?
Reponse: **Noyau attendu** : Définir la covariance $C$ des résidus, supposée définie positive, puis les blanchir : avec $C=LL^T$, utiliser $L^{-1}r$. Sa norme au carré est $r^TC^{-1}r$, cohérente avec l’incertitude et les unités.

**Approfondissement** : Changer mètres en millimètres ne doit pas changer arbitrairement la solution. Vérifier modèle de bruit et corrélations.

**Erreurs bloquantes** : Additionner les valeurs brutes puis interpréter leur somme comme une vraisemblance.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Ceres, Covariance Estimation, Introduction et Rank of the Jacobian (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html).
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-SVD-003 provenance::agent pole::B pole::C
END

## CV-SVD-004

Objectif : distinguer outliers et rang déficient. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-SVD-004
Question: RANSAC trouve un consensus mais la transformation reste instable. Pourquoi cela ne contredit-il pas son rôle ?
Reponse: **Noyau attendu** : Le rejet d’outliers et l’identifiabilité sont distincts ; les inliers peuvent être presque alignés ou mal répartis.

**Approfondissement** : Inspecter couverture, valeurs singulières et extrapolation sur la zone utile.

**Erreurs bloquantes** : Supposer qu’un estimateur robuste corrige une géométrie dégénérée.
Source: [[10-mathematiques-estimation/references/11-moindres-carres-svd|Fiche complète]] ; [Ceres, Covariance Estimation, Introduction et Rank of the Jacobian (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) ; [Ceres, Modeling Non-linear Least Squares, Introduction (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html) ; diagnostic géométrique déduit par le projet.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-SVD-004 provenance::agent pole::B pole::C
END
