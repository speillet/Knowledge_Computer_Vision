# Cartographie initiale de la couverture

**Statut** : proposition éditoriale enrichie après revues, 2026-10-18.

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
dans la ligne d'un domaine. Champs attendus : identifiant, domaine,
problème/famille, méthode/variante, prérequis obligatoires, notions connexes,
priorité, profondeur cible, compétences visées, sources, fiche canonique,
cartes ou cas associés et états éditoriaux.

Les prérequis obligatoires sont distincts des liens thématiques. Les boucles
apparentes de prérequis sont résolues par un socle partagé explicite.
Une entrée est couverte seulement pour les compétences et la profondeur
étayées par ses artefacts ; les lacunes restantes sont conservées.

Les spécialisations seront rattachées au socle : inspection industrielle,
robotique/autonomie, documents/OCR, télédétection, imagerie médicale et autres
applications pertinentes. Leur inventaire détaillé reste à enrichir.

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
