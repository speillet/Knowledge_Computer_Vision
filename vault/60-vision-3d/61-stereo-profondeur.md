# Stéréo rectifiée, SGM et profondeur — cartes

Fiche : [[60-vision-3d/references/61-stereo-profondeur|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-STEREO-001

Objectif : calculer une profondeur rectifiée. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-STEREO-001
Question: En stéréo rectifiée horizontale avec points principaux de même abscisse, pour f=1000 px, baseline 0,2 m et disparité gauche−droite 20 px, quelle profondeur ?
Reponse: **Noyau attendu** : 10 m par $Z=fB/d$.

**Approfondissement** : À 10 px de disparité, on obtiendrait 20 m. La formule suppose une géométrie rectifiée compatible et une disparité valide ; f et d doivent être dans la même unité pixel.

**Erreurs bloquantes** : Utiliser une baseline en millimètres et annoncer directement des mètres.
Source: [[60-vision-3d/references/61-stereo-profondeur|Fiche complète]] ; [OpenCV 4.13.0, stereoRectify et reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; calcul analytique du projet.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-STEREO-001 provenance::agent pole::B pole::C
END

## CV-STEREO-002

Objectif : interpréter l’incertitude de profondeur. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-STEREO-002
Question: Pourquoi la précision de profondeur stéréo se dégrade-t-elle souvent à longue distance ?
Reponse: **Noyau attendu** : La sensibilité à la disparité croît comme $fB/d^2$ ; de petites erreurs de d deviennent de grandes erreurs de Z quand d est faible.

**Approfondissement** : Comparer une erreur de reprojection et une erreur métrique sur distances connues.

**Erreurs bloquantes** : Supposer un bruit de profondeur constant pour toute distance.
Source: [[60-vision-3d/references/61-stereo-profondeur|Fiche complète]] ; [OpenCV 4.13.0, stereoRectify et reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; dérivation de Z=fB/d, à f et B fixés.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-STEREO-002 provenance::agent pole::B pole::C
END

## CV-STEREO-003

Objectif : décoder une disparité fixe. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-STEREO-003
Question: Une reconstruction SGBM a une échelle fausse malgré une bonne calibration. Quel contrat numérique vérifier ?
Reponse: **Noyau attendu** : Le stockage de la disparité et son facteur d’échelle, notamment les quatre bits fractionnaires des sorties concernées ; convertir et masquer les invalides.

**Approfondissement** : Vérifier aussi baseline et Q avant de corriger arbitrairement les coordonnées finales.

**Erreurs bloquantes** : Reprojeter des entiers fixes comme des pixels de disparité ordinaires.
Source: [[60-vision-3d/references/61-stereo-profondeur|Fiche complète]] ; [OpenCV 4.13.0, StereoSGBM, Detailed Description et create](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html) ; [OpenCV 4.13.0, stereoRectify et reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-STEREO-003 provenance::agent pole::B pole::C
END

## CV-STEREO-004

Objectif : séparer rectification et matching. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-STEREO-004
Question: La rectification garantit-elle une correspondance correcte à chaque pixel ?
Reponse: **Noyau attendu** : Non : elle simplifie la géométrie de recherche ; texture, répétition et occlusion peuvent encore rendre le matching ambigu.

**Approfondissement** : La confiance et les masques invalides doivent être évalués, pas remplis par une profondeur fictive.

**Erreurs bloquantes** : Déduire une profondeur fiable de la seule horizontalité des lignes épipolaires.
Source: [[60-vision-3d/references/61-stereo-profondeur|Fiche complète]] ; [OpenCV StereoSGBM, description et compute](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html) ; [OpenCV reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-STEREO-004 provenance::agent pole::B pole::C
END
