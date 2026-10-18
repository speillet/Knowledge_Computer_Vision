# Tracking monoobjet : corrélation, siamois et MeanShift — cartes

Fiche : [[110-tracking-association/references/113-tracking-monoobjet|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-SOT-001

Objectif : distinguer SOT et MOT. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-SOT-001
Question: Pourquoi un tracker monoobjet initialisé ne remplace-t-il pas directement un MOT de toutes les personnes d’une scène ?
Reponse: **Noyau attendu** : Il part d’une cible fournie et doit la relocaliser ; MOT gère aussi détections multiples, association, créations et disparitions.

**Approfondissement** : Les entrées et évaluations diffèrent, même si certains composants de matching peuvent être partagés.

**Erreurs bloquantes** : Supposer que suivre une boîte résout la gestion de toutes identités.
Source: [[110-tracking-association/references/113-tracking-monoobjet|Fiche complète]] ; [OpenCV, Meanshift/Camshift](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html) ; [SiamFC, méthode](https://arxiv.org/abs/1606.09549).
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-SOT-001 provenance::agent pole::C pole::D pole::E
END

## CV-SOT-002

Objectif : comprendre une dérive de template. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-SOT-002
Question: Une cible occultée est remplacée par un distracteur dans le template du tracker. Quel mécanisme peut entretenir l’erreur ?
Reponse: **Noyau attendu** : La mise à jour du modèle sur une observation mal associée peut renforcer le distracteur et accroître la dérive.

**Approfondissement** : Tester gel sous incertitude, politique de perte et réinitialisation sur séquences réservées.

**Erreurs bloquantes** : Interpréter chaque mise à jour comme une amélioration automatique du modèle.
Source: [[110-tracking-association/references/113-tracking-monoobjet|Fiche complète]] ; [OpenCV, Meanshift/Camshift](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html) ; [SiamFC, méthode](https://arxiv.org/abs/1606.09549).
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-SOT-002 provenance::agent pole::C pole::D pole::E
END
