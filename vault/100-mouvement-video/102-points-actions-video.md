# Suivi de points, actions et compréhension vidéo — cartes

Fiche : [[100-mouvement-video/references/102-points-actions-video|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::100-mouvement-video

## CV-VIDEO-001

Objectif : choisir la bonne sortie vidéo. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-VIDEO-001
Question: Quelle différence entre CoTracker, classification vidéo et localisation temporelle d’action ?
Reponse: **Noyau attendu** : CoTracker suit des points avec visibilité ; la classification étiquette un clip ; la localisation estime aussi des intervalles temporels.

**Approfondissement** : Ni les cibles ni les métriques ne sont interchangeables. Nommer la version et l’accès au futur.

**Erreurs bloquantes** : Déduire les frontières d’une action d’un seul label de clip.
Source: [[100-mouvement-video/references/102-points-actions-video|Fiche complète]] ; [CoTracker, §3 : trajectoires et visibilité](https://arxiv.org/abs/2307.07635) ; [TimeSformer, résumé](https://arxiv.org/abs/2102.05095) ; distinction label/intervalles : contrat du projet.
Tags: cv::pilote cv::d10 famille::comparaison cv_id::CV-VIDEO-001 provenance::agent pole::D
END

## CV-VIDEO-002

Objectif : tester la perte d’événements courts. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-VIDEO-002
Question: Une vidéo est résumée par une frame par seconde. Pourquoi ne peut-on pas garantir la détection d’un événement de 100 ms ?
Reponse: **Noyau attendu** : L’événement peut survenir entièrement entre deux frames échantillonnées.

**Approfondissement** : Tester phases, cadence et fenêtres avec référence ; le modèle ne peut pas observer une information jamais échantillonnée directement.

**Erreurs bloquantes** : Supposer qu’un modèle plus gros garantit le rappel de tout événement court.
Source: [[100-mouvement-video/references/102-points-actions-video|Fiche complète]] ; Contre-exemple temporel construit dans la fiche : événement entre deux instants échantillonnés ; [CoTracker, §3](https://arxiv.org/abs/2307.07635) pour le contexte des entrées vidéo discrètes, sans attribution du contre-exemple à cet article.
Tags: cv::pilote cv::d10 famille::raisonnement cv_id::CV-VIDEO-002 provenance::agent pole::D
END

## CV-VIDEO-003

Objectif : contrôler causalité et délai. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-VIDEO-003
Question: Un tracker de points utilise une fenêtre et des frames futures. Peut-on comparer sa sortie directement à un modèle causal sans délai ?
Reponse: **Noyau attendu** : Non sans préciser les informations disponibles et le délai de sortie.

**Approfondissement** : Évaluer même fenêtre, timestamps, politique de visibilité et temps de décision.

**Erreurs bloquantes** : Confondre mot online et absence de latence ou de futur dans toute implémentation.
Source: [[100-mouvement-video/references/102-points-actions-video|Fiche complète]] ; [CoTracker, §3 : fenêtres glissantes](https://arxiv.org/abs/2307.07635) ; [CoTracker3, introduction : variantes online/offline](https://arxiv.org/abs/2410.11831) ; comparaison de latence proposée par le projet.
Tags: cv::pilote cv::d10 famille::evaluation cv_id::CV-VIDEO-003 provenance::agent pole::D
END

## CV-VIDEO-004

Objectif : vérifier l’utilisation de l’ordre temporel. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-VIDEO-004
Question: Un classifieur vidéo reconnaît l’action même après permutation des frames. Que tester avant d’affirmer qu’il comprend la dynamique ?
Reponse: **Noyau attendu** : Comparer à une baseline image/contexte, contrôler les labels et les actions qui exigent réellement l’ordre.

**Approfondissement** : La scène ou un objet peut suffire au score ; utiliser des cas où l’ordre distingue deux événements.

**Erreurs bloquantes** : Déduire une compréhension temporelle d’une accuracy globale seule.
Source: [[100-mouvement-video/references/102-points-actions-video|Fiche complète]] ; Test contrôlé proposé par le projet ; [TimeSformer, résumé et architecture](https://arxiv.org/abs/2102.05095) pour le mécanisme d’attention temporelle.
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-VIDEO-004 provenance::agent pole::D
END
