# Graphes de facteurs et optimisation incrémentale — cartes

Fiche : [[10-mathematiques-estimation/references/14-graphes-facteurs|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-FACTEURS-001

Objectif : séparer représentation et solveur. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-FACTEURS-001
Question: Un factor graph est-il déjà un algorithme de SLAM ?
Reponse: **Noyau attendu** : Non : il représente variables et facteurs ; il faut aussi observations, associations, modèles, initialisation et stratégie d’inférence.

**Approfondissement** : GTSAM et iSAM2 apportent des outils et algorithmes, sans rendre corrects des facteurs mal définis.

**Erreurs bloquantes** : Déduire une trajectoire fiable de la seule présence d’un graphe.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Fiche complète]] ; [Dellaert, Factor Graphs and GTSAM, §§2.3–2.4, 4.1 et 7 (consulté le 2026-10-18)](https://gtsam.org/tutorials/intro.html) ; [Kaess et al. 2012, iSAM2, §2 Gaussian Case et §4](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf).
Tags: cv::pilote cv::d01 famille::comprehension cv_id::CV-FACTEURS-001 provenance::agent pole::B pole::C
END

## CV-FACTEURS-002

Objectif : expliquer une jauge. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FACTEURS-002
Question: Pourquoi une optimisation de poses relatives peut-elle exiger un ancrage malgré des observations nombreuses ?
Reponse: **Noyau attendu** : Les observations relatives ne définissent pas nécessairement le repère global ; des transformations communes peuvent laisser les résidus inchangés.

**Approfondissement** : Fixer une jauge enlève une ambiguïté de représentation, sans ajouter une mesure absolue. Le groupe autorisé dépend des capteurs.

**Erreurs bloquantes** : Interpréter un prior arbitraire comme une preuve de précision globale.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Fiche complète]] ; [Ceres, Covariance Estimation, Gauge Invariance (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html#gauge-invariance).
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-FACTEURS-002 provenance::agent pole::B pole::C
END

## CV-FACTEURS-003

Objectif : vérifier une fermeture de boucle. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FACTEURS-003
Question: Après loop closure, le coût diminue mais la carte se plie de façon incohérente. Que tester ?
Reponse: **Noyau attendu** : Vérifier l’association de lieux, la transformation relative, les repères et le poids du facteur de boucle.

**Approfondissement** : Une fausse contrainte forte peut être satisfaite au détriment du reste. Conserver vérification géométrique et observations indépendantes.

**Erreurs bloquantes** : Augmenter les itérations sans inspecter le facteur ajouté.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Fiche complète]] ; [Dellaert, Factor Graphs and GTSAM, §§2.3–2.4, 4.1 et 7 (consulté le 2026-10-18)](https://gtsam.org/tutorials/intro.html) ; scénario de faux facteur déduit par le projet.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-FACTEURS-003 provenance::agent pole::B pole::C
END
