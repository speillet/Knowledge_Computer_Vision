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

**Différence de problème** : une cible fournie dans la première frame donne au tracker une information d'initialisation qu'un système multiobjet doit souvent découvrir. Le MOT doit en plus décider quels objets entrent ou sortent, empêcher plusieurs pistes de représenter le même objet et maintenir des identités malgré les interactions.

**Exemple construit** : lancer un tracker monoobjet sur une personne n'identifie pas automatiquement une deuxième personne qui entre plus tard. Lancer plusieurs instances peut aider à localiser des cibles initialisées, mais ne résout pas seul leurs collisions d'identité, leurs créations et la suppression des doublons. Définir les entrées et les événements attendus avant le choix d'architecture. Les métriques doivent également refléter ce contrat : une précision conditionnée à une initialisation manuelle favorable n'est pas directement comparable à une évaluation où toutes les cibles doivent être découvertes automatiquement.

**Erreurs bloquantes** : Supposer que suivre une boîte résout la gestion de toutes identités.
Source: [[110-tracking-association/references/113-tracking-monoobjet|Fiche complète]] ; [SiamFC, introduction et §4 : cible initialisée](https://arxiv.org/abs/1606.09549) ; [SORT, §3 : cycle de vie multiobjet](https://arxiv.org/abs/1602.00763).
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

**Boucle de dérive** : le modèle apprend l'apparence de la région qu'il croit être la cible. Si la localisation devient fausse puis sert de nouvelle supervision, l'erreur est intégrée au modèle ; les frames suivantes peuvent alors favoriser encore davantage le distracteur. Une adaptation plus rapide renforce parfois cette boucle au lieu de la corriger.

**Contrôle proposé** : enregistrer les crops utilisés pour la mise à jour, les réponses et les décisions de perte. Comparer une politique de gel sous incertitude à la politique initiale, avec mêmes séquences et initialisation. Vérifier aussi le retour de la cible après occultation. Le gel protège éventuellement le modèle mais ne garantit pas la redétection si la cible sort de la région de recherche. Ce mécanisme concerne les variantes qui mettent leur modèle à jour ; il ne doit pas être attribué indistinctement à tout tracker siamois ou à tout template fixe.

**Erreurs bloquantes** : Interpréter chaque mise à jour comme une amélioration automatique du modèle.
Source: [[110-tracking-association/references/113-tracking-monoobjet|Fiche complète]] ; Déduction sur une mise à jour erronée du modèle, par exemple le [pipeline KCF avec interpolation](https://arxiv.org/abs/1404.7584) ; [SiamFC §4](https://arxiv.org/abs/1606.09549) garde son template fixe et n’illustre pas ce mécanisme.
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-SOT-002 provenance::agent pole::C pole::D pole::E
END
