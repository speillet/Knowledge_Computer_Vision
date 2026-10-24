# Calibration fisheye — projection angulaire et validation hors centre — cartes

Fiche : [[50-calibration-geometrie/references/56-calibration-fisheye|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-FISHEYE-001

Objectif : distinguer projection fisheye et pinhole. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FISHEYE-001
Question: Dans OpenCV fisheye, mettre les quatre coefficients de distorsion à zéro redonne-t-il la projection pinhole ? Expliquer avec un rayon hors axe.
Reponse: **Noyau attendu** : Non : le rayon normalisé vaut alors $r_d=\theta$, tandis que le pinhole donne $r=\tan\theta$, avec $\theta$ l’angle au centre optique en radians. Les projections ne coïncident qu’approximativement près de l’axe.

**Approfondissement** : Cas analytique : à 60° et avec une focale de 300 px, le rayon vaut environ 314 px contre 520 px en pinhole. Comparer les modèles sur les rayons effectivement observés, pas uniquement sur leurs noms ou le nombre de coefficients.

**Erreurs bloquantes** : Assimiler les coefficients fisheye aux premiers coefficients pinhole ; conclure à une projection identique partout.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Fiche complète]] ; [OpenCV 4.13, fisheye, Detailed Description et estimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-FISHEYE-001 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-002

Objectif : concevoir des vues de calibration grand angle. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-FISHEYE-002
Question: Quelles acquisitions ajouter lorsqu’une calibration grand angle utilise beaucoup de vues mais seulement près du centre de l’image ?
Reponse: **Noyau attendu** : Ajouter des vues couvrant la périphérie et diversifier orientations et distances de la mire. Réserver des poses et régions pour la validation. Le nombre de photos ne remplace pas l’information géométrique qu’elles apportent.

**Approfondissement** : Les paramètres périphériques sont peu contraints par des rayons proches de l’axe. Contrôler netteté, détection des points, rigidité de la mire et stabilité du montage. Le protocole proposé vise le conditionnement, sans garantir la calibration d’un dispositif quelconque.

**Erreurs bloquantes** : Multiplier uniquement des vues frontales centrales ; valider sur les seules images d’ajustement.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Fiche complète]] ; [OpenCV 4.13, fisheye, Detailed Description et estimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::conception cv_id::CV-FISHEYE-002 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-003

Objectif : localiser un défaut de modèle de caméra. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FISHEYE-003
Question: Le RMS global de reprojection d’un fisheye est faible, mais des mesures aux bords deviennent fausses. Quelles vérifications faire ?
Reponse: **Noyau attendu** : Cartographier les résidus selon rayon, position et pose sur des observations réservées ; inspecter les points de mire aux bords et vérifier le modèle de projection. Comparer ensuite les erreurs métriques de l’usage cible.

**Approfondissement** : Une moyenne est dominée par les zones les plus échantillonnées. Des biais systématiques en périphérie peuvent venir du modèle, de la mire, du flou ou du manque de vues. Un aspect visuel redressé ne les départage pas.

**Erreurs bloquantes** : Conclure à une calibration correcte à partir d’un seul RMS d’apprentissage.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Fiche complète]] ; [OpenCV 4.13, fisheye, Detailed Description et estimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-FISHEYE-003 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-004

Objectif : propager le contrat après rectification. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-FISHEYE-004
Question: Après remap d’une image fisheye vers une image rectifiée, quelle calibration utiliser pour reconstruire des rayons ou faire une pose ?
Reponse: **Noyau attendu** : Utiliser le modèle et la nouvelle matrice associés à l’image rectifiée, avec ses dimensions et sa région valide. Les intrinsics et coefficients de l’image brute décrivent une autre géométrie de pixels.

**Approfondissement** : La map fixe une correspondance entre pixels de sortie et source. Changer la résolution, le crop ou la projection de sortie impose de propager cette transformation. Vérifier un point 3D connu à travers la chaîne complète.

**Erreurs bloquantes** : Réutiliser sans adaptation la distorsion brute sur une image déjà rectifiée.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Fiche complète]] ; [OpenCV 4.13, fisheye, Detailed Description et estimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-FISHEYE-004 provenance::agent pole::B pole::C pole::E
END

## CV-FISHEYE-005

Objectif : interpréter le paramètre de champ rectifié. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-FISHEYE-005
Question: Une modification du paramètre balance d’OpenCV montre davantage de scène mais ajoute des bordures. La caméra est-elle mieux calibrée ?
Reponse: **Noyau attendu** : Non : `balance` modifie le choix de la projection de sortie et le compromis de champ, pas les paramètres physiques déjà estimés. Comparer champ utile, résolution locale et pixels valides avec la même calibration.

**Approfondissement** : Une grande zone de sortie peut contenir des pixels sans observation d’origine ou très interpolés. Le critère de qualité doit venir de la tâche : couverture, métrique ou géométrie, pas de la seule taille de l’image.

**Erreurs bloquantes** : Assimiler augmentation du champ affiché et diminution de l’erreur de calibration.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Fiche complète]] ; [OpenCV 4.13, fisheye, Detailed Description et estimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-FISHEYE-005 provenance::agent pole::B pole::C pole::E
END
