# SO(3), SE(3) et conventions de transformation — cartes

Fiche : [[10-mathematiques-estimation/references/12-rotations-se3|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-SE3-001

Objectif : composer avec des repères nommés. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-SE3-001
Question: Si $p_a=T_{ab}p_b$ et $p_b=T_{bc}p_c$ en coordonnées homogènes, quelle transformation donne p_a depuis p_c ?
Reponse: **Noyau attendu** : $T_{ac}=T_{ab}T_{bc}$ : le repère intermédiaire b s’enchaîne.

**Approfondissement** : Les translations sont exprimées dans le repère de sortie de chaque transformation ; l’ordre inverse décrit généralement autre chose.

**Erreurs bloquantes** : Supposer la composition commutative.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Fiche complète]] ; [Solà, Quaternion kinematics, §§2–4](https://arxiv.org/abs/1711.02508).
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-SE3-001 provenance::agent pole::B pole::C
END

## CV-SE3-002

Objectif : inverser une pose rigide. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-SE3-002
Question: Pour $p_c=Rp_w+t$, comment retrouver le centre caméra dans le repère monde ?
Reponse: **Noyau attendu** : $C_w=-R^Tt$ ; la pose inverse est $(R^T,-R^Tt)$.

**Approfondissement** : Le centre caméra a coordonnées nulles dans son propre repère. La translation t n’est donc pas directement sa position monde.

**Erreurs bloquantes** : Répondre simplement t ou −t sans rotation.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Fiche complète]] ; [Solà, Quaternion kinematics, §§2–4](https://arxiv.org/abs/1711.02508).
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-SE3-002 provenance::agent pole::B pole::C
END

## CV-SE3-003

Objectif : distinguer perturbations locale et globale. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-SE3-003
Question: Pourquoi deux Jacobiennes de rotation peuvent-elles différer sans qu’une des deux soit fausse ?
Reponse: **Noyau attendu** : Elles peuvent utiliser une perturbation locale à droite ou globale à gauche ; la convention change le repère de la petite rotation.

**Approfondissement** : Annoncer la convention et transformer les Jacobiennes/covariances lorsqu’on change de repère.

**Erreurs bloquantes** : Copier une Jacobienne sans vérifier où agit la perturbation.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Fiche complète]] ; [Solà, Quaternion kinematics, §§2–4](https://arxiv.org/abs/1711.02508).
Tags: cv::pilote cv::d01 famille::comparaison cv_id::CV-SE3-003 provenance::agent pole::B pole::C
END

## CV-SE3-004

Objectif : contrôler un quaternion. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-SE3-004
Question: Un quaternion normalisé suffit-il à rendre une extrinsèque compatible avec une autre bibliothèque ?
Reponse: **Noyau attendu** : Non : vérifier ordre scalaire/vectoriel, sens de transformation, axes et convention de multiplication.

**Approfondissement** : Normaliser garantit une contrainte de représentation, pas que les deux API interprètent les composantes de la même façon.

**Erreurs bloquantes** : Assimiler quatre nombres de norme un à une convention universelle.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Fiche complète]] ; [Solà, Quaternion kinematics, §§2–4](https://arxiv.org/abs/1711.02508).
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-SE3-004 provenance::agent pole::B pole::C
END
