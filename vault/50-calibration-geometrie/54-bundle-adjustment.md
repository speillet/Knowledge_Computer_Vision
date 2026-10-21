# Bundle adjustment et complément de Schur — cartes

Fiche : [[50-calibration-geometrie/references/54-bundle-adjustment|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-BA-001

Objectif : identifier les inconnues d’un BA. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-BA-001
Question: Qu’optimise un bundle adjustment et pourquoi le distinguer d’un pose graph ?
Reponse: **Noyau attendu** : Le BA optimise poses et points, éventuellement intrinsics, à partir de reprojections ; un pose graph repose sur des contraintes entre poses.

**Approfondissement** : Le niveau d’information et la sparsité diffèrent. Une reprojection faible peut encore cacher une jauge ou un biais.

**Erreurs bloquantes** : Présenter BA comme un simple lissage des positions caméra.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Fiche complète]] ; [Ceres, Schur solvers et équations blocs](https://ceres-solver.readthedocs.io/latest/nnls_solving.html).
Tags: cv::pilote cv::d05 famille::comprehension cv_id::CV-BA-001 provenance::agent pole::B pole::C
END

## CV-BA-002

Objectif : expliquer l’élimination de Schur. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-BA-002
Question: Éliminer les points avec Schur signifie-t-il les ignorer dans le BA ?
Reponse: **Noyau attendu** : Non : leur effet est transmis au système réduit des caméras, puis leurs incréments sont récupérés par substitution.

**Approfondissement** : La structure des observations rend le bloc points exploitable ; cela ne supprime ni non-linéarité ni minima locaux.

**Erreurs bloquantes** : Dire que Schur retire les observations 3D du problème.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Fiche complète]] ; [Ceres, Schur solvers et équations blocs](https://ceres-solver.readthedocs.io/latest/nnls_solving.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-BA-002 provenance::agent pole::B pole::C
END

## CV-BA-003

Objectif : ne pas masquer une jauge. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-BA-003
Question: Un BA converge à plusieurs échelles avec le même coût sur une reconstruction monoculaire. Quel contrôle manque ?
Reponse: **Noyau attendu** : Vérifier la jauge d’échelle et la présence d’une référence métrique ; fixer une convention n’est pas mesurer cette échelle.

**Approfondissement** : Évaluer les paramètres avec un alignement autorisé par la tâche ; un coût pixel peut rester invariant à une transformation globale.

**Erreurs bloquantes** : Attribuer automatiquement la multiplicité à une panne du solveur.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Fiche complète]] ; [Ceres, Covariance Estimation, Gauge Invariance, consulté le 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-BA-003 provenance::agent pole::B pole::C
END

## CV-BA-004

Objectif : contrôler un modèle trop libre. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-BA-004
Question: Pourquoi libérer davantage de coefficients de caméra peut-il réduire le coût tout en dégradant la calibration ?
Reponse: **Noyau attendu** : Des paramètres supplémentaires peuvent surajuster un jeu peu informatif ou être corrélés.

**Approfondissement** : Mesurer stabilité par sous-ensembles et erreur sur observations indépendantes ; choisir les contraintes du modèle physiquement.

**Erreurs bloquantes** : Comparer uniquement les coûts d’ajustement.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Fiche complète]] ; [Ceres, Covariance Estimation, Gauge Invariance, consulté le 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) ; effet de paramètres libres et protocole de validation : déductions du projet.
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-BA-004 provenance::agent pole::B pole::C
END
