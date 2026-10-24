# Calibration multicapteurs, hand-eye et temps — cartes

Fiche : [[50-calibration-geometrie/references/55-calibration-multicapteurs|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-MULTICALIB-001

Objectif : interpréter hand-eye. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-MULTICALIB-001
Question: Pourquoi écrire $AX=XB$ ne suffit-il pas à appliquer une calibration hand-eye ?
Reponse: **Noyau attendu** : Il faut définir les repères, les mouvements relatifs A/B, leur sens et la transformation inconnue X.

**Approfondissement** : Vérifier une chaîne de transformations sur un point et des mouvements réservés ; des conventions différentes donnent des équations différentes.

**Dérivation par chaîne** : en eye-in-hand avec une mire fixe, la composition outil→base, caméra→outil puis mire→caméra doit donner la même pose mire→base pour chaque acquisition. L'égalité de ces compositions conduit à des mouvements relatifs de part et d'autre de l'extrinsèque inconnue. Le sens des produits n'est pas libre : il découle des repères adjacents.

**Test construit** : prendre une pose connue, transformer un point de mire jusqu'à la base, puis vérifier l'inverse de la chaîne. Répéter avec une rotation non triviale et des translations non nulles dans des unités communes. Un test identité peut laisser des inversions invisibles. Cette validation d'interface précède le réglage du solveur ; si elle échoue, ajouter des données ou changer la méthode d'optimisation traite un autre problème que l'erreur de convention.

**Erreurs bloquantes** : Copier les matrices d’une API sans vérifier leur sens.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Fiche complète]] ; [OpenCV 4.13.0, calibrateHandEye, équations eye-in-hand et note sur les axes](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-MULTICALIB-001 provenance::agent pole::B pole::C pole::E
END

## CV-MULTICALIB-002

Objectif : évaluer des mouvements informatifs. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-MULTICALIB-002
Question: De nombreuses poses robot sur un même axe donnent une extrinsèque instable. Que changer ?
Reponse: **Noyau attendu** : Examiner l’observabilité et varier les rotations/positions qui contraignent les composantes manquantes.

**Approfondissement** : Comparer stabilité et validation sur une autre trajectoire, sans considérer le nombre brut de poses comme preuve.

**Intuition d'observabilité** : répéter un mouvement similaire ajoute du bruit moyen en moins, mais pas nécessairement de nouvelles directions de contrainte. Certaines composantes de l'extrinsèque peuvent alors varier fortement sans beaucoup changer les équations observées. Toutes les paires construites à partir des mêmes poses restent en outre corrélées.

**Acquisition proposée** : comparer, à nombre de poses comparable, une trajectoire à axe unique et une trajectoire avec axes de rotation variés, dans les limites physiques du dispositif. Garder qualité de mire et synchronisation contrôlées, puis vérifier la chaîne sur une trajectoire réservée. Si l'instabilité persiste, rechercher aussi une erreur de timestamp ou de pose robot. Une diversité de mouvements est une source d'information ; elle ne garantit pas que chaque autre hypothèse de calibration soit correcte. Le critère final reste la stabilité et l'erreur utile dans le volume d'exploitation.

**Erreurs bloquantes** : Répondre seulement « plus d’images » sans diversité de mouvement.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Fiche complète]] ; [OpenCV 4.13.0, calibrateHandEye, équations eye-in-hand et note sur les axes](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-MULTICALIB-002 provenance::agent pole::B pole::C pole::E
END

## CV-MULTICALIB-003

Objectif : séparer intrinsèques extrinsèques et temps. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-MULTICALIB-003
Question: Pourquoi une faible reprojection intrinsèque ne valide-t-elle pas une fusion caméra–LiDAR en mouvement ?
Reponse: **Noyau attendu** : Elle ne teste pas à elle seule l’extrinsèque entre capteurs, leur offset temporel ou la déformation du scan.

**Approfondissement** : Valider séparément puis conjointement sur mouvements et scènes adaptés.

**Séparer les contrats** : l'intrinsèque relie rayons et pixels d'une caméra. L'extrinsèque relie les axes des capteurs. Le temps détermine quelles positions de la scène et du porteur sont comparées. Une fusion peut respecter le premier contrat et violer les deux autres, particulièrement pendant une rotation.

**Enquête construite** : commencer par des observations immobiles pour contrôler une partie de la géométrie, puis comparer translation et rotation en inspectant temps par point du LiDAR et instant de capture caméra. Corriger séparément les offsets, le deskew et les transformations pour mesurer leur effet. Une translation ajustée pour une seule vitesse peut masquer un retard sans généraliser. Réserver une séquence avec d'autres mouvements pour la validation finale. Une bonne reprojection caméra reste utile, mais elle ne teste ni la simultanéité des mesures ni toute la projection d'un nuage vers l'image.

**Erreurs bloquantes** : Assimiler qualité d’une calibration caméra et qualité complète de fusion.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Fiche complète]] ; [Zhang–Singh 2014, LOAM, §§II, IV et V-B](https://www.roboticsproceedings.org/rss10/p07.pdf) ; comparaison intrinsèques/extrinsèques/temps déduite par le projet.
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-MULTICALIB-003 provenance::agent pole::B pole::C pole::E
END
