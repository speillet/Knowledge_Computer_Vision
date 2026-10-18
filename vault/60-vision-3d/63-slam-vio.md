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

**Erreurs bloquantes** : Décrire la préintégration comme une pose absolue prête à l’emploi.
Source: [[60-vision-3d/references/63-slam-vio|Fiche complète]] ; [Forster, préintégration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf) ; [Zhang–Scaramuzza, alignement §III et Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [GTSAM, SLAM et facteurs](https://gtsam.org/tutorials/intro.html).
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

**Erreurs bloquantes** : Garantir une position globale exacte dès qu’une boucle est détectée.
Source: [[60-vision-3d/references/63-slam-vio|Fiche complète]] ; [Forster, préintégration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf) ; [Zhang–Scaramuzza, alignement §III et Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [GTSAM, SLAM et facteurs](https://gtsam.org/tutorials/intro.html).
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

**Erreurs bloquantes** : Dire que tout VIO est toujours à une échelle arbitraire comme un monoculaire visuel.
Source: [[60-vision-3d/references/63-slam-vio|Fiche complète]] ; [Forster, préintégration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf) ; [Zhang–Scaramuzza, alignement §III et Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [GTSAM, SLAM et facteurs](https://gtsam.org/tutorials/intro.html).
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

**Erreurs bloquantes** : Promettre une pose métrique fiable sans calibration temporelle ni protocole d’évaluation.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[60-vision-3d/references/63-slam-vio|Fiche complète]] ; [Forster, préintégration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf) ; [Zhang–Scaramuzza, alignement §III et Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [GTSAM, SLAM et facteurs](https://gtsam.org/tutorials/intro.html).
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

**Erreurs bloquantes** : Corriger en alignant librement l’échelle puis déclarer le VIO précis.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[60-vision-3d/references/63-slam-vio|Fiche complète]] ; [Forster, préintégration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf) ; [Zhang–Scaramuzza, alignement §III et Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [GTSAM, SLAM et facteurs](https://gtsam.org/tutorials/intro.html).
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-VIO-005 provenance::agent pole::B pole::C cas_pole::B::diagnostic
END
