# Cartographie initiale de la couverture

**Statut** : proposition éditoriale enrichie après revues et ajout des pôles
métiers, 2026-10-18.

Cette cartographie organise un catalogue évolutif. Les méthodes citées sont
des entrées à documenter, et non des fiches déjà produites ou une liste exhaustive
de tous les algorithmes. Les noms originaux sont conservés.

## Priorités proposées

- **V0** : lacunes exprimées — méthodes classiques, matching, calibration,
  géométrie, tracking et détection.
- **V1** : compléter le socle généraliste et les connexions entre problèmes.
- **V2** : approfondir les familles avancées et spécialisations, sans les exclure.
- **Transverse** : données, évaluation et contraintes industrielles dès les
  premières fiches.

Les priorités désignent un ordre pédagogique, pas un classement scientifique.
Elles sont notées V0 à V2 (vagues) pour ne pas être confondues avec les
priorités P1/P2 des parcours de la spec.
La segmentation sémantique déjà maîtrisée reste couverte, avec une profondeur adaptée.

## Niveaux de profondeur et compétences

La priorité indique quand travailler un sujet ; la profondeur indique le
résultat attendu. Ces informations sont distinctes de l'état de rédaction
et de la maîtrise personnelle.

| Niveau cible | Résultat observable |
| --- | --- |
| Repérage | Identifier le problème, les entrées/sorties, la famille et les limites principales |
| Usage opérationnel | Expliquer les étapes, utiliser une référence, régler les paramètres et interpréter une évaluation |
| Approfondissement | Justifier les hypothèses, reconstruire le raisonnement central, comparer et diagnostiquer un cas nouveau |

Le socle généraliste vise au moins l'usage opérationnel des familles retenues.
Les lacunes prioritaires visent l'approfondissement. Les spécialisations peuvent
commencer au repérage si cette profondeur est affichée : leur présence dans
une liste ne signifie pas qu'elles sont maîtrisées.

Chaque entrée précisera les compétences travaillées : expliquer, raisonner,
appliquer, comparer, évaluer et diagnostiquer. Une compétence n'est couverte
que si un artefact correspondant existe ; une non-applicabilité est justifiée.

## Domaines et premières entrées

| Domaine | Méthodes et notions à inventorier | Orientation proposée |
| --- | --- | --- |
| 1. Mathématiques et estimation pour la vision | SVD, moindres carrés, estimation robuste, optimisation non linéaire, conditionnement, observabilité, incertitude | Rappels contextualisés ; prérequis ML déjà acquis |
| 2. Formation et acquisition des images | Projection perspective, optique, radiométrie, couleur/gamma, bruit, exposition, échantillonnage/aliasing, rolling/global shutter, synchronisation | V1 ; acquisition et échecs de traitement |
| 3. Traitement d'image classique | Convolution, filtres gaussien/médian/bilatéral, gradients, Fourier, pyramides, morphologie, Canny, Hough, histogrammes, restauration/déconvolution | V0 ; bruit, résolution, fréquences et paramètres |
| 4. Features, matching et recalage | Harris, Shi–Tomasi, FAST, BRIEF, SIFT, ORB, AKAZE ; brute-force, FLANN, ratio test, cross-check, RANSAC ; SuperPoint, SuperGlue/LightGlue, LoFTR ; recalage par intensités/ECC | V0 ; classique/appris, sparse/dense et validation géométrique |
| 5. Calibration et géométrie multivue | Intrinsèques, extrinsèques, distorsion, mire, fisheye, stéréo/rectification, hand-eye, calibration multicapteurs caméra–LiDAR/IMU, homographie, matrices fondamentale/essentielle, PnP, triangulation, bundle adjustment | V0 ; repères, unités, observabilité et dégénérescences |
| 6. Vision 3D | StereoBM/SGBM, profondeur, SfM, odométrie, SLAM/bouclage ; normales, voxels, FPFH, RANSAC global, ICP point-to-point/point-to-plane, maillages ; fusion multicapteurs à approfondir | V1 ; échelle, initialisation et correspondances |
| 7. Reconnaissance et représentations | HOG, descripteurs globaux, classification, CNN/ResNet, ViT, apprentissage métrique, autosupervision/DINO, retrieval ; open-set et détection/localisation d'anomalies, dont PatchCore | V1 ; propriétés visuelles, anomalies et transfert |
| 8. Détection et pose | R-CNN/Faster R-CNN, familles YOLO, DETR ; one-stage/two-stage, anchors/anchor-free, pyramides de features, affectation, NMS, points clés, pose articulée 2D/3D et pose d'objet | V0 ; cibles, losses spécifiques et localisation |
| 9. Segmentation | Seuillages global/adaptatif/Otsu, composantes connexes, distance transform, watershed, region growing, graph cuts/GrabCut, contours actifs, superpixels ; U-Net/DeepLab, Mask R-CNN, sémantique, instances, panoptique, prompts et vidéo | V0 pour le classique ; V1/V2 pour les variantes moins maîtrisées |
| 10. Mouvement et compréhension vidéo | Lucas–Kanade pyramidal, Farnebäck, RAFT, flot sparse/dense ; suivi de points/CoTracker, visibilité ; two-stream, 3D CNN, modèles temporels, actions | V0 pour les bases ; causal/offline et tâches temporelles |
| 11. Tracking et association | MeanShift/CamShift, trackers monoobjet par corrélation/siamois ; Kalman, gating, affectation/Hungarian, SORT, DeepSORT, ByteTrack, ReID et cycle de vie des pistes | V0 ; identité, occlusion, caméra mobile, online/offline |
| 12. Vision générative et multimodale | VAE, GAN, diffusion, restauration/super-résolution, vision-langage, grounding, vocabulaire ouvert, modèles de fondation, représentations implicites/explicites et rendu neuronal | V2 ; objectifs, supervision, capacités et limites |
| 13. Données, évaluation et fiabilité | Annotation, ambiguïté du ground truth, splits par scène/séquence, fuites, IoU/AP, erreurs géométriques, MOTA/IDF1/HOTA, calibration des scores, incertitude, OOD, dérive et sous-groupes | Transverse ; protocoles, seuils et erreurs rares |
| 14. Ingénierie des systèmes de vision | Baselines, reproductibilité, tests, pré/posttraitements, augmentations cohérentes, profiling, latence/débit, mémoire/transferts, quantification, déploiement et surveillance ; conception de bout en bout, des exigences au choix classique/appris et à la validation | Transverse ; contrats de données et mesures complètes |

Les entrées propres aux pôles métiers, décrites plus bas, complètent ce tableau ;
chacune est rattachée à un seul domaine d'accueil.

## Axes à vérifier dans chaque famille pertinente

| Axe | Question de couverture |
| --- | --- |
| Acquisition et représentation | Quels effets ont lumière, couleur, exposition, cadence, échantillonnage et capteur ? |
| Contrat des données | Quels repères, types, plages, unités, normalisations et transformations sont supposés ? |
| Géométrie et calcul numérique | Quelles ambiguïtés, dégénérescences, sensibilités et conditions d'initialisation ? |
| Supervision | Quelles données, annotations, cibles et losses spécifiques à la tâche ? |
| Généralisation | Quelles variations, scènes inédites, erreurs rares et décalages de domaine ? |
| Évaluation | Quelle référence simple, quel protocole, quels seuils et quelles limites des métriques ? |
| Exploitation | Quel coût complet, quel diagnostic et quelle alternative sous contrainte ? |

Ces axes portent sur les particularités de la vision. Ils n'imposent ni un
nouveau cours général de ML ni la reproduction de chaque entraînement lourd.

## Profondeur dans les domaines prioritaires

### Matching et recalage

Documenter le rôle de chaque étape, les transformations supportées, les
propriétés exactes ou approximatives des descripteurs, les distances, les
paramètres, les filtres de correspondances et la vérification géométrique.
Relier les échecs à des observations : ambiguïtés, texture, apparence,
géométrie, bruit et distribution des correspondances.

Un grand nombre de correspondances ne suffit pas à démontrer la validité d'une
estimation. Chaque étape de filtrage doit avoir sa justification.

### Calibration, pose et géométrie

Expliquer ce qui est estimé, à partir de quelles observations et dans quels
repères. Traiter unités, transformations, distorsions, identifiabilité,
conditions dégénérées et limites du modèle. Les conditions minimales doivent
être données pour la variante concernée, sans généralisation abusive.

Distinguer erreur sur les observations d'ajustement et validation sur d'autres
observations. Expliquer ce que mesure une erreur de reprojection et les
conclusions qu'elle ne permet pas, seule, de tirer.

### Tracking

Distinguer monoobjet/multiobjet, mouvement/apparence, détection/association,
prédiction/mise à jour, gating/affectation, création/confirmation/fin de piste.
Relier les hypothèses de mouvement à la cadence, à la caméra et aux observations
manquantes. Traiter échanges d'identité, fragmentation, occlusion,
entrées/sorties du champ et dépendances au détecteur.

### Détection

Documenter représentation des boîtes, repères et normalisation, affectation,
localisation/classification, stratégies de sortie et posttraitements.
Relier architecture et objectif d'apprentissage à la tâche sans redonner un
cours général de DL. Inclure petits objets, recouvrement, déséquilibre,
changement d'échelle et conséquences des seuils sur le pipeline aval.

## Connexions à rendre explicites

- Calibration, estimation de pose et recalage : objectifs distincts pouvant
  intervenir dans un même pipeline.
- Flot optique, tracking et réidentification : sorties et évaluations distinctes,
  avec des connexions à expliquer.
- Géométrie, méthodes classiques et apprentissage : approches qui se combinent.
- Méthodes et métriques transverses : une fiche canonique reliée depuis
  plusieurs domaines, plutôt que des explications divergentes.

## Pôles métiers

Les six pôles ci-dessous décrivent des axes de spécialisation et les familles
de métiers correspondantes, à la demande de l'apprenant (2026-10-18). Ils forment
une surcouche des domaines : chaque entrée propre à un pôle est inventoriée dans
un seul domaine d'accueil, indiqué entre parenthèses, et un sujet partagé entre
pôles garde une seule fiche canonique.

Les intitulés de métiers sont indicatifs ; leur contenu varie selon les
entreprises. Couvrir un pôle signifie disposer des fiches, cartes et cas
correspondants, pas être prêt pour un poste.

**Socle d'abord** : la vague V0 reste consacrée aux lacunes exprimées. Dans
chaque pôle, les entrées clés visent V1 et l'usage opérationnel ; les
approfondissements sont en V2, au repérage par défaut. Relever la priorité
d'un pôle est une décision de l'apprenant, consignée dans la spec.
Une notion déjà en V0 conserve sa priorité : son rattachement à un pôle
ne la reporte pas artificiellement en V1.

| Pôle | Périmètre | Métiers indicatifs | Domaines mobilisés |
| --- | --- | --- | --- |
| A. Deep Learning & Image Understanding | Classification, détection, segmentation, reconnaissance, vision transformers et modèles de fondation visuels | 2D CV Engineer, Visual Recognition Engineer, Vision Foundation Model Engineer | 7, 8, 9, 12, 13 |
| B. Geometric Vision & Spatial AI | Reconstruction 3D, calibration, estimation de pose, SLAM, VIO et géométrie multivue | 3D Vision Engineer, VIO Engineer, SLAM Engineer, Spatial AI Engineer | 1, 2, 4, 5, 6, 12, 13 |
| C. Robotics & Autonomous Perception | Fusion de capteurs, perception temps réel, estimation d'environnement et navigation | Robotics Perception Engineer, Autonomous Perception Engineer, Sensor Fusion Engineer | 1, 2, 5, 6, 8, 11, 13, 14 |
| D. Multimodal AI & Video Intelligence | VLM, alignement image-texte, compréhension vidéo, grounding et modèles vision-langage-action | Multimodal AI Engineer, Video AI Engineer, VLM Research Engineer | 7, 10, 12, 13 |
| E. Applied Computer Vision | Télédétection, imagerie médicale, inspection industrielle, biométrie et analyse documentaire | Remote Sensing AI Engineer, Medical Imaging AI Engineer, Industrial Vision Engineer | 2, 7, 9, 13, 14 |
| F. Vision Systems & Deployment | Optimisation GPU, déploiement embarqué, quantification et pipelines vidéo à faible latence | Edge AI Engineer, Computer Vision Systems Engineer, Inference Optimization Engineer | 2, 3, 13, 14 |

### A — Deep Learning & Image Understanding

- **Entrées clés (V1/U)** : ViT, Swin et ConvNeXt (d07) ; DINOv2 et features
  autosupervisées (d07) ; alignement image-texte CLIP/SigLIP, partagé avec D (d07) ;
  SAM et SAM 2 (d09) ; détection open-vocabulary Grounding DINO et OWL-ViT (d08) ;
  adaptation par linear probing, fine-tuning et LoRA/adapters (d07) ; long-tail,
  stratégie d'annotation et active learning (d13) ; mIoU, PQ et AP par taille
  d'objet (d13).
- **Approfondissements (V2/R)** : pré-entraînement masqué MAE et effets
  d'échelle (d07) ; modèles de fondation multitâches comme Florence-2 (d12).
  La distillation est rattachée au pôle F (d14).
- **Cas propres** : conception — choisir entre un détecteur fermé réentraîné et
  une détection open-vocabulary pour un catalogue de produits qui change chaque
  mois ; diagnostic — AP des petits objets qui chute après une réduction de la
  résolution d'entrée.

### B — Geometric Vision & Spatial AI

- **Entrées clés (V1/U)** : groupes SO(3)/SE(3) et paramétrisations des
  rotations (d01) ; graphes de facteurs, GTSAM et iSAM2 (d01) ; bundle adjustment
  creux et complément de Schur (d05) ; VIO : préintégration IMU, MSCKF,
  VINS-Mono et OKVIS (d06) ; fermeture de boucle et reconnaissance de lieux,
  DBoW2 et NetVLAD (d06) ; reconstruction dense MVS et fusion TSDF (d06) ;
  ATE et RPE (d13).
- **Approfondissements (V2/R)** : DUSt3R et MASt3R (d06) ; profondeur
  monoculaire, Depth Anything (d06) ; NeRF et 3D Gaussian Splatting (d12) ;
  caméras événementielles (d02).
- **Cas propres** : conception — localisation d'un casque de réalité augmentée
  en intérieur, avec caméras et IMU, sous contrainte de latence ; diagnostic —
  dérive d'échelle et de lacet d'un VIO dans un couloir peu texturé, en séparant
  erreurs d'estimation, excitation insuffisante et jauge globale de yaw.

### C — Robotics & Autonomous Perception

- **Entrées clés (V1/U)** : filtres EKF, UKF et ESKF pour la fusion (d01) ;
  LiDAR, radar et ToF, formation des mesures et bruit (d02) ; horodatage et
  synchronisation matériels (d02) ; calibration extrinsèque
  caméra–LiDAR–radar–IMU et décalage temporel (d05) ; représentations de nuages
  de points, PointNet++ et voxels (d06) ; odométrie et localisation LiDAR, LOAM
  et NDT (d06) ; vue de dessus (BEV) et grilles d'occupation, Lift-Splat-Shoot,
  BEVFormer et BEVFusion (d06) ; détection 3D PointPillars et CenterPoint (d08) ;
  suivi 3D multiobjet, AB3DMOT (d11) ; NDS et mAP 3D (d13) ; ROS 2 et budgets
  de latence temps réel (d14).
- **Approfondissements (V2/R)** : espace libre et traversabilité (d06) ;
  représentations de surfaces implicites occupancy/SDF (d06), à distinguer
  des grilles probabilistes libre/occupé/inconnu utilisées par un robot.
- **Périmètre** : la planification de trajectoire et le contrôle sont hors
  périmètre ; seule la perception qui les alimente est couverte.
- **Cas propres** : conception — perception d'un robot mobile d'entrepôt avec
  caméras et LiDAR, sous exigences de sécurité ; diagnostic — obstacles dédoublés
  après fusion caméra–LiDAR lorsque le robot tourne.

### D — Multimodal AI & Video Intelligence

- **Entrées clés (V1/U)** : CLIP/SigLIP (fiche d07 partagée avec A) ;
  architectures VLM BLIP-2, LLaVA et Flamingo, tokenisation visuelle (d12) ;
  grounding et segmentation référentielle (d12) ; transformers vidéo TimeSformer,
  ViViT et VideoMAE (d10) ; localisation temporelle d'actions (d10) ; évaluation
  des VLM : hallucination, contamination des benchmarks et sensibilité au
  prompt (d13).
- **Approfondissements (V2/R)** : video-LLM et vidéo longue, échantillonnage
  de frames et mémoire (d10) ; modèles vision-langage-action RT-2, OpenVLA
  et π0 (d12).
  Les VLA sont étudiés comme frontière perception/action : leurs sorties
  et limites sont expliquées, sans implémenter une politique de commande
  robotique ou étendre le périmètre au contrôle.
- **Cas propres** : conception — indexer des heures de vidéo de surveillance
  avec un VLM généraliste ou un pipeline détection, tracking et règles ;
  diagnostic — VLM qui décrit des objets absents sur des images industrielles
  hors distribution.

### E — Applied Computer Vision

- **Entrées clés (V1/U), inspection industrielle** : éclairage, optiques
  télécentriques et caméras line-scan (d02) ; golden template et détection
  d'anomalies PatchCore, PaDiM (d07) ; métrologie et Gauge R&R (d13).
  L'inspection est retenue comme cas industriel central.
- **Approfondissements (V2/R), par application** :
  - Télédétection : imagerie multispectrale et SAR, géoréférencement (d02) ;
    détection de changements (d09) ; tuilage de grandes images (d14).
  - Imagerie médicale : formats DICOM/NIfTI et volumes (d02) ; nnU-Net (d09) ;
    Dice, HD95, validation externe et distinction entre performance algorithmique
    et utilité clinique (d13).
  - Biométrie : reconnaissance faciale ArcFace et détection d'attaques par
    présentation, cadre ISO/IEC 30107 à versionner lors de son étude (d07) ;
    FMR/FNMR, FAR/FRR selon le protocole, EER, métriques PAD et sous-groupes (d13).
  - Documents : OCR CRNN/CTC et TrOCR, mise en page LayoutLM, Donut sans OCR
    (d07) ; CER et WER (d13).
- **Cas propres** : conception — inspection de défauts rares sur une ligne
  cadencée avec très peu d'exemples défectueux ; diagnostic — modèle de
  télédétection qui se dégrade d'une saison à l'autre.

### F — Vision Systems & Deployment

- **Entrées clés (V1/U)** : modèle d'exécution GPU, hiérarchie mémoire,
  transferts et profilage Nsight (d14) ; runtimes TensorRT, ONNX Runtime,
  OpenVINO et LiteRT (d14) ; PTQ/QAT, granularité et calibration représentative,
  avec INT8/FP8 selon opérateurs, runtime et matériel (d14) ; pruning
  et distillation, utiles aussi au pôle A (d14) ; pipelines vidéo : décodage
  matériel NVDEC, GStreamer/DeepStream, zéro-copie, batching et contre-pression
  (d14) ; budget de latence de bout en bout, p50/p99 et gigue (d14).
- **Approfondissements (V2/R)** : cibles embarquées Jetson et NPU, consommation
  et thermique (d14) ; serving avec Triton (d14) ; mises à jour OTA et
  surveillance en périphérie (d14).
- **Cas propres** : conception — huit flux 1080p à 30 images/s sur un module
  embarqué, avec un p99 contraint ; diagnostic — quantification INT8 sans gain
  de latence parce que le goulot est le prétraitement CPU ou les transferts.

## Pilote pédagogique proposé

| Sujet | Ce qu'il permet de vérifier dans la conception |
| --- | --- |
| SIFT | Fiche développée, invariances, équations et paramètres |
| ORB | Comparaison, représentation, distance et contraintes de calcul |
| RANSAC appliqué à une homographie | Hypothèses, estimation robuste et diagnostic géométrique |
| Calibration sur mire, méthode de Zhang | Repères, paramètres caméra et validation |
| SORT et ses limites | Estimation d'état, association, identités et diagramme de pipeline |
| NMS en détection | Posttraitement, seuils, cas d'échec et évaluation |
| IoU et AP, protocole COCO | Fiche de type métrique/protocole, canonique et reliée depuis la détection, la segmentation et l'association de SORT |

Ce premier étage vérifie le format sur les lacunes immédiates. Un second
étage contrasté est proposé avant généralisation :

| Extension du pilote | Risque pédagogique éprouvé |
| --- | --- |
| Otsu, distance transform et watershed | Pipeline classique, tâches distinctes et diagnostic des marqueurs |
| SuperPoint + LightGlue face à une référence classique | Méthode apprise, composants, protocole et coûts comparables |
| ICP local et initialisation par recalage global | Géométrie 3D, repères, minimum local et évaluation |

Le pilote comprend sept sujets initiaux et trois extensions, pas dix fiches
au format imposé. Une comparaison ou un pipeline peut relier plusieurs fiches
canoniques. Les deux étages restent des propositions à valider.

## Suivi de couverture pendant la production

Chaque méthode retenue aura une entrée identifiable, au-delà d'une mention
dans la ligne d'un domaine. Champs attendus : identifiant, domaine, pôles servis,
problème/famille, méthode/variante, prérequis obligatoires, notions connexes,
priorité, profondeur cible, compétences visées, sources, fiche canonique,
cartes ou cas associés et états éditoriaux.

Les prérequis obligatoires sont distincts des liens thématiques. Les boucles
apparentes de prérequis sont résolues par un socle partagé explicite.
Une entrée est couverte seulement pour les compétences et la profondeur
étayées par ses artefacts ; les lacunes restantes sont conservées.

Les spécialisations sont décrites par les pôles C (robotique et autonomie)
et E (télédétection, imagerie médicale, inspection, biométrie et documents).
Leur inventaire détaillé reste à enrichir à chaque lot.

## Sources de cadrage

- [Cursus classique de CMU](https://www.cs.cmu.edu/~16385/s14/) : formation
  des images, traitement, géométrie, mouvement et correspondances.
- [CS231n de Stanford](https://cs231n.stanford.edu/schedule) : apprentissage,
  reconnaissance, détection, segmentation, vidéo, 3D et multimodalité.
- [OpenCV 4.13 — features et matching](https://docs.opencv.org/4.13.0/db/d27/tutorial_py_table_of_contents_feature2d.html).
- [OpenCV 4.13 — calibration et géométrie](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [OpenCV 4.13 — mouvement et tracking](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html).
- [ByteTrack — dépôt des auteurs](https://github.com/FoundationVision/ByteTrack).

Les ajouts et leurs sources sont détaillés dans [la revue de pertinence](review.md).
Le catalogue ne doit pas être limité aux méthodes d'une bibliothèque particulière.

Ces sources étayent le découpage et l'inventaire. Chaque fiche produite devra
citer ses propres sources primaires et vérifier les caractéristiques de la
variante expliquée ; aucune préférence universelle entre méthodes n'est présumée.
