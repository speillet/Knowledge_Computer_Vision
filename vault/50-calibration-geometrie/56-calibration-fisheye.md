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

**Pourquoi le centre trompe** : près de zéro, $\tan\theta$ est proche de $\theta$. Les deux modèles peuvent donc sembler semblables sur une petite région centrale. L'écart grandit hors axe ; des coefficients nuls ne signifient pas « aucune différence avec le pinhole », mais aucune correction supplémentaire au modèle angulaire choisi.

**Contrôle proposé** : projeter quelques rayons connus, dont un suffisamment oblique, avec les deux modèles dans les mêmes conventions et unités. Comparer ensuite aux observations réservées de la caméra réelle. Une image visuellement plausible ne départage pas les modèles sur leur précision périphérique. Les coefficients et la matrice de chaque modèle doivent rester associés à l'image et à la fonction de projection qui les interprètent.

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

**Lecture des observations** : des points proches de l'axe explorent une petite plage d'angles. Plusieurs modèles ou paramètres peuvent alors produire des projections similaires dans cette plage tout en divergeant aux bords. Ajouter des images centrales presque identiques ne teste pas cette extrapolation.

**Acquisition construite** : répartir les coins sur le champ utile, varier les inclinaisons et conserver des vues périphériques nettes à l'écart de l'ajustement. Examiner les résidus par rayon et la stabilité sur sous-ensembles. Une difficulté de détection des coins au bord peut elle-même introduire un biais ; inspecter les observations plutôt que demander seulement plus de coefficients. Le protocole vise une information géométrique plus complète et doit rester compatible avec le modèle optique et la rigidité de la mire.

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

**Pourquoi la moyenne masque le défaut** : si la plupart des coins se trouvent près du centre, leur faible erreur domine le RMS, alors que la région périphérique utile est peu évaluée. Une moyenne globale doit donc être accompagnée d'une carte spatiale et de groupes d'erreurs comparables.

**Diagnostic construit** : fixer la calibration et projeter des points réservés à plusieurs rayons, puis observer direction et amplitude des erreurs. Un motif systématique suggère une cause structurée, mais ne départage pas à lui seul modèle optique et biais de localisation. Inspecter les points et répéter avec de nouvelles poses. Valider aussi une grandeur liée à l'usage : la précision d'une projection aux bords n'est pas résumée par l'apparence rectifiée.

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

**Chaîne de données** : le remap définit quelle position source contribue à chaque pixel de sortie. La nouvelle grille décrit donc une autre projection, même si elle provient du même capteur. Pour remonter un pixel vers un rayon, utiliser le contrat de cette grille, pas celui du fichier brut.

**Test construit** : partir d'un point 3D connu, le projeter dans l'image brute, suivre la transformation vers la sortie, puis vérifier le rayon ou la pose calculée dans le modèle rectifié. Inclure crop, padding et zones sans données. Appliquer ensuite la distorsion brute une deuxième fois revient à transformer des coordonnées déjà corrigées. Une cohérence visuelle générale peut laisser passer cette erreur, notamment près du centre où les modèles se ressemblent davantage.

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

**Interprétation du compromis** : une projection de sortie peut privilégier un cadrage qui remplit le rectangle ou un champ plus large avec des zones invalides. Ces choix changent la quantité d'information disponible et sa résolution locale, sans modifier les observations ayant servi à estimer la caméra.

**Évaluation proposée** : comparer les sorties sur la même calibration en reportant masque valide, champ utile et erreur de la tâche. Pour une mesure près d'une bordure, l'interpolation et la faible densité d'observations peuvent compter davantage que le nombre total de pixels affichés. La géométrie de sortie doit être propagée aux algorithmes suivants. Un changement de présentation peut donc aider un produit sans constituer une amélioration de calibration physique.

**Erreurs bloquantes** : Assimiler augmentation du champ affiché et diminution de l’erreur de calibration.
Source: [[50-calibration-geometrie/references/56-calibration-fisheye|Fiche complète]] ; [OpenCV 4.13, fisheye, Detailed Description et estimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-FISHEYE-005 provenance::agent pole::B pole::C pole::E
END
