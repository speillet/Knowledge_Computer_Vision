# Kalman, EKF, UKF et ESKF pour la fusion — cartes

Fiche : [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-FUSION-001

Objectif : distinguer variantes de filtre. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-FUSION-001
Question: Comment distinguer EKF, UKF et ESKF sans les classer en précision absolue ?
Reponse: **Noyau attendu** : EKF linéarise, UKF utilise des sigma-points, ESKF organise état nominal et erreur locale ; leurs hypothèses et représentations diffèrent.

**Approfondissement** : Le résultat dépend du modèle, du bruit, de l’initialisation et de la cohérence temporelle ; une étiquette d’algorithme n’est pas un classement universel.

**Erreurs bloquantes** : Dire qu’UKF est toujours meilleur ou qu’ESKF supprime la non-linéarité.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Fiche complète]] ; [Solà, ESKF : injection et reset, §§5–6](https://arxiv.org/abs/1711.02508).
Tags: cv::pilote cv::d01 famille::comprehension cv_id::CV-FUSION-001 provenance::agent pole::B pole::C
END

## CV-FUSION-002

Objectif : interpréter une innovation normalisée. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FUSION-002
Question: Que mesure $\nu^TS^{-1}\nu$ dans un contrôle dinnovation ?
Reponse: **Noyau attendu** : Un écart mesure/prédiction pondéré par son incertitude, sans unité lorsque les grandeurs sont cohérentes.

**Approfondissement** : Son interprétation statistique dépend des hypothèses de bruit et du modèle ; il peut servir au gating sans prouver l’identité du bon objet.

**Erreurs bloquantes** : Confondre grand résidu pixel et grande incohérence statistique dans tous les cas.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Fiche complète]] ; [Solà, ESKF : injection et reset, §§5–6](https://arxiv.org/abs/1711.02508).
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-FUSION-002 provenance::agent pole::B pole::C
END

## CV-FUSION-003

Objectif : préserver la covariance ESKF. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FUSION-003
Question: Dans un ESKF, pourquoi mettre l’erreur moyenne à zéro après injection ne justifie-t-il pas de remettre P à zéro ?
Reponse: **Noyau attendu** : Le reset change le point de référence de l’erreur, pas l’information disponible ; transformer la covariance avec la Jacobienne adaptée.

**Approfondissement** : Une covariance nulle déclarerait une connaissance parfaite fictive et ferait mal pondérer les mesures suivantes.

**Erreurs bloquantes** : Assimiler reset de représentation et disparition de l’incertitude.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Fiche complète]] ; [Solà, ESKF : injection et reset, §§5–6](https://arxiv.org/abs/1711.02508).
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-FUSION-003 provenance::agent pole::B pole::C
END

## CV-FUSION-004

Objectif : traiter temps et données manquantes. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-FUSION-004
Question: Une caméra ralentit alors que l’IMU garde sa fréquence. Quel contrat doit respecter la fusion ?
Reponse: **Noyau attendu** : Propager selon les timestamps et le pas réel, intégrer les mesures disponibles et distinguer absence de mesure et mesure nulle.

**Approfondissement** : Vérifier délais, ordre de réception et bruit de processus lié à la durée avant de simplement régler le gain.

**Erreurs bloquantes** : Conserver implicitement un pas constant malgré des intervalles différents.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Fiche complète]] ; [Solà, ESKF : injection et reset, §§5–6](https://arxiv.org/abs/1711.02508).
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-FUSION-004 provenance::agent pole::B pole::C
END
