# Revue de profondeur et cohérence — 2026-10-24

## Résultat

Les 60 sujets et leurs 282 cartes ont été examinés sur l'objectif de rappel,
la pertinence pour un ingénieur confirmé et le développement des explications.
**274 réponses enrichies**, huit conservées car déjà développées ; aucun ajout
ni retrait de carte. Les 60 fiches canoniques prennent une révision et relient
leurs propriétés à deux cas guidés, avec question et réponse de référence.

| Mots lexicaux par réponse | Avant | Après |
| --- | ---: | ---: |
| Minimum | 32 | 180 |
| Médiane | 57 | 200,5 |
| Maximum | 252 | 329 |

Calcul : `len(re.findall(r'\w+', Reponse))`, sans compter question, Source ou
tags. Le seuil de 180 est un choix éditorial propre à cette demande : il repère
les réponses de quelques lignes, sans établir une longueur optimale ni garantir
la qualité. La réponse reste notée sur un noyau fini ; les explications longues
servent à comprendre et reconstruire, sans récitation intégrale.

## Pertinence et corrections de conception

Le lot est pertinent pour le profil : mécanismes classiques, contrats des
méthodes modernes, géométrie, évaluation et décisions industrielles. La faiblesse
récurrente était de donner une conclusion correcte sans assez expliquer comment
la retrouver ou vérifier qu'elle s'applique. Les ajouts explicitent mécanisme,
cas interprété, hypothèses et contrôle discriminant, plutôt qu'une définition
isolée ou un résultat de benchmark sans contexte.

Les cartes de synthèse et leurs approfondissements restent distincts : SIFT
pipeline versus construction du descripteur ; flot apparent versus algorithme
Farnebäck ; filtrage SORT versus choix d'association ; rang/identifiabilité
versus covariance locale. Aucun retrait d'objectif n'est justifié dans cette
passe. Les familles pertinentes dépendent du sujet : ajouter huit familles à
chaque algorithme créerait des répétitions sans nouvel objectif utile.

Les nouveaux calculs sont des déductions sous hypothèses et les ablations sont
proposées. Ils ne constituent pas des mesures publiées ni des expériences image,
vidéo, capteur ou matériel exécutées. Les noyaux antérieurs restent conservés.
Le lien TensorRT Quantization Workflows a été confirmé depuis la navigation
primaire après un premier échec d'extraction ; la date de consultation de la
fiche est actualisée, sans modifier les champs Source des cartes.

## Cohérence du parcours

Le [parcours senior](../../../vault/01-Parcours/Parcours-senior.md) donne neuf
étapes et un ordre explicite des 60 sujets, adapté aux acquis ML/DL/segmentation.
Les numéros thématiques ne définissent plus implicitement la progression.
L'IoU précède NMS/SORT ; le filtrage précède l'association ; repères et calibration
précèdent fusion/reconstruction. Les prérequis sont des notions requises : toute
l'AP COCO n'est pas exigée pour SORT, ni tout l'ESKF pour le Kalman linéaire.

Chaque étape propose un critère de passage. Trois intégrations vérifient le
transfert : recalage/métrologie, détection/suivi, perception spatiale. Ce sont
des exercices proposés, sans résultat annoncé. L'ordre et la couverture sont
contrôlés par script ; un prérequis inconnu, un cycle, un doublon ou un sujet
absent font échouer le contrôle.

Les 119 approfondissements APP restent ouverts. Ce travail améliore le lot
courant et ne prétend couvrir tous les algorithmes de computer vision ni
certifier une maîtrise senior.

## Rapports par sujet

Chaque rapport indique les cartes, les sources réellement consultées et la
portée de la confrontation. Les chiffres de longueur et la traçabilité sont
automatiques ; les verdicts de pertinence sont une auto-revue par agent.

| Rapport | Cartes | Réponses enrichies | Point développé |
| --- | ---: | ---: | --- |
| [CV-SVD](11-moindres-carres-svd.md) | 9 | 5 | blanchiment, perte de rang et distinction ajustement–identifiabilité |
| [CV-SE3](12-rotations-se3.md) | 6 | 5 | composition des repères et perturbations gauche/droite |
| [CV-FUSION](13-kalman-ekf-eskf.md) | 6 | 5 | innovations, covariance et réinitialisation de l’ESKF |
| [CV-FACTEURS](14-graphes-facteurs.md) | 5 | 4 | graphe, jauge et coût d’une élimination |
| [CV-ACQUISITION](21-exposition-bruit-echantillonnage.md) | 4 | 4 | exposition, bruit et échantillonnage reliés à la tâche |
| [CV-CAPTEURS](22-capteurs-horodatage.md) | 4 | 4 | séparer temps d’exposition, lecture et synchronisation |
| [CV-IMAGERIES](23-imageries-specialisees.md) | 3 | 3 | géométrie physique, line-scan et unité de généralisation |
| [CV-FILTRES](31-filtrage-gradients.md) | 4 | 4 | effet du support, unités du bilatéral et sous-échantillonnage |
| [CV-CANNY-HOUGH](32-canny-hough.md) | 4 | 4 | relier contours, votes et validation géométrique |
| [CV-MORPHO](33-morphologie-composantes.md) | 3 | 3 | support géométrique, topologie et convention de connectivité |
| [CV-SIFT](41-sift.md) | 7 | 7 | normalisations, ambiguïté du ratio et couverture géométrique |
| [CV-ORB](42-orb.md) | 6 | 6 | séparer détection, orientation, représentation et norme |
| [CV-MATCHING](43-detecteurs-matchers.md) | 4 | 4 | contrats des étapes et diagnostic avant changement de méthode |
| [CV-MATCH-APPRIS](44-superpoint-lightglue-loftr.md) | 5 | 5 | compatibilité features–matcher, résolution et validation |
| [CV-ECC](45-recalage-ecc.md) | 3 | 3 | critère photométrique, bassin de convergence et masques |
| [CV-CORNERS](46-harris-shi-tomasi.md) | 5 | 5 | tenseur de structure, directions observables et répétabilité |
| [CV-FAST-BRIEF](47-fast-brief.md) | 5 | 5 | test de segment et signature binaire sous transformations |
| [CV-FLANN](48-flann.md) | 4 | 4 | rappel des voisins, ratio et amortissement de l’index |
| [CV-HOMOGRAPHIE](51-ransac-homographie.md) | 7 | 7 | succès d’échantillonnage, couverture et validité du modèle |
| [CV-ZHANG](52-calibration-zhang.md) | 7 | 7 | contraintes des vues, resize et contrôle hors apprentissage |
| [CV-EPIPOLAIRE](53-epipolaire-pnp-triangulation.md) | 5 | 5 | épipolarité, pose et profondeur distinguées par leur contrat |
| [CV-BA](54-bundle-adjustment.md) | 4 | 4 | jauge, résidus robustes et blocs d’optimisation |
| [CV-MULTICALIB](55-calibration-multicapteurs.md) | 3 | 3 | séparer transformations spatiales et désynchronisation |
| [CV-FISHEYE](56-calibration-fisheye.md) | 5 | 5 | couverture angulaire et compatibilité du modèle de projection |
| [CV-HANDEYE](57-calibration-hand-eye.md) | 5 | 5 | conventions AX=XB, excitation et validation indépendante |
| [CV-STEREO](61-stereo-profondeur.md) | 4 | 4 | disparité, incertitude de profondeur et géométrie rectifiée |
| [CV-ICP](62-recalage-global-icp.md) | 5 | 5 | initialisation, correspondances et directions peu contraintes |
| [CV-VIO](63-slam-vio.md) | 5 | 5 | fusion inertielle, jauges et évaluation sans masquer les erreurs |
| [CV-BEV](64-nuages-bev-occupation.md) | 5 | 5 | visibilité, inconnue et limites de la représentation spatiale |
| [CV-REPRESENTATIONS](71-representations-transfert.md) | 5 | 5 | biais d’architecture, échelle et protocole de transfert |
| [CV-CLIP](72-clip-siglip.md) | 4 | 4 | contraste image–texte, candidats et décalage de domaine |
| [CV-ANOMALIES](73-patchcore-padim.md) | 4 | 4 | référence normale, voisinage de patches et décision métier |
| [CV-OCR](74-ocr-documents.md) | 3 | 3 | chaîne OCR, normalisation et métrique adaptée au document |
| [CV-BIOMETRIE](75-embeddings-biometrie.md) | 2 | 2 | vérification, identification et point d’exploitation |
| [CV-NMS](81-nms.md) | 6 | 6 | suppression, seuil d’égalité et rappel des objets proches |
| [CV-DETECTEURS](82-detection-fasterrcnn-yolo-detr.md) | 13 | 12 | contrats d’architecture, appariement et décomposition des erreurs |
| [CV-OPENVOC](83-detection-open-vocabulary.md) | 3 | 3 | vocabulaire variable, protocole et sortie localisée |
| [CV-POSE3D](84-detection-pose-3d.md) | 4 | 4 | contrat métrique et ambiguïtés de pose/symétrie |
| [CV-WATERSHED](91-otsu-distance-watershed.md) | 5 | 5 | histogramme, distance et rôle des marqueurs |
| [CV-GRABCUT](92-grabcut-regions.md) | 3 | 3 | optimisation conditionnelle et rôle des contraintes utilisateur |
| [CV-SEGMENTATION](93-semantique-instances-panoptique.md) | 4 | 4 | unité de sortie et agrégation des erreurs de segmentation |
| [CV-SAM](94-sam-sam2.md) | 3 | 3 | prompts, ambiguïté de masque et mémoire temporelle |
| [CV-FLOT](101-flot-optique.md) | 4 | 4 | contrainte de luminance, ouverture et correspondance dense |
| [CV-VIDEO](102-points-actions-video.md) | 4 | 4 | trajectoires de points, visibilité et horizon temporel |
| [CV-FARNEBACK](103-farneback.md) | 5 | 5 | approximation quadratique et domaine de capture du déplacement |
| [CV-SORT](111-sort.md) | 8 | 8 | filtrage, affectation et cycle de vie des pistes |
| [CV-ASSOCIATION](112-deepsort-bytetrack.md) | 4 | 4 | gating, apparence et association des scores faibles |
| [CV-SOT](113-tracking-monoobjet.md) | 2 | 2 | recherche locale, adaptation et identité après occultation |
| [CV-CORRELATION](114-mosse-kcf.md) | 5 | 5 | circulant, fenêtre et risque de contamination du modèle |
| [CV-MEANSHIFT](115-meanshift-camshift.md) | 4 | 4 | backprojection, mode local et adaptation de la fenêtre |
| [CV-VLM](121-vlm-grounding.md) | 4 | 4 | connecteur, ancrage visuel et test de dépendance à l’image |
| [CV-DIFFUSION](122-generation-restauration.md) | 3 | 3 | distribution conditionnelle et fidélité de la restauration |
| [CV-RENDU3D](123-nerf-gaussian-splatting.md) | 3 | 3 | synthèse de vues, support d’observation et géométrie |
| [CV-IOU-AP](131-iou-ap-coco.md) | 7 | 7 | appariement, classement et conventions COCO |
| [CV-METRIQUES-TEMPS](132-tracking-trajectoires.md) | 5 | 5 | identité, agrégation HOTA et alignement de trajectoire |
| [CV-FIABILITE](133-donnees-generalisation.md) | 5 | 5 | unité de split, sélection et calibration des probabilités |
| [CV-METRIQUES-APPLIQUEES](134-metriques-applications.md) | 4 | 4 | topologie, surfaces physiques et références incertaines |
| [CV-PIPELINE](141-contrats-profiling-video.md) | 5 | 5 | contrats, files et âge de l’information |
| [CV-QUANT](142-quantification-runtimes.md) | 5 | 5 | échelle, saturation et exécution réelle du runtime |
| [CV-DEPLOIEMENT](143-edge-reproductibilite.md) | 4 | 4 | goulot séquentiel, régime thermique et reproductibilité |

## Contrôles exécutés

Référence de comparaison : `8c428b458753740737bbc79659eaa2fd797a6a17`.
Préparation initiale sur `docs/deepen-cards-and-learning-path`. Les preuves
ci-dessous décrivent les contrôles locaux avant publication ; les PR et leurs
fusions se suivent dans l'historique GitHub du dépôt.

- `python3 scripts/check_vault.py` : **OK, 142 Markdown, 60 fiches, 282 cartes**.
- `python3 scripts/learning_path.py` : **OK, 60 sujets ordonnés, 282 réponses,
  minimum 180 mots lexicaux, aucune erreur**.
- `python3 scripts/sync_catalog.py --check` : **19 documents, aucun périmé**.
- `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` :
  **55 tests réussis**, aucun ignoré. Cinq nouveaux tests couvrent ordre des
  dépendances, cycle, prérequis inconnu, sujet absent/dupliqué/inconnu et le
  parcours réel.
- `python3 examples/pilot_math.py` : calculs du pilote exécutés, sans changement
  de leurs attentes. Ce ne sont pas des expériences sur des images.
- Inventaire du skill `revue-cartes`, comparaison au snapshot initial : **aucun
  ID disparu, ajouté ni identité Anki modifiée**. Vérification complémentaire :
  questions, objectifs, Source, tags, sous-decks, noyaux et erreurs bloquantes
  inchangés.
- `uv run --no-project --with genanki==0.13.1 python scripts/build_apkg.py`, puis
  `python3 scripts/build_apkg.py --verifier dist/CV-Pilote.apkg` : **OK, 282 notes
  et cartes, 14 sous-decks, un SVG embarqué**.
- Comparaison au paquet local initial : **274 notes modifiées, zéro ajout,
  zéro retrait ; les 282 GUID et le modèle 1153189853 sont conservés**. Il s'agit
  d'un paquet de travail issu d'un arbre modifié, pas d'une release.
- `uv run --no-project --python 3.12 --with anki==26.9.3 --with genanki==0.13.1
  python scripts/simulate_anki_import.py` : **OK**, import et réimport du même
  paquet, trois cartes révisées, modification de réponse puis de réponse/style
  dans une copie. Identités et historique conservés, mises à jour appliquées,
  aucun doublon dans la collection jetable.
- `git diff --check` : aucune erreur d'espace. Catalogue et liens du vault
  contrôlés ; le paquet généré reste hors Git.

## Portée de la revue et limites

Auto-revue pédagogique et confrontation documentaire **ciblée**, agent Codex,
2026-10-24. Les sources centrales sont des articles ou documentations primaires ;
Context7 a servi aux vérifications OpenCV. Les rapports distinguent les passages
lus des résumés, des déductions et des accès échoués avec leur repli. Toutes les
affirmations du contenu antérieur ne sont pas reconfirmées ligne à ligne dans
cette passe. Aucun contenu n'est déclaré « relu » par une personne indépendante.

Les tests vérifient la structure, les identités et l'import dans le moteur Anki,
sans prouver le rendu Obsidian/AnkiDroid, l'import sur le téléphone ou l'efficacité
du rappel. Les sessions d'apprentissage et essais applicatifs restent à réaliser.
Les preuves datées antérieures du journal sont conservées.
