# SLAM, VIO, préintégration IMU et bouclage — cartes

Fiche : [[60-vision-3d/references/63-slam-vio|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-VIO-001

Objectif : situer la préintégration. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-VIO-001
Question: La préintégration IMU constitue-t-elle à elle seule un système VIO ?
Reponse: **Noyau attendu** : Non : elle résume des mesures entre keyframes en contraintes avec bruit et biais ; le système doit aussi associer la vision, initialiser et estimer les états.

**Approfondissement** : L’accéléromètre n’est pas directement une accélération monde sans gravité.

**Contrat de la préintégration** : entre deux keyframes, les nombreuses observations inertielles sont condensées dans des contraintes de mouvement avec leur incertitude et leur dépendance aux biais. Ces contraintes doivent être combinées aux observations visuelles, à un état initial et à la gravité dans des repères cohérents.

**Exemple de limite** : intégrer une accélération mesurée dans le repère IMU comme si elle était directement une accélération monde confond orientation, force spécifique et gravité. Une très bonne vision ne répare pas automatiquement cette incohérence de modèle. Un système complet doit aussi gérer horodatages, extrinsèques, biais, keyframes et pertes d'observation. La préintégration évite de reprendre naïvement toute la séquence brute à chaque calcul ; elle ne fournit pas une pose absolue ni une référence globale absente des capteurs. Valider le système demande donc trajectoire, incertitude, disponibilité et latence sur des mouvements représentatifs.

**Erreurs bloquantes** : Décrire la préintégration comme une pose absolue prête à l’emploi.
Source: [[60-vision-3d/references/63-slam-vio|Fiche complète]] ; [Forster et al., §§V–VI, équations 31–34 et VI-C](https://dellaert.github.io/files/Forster16tro.pdf).
Tags: cv::pilote cv::d06 famille::comprehension cv_id::CV-VIO-001 provenance::agent pole::B pole::C
END

## CV-VIO-002

Objectif : distinguer odométrie et boucle. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-VIO-002
Question: Que change une fermeture de boucle par rapport à l’odométrie locale ?
Reponse: **Noyau attendu** : Elle ajoute une contrainte sur un lieu revisité et peut réduire la dérive accumulée en réestimant la carte/trajectoire.

**Approfondissement** : Le candidat de lieu doit être vérifié ; une fausse boucle peut rendre le résultat pire malgré un coût faible.

**Exemple construit** : après un long trajet, reconnaître une zone déjà visitée fournit une relation entre états éloignés dans le temps. Cette relation peut redistribuer les corrections sur la trajectoire et la carte, alors qu'une odométrie locale ne revisite pas nécessairement toutes ces estimations passées.

**Deux validations distinctes** : le front-end propose un lieu sur la base d'apparence ; une vérification géométrique doit établir que les observations soutiennent la même zone. Le back-end intègre ensuite une contrainte avec son poids et ses hypothèses. Des couloirs identiques peuvent tromper la première étape et produire une déformation globale si la contrainte fausse est acceptée. Examiner les résidus des autres facteurs et une référence réservée. Une boucle correcte peut réduire une dérive relative, mais elle ne crée pas automatiquement une position mondiale absolue, une échelle mieux observée ou une absence complète d'erreur.

**Erreurs bloquantes** : Garantir une position globale exacte dès qu’une boucle est détectée.
Source: [[60-vision-3d/references/63-slam-vio|Fiche complète]] ; [GTSAM, §4.1 Loop Closure Constraints, consulté le 2026-10-20](https://gtsam.org/tutorials/intro.html) ; fausse boucle : diagnostic du projet.
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-VIO-002 provenance::agent pole::B pole::C
END

## CV-VIO-003

Objectif : identifier les jauges VIO. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-VIO-003
Question: Pourquoi yaw global et erreur d’échelle d’un VIO ne doivent-ils pas être diagnostiqués comme la même ambiguïté ?
Reponse: **Noyau attendu** : Sans référence externe, le yaw global peut rester une jauge, tandis que l’échelle métrique dépend d’une excitation et d’une calibration suffisantes et peut être estimée avec erreur.

**Approfondissement** : La translation globale reste aussi libre ; distinguer convention d’alignement et information physique réellement disponible.

**Différence conceptuelle** : une jauge transforme ensemble toutes les estimations sans changer les observations relatives. Le choix d'un nord arbitraire dans une trajectoire sans référence de cap relève de cette convention. Une échelle métrique erronée, lorsqu'elle est censée être observable avec l'IMU, traduit au contraire une estimation ou un modèle insuffisamment contraint.

**Diagnostic proposé** : annoncer les degrés d'alignement permis avant de comparer à la vérité terrain. Utiliser une transformation qui retire seulement les ambiguïtés légitimes ; laisser l'échelle libre masquerait précisément le défaut que l'on cherche à mesurer. Tester excitation, calibration et biais sur des séquences différentes aide à comprendre une mauvaise estimation d'échelle. Il faut aussi distinguer un décalage de lacet constant d'une dérive de lacet dans le temps. Le graphe final seul ne permet pas d'attribuer toutes ces différences à la même cause.

**Erreurs bloquantes** : Dire que tout VIO est toujours à une échelle arbitraire comme un monoculaire visuel.
Source: [[60-vision-3d/references/63-slam-vio|Fiche complète]] ; [Zhang–Scaramuzza 2018, §III et table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; condition d’excitation : hypothèse du modèle inertiel.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-VIO-003 provenance::agent pole::B pole::C
END

## CV-VIO-004

Objectif : concevoir un VIO pour réalité augmentée. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-VIO-004
Question: Cas B — conception : localiser un casque AR en intérieur avec caméras et IMU sous contrainte de latence. Quelle chaîne valider ?
Reponse: **Noyau attendu** : Définir repères/temps, calibrer capteurs et délais, choisir estimation causale et gestion des pertes, puis mesurer précision, dérive et latence sur mouvements représentatifs.

**Approfondissement** : Prévoir faible texture, excitation, relocalisation et référence indépendante ; annoncer les jauges et un comportement en cas d’incertitude.

**Chaîne proposée** : définir d'abord quand la pose doit être valable, dans quel repère et avec quelle ancienneté maximale. La latence d'une caméra, de son transfert et du traitement peut décaler l'observation utilisée, même si l'algorithme d'estimation est rapide. L'interface doit communiquer instant de validité et incertitude.

**Essais de transfert** : comparer mouvements lents et rapides, zones texturées et murs uniformes, puis interruption et retour des observations. Mesurer disponibilité, dérive relative et récupération avec une référence indépendante, en conservant les mêmes règles d'alignement. Une trajectoire lissée a posteriori ne valide pas une pose causale disponible à temps pour l'affichage. Ces contrôles relient qualité géométrique et usage AR ; ils constituent un protocole de conception, sans démonstration exécutée sur un casque réel.

**Erreurs bloquantes** : Promettre une pose métrique fiable sans calibration temporelle ni protocole d’évaluation.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[60-vision-3d/references/63-slam-vio|Fiche complète]] ; [Forster et al., §§V–VI, équations 31–34 et VI-C](https://dellaert.github.io/files/Forster16tro.pdf) ; [Zhang–Scaramuzza 2018, §III et table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; protocole du projet.
Tags: cv::pilote cv::d06 famille::conception cv_id::CV-VIO-004 provenance::agent pole::B pole::C cas_pole::B::conception
END

## CV-VIO-005

Objectif : diagnostiquer une dérive en couloir. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-VIO-005
Question: Cas B — diagnostic : un VIO dérive en échelle et lacet dans un couloir peu texturé. Quels contrôles départagent les causes ?
Reponse: **Noyau attendu** : Inspecter texture/parallaxe, excitation, biais et synchronisation ; vérifier fausses boucles et groupe d’alignement utilisé.

**Approfondissement** : Séparer yaw global non observable et dérive relative ; conserver une référence métrique qui ne masque pas l’erreur d’échelle. Une cause unique n’est pas identifiable au seul tracé final.

**Enquête par signatures** : une faible texture dégrade les contraintes visuelles ; une excitation insuffisante limite certaines estimations inertielles ; un retard ou un biais peut produire une erreur dépendant du mouvement. Comparer la chronologie des résidus et des pertes de suivi, plutôt que seulement la trajectoire finale.

**Ablations proposées** : contrôler les timestamps sur des mouvements instrumentés, inspecter les features et la parallaxe, puis examiner les contraintes de boucle une par une. Réserver des séquences où un seul facteur change pour distinguer les hypothèses. Un alignement avec échelle libre peut rendre la superposition visuelle convaincante tout en cachant l'erreur métrique. Rapporter donc l'erreur avant et après l'alignement permis, avec sa justification. Aucun contrôle isolé ne prouve une cause unique lorsque plusieurs défauts de capteurs et d'estimation coexistent.

**Erreurs bloquantes** : Corriger en alignant librement l’échelle puis déclarer le VIO précis.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[60-vision-3d/references/63-slam-vio|Fiche complète]] ; [Forster et al., §§V–VI, équations 31–34 et VI-C](https://dellaert.github.io/files/Forster16tro.pdf) ; [Zhang–Scaramuzza 2018, §III et table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; diagnostic du projet.
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-VIO-005 provenance::agent pole::B pole::C cas_pole::B::diagnostic
END
