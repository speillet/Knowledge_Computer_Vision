# Nuages, BEV et représentations d’occupation — cartes

Fiche : [[60-vision-3d/references/64-nuages-bev-occupation|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-BEV-001

Objectif : distinguer voxel pilier et BEV. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-BEV-001
Question: Pourquoi un pilier vertical et un voxel 3D ne conservent-ils pas la même organisation spatiale ?
Reponse: **Noyau attendu** : Le voxel discrétise aussi la hauteur ; le pilier regroupe les points d’une colonne, ensuite encodée en pseudo-image.

**Approfondissement** : Une représentation BEV peut venir d’images ou de LiDAR ; elle n’identifie pas une modalité unique.

**Lecture des représentations** : une grille de voxels discrétise les trois dimensions spatiales ; un pilier regroupe une colonne verticale avant d'en produire des features. Une pseudo-image BEV organise ensuite des informations dans le plan horizontal. Le regroupement peut encoder la hauteur sans conserver une case explicite pour chaque altitude.

**Exemple construit** : un obstacle bas et une structure en hauteur peuvent occuper les mêmes coordonnées horizontales. Leur distinction dépend de l'information verticale effectivement conservée et exploitée, pas du seul mot BEV. Définir origine, résolution en mètres, étendue et repère avant de comparer les tenseurs. Une BEV issue de caméras nécessite elle aussi des hypothèses de projection et de profondeur. Le choix de représentation est donc un compromis entre information, mémoire, calcul et interface de perception, et non une simple conversion universelle d'un nuage en image.

**Erreurs bloquantes** : Dire que toute BEV est un nuage LiDAR aplati identique.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Fiche complète]] ; [Lang et al., PointPillars, §2.1](https://arxiv.org/abs/1812.05784) ; [Li et al., BEVFormer, §§3.3–3.4](https://arxiv.org/abs/2203.17270).
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-BEV-001 provenance::agent pole::C
END

## CV-BEV-002

Objectif : préserver l’inconnu. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-BEV-002
Question: Pourquoi l’absence de retour ou de détection ne permet-elle pas de déclarer un volume libre ?
Reponse: **Noyau attendu** : La zone peut être masquée, hors portée ou jamais observée ; libre et inconnu doivent être distingués selon le modèle de mesure.

**Approfondissement** : Mesurer visibilité et raycasting ; une interface aval doit savoir quelles régions ont réellement été contraintes.

**Raisonnement d'observation** : ne pas voir un retour peut signifier absence d'obstacle, occultation par un autre objet, portée insuffisante ou matériau difficile. Ces causes n'ont pas la même implication sur l'espace. Une représentation de libre doit s'appuyer sur un modèle de mesure et une zone effectivement observée.

**Exemple construit** : derrière une palette détectée, une région sans point LiDAR n'a pas été traversée par une observation libre ; elle peut contenir un autre obstacle. Marquer cette région comme inconnue conserve une information utile pour l'interface aval. Tester la visibilité, les limites de champ et la provenance des mises à jour au lieu de remplir toute case vide par libre. L'incertitude d'une carte et les décisions de déplacement restent des problèmes supplémentaires : cette carte de perception ne certifie pas à elle seule la traversabilité ni la sécurité de tout le robot.

**Erreurs bloquantes** : Assimiler non détecté et sans obstacle.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Fiche complète]] ; [OctoMap, Full 3D model, consulté le 2026-10-20](https://octomap.github.io/).
Tags: cv::pilote cv::d06 famille::comprehension cv_id::CV-BEV-002 provenance::agent pole::C
END

## CV-BEV-003

Objectif : séparer les sens d’occupation. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-BEV-003
Question: Quelle différence entre grille d’occupation robotique et Occupancy Network de reconstruction ?
Reponse: **Noyau attendu** : La première représente une croyance sur espace observé/libre/occupé ; la seconde modélise une fonction continue d’intérieur/extérieur d’une forme.

**Approfondissement** : Une SDF représente encore un autre objet mathématique ; vérifier signes, unités et labels.

**Contrats mathématiques distincts** : une carte d'occupation pour la robotique fusionne des observations et doit définir ce qui signifie observé, libre ou inconnu. Une représentation implicite de forme cherche une frontière intérieur/extérieur dans un espace de reconstruction. Une distance signée décrit encore une autre quantité, avec une unité de longueur et une convention de signe.

**Exemple construit** : un score élevé d'intérieur d'une forme apprise n'exprime pas automatiquement la probabilité qu'un robot entre en collision à cet endroit dans son environnement actuel. Il manque contexte de visibilité, calibration du score, géométrie du robot et temps de validité. Examiner donc entrées, cibles d'apprentissage et sens de la sortie avant de relier deux modules. Des représentations peuvent être converties ou combinées, mais l'interface doit expliciter quelles informations sont conservées et lesquelles sont ajoutées par une hypothèse du système.

**Erreurs bloquantes** : Utiliser le score d’une forme implicite comme probabilité de collision calibrée.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Fiche complète]] ; [OctoMap, Full 3D model, consulté le 2026-10-20](https://octomap.github.io/) ; [Mescheder et al., Occupancy Networks, §3.1](https://arxiv.org/abs/1812.03828) ; [Park et al., DeepSDF, §3](https://arxiv.org/abs/1901.05103).
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-BEV-003 provenance::agent pole::C
END

## CV-BEV-004

Objectif : vérifier une fusion BEV. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-BEV-004
Question: Des objets BEV sont bien localisés à l’arrêt et décalés lors d’une rotation. Quelles données examiner ?
Reponse: **Noyau attendu** : Timestamps, ego-motion, deskew et transformation vers le repère BEV avant de changer l’architecture.

**Approfondissement** : Stratifier erreur par vitesse, distance et angle ; un décalage temporel peut se cacher dans des essais statiques.

**Pourquoi le mouvement révèle l'erreur** : une transformation spatiale appliquée à des observations de temps différents ne les place pas nécessairement dans la même scène instantanée. Lors d'une rotation du porteur, l'erreur apparente peut dépendre de la distance et de la direction observées. L'immobilité peut donc masquer un défaut temporel.

**Vérification construite** : comparer capteur seul, fusion statique puis fusion sur translations et rotations contrôlées. Relever instant de capture, instant de réception et temps par point ou frame, puis vérifier le sens des transformations vers la BEV. Examiner les résidus selon la vitesse angulaire. Si une correction temporelle améliore ces signatures sur une séquence réservée, cela soutient cette cause sans exclure un défaut spatial résiduel. Changer de backbone avant ce contrôle risquerait de demander au réseau d'absorber une incohérence de données plutôt que d'améliorer la perception.

**Erreurs bloquantes** : Conclure d’emblée à une capacité insuffisante du backbone.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Fiche complète]] ; [Li et al., BEVFormer, §§3.3–3.4](https://arxiv.org/abs/2203.17270) ; diagnostic temporel déduit par le projet.
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-BEV-004 provenance::agent pole::C
END

## CV-BEV-005

Objectif : concevoir une perception d’entrepôt. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-BEV-005
Question: Cas C — conception : un robot d’entrepôt utilise caméras et LiDAR. Quelle interface de perception et quel protocole construire ?
Reponse: **Noyau attendu** : Définir objets/occupation attendus, repères/temps, visibilité et incertitude ; concevoir fusion et comportement en cas de perte puis tester obstacles rares, occultations et latence.

**Approfondissement** : Une absence de boîte ne vaut pas espace libre ; séparer validation de perception et exigences de commande/sécurité du robot.

**Interface proposée** : fournir pour chaque sortie le repère, l'instant de validité, la zone observée, les classes ou états d'occupation et une indication d'incertitude exploitable. Prévoir ce qui se passe si un capteur disparaît ou si les données deviennent anciennes. Une liste de boîtes et une carte d'espace libre ne répondent pas au même besoin.

**Protocole de transfert** : construire des cas avec obstacle partiellement occulté, objet rare, matière peu réfléchissante et désynchronisation contrôlée. Mesurer erreurs par distance, zones inconnues traitées à tort comme libres et latence de bout en bout. Comparer modalités seules et fusion pour identifier l'apport réel de chacune. Les critères sont ceux de la perception et de son contrat ; la validation de la commande et de la sécurité globale demande un périmètre distinct et n'est pas déduite d'une AP moyenne.

**Erreurs bloquantes** : Garantir la sécurité globale avec une seule métrique de détection.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Fiche complète]] ; [OctoMap, Full 3D model, consulté le 2026-10-20](https://octomap.github.io/) ; protocole de conception proposé par le projet.
Tags: cv::pilote cv::d06 famille::conception cv_id::CV-BEV-005 provenance::agent pole::C cas_pole::C::conception
END
