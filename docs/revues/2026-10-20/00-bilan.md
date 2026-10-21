# Bilan de revue des cartes — 2026-10-20

Bilan consolidé le 21 octobre 2026.

## Périmètre et résultat

Les **52 sujets et 224 cartes existants** ont un rapport individuel et une
évaluation des quatre axes du skill `revue-cartes` : exactitude, pertinence,
corrigibilité et cohérence. Les 12 rapports du 18 octobre (50 cartes), déjà
présents à la reprise, sont intégrés au bilan ; les 40 sujets restants
(174 cartes) ont été examinés le 20 octobre. Les sources des 12 premiers
rapports ne sont pas présentées comme nouvellement consultées le 20 octobre.
Les synthèses et liens de ces rapports ont été harmonisés à la consolidation.

Le périmètre est le contenu existant, pas l'ensemble du programme de computer
vision. Aucun ajout, suppression, changement d'objectif ou d'ID ; aucun
identifiant de synchronisation Anki n'était présent. Les fiches modifiées
ont une révision incrémentée et restent `statut: redige`, provenance `agent`.
Les comptes courants (52 fiches, 224 cartes) restent inchangés.

| Gravité maximale par carte avant correction | Cartes |
| --- | ---: |
| Bloquante | 0 |
| Importante | 46 |
| Mineure | 92 |
| Aucun défaut relevé dans le passage audité | 86 |
| Total | 224 |

Ce décompte compte chaque carte une fois ; il ne compte ni les erreurs
indépendantes ni les défauts limités aux fiches. « Aucun défaut relevé »
n'est pas une certification d'exactitude. Les corrections concernent surtout
les sources insuffisantes, les hypothèses et conventions implicites, ainsi
que des critères de réponse trop vagues. Le [journal de correction](../../../vault/01-Parcours/Suivi-pilote.md#suite-et-corrections)
consigne chaque intervention et sa révision.

## Corrections principales

- Pondération et blanchiment des résidus ; articulation EKF/ESKF, repères et
  unités ; critères de réponse pour Hough et morphologie.
- Contrats `solvePnP`/`solveP3P`, mouvements relatifs hand–eye, conditions de
  Schur et convention de disparité pour la profondeur stéréo.
- Convention CER classique distinguée de celle des benchmarks OCR-D ;
  partition panoptique sans recouvrement ; sources propres aux variantes de
  méthodes, à la pose et aux symétries.
- Contrat SORT sans détection, entrée vide de forme `(0, 5)` ; distinction
  entre template fixe SiamFC et actualisation dans un tracker adaptatif.
- Marginale de bruit DDPM distinguée d'une transition ; densité NeRF
  dépendant de la position, couleur dépendant aussi de la direction.
- Quantification entière bornée et distincte de FP8 ; limites matérielles
  de la sparsité et du régime thermique ; modèle séquentiel d'Amdahl explicite.
- Passages de sources ciblés par carte ; dates ou versions des documentations
  précisées ; raisonnements, diagnostics et protocoles du projet distingués
  des résultats publiés et des expériences réellement exécutées.

## Cartographie des rapports

| Sujet et fiche canonique | Cartes | Rapport |
| --- | ---: | --- |
| [Moindres carrés, SVD et conditionnement](../../../vault/10-mathematiques-estimation/references/11-moindres-carres-svd.md) | [4](../../../vault/10-mathematiques-estimation/11-moindres-carres-svd.md) | [2026-10-18](../2026-10-18/11-moindres-carres-svd.md) |
| [SO(3), SE(3) et conventions de transformation](../../../vault/10-mathematiques-estimation/references/12-rotations-se3.md) | [4](../../../vault/10-mathematiques-estimation/12-rotations-se3.md) | [2026-10-18](../2026-10-18/12-rotations-se3.md) |
| [Kalman, EKF, UKF et ESKF pour la fusion](../../../vault/10-mathematiques-estimation/references/13-kalman-ekf-eskf.md) | [4](../../../vault/10-mathematiques-estimation/13-kalman-ekf-eskf.md) | [2026-10-18](../2026-10-18/13-kalman-ekf-eskf.md) |
| [Graphes de facteurs et optimisation incrémentale](../../../vault/10-mathematiques-estimation/references/14-graphes-facteurs.md) | [3](../../../vault/10-mathematiques-estimation/14-graphes-facteurs.md) | [2026-10-18](../2026-10-18/14-graphes-facteurs.md) |
| [Exposition, bruit, couleur et échantillonnage](../../../vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md) | [4](../../../vault/20-acquisition-images/21-exposition-bruit-echantillonnage.md) | [2026-10-18](../2026-10-18/21-exposition-bruit-echantillonnage.md) |
| [Capteurs, rolling shutter et synchronisation](../../../vault/20-acquisition-images/references/22-capteurs-horodatage.md) | [4](../../../vault/20-acquisition-images/22-capteurs-horodatage.md) | [2026-10-18](../2026-10-18/22-capteurs-horodatage.md) |
| [Line-scan, télédétection et volumes médicaux](../../../vault/20-acquisition-images/references/23-imageries-specialisees.md) | [3](../../../vault/20-acquisition-images/23-imageries-specialisees.md) | [2026-10-18](../2026-10-18/23-imageries-specialisees.md) |
| [Filtres, gradients et pyramides](../../../vault/30-traitement-image/references/31-filtrage-gradients.md) | [4](../../../vault/30-traitement-image/31-filtrage-gradients.md) | [2026-10-18](../2026-10-18/31-filtrage-gradients.md) |
| [Canny et Hough : contours, droites et segments](../../../vault/30-traitement-image/references/32-canny-hough.md) | [4](../../../vault/30-traitement-image/32-canny-hough.md) | [2026-10-18](../2026-10-18/32-canny-hough.md) |
| [Morphologie et composantes connexes](../../../vault/30-traitement-image/references/33-morphologie-composantes.md) | [3](../../../vault/30-traitement-image/33-morphologie-composantes.md) | [2026-10-18](../2026-10-18/33-morphologie-composantes.md) |
| [SIFT — points locaux et description à plusieurs échelles](../../../vault/40-features-matching/references/41-sift.md) | [7](../../../vault/40-features-matching/41-sift.md) | [2026-10-18](../2026-10-18/41-sift.md) |
| [ORB — détection et descripteur binaire orienté](../../../vault/40-features-matching/references/42-orb.md) | [6](../../../vault/40-features-matching/42-orb.md) | [2026-10-18](../2026-10-18/42-orb.md) |
| [Détecteurs locaux, descripteurs et matchers](../../../vault/40-features-matching/references/43-detecteurs-matchers.md) | [4](../../../vault/40-features-matching/43-detecteurs-matchers.md) | [2026-10-20](43-detecteurs-matchers.md) |
| [SuperPoint, LightGlue et LoFTR](../../../vault/40-features-matching/references/44-superpoint-lightglue-loftr.md) | [5](../../../vault/40-features-matching/44-superpoint-lightglue-loftr.md) | [2026-10-20](44-superpoint-lightglue-loftr.md) |
| [Recalage par intensités et ECC](../../../vault/40-features-matching/references/45-recalage-ecc.md) | [3](../../../vault/40-features-matching/45-recalage-ecc.md) | [2026-10-20](45-recalage-ecc.md) |
| [RANSAC appliqué à une homographie](../../../vault/50-calibration-geometrie/references/51-ransac-homographie.md) | [7](../../../vault/50-calibration-geometrie/51-ransac-homographie.md) | [2026-10-20](51-ransac-homographie.md) |
| [Calibration caméra sur mire — méthode de Zhang](../../../vault/50-calibration-geometrie/references/52-calibration-zhang.md) | [7](../../../vault/50-calibration-geometrie/52-calibration-zhang.md) | [2026-10-20](52-calibration-zhang.md) |
| [Épipolaire, PnP et triangulation](../../../vault/50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md) | [5](../../../vault/50-calibration-geometrie/53-epipolaire-pnp-triangulation.md) | [2026-10-20](53-epipolaire-pnp-triangulation.md) |
| [Bundle adjustment et complément de Schur](../../../vault/50-calibration-geometrie/references/54-bundle-adjustment.md) | [4](../../../vault/50-calibration-geometrie/54-bundle-adjustment.md) | [2026-10-20](54-bundle-adjustment.md) |
| [Calibration multicapteurs, hand-eye et temps](../../../vault/50-calibration-geometrie/references/55-calibration-multicapteurs.md) | [3](../../../vault/50-calibration-geometrie/55-calibration-multicapteurs.md) | [2026-10-20](55-calibration-multicapteurs.md) |
| [Stéréo rectifiée, SGM et profondeur](../../../vault/60-vision-3d/references/61-stereo-profondeur.md) | [4](../../../vault/60-vision-3d/61-stereo-profondeur.md) | [2026-10-20](61-stereo-profondeur.md) |
| [Recalage global et ICP local](../../../vault/60-vision-3d/references/62-recalage-global-icp.md) | [5](../../../vault/60-vision-3d/62-recalage-global-icp.md) | [2026-10-20](62-recalage-global-icp.md) |
| [SLAM, VIO, préintégration IMU et bouclage](../../../vault/60-vision-3d/references/63-slam-vio.md) | [5](../../../vault/60-vision-3d/63-slam-vio.md) | [2026-10-20](63-slam-vio.md) |
| [Nuages, BEV et représentations d’occupation](../../../vault/60-vision-3d/references/64-nuages-bev-occupation.md) | [5](../../../vault/60-vision-3d/64-nuages-bev-occupation.md) | [2026-10-20](64-nuages-bev-occupation.md) |
| [Représentations visuelles, ViT, Swin, ConvNeXt et DINOv2](../../../vault/70-reconnaissance-representations/references/71-representations-transfert.md) | [5](../../../vault/70-reconnaissance-representations/71-representations-transfert.md) | [2026-10-20](71-representations-transfert.md) |
| [CLIP, SigLIP et reconnaissance par texte](../../../vault/70-reconnaissance-representations/references/72-clip-siglip.md) | [4](../../../vault/70-reconnaissance-representations/72-clip-siglip.md) | [2026-10-20](72-clip-siglip.md) |
| [Inspection : golden template, PatchCore et PaDiM](../../../vault/70-reconnaissance-representations/references/73-patchcore-padim.md) | [4](../../../vault/70-reconnaissance-representations/73-patchcore-padim.md) | [2026-10-20](73-patchcore-padim.md) |
| [OCR et compréhension documentaire](../../../vault/70-reconnaissance-representations/references/74-ocr-documents.md) | [3](../../../vault/70-reconnaissance-representations/74-ocr-documents.md) | [2026-10-20](74-ocr-documents.md) |
| [Reconnaissance biométrique, ArcFace et PAD](../../../vault/70-reconnaissance-representations/references/75-embeddings-biometrie.md) | [2](../../../vault/70-reconnaissance-representations/75-embeddings-biometrie.md) | [2026-10-20](75-embeddings-biometrie.md) |
| [NMS — supprimer des détections redondantes](../../../vault/80-detection-pose/references/81-nms.md) | [5](../../../vault/80-detection-pose/81-nms.md) | [2026-10-20](81-nms.md) |
| [Détection : Faster R-CNN, familles YOLO et DETR](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md) | [5](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md) | [2026-10-20](82-detection-fasterrcnn-yolo-detr.md) |
| [Détection open-vocabulary et grounding](../../../vault/80-detection-pose/references/83-detection-open-vocabulary.md) | [3](../../../vault/80-detection-pose/83-detection-open-vocabulary.md) | [2026-10-20](83-detection-open-vocabulary.md) |
| [Détection 3D, pose d’objet et pose articulée](../../../vault/80-detection-pose/references/84-detection-pose-3d.md) | [4](../../../vault/80-detection-pose/84-detection-pose-3d.md) | [2026-10-20](84-detection-pose-3d.md) |
| [Otsu, distance transform et watershed](../../../vault/90-segmentation/references/91-otsu-distance-watershed.md) | [5](../../../vault/90-segmentation/91-otsu-distance-watershed.md) | [2026-10-20](91-otsu-distance-watershed.md) |
| [GrabCut, régions et modèles d’apparence](../../../vault/90-segmentation/references/92-grabcut-regions.md) | [3](../../../vault/90-segmentation/92-grabcut-regions.md) | [2026-10-20](92-grabcut-regions.md) |
| [Segmentation sémantique, instances et panoptique](../../../vault/90-segmentation/references/93-semantique-instances-panoptique.md) | [4](../../../vault/90-segmentation/93-semantique-instances-panoptique.md) | [2026-10-20](93-semantique-instances-panoptique.md) |
| [SAM, SAM 2 et segmentation guidée en vidéo](../../../vault/90-segmentation/references/94-sam-sam2.md) | [3](../../../vault/90-segmentation/94-sam-sam2.md) | [2026-10-20](94-sam-sam2.md) |
| [Flot optique : Lucas–Kanade, Farnebäck et RAFT](../../../vault/100-mouvement-video/references/101-flot-optique.md) | [4](../../../vault/100-mouvement-video/101-flot-optique.md) | [2026-10-20](101-flot-optique.md) |
| [Suivi de points, actions et compréhension vidéo](../../../vault/100-mouvement-video/references/102-points-actions-video.md) | [4](../../../vault/100-mouvement-video/102-points-actions-video.md) | [2026-10-20](102-points-actions-video.md) |
| [SORT — tracking multiobjet par mouvement et association](../../../vault/110-tracking-association/references/111-sort.md) | [8](../../../vault/110-tracking-association/111-sort.md) | [2026-10-20](111-sort.md) |
| [DeepSORT, ByteTrack et association multiobjet](../../../vault/110-tracking-association/references/112-deepsort-bytetrack.md) | [4](../../../vault/110-tracking-association/112-deepsort-bytetrack.md) | [2026-10-20](112-deepsort-bytetrack.md) |
| [Tracking monoobjet : corrélation, siamois et MeanShift](../../../vault/110-tracking-association/references/113-tracking-monoobjet.md) | [2](../../../vault/110-tracking-association/113-tracking-monoobjet.md) | [2026-10-20](113-tracking-monoobjet.md) |
| [VLM, grounding et frontière vision–action](../../../vault/120-generatif-multimodal/references/121-vlm-grounding.md) | [4](../../../vault/120-generatif-multimodal/121-vlm-grounding.md) | [2026-10-20](121-vlm-grounding.md) |
| [VAE, GAN et diffusion pour génération/restauration](../../../vault/120-generatif-multimodal/references/122-generation-restauration.md) | [3](../../../vault/120-generatif-multimodal/122-generation-restauration.md) | [2026-10-20](122-generation-restauration.md) |
| [NeRF, 3D Gaussian Splatting et reconstruction](../../../vault/120-generatif-multimodal/references/123-nerf-gaussian-splatting.md) | [3](../../../vault/120-generatif-multimodal/123-nerf-gaussian-splatting.md) | [2026-10-20](123-nerf-gaussian-splatting.md) |
| [IoU et AP — protocole COCO de détection](../../../vault/130-evaluation-fiabilite/references/131-iou-ap-coco.md) | [7](../../../vault/130-evaluation-fiabilite/131-iou-ap-coco.md) | [2026-10-20](131-iou-ap-coco.md) |
| [Évaluer identités, trajectoires et localisation 3D](../../../vault/130-evaluation-fiabilite/references/132-tracking-trajectoires.md) | [5](../../../vault/130-evaluation-fiabilite/132-tracking-trajectoires.md) | [2026-10-20](132-tracking-trajectoires.md) |
| [Splits, annotations, calibration des scores et dérive](../../../vault/130-evaluation-fiabilite/references/133-donnees-generalisation.md) | [5](../../../vault/130-evaluation-fiabilite/133-donnees-generalisation.md) | [2026-10-20](133-donnees-generalisation.md) |
| [Métriques de segmentation, inspection et applications](../../../vault/130-evaluation-fiabilite/references/134-metriques-applications.md) | [4](../../../vault/130-evaluation-fiabilite/134-metriques-applications.md) | [2026-10-20](134-metriques-applications.md) |
| [Contrats de données, profiling et pipelines vidéo](../../../vault/140-ingenierie-systemes/references/141-contrats-profiling-video.md) | [5](../../../vault/140-ingenierie-systemes/141-contrats-profiling-video.md) | [2026-10-20](141-contrats-profiling-video.md) |
| [PTQ, QAT, INT8/FP8 et runtimes](../../../vault/140-ingenierie-systemes/references/142-quantification-runtimes.md) | [5](../../../vault/140-ingenierie-systemes/142-quantification-runtimes.md) | [2026-10-20](142-quantification-runtimes.md) |
| [Déploiement edge, compression et surveillance](../../../vault/140-ingenierie-systemes/references/143-edge-reproductibilite.md) | [4](../../../vault/140-ingenierie-systemes/143-edge-reproductibilite.md) | [2026-10-20](143-edge-reproductibilite.md) |

## Enrichissements prioritaires proposés

Aucune nouvelle carte n'a été rédigée. Les propositions détaillées sont dans
les rapports ; la priorité ci-dessous est un choix éditorial à discuter, pas
une mesure de la maîtrise de l'apprenant.

| Proposition | Lacune comblée | Famille | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Contrôler NIS et résidus biaisés | Distinguer faible résidu et covariance cohérente | Évaluation | 1 carte, 3 critères ; durée à mesurer | [Gamse et al., §§2.2.2 et 3.4](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/) |
| Transporter une covariance par l'adjoint | Éviter le mélange des repères d'incertitude | Raisonnement | 1 carte, 3 critères ; durée à mesurer | [Solà et al., §II-H](https://arxiv.org/abs/1812.01537) |
| Calculer PQ sur un mini-appariement | Rendre opératoire la métrique panoptique | Évaluation | 1 carte, TP/FP/FN et IoU moyenne | [Panoptic Segmentation, §4](https://arxiv.org/abs/1801.00868) |
| Calculer l'effet d'un ID switch sur IDF1 | Passer de la distinction qualitative à un cas calculé | Raisonnement | 1 carte sur une courte séquence | [Ristani et al., métriques d'identité](https://arxiv.org/abs/1609.01775) |

## Contrôles exécutés

Contrôles exécutés le 20 octobre, puis vérifiés à la livraison du 21 octobre :

| Contrôle | Résultat |
| --- | --- |
| `python3 scripts/check_vault.py` | OK : 125 documents Markdown, 52 fiches, 224 cartes |
| `python3 -m unittest discover -s tests` | 34 tests réussis |
| `python3 scripts/sync_catalog.py --check` | 18 documents générés, aucun périmé |
| `inventaire_cartes.py vault --comparer <inventaire_base.json>` | Aucun ID ajouté/disparu, aucune identité Anki modifiée |
| `python3 examples/pilot_math.py` | IoU 2/3 ; NMS [0,2] puis [0,1,2] ; RANSAC 72/9 ; Kalman et AP cohérents |
| `python3 examples/curriculum_math.py` | Otsu 1→21 avec partition identique ; projection/associations cohérentes ; stéréo 10/20 m ; 240 images/s ; gain 1,05263 |
| `git diff --check` et relecture du diff | Aucune erreur d'espacement ; modifications du périmètre relues |

La comparaison initiale du 20 octobre a été complétée à la livraison par une
comparaison à l'inventaire du commit de départ `e5b41f0`, extrait hors du dépôt.
Des contrôles ponctuels ont aussi vérifié : une ligne de rapport par carte
(224 IDs distincts dans 52 rapports), les liens locaux du bilan et des rapports,
les colonnes des tableaux, l'absence de caractères de contrôle, les objectifs
inchangés, les révisions incrémentées et les sections historiques préservées.
Ces contrôles ponctuels ne sont pas une CI ni une nouvelle commande du dépôt.

## Limites et points ouverts

- Auto-revue d'agent, sans relecture scientifique indépendante. Les fiches ne
  sont pas promues au statut « relu ».
- [UKF](../2026-10-18/13-kalman-ekf-eskf.md) : mécanisme des sigma-points
  non vérifié dans le texte primaire intégral accessible lors du passage.
  [ECC](45-recalage-ecc.md) : résumé primaire et documentation OpenCV
  consultés ; dérivation complète du papier non vérifiable pendant la revue.
- Les limites d'accès plus locales (notamment résumé HOG et mécanisme
  GrabCut vérifié dans la documentation officielle) sont indiquées dans
  leurs rapports. Une source absente n'est pas déclarée confirmée.
- Context7 indisponible : recours direct aux documentations officielles,
  avec versions et dates consignées. Les liens `latest` restent évolutifs.
- Aucun essai réel d'export, de mise à jour Anki ou de rendu
  Obsidian/AnkiDroid pendant cette revue ; les preuves datées du 18 octobre
  n'ont pas été réécrites. Le contenu reste non synchronisé.
- Maîtrise, durée de rappel et coût réel des cartes non mesurés. Les
  contre-exemples analytiques ne constituent pas des benchmarks d'images
  ni des performances mesurées sur matériel.
