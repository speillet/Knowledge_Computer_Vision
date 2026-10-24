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

**Contrats à distinguer** : une trajectoire de point répond à « où se trouve cette observation au fil du temps ? ». Un label de clip répond à « quelle action caractérise cet extrait ? ». Un intervalle temporel ajoute une estimation de début et de fin. Une sortie peut être correcte pour l'un de ces contrats et insuffisante pour un autre.

**Exemple construit** : reconnaître qu'une personne s'assoit dans un clip ne fournit pas nécessairement l'instant de contact avec la chaise. Suivre un point de vêtement ne fournit pas non plus automatiquement la classe d'action. Définir la sortie utile avant de choisir architecture et métrique : erreur de point, visibilité, classification ou frontières temporelles. Préciser les frames accessibles au modèle et le délai de décision. Une performance obtenue avec le clip complet ne valide pas une alarme devant se déclencher avant la fin de l'événement.

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

**Exemple temporel** : si les observations sont prises aux instants 0 s et 1 s, un événement présent uniquement de 0,35 à 0,45 s ne figure dans aucune frame retenue. Il peut éventuellement laisser des indices avant ou après, mais ce serait une autre hypothèse que l'observation directe de l'événement.

**Conception proposée** : fixer la durée minimale d'événement utile et la tolérance de délai, puis comparer plusieurs phases d'échantillonnage, pas seulement une vidéo favorable. Vérifier si une augmentation de cadence, une fenêtre ou un déclenchement événementiel apporte l'information nécessaire. La mémoire et le coût augmentent avec les observations traitées. Un modèle temporel plus puissant peut exploiter les données disponibles ; il ne garantit pas de reconstruire un événement invisible sans hypothèse supplémentaire. Le protocole doit donc séparer événement observé, événement inféré et événement manqué.

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

**Équité de la comparaison** : une frame future peut aider à résoudre une occultation ou un mouvement ambigu. Cette information n'existe pas encore pour un système qui doit répondre immédiatement. Une méthode offline ou fenêtrée peut donc accomplir une tâche plus informée, au prix d'un délai.

**Protocole construit** : pour chaque sortie, noter l'instant du point estimé, la dernière frame consommée et l'instant de disponibilité. Comparer précision et délai avec une politique identique d'observations, ou présenter explicitement la différence comme un compromis. Inclure attente de fenêtre, transfert et calcul dans la latence. Le terme online peut signifier traitement progressif d'un flux sans signifier délai nul. Une bonne trajectoire calculée après l'événement n'est pas équivalente à une localisation suffisamment tôt pour piloter un autre module. Cette distinction s'applique aussi aux évaluations de VIO, lissage et détection d'actions.

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

**Hypothèse alternative** : la présence d'un outil, d'un décor ou d'une posture caractéristique peut suffire à prédire le label du clip. La permutation des frames préserve une grande partie de ces indices. Une accuracy élevée ne permet donc pas, seule, d'attribuer la décision à l'ordre temporel.

**Ablation proposée** : comparer le modèle à une agrégation de prédictions image, puis sélectionner des cas où les mêmes états visuels dans un ordre différent correspondent à des événements différents. Contrôler échantillonnage, labels, arrière-plan et fuite entre clips voisins. Si la performance reste identique sur des tâches réellement sensibles à l'ordre, examiner les informations utilisées. Une chute après permutation soutient une dépendance temporelle, mais ne prouve pas toute forme de compréhension causale. Le raisonnement doit rester lié aux tâches et aux contrôles effectués, pas au seul nom de l'architecture.

**Erreurs bloquantes** : Déduire une compréhension temporelle d’une accuracy globale seule.
Source: [[100-mouvement-video/references/102-points-actions-video|Fiche complète]] ; Test contrôlé proposé par le projet ; [TimeSformer, résumé et architecture](https://arxiv.org/abs/2102.05095) pour le mécanisme d’attention temporelle.
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-VIDEO-004 provenance::agent pole::D
END
