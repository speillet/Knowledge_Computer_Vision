# Parcours par pôle métier

Les pôles sont une surcouche des thèmes ; une fiche partagée conserve un seul domaine et un seul ID. Ces comptes suivent la rédaction, pas l’aptitude à un poste ni la maîtrise. La vague V0 reste prioritaire.

## A — Deep Learning & Image Understanding

21 fiches rattachées, 97 cartes ; export non vérifié, maîtrise non mesurée.

| Sujet | Profondeur cible de la fiche | Artefacts |
| --- | --- | --- |
| Exposition, bruit, couleur et échantillonnage | approfondissement | [Fiche](../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md) · [Cartes](../20-acquisition-images/21-exposition-bruit-echantillonnage.md) |
| Filtres, gradients et pyramides | approfondissement | [Fiche](../30-traitement-image/references/31-filtrage-gradients.md) · [Cartes](../30-traitement-image/31-filtrage-gradients.md) |
| Morphologie et composantes connexes | approfondissement | [Fiche](../30-traitement-image/references/33-morphologie-composantes.md) · [Cartes](../30-traitement-image/33-morphologie-composantes.md) |
| Représentations visuelles, ViT, Swin, ConvNeXt et DINOv2 | usage-operationnel | [Fiche](../70-reconnaissance-representations/references/71-representations-transfert.md) · [Cartes](../70-reconnaissance-representations/71-representations-transfert.md) |
| CLIP, SigLIP et reconnaissance par texte | usage-operationnel | [Fiche](../70-reconnaissance-representations/references/72-clip-siglip.md) · [Cartes](../70-reconnaissance-representations/72-clip-siglip.md) |
| Inspection : golden template, PatchCore et PaDiM | usage-operationnel | [Fiche](../70-reconnaissance-representations/references/73-patchcore-padim.md) · [Cartes](../70-reconnaissance-representations/73-patchcore-padim.md) |
| NMS — supprimer des détections redondantes | approfondissement | [Fiche](../80-detection-pose/references/81-nms.md) · [Cartes](../80-detection-pose/81-nms.md) |
| Détection : Faster R-CNN, familles YOLO et DETR | approfondissement | [Fiche](../80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md) · [Cartes](../80-detection-pose/82-detection-fasterrcnn-yolo-detr.md) |
| Détection open-vocabulary et grounding | usage-operationnel | [Fiche](../80-detection-pose/references/83-detection-open-vocabulary.md) · [Cartes](../80-detection-pose/83-detection-open-vocabulary.md) |
| Détection 3D, pose d’objet et pose articulée | usage-operationnel | [Fiche](../80-detection-pose/references/84-detection-pose-3d.md) · [Cartes](../80-detection-pose/84-detection-pose-3d.md) |
| Otsu, distance transform et watershed | approfondissement | [Fiche](../90-segmentation/references/91-otsu-distance-watershed.md) · [Cartes](../90-segmentation/91-otsu-distance-watershed.md) |
| GrabCut, régions et modèles d’apparence | usage-operationnel | [Fiche](../90-segmentation/references/92-grabcut-regions.md) · [Cartes](../90-segmentation/92-grabcut-regions.md) |
| Segmentation sémantique, instances et panoptique | usage-operationnel | [Fiche](../90-segmentation/references/93-semantique-instances-panoptique.md) · [Cartes](../90-segmentation/93-semantique-instances-panoptique.md) |
| SAM, SAM 2 et segmentation guidée en vidéo | usage-operationnel | [Fiche](../90-segmentation/references/94-sam-sam2.md) · [Cartes](../90-segmentation/94-sam-sam2.md) |
| VLM, grounding et frontière vision–action | usage-operationnel | [Fiche](../120-generatif-multimodal/references/121-vlm-grounding.md) · [Cartes](../120-generatif-multimodal/121-vlm-grounding.md) |
| VAE, GAN et diffusion pour génération/restauration | reperage | [Fiche](../120-generatif-multimodal/references/122-generation-restauration.md) · [Cartes](../120-generatif-multimodal/122-generation-restauration.md) |
| IoU et AP — protocole COCO de détection | approfondissement | [Fiche](../130-evaluation-fiabilite/references/131-iou-ap-coco.md) · [Cartes](../130-evaluation-fiabilite/131-iou-ap-coco.md) |
| Splits, annotations, calibration des scores et dérive | usage-operationnel | [Fiche](../130-evaluation-fiabilite/references/133-donnees-generalisation.md) · [Cartes](../130-evaluation-fiabilite/133-donnees-generalisation.md) |
| Métriques de segmentation, inspection et applications | usage-operationnel | [Fiche](../130-evaluation-fiabilite/references/134-metriques-applications.md) · [Cartes](../130-evaluation-fiabilite/134-metriques-applications.md) |
| PTQ, QAT, INT8/FP8 et runtimes | usage-operationnel | [Fiche](../140-ingenierie-systemes/references/142-quantification-runtimes.md) · [Cartes](../140-ingenierie-systemes/142-quantification-runtimes.md) |
| Déploiement edge, compression et surveillance | usage-operationnel | [Fiche](../140-ingenierie-systemes/references/143-edge-reproductibilite.md) · [Cartes](../140-ingenierie-systemes/143-edge-reproductibilite.md) |

Cas propres au pôle, avec réponse et critères dans la carte :

- Conception : [CV-OPENVOC-002](../80-detection-pose/83-detection-open-vocabulary.md#cv-openvoc-002).
- Diagnostic : [CV-DETECTEURS-004](../80-detection-pose/82-detection-fasterrcnn-yolo-detr.md#cv-detecteurs-004).

## B — Geometric Vision & Spatial AI

24 fiches rattachées, 108 cartes ; export non vérifié, maîtrise non mesurée.

| Sujet | Profondeur cible de la fiche | Artefacts |
| --- | --- | --- |
| Moindres carrés, SVD et conditionnement | approfondissement | [Fiche](../10-mathematiques-estimation/references/11-moindres-carres-svd.md) · [Cartes](../10-mathematiques-estimation/11-moindres-carres-svd.md) |
| SO(3), SE(3) et conventions de transformation | approfondissement | [Fiche](../10-mathematiques-estimation/references/12-rotations-se3.md) · [Cartes](../10-mathematiques-estimation/12-rotations-se3.md) |
| Kalman, EKF, UKF et ESKF pour la fusion | usage-operationnel | [Fiche](../10-mathematiques-estimation/references/13-kalman-ekf-eskf.md) · [Cartes](../10-mathematiques-estimation/13-kalman-ekf-eskf.md) |
| Graphes de facteurs et optimisation incrémentale | usage-operationnel | [Fiche](../10-mathematiques-estimation/references/14-graphes-facteurs.md) · [Cartes](../10-mathematiques-estimation/14-graphes-facteurs.md) |
| Exposition, bruit, couleur et échantillonnage | approfondissement | [Fiche](../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md) · [Cartes](../20-acquisition-images/21-exposition-bruit-echantillonnage.md) |
| Capteurs, rolling shutter et synchronisation | usage-operationnel | [Fiche](../20-acquisition-images/references/22-capteurs-horodatage.md) · [Cartes](../20-acquisition-images/22-capteurs-horodatage.md) |
| Filtres, gradients et pyramides | approfondissement | [Fiche](../30-traitement-image/references/31-filtrage-gradients.md) · [Cartes](../30-traitement-image/31-filtrage-gradients.md) |
| Canny et Hough : contours, droites et segments | approfondissement | [Fiche](../30-traitement-image/references/32-canny-hough.md) · [Cartes](../30-traitement-image/32-canny-hough.md) |
| SIFT — points locaux et description à plusieurs échelles | approfondissement | [Fiche](../40-features-matching/references/41-sift.md) · [Cartes](../40-features-matching/41-sift.md) |
| ORB — détection et descripteur binaire orienté | approfondissement | [Fiche](../40-features-matching/references/42-orb.md) · [Cartes](../40-features-matching/42-orb.md) |
| Détecteurs locaux, descripteurs et matchers | approfondissement | [Fiche](../40-features-matching/references/43-detecteurs-matchers.md) · [Cartes](../40-features-matching/43-detecteurs-matchers.md) |
| SuperPoint, LightGlue et LoFTR | usage-operationnel | [Fiche](../40-features-matching/references/44-superpoint-lightglue-loftr.md) · [Cartes](../40-features-matching/44-superpoint-lightglue-loftr.md) |
| Recalage par intensités et ECC | usage-operationnel | [Fiche](../40-features-matching/references/45-recalage-ecc.md) · [Cartes](../40-features-matching/45-recalage-ecc.md) |
| RANSAC appliqué à une homographie | approfondissement | [Fiche](../50-calibration-geometrie/references/51-ransac-homographie.md) · [Cartes](../50-calibration-geometrie/51-ransac-homographie.md) |
| Calibration caméra sur mire — méthode de Zhang | approfondissement | [Fiche](../50-calibration-geometrie/references/52-calibration-zhang.md) · [Cartes](../50-calibration-geometrie/52-calibration-zhang.md) |
| Épipolaire, PnP et triangulation | approfondissement | [Fiche](../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md) · [Cartes](../50-calibration-geometrie/53-epipolaire-pnp-triangulation.md) |
| Bundle adjustment et complément de Schur | usage-operationnel | [Fiche](../50-calibration-geometrie/references/54-bundle-adjustment.md) · [Cartes](../50-calibration-geometrie/54-bundle-adjustment.md) |
| Calibration multicapteurs, hand-eye et temps | usage-operationnel | [Fiche](../50-calibration-geometrie/references/55-calibration-multicapteurs.md) · [Cartes](../50-calibration-geometrie/55-calibration-multicapteurs.md) |
| Stéréo rectifiée, SGM et profondeur | usage-operationnel | [Fiche](../60-vision-3d/references/61-stereo-profondeur.md) · [Cartes](../60-vision-3d/61-stereo-profondeur.md) |
| Recalage global et ICP local | usage-operationnel | [Fiche](../60-vision-3d/references/62-recalage-global-icp.md) · [Cartes](../60-vision-3d/62-recalage-global-icp.md) |
| SLAM, VIO, préintégration IMU et bouclage | usage-operationnel | [Fiche](../60-vision-3d/references/63-slam-vio.md) · [Cartes](../60-vision-3d/63-slam-vio.md) |
| Flot optique : Lucas–Kanade, Farnebäck et RAFT | approfondissement | [Fiche](../100-mouvement-video/references/101-flot-optique.md) · [Cartes](../100-mouvement-video/101-flot-optique.md) |
| NeRF, 3D Gaussian Splatting et reconstruction | reperage | [Fiche](../120-generatif-multimodal/references/123-nerf-gaussian-splatting.md) · [Cartes](../120-generatif-multimodal/123-nerf-gaussian-splatting.md) |
| Évaluer identités, trajectoires et localisation 3D | usage-operationnel | [Fiche](../130-evaluation-fiabilite/references/132-tracking-trajectoires.md) · [Cartes](../130-evaluation-fiabilite/132-tracking-trajectoires.md) |

Cas propres au pôle, avec réponse et critères dans la carte :

- Conception : [CV-VIO-004](../60-vision-3d/63-slam-vio.md#cv-vio-004).
- Diagnostic : [CV-VIO-005](../60-vision-3d/63-slam-vio.md#cv-vio-005).

## C — Robotics & Autonomous Perception

26 fiches rattachées, 128 cartes ; export non vérifié, maîtrise non mesurée.

| Sujet | Profondeur cible de la fiche | Artefacts |
| --- | --- | --- |
| Moindres carrés, SVD et conditionnement | approfondissement | [Fiche](../10-mathematiques-estimation/references/11-moindres-carres-svd.md) · [Cartes](../10-mathematiques-estimation/11-moindres-carres-svd.md) |
| SO(3), SE(3) et conventions de transformation | approfondissement | [Fiche](../10-mathematiques-estimation/references/12-rotations-se3.md) · [Cartes](../10-mathematiques-estimation/12-rotations-se3.md) |
| Kalman, EKF, UKF et ESKF pour la fusion | usage-operationnel | [Fiche](../10-mathematiques-estimation/references/13-kalman-ekf-eskf.md) · [Cartes](../10-mathematiques-estimation/13-kalman-ekf-eskf.md) |
| Graphes de facteurs et optimisation incrémentale | usage-operationnel | [Fiche](../10-mathematiques-estimation/references/14-graphes-facteurs.md) · [Cartes](../10-mathematiques-estimation/14-graphes-facteurs.md) |
| Exposition, bruit, couleur et échantillonnage | approfondissement | [Fiche](../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md) · [Cartes](../20-acquisition-images/21-exposition-bruit-echantillonnage.md) |
| Capteurs, rolling shutter et synchronisation | usage-operationnel | [Fiche](../20-acquisition-images/references/22-capteurs-horodatage.md) · [Cartes](../20-acquisition-images/22-capteurs-horodatage.md) |
| Calibration caméra sur mire — méthode de Zhang | approfondissement | [Fiche](../50-calibration-geometrie/references/52-calibration-zhang.md) · [Cartes](../50-calibration-geometrie/52-calibration-zhang.md) |
| Épipolaire, PnP et triangulation | approfondissement | [Fiche](../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md) · [Cartes](../50-calibration-geometrie/53-epipolaire-pnp-triangulation.md) |
| Bundle adjustment et complément de Schur | usage-operationnel | [Fiche](../50-calibration-geometrie/references/54-bundle-adjustment.md) · [Cartes](../50-calibration-geometrie/54-bundle-adjustment.md) |
| Calibration multicapteurs, hand-eye et temps | usage-operationnel | [Fiche](../50-calibration-geometrie/references/55-calibration-multicapteurs.md) · [Cartes](../50-calibration-geometrie/55-calibration-multicapteurs.md) |
| Stéréo rectifiée, SGM et profondeur | usage-operationnel | [Fiche](../60-vision-3d/references/61-stereo-profondeur.md) · [Cartes](../60-vision-3d/61-stereo-profondeur.md) |
| Recalage global et ICP local | usage-operationnel | [Fiche](../60-vision-3d/references/62-recalage-global-icp.md) · [Cartes](../60-vision-3d/62-recalage-global-icp.md) |
| SLAM, VIO, préintégration IMU et bouclage | usage-operationnel | [Fiche](../60-vision-3d/references/63-slam-vio.md) · [Cartes](../60-vision-3d/63-slam-vio.md) |
| Nuages, BEV et représentations d’occupation | usage-operationnel | [Fiche](../60-vision-3d/references/64-nuages-bev-occupation.md) · [Cartes](../60-vision-3d/64-nuages-bev-occupation.md) |
| NMS — supprimer des détections redondantes | approfondissement | [Fiche](../80-detection-pose/references/81-nms.md) · [Cartes](../80-detection-pose/81-nms.md) |
| Détection : Faster R-CNN, familles YOLO et DETR | approfondissement | [Fiche](../80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md) · [Cartes](../80-detection-pose/82-detection-fasterrcnn-yolo-detr.md) |
| Détection 3D, pose d’objet et pose articulée | usage-operationnel | [Fiche](../80-detection-pose/references/84-detection-pose-3d.md) · [Cartes](../80-detection-pose/84-detection-pose-3d.md) |
| Flot optique : Lucas–Kanade, Farnebäck et RAFT | approfondissement | [Fiche](../100-mouvement-video/references/101-flot-optique.md) · [Cartes](../100-mouvement-video/101-flot-optique.md) |
| SORT — tracking multiobjet par mouvement et association | approfondissement | [Fiche](../110-tracking-association/references/111-sort.md) · [Cartes](../110-tracking-association/111-sort.md) |
| DeepSORT, ByteTrack et association multiobjet | approfondissement | [Fiche](../110-tracking-association/references/112-deepsort-bytetrack.md) · [Cartes](../110-tracking-association/112-deepsort-bytetrack.md) |
| Tracking monoobjet : corrélation, siamois et MeanShift | usage-operationnel | [Fiche](../110-tracking-association/references/113-tracking-monoobjet.md) · [Cartes](../110-tracking-association/113-tracking-monoobjet.md) |
| IoU et AP — protocole COCO de détection | approfondissement | [Fiche](../130-evaluation-fiabilite/references/131-iou-ap-coco.md) · [Cartes](../130-evaluation-fiabilite/131-iou-ap-coco.md) |
| Évaluer identités, trajectoires et localisation 3D | usage-operationnel | [Fiche](../130-evaluation-fiabilite/references/132-tracking-trajectoires.md) · [Cartes](../130-evaluation-fiabilite/132-tracking-trajectoires.md) |
| Splits, annotations, calibration des scores et dérive | usage-operationnel | [Fiche](../130-evaluation-fiabilite/references/133-donnees-generalisation.md) · [Cartes](../130-evaluation-fiabilite/133-donnees-generalisation.md) |
| Contrats de données, profiling et pipelines vidéo | approfondissement | [Fiche](../140-ingenierie-systemes/references/141-contrats-profiling-video.md) · [Cartes](../140-ingenierie-systemes/141-contrats-profiling-video.md) |
| Déploiement edge, compression et surveillance | usage-operationnel | [Fiche](../140-ingenierie-systemes/references/143-edge-reproductibilite.md) · [Cartes](../140-ingenierie-systemes/143-edge-reproductibilite.md) |

Cas propres au pôle, avec réponse et critères dans la carte :

- Conception : [CV-BEV-005](../60-vision-3d/64-nuages-bev-occupation.md#cv-bev-005).
- Diagnostic : [CV-CAPTEURS-003](../20-acquisition-images/22-capteurs-horodatage.md#cv-capteurs-003).

## D — Multimodal AI & Video Intelligence

14 fiches rattachées, 57 cartes ; export non vérifié, maîtrise non mesurée.

| Sujet | Profondeur cible de la fiche | Artefacts |
| --- | --- | --- |
| Représentations visuelles, ViT, Swin, ConvNeXt et DINOv2 | usage-operationnel | [Fiche](../70-reconnaissance-representations/references/71-representations-transfert.md) · [Cartes](../70-reconnaissance-representations/71-representations-transfert.md) |
| CLIP, SigLIP et reconnaissance par texte | usage-operationnel | [Fiche](../70-reconnaissance-representations/references/72-clip-siglip.md) · [Cartes](../70-reconnaissance-representations/72-clip-siglip.md) |
| Détection open-vocabulary et grounding | usage-operationnel | [Fiche](../80-detection-pose/references/83-detection-open-vocabulary.md) · [Cartes](../80-detection-pose/83-detection-open-vocabulary.md) |
| SAM, SAM 2 et segmentation guidée en vidéo | usage-operationnel | [Fiche](../90-segmentation/references/94-sam-sam2.md) · [Cartes](../90-segmentation/94-sam-sam2.md) |
| Flot optique : Lucas–Kanade, Farnebäck et RAFT | approfondissement | [Fiche](../100-mouvement-video/references/101-flot-optique.md) · [Cartes](../100-mouvement-video/101-flot-optique.md) |
| Suivi de points, actions et compréhension vidéo | usage-operationnel | [Fiche](../100-mouvement-video/references/102-points-actions-video.md) · [Cartes](../100-mouvement-video/102-points-actions-video.md) |
| SORT — tracking multiobjet par mouvement et association | approfondissement | [Fiche](../110-tracking-association/references/111-sort.md) · [Cartes](../110-tracking-association/111-sort.md) |
| DeepSORT, ByteTrack et association multiobjet | approfondissement | [Fiche](../110-tracking-association/references/112-deepsort-bytetrack.md) · [Cartes](../110-tracking-association/112-deepsort-bytetrack.md) |
| Tracking monoobjet : corrélation, siamois et MeanShift | usage-operationnel | [Fiche](../110-tracking-association/references/113-tracking-monoobjet.md) · [Cartes](../110-tracking-association/113-tracking-monoobjet.md) |
| VLM, grounding et frontière vision–action | usage-operationnel | [Fiche](../120-generatif-multimodal/references/121-vlm-grounding.md) · [Cartes](../120-generatif-multimodal/121-vlm-grounding.md) |
| VAE, GAN et diffusion pour génération/restauration | reperage | [Fiche](../120-generatif-multimodal/references/122-generation-restauration.md) · [Cartes](../120-generatif-multimodal/122-generation-restauration.md) |
| NeRF, 3D Gaussian Splatting et reconstruction | reperage | [Fiche](../120-generatif-multimodal/references/123-nerf-gaussian-splatting.md) · [Cartes](../120-generatif-multimodal/123-nerf-gaussian-splatting.md) |
| Évaluer identités, trajectoires et localisation 3D | usage-operationnel | [Fiche](../130-evaluation-fiabilite/references/132-tracking-trajectoires.md) · [Cartes](../130-evaluation-fiabilite/132-tracking-trajectoires.md) |
| Splits, annotations, calibration des scores et dérive | usage-operationnel | [Fiche](../130-evaluation-fiabilite/references/133-donnees-generalisation.md) · [Cartes](../130-evaluation-fiabilite/133-donnees-generalisation.md) |

Cas propres au pôle, avec réponse et critères dans la carte :

- Conception : [CV-VLM-003](../120-generatif-multimodal/121-vlm-grounding.md#cv-vlm-003).
- Diagnostic : [CV-VLM-004](../120-generatif-multimodal/121-vlm-grounding.md#cv-vlm-004).

## E — Applied Computer Vision

31 fiches rattachées, 146 cartes ; export non vérifié, maîtrise non mesurée.

| Sujet | Profondeur cible de la fiche | Artefacts |
| --- | --- | --- |
| Exposition, bruit, couleur et échantillonnage | approfondissement | [Fiche](../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md) · [Cartes](../20-acquisition-images/21-exposition-bruit-echantillonnage.md) |
| Capteurs, rolling shutter et synchronisation | usage-operationnel | [Fiche](../20-acquisition-images/references/22-capteurs-horodatage.md) · [Cartes](../20-acquisition-images/22-capteurs-horodatage.md) |
| Line-scan, télédétection et volumes médicaux | reperage | [Fiche](../20-acquisition-images/references/23-imageries-specialisees.md) · [Cartes](../20-acquisition-images/23-imageries-specialisees.md) |
| Filtres, gradients et pyramides | approfondissement | [Fiche](../30-traitement-image/references/31-filtrage-gradients.md) · [Cartes](../30-traitement-image/31-filtrage-gradients.md) |
| Canny et Hough : contours, droites et segments | approfondissement | [Fiche](../30-traitement-image/references/32-canny-hough.md) · [Cartes](../30-traitement-image/32-canny-hough.md) |
| Morphologie et composantes connexes | approfondissement | [Fiche](../30-traitement-image/references/33-morphologie-composantes.md) · [Cartes](../30-traitement-image/33-morphologie-composantes.md) |
| SIFT — points locaux et description à plusieurs échelles | approfondissement | [Fiche](../40-features-matching/references/41-sift.md) · [Cartes](../40-features-matching/41-sift.md) |
| ORB — détection et descripteur binaire orienté | approfondissement | [Fiche](../40-features-matching/references/42-orb.md) · [Cartes](../40-features-matching/42-orb.md) |
| Détecteurs locaux, descripteurs et matchers | approfondissement | [Fiche](../40-features-matching/references/43-detecteurs-matchers.md) · [Cartes](../40-features-matching/43-detecteurs-matchers.md) |
| Recalage par intensités et ECC | usage-operationnel | [Fiche](../40-features-matching/references/45-recalage-ecc.md) · [Cartes](../40-features-matching/45-recalage-ecc.md) |
| RANSAC appliqué à une homographie | approfondissement | [Fiche](../50-calibration-geometrie/references/51-ransac-homographie.md) · [Cartes](../50-calibration-geometrie/51-ransac-homographie.md) |
| Calibration caméra sur mire — méthode de Zhang | approfondissement | [Fiche](../50-calibration-geometrie/references/52-calibration-zhang.md) · [Cartes](../50-calibration-geometrie/52-calibration-zhang.md) |
| Calibration multicapteurs, hand-eye et temps | usage-operationnel | [Fiche](../50-calibration-geometrie/references/55-calibration-multicapteurs.md) · [Cartes](../50-calibration-geometrie/55-calibration-multicapteurs.md) |
| Représentations visuelles, ViT, Swin, ConvNeXt et DINOv2 | usage-operationnel | [Fiche](../70-reconnaissance-representations/references/71-representations-transfert.md) · [Cartes](../70-reconnaissance-representations/71-representations-transfert.md) |
| Inspection : golden template, PatchCore et PaDiM | usage-operationnel | [Fiche](../70-reconnaissance-representations/references/73-patchcore-padim.md) · [Cartes](../70-reconnaissance-representations/73-patchcore-padim.md) |
| OCR et compréhension documentaire | reperage | [Fiche](../70-reconnaissance-representations/references/74-ocr-documents.md) · [Cartes](../70-reconnaissance-representations/74-ocr-documents.md) |
| Reconnaissance biométrique, ArcFace et PAD | reperage | [Fiche](../70-reconnaissance-representations/references/75-embeddings-biometrie.md) · [Cartes](../70-reconnaissance-representations/75-embeddings-biometrie.md) |
| NMS — supprimer des détections redondantes | approfondissement | [Fiche](../80-detection-pose/references/81-nms.md) · [Cartes](../80-detection-pose/81-nms.md) |
| Détection : Faster R-CNN, familles YOLO et DETR | approfondissement | [Fiche](../80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md) · [Cartes](../80-detection-pose/82-detection-fasterrcnn-yolo-detr.md) |
| Otsu, distance transform et watershed | approfondissement | [Fiche](../90-segmentation/references/91-otsu-distance-watershed.md) · [Cartes](../90-segmentation/91-otsu-distance-watershed.md) |
| GrabCut, régions et modèles d’apparence | usage-operationnel | [Fiche](../90-segmentation/references/92-grabcut-regions.md) · [Cartes](../90-segmentation/92-grabcut-regions.md) |
| Segmentation sémantique, instances et panoptique | usage-operationnel | [Fiche](../90-segmentation/references/93-semantique-instances-panoptique.md) · [Cartes](../90-segmentation/93-semantique-instances-panoptique.md) |
| SORT — tracking multiobjet par mouvement et association | approfondissement | [Fiche](../110-tracking-association/references/111-sort.md) · [Cartes](../110-tracking-association/111-sort.md) |
| DeepSORT, ByteTrack et association multiobjet | approfondissement | [Fiche](../110-tracking-association/references/112-deepsort-bytetrack.md) · [Cartes](../110-tracking-association/112-deepsort-bytetrack.md) |
| Tracking monoobjet : corrélation, siamois et MeanShift | usage-operationnel | [Fiche](../110-tracking-association/references/113-tracking-monoobjet.md) · [Cartes](../110-tracking-association/113-tracking-monoobjet.md) |
| VAE, GAN et diffusion pour génération/restauration | reperage | [Fiche](../120-generatif-multimodal/references/122-generation-restauration.md) · [Cartes](../120-generatif-multimodal/122-generation-restauration.md) |
| IoU et AP — protocole COCO de détection | approfondissement | [Fiche](../130-evaluation-fiabilite/references/131-iou-ap-coco.md) · [Cartes](../130-evaluation-fiabilite/131-iou-ap-coco.md) |
| Splits, annotations, calibration des scores et dérive | usage-operationnel | [Fiche](../130-evaluation-fiabilite/references/133-donnees-generalisation.md) · [Cartes](../130-evaluation-fiabilite/133-donnees-generalisation.md) |
| Métriques de segmentation, inspection et applications | usage-operationnel | [Fiche](../130-evaluation-fiabilite/references/134-metriques-applications.md) · [Cartes](../130-evaluation-fiabilite/134-metriques-applications.md) |
| Contrats de données, profiling et pipelines vidéo | approfondissement | [Fiche](../140-ingenierie-systemes/references/141-contrats-profiling-video.md) · [Cartes](../140-ingenierie-systemes/141-contrats-profiling-video.md) |
| Déploiement edge, compression et surveillance | usage-operationnel | [Fiche](../140-ingenierie-systemes/references/143-edge-reproductibilite.md) · [Cartes](../140-ingenierie-systemes/143-edge-reproductibilite.md) |

Cas propres au pôle, avec réponse et critères dans la carte :

- Conception : [CV-ANOMALIES-004](../70-reconnaissance-representations/73-patchcore-padim.md#cv-anomalies-004).
- Diagnostic : [CV-FIABILITE-004](../130-evaluation-fiabilite/133-donnees-generalisation.md#cv-fiabilite-004).

## F — Vision Systems & Deployment

9 fiches rattachées, 41 cartes ; export non vérifié, maîtrise non mesurée.

| Sujet | Profondeur cible de la fiche | Artefacts |
| --- | --- | --- |
| Exposition, bruit, couleur et échantillonnage | approfondissement | [Fiche](../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md) · [Cartes](../20-acquisition-images/21-exposition-bruit-echantillonnage.md) |
| Capteurs, rolling shutter et synchronisation | usage-operationnel | [Fiche](../20-acquisition-images/references/22-capteurs-horodatage.md) · [Cartes](../20-acquisition-images/22-capteurs-horodatage.md) |
| Filtres, gradients et pyramides | approfondissement | [Fiche](../30-traitement-image/references/31-filtrage-gradients.md) · [Cartes](../30-traitement-image/31-filtrage-gradients.md) |
| Canny et Hough : contours, droites et segments | approfondissement | [Fiche](../30-traitement-image/references/32-canny-hough.md) · [Cartes](../30-traitement-image/32-canny-hough.md) |
| ORB — détection et descripteur binaire orienté | approfondissement | [Fiche](../40-features-matching/references/42-orb.md) · [Cartes](../40-features-matching/42-orb.md) |
| Splits, annotations, calibration des scores et dérive | usage-operationnel | [Fiche](../130-evaluation-fiabilite/references/133-donnees-generalisation.md) · [Cartes](../130-evaluation-fiabilite/133-donnees-generalisation.md) |
| Contrats de données, profiling et pipelines vidéo | approfondissement | [Fiche](../140-ingenierie-systemes/references/141-contrats-profiling-video.md) · [Cartes](../140-ingenierie-systemes/141-contrats-profiling-video.md) |
| PTQ, QAT, INT8/FP8 et runtimes | usage-operationnel | [Fiche](../140-ingenierie-systemes/references/142-quantification-runtimes.md) · [Cartes](../140-ingenierie-systemes/142-quantification-runtimes.md) |
| Déploiement edge, compression et surveillance | usage-operationnel | [Fiche](../140-ingenierie-systemes/references/143-edge-reproductibilite.md) · [Cartes](../140-ingenierie-systemes/143-edge-reproductibilite.md) |

Cas propres au pôle, avec réponse et critères dans la carte :

- Conception : [CV-PIPELINE-004](../140-ingenierie-systemes/141-contrats-profiling-video.md#cv-pipeline-004).
- Diagnostic : [CV-QUANT-004](../140-ingenierie-systemes/142-quantification-runtimes.md#cv-quant-004).

[Accueil](../00-Accueil.md) · [Inventaire](Inventaire.md) · [Suivi](Suivi-pilote.md).
