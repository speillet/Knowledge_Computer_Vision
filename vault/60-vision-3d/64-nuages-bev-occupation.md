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

**Erreurs bloquantes** : Dire que toute BEV est un nuage LiDAR aplati identique.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Fiche complète]] ; [PointPillars, architecture](https://openaccess.thecvf.com/content_CVPR_2019/html/Lang_PointPillars_Fast_Encoders_for_Object_Detection_From_Point_Clouds_CVPR_2019_paper.html) ; [BEVFormer, méthode](https://arxiv.org/abs/2203.17270) ; [OctoMap, probabilistic occupancy](https://octomap.github.io/octomap/doc/index.html) ; [Occupancy Networks, surface implicite](https://openaccess.thecvf.com/content_CVPR_2019/html/Mescheder_Occupancy_Networks_Learning_3D_Reconstruction_in_Function_Space_CVPR_2019_paper.html).
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

**Erreurs bloquantes** : Assimiler non détecté et sans obstacle.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Fiche complète]] ; [PointPillars, architecture](https://openaccess.thecvf.com/content_CVPR_2019/html/Lang_PointPillars_Fast_Encoders_for_Object_Detection_From_Point_Clouds_CVPR_2019_paper.html) ; [BEVFormer, méthode](https://arxiv.org/abs/2203.17270) ; [OctoMap, probabilistic occupancy](https://octomap.github.io/octomap/doc/index.html) ; [Occupancy Networks, surface implicite](https://openaccess.thecvf.com/content_CVPR_2019/html/Mescheder_Occupancy_Networks_Learning_3D_Reconstruction_in_Function_Space_CVPR_2019_paper.html).
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

**Erreurs bloquantes** : Utiliser le score d’une forme implicite comme probabilité de collision calibrée.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Fiche complète]] ; [PointPillars, architecture](https://openaccess.thecvf.com/content_CVPR_2019/html/Lang_PointPillars_Fast_Encoders_for_Object_Detection_From_Point_Clouds_CVPR_2019_paper.html) ; [BEVFormer, méthode](https://arxiv.org/abs/2203.17270) ; [OctoMap, probabilistic occupancy](https://octomap.github.io/octomap/doc/index.html) ; [Occupancy Networks, surface implicite](https://openaccess.thecvf.com/content_CVPR_2019/html/Mescheder_Occupancy_Networks_Learning_3D_Reconstruction_in_Function_Space_CVPR_2019_paper.html).
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

**Erreurs bloquantes** : Conclure d’emblée à une capacité insuffisante du backbone.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Fiche complète]] ; [PointPillars, architecture](https://openaccess.thecvf.com/content_CVPR_2019/html/Lang_PointPillars_Fast_Encoders_for_Object_Detection_From_Point_Clouds_CVPR_2019_paper.html) ; [BEVFormer, méthode](https://arxiv.org/abs/2203.17270) ; [OctoMap, probabilistic occupancy](https://octomap.github.io/octomap/doc/index.html) ; [Occupancy Networks, surface implicite](https://openaccess.thecvf.com/content_CVPR_2019/html/Mescheder_Occupancy_Networks_Learning_3D_Reconstruction_in_Function_Space_CVPR_2019_paper.html).
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

**Erreurs bloquantes** : Garantir la sécurité globale avec une seule métrique de détection.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[60-vision-3d/references/64-nuages-bev-occupation|Fiche complète]] ; [PointPillars, architecture](https://openaccess.thecvf.com/content_CVPR_2019/html/Lang_PointPillars_Fast_Encoders_for_Object_Detection_From_Point_Clouds_CVPR_2019_paper.html) ; [BEVFormer, méthode](https://arxiv.org/abs/2203.17270) ; [OctoMap, probabilistic occupancy](https://octomap.github.io/octomap/doc/index.html) ; [Occupancy Networks, surface implicite](https://openaccess.thecvf.com/content_CVPR_2019/html/Mescheder_Occupancy_Networks_Learning_3D_Reconstruction_in_Function_Space_CVPR_2019_paper.html).
Tags: cv::pilote cv::d06 famille::conception cv_id::CV-BEV-005 provenance::agent pole::C cas_pole::C::conception
END
