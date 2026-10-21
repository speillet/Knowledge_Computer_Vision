---
id: CV-DETECTEURS
type: methode
domaine: d08
poles: [A, C, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-IOU-AP", "CV-NMS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d08]
---
# Détection : Faster R-CNN, familles YOLO et DETR

## Problème, données et hypothèses

Localiser et classer des objets selon boîtes, scores et labels. Entrées : images et annotations avec repères/tailles ; sorties : ensemble de détections. Les particularités sont affectation, localisation et posttraitements, au-delà des bases DL déjà acquises.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-IOU-AP](../../130-evaluation-fiabilite/references/131-iou-ap-coco.md) ; [CV-NMS](81-nms.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Faster R-CNN propose des régions avec RPN puis les traite avec une tête partageant des features. YOLO regroupe plusieurs conceptions one-stage dont il faut nommer la variante. DETR prédit un ensemble et utilise un matching biparti pendant l'entraînement.

## Mathématiques, conventions et unités

Une loss combine termes de classe et localisation selon l'affectation. Pour DETR, choisir une bijection de coût minimal lie cibles et requêtes ; les requêtes sans cible apprennent no-object. Ce matching d'apprentissage n'est ni la NMS ni le matching d'évaluation. Les boîtes normalisées doivent être restituées dans le bon repère.

## Paramètres et propriétés

Résolution, assigner, poids des losses, anchors ou centres, scores, NMS/top-k. Les règles de sortie varient : la conception DETR permet de se passer de NMS. Les recettes d'une version YOLO ne définissent pas toute la famille.

## Coût et implémentation

Backbone, multiéchelles, nombre de régions/requêtes et posttraitements comptent ; mesurer toute la chaîne. Aucun modèle entraîné ou benchmark exécuté.

## Évaluation et variation contrôlée

Baseline et variation : même split par scène ; réduire la résolution puis mesurer AP par taille et rappel des petits objets. Distinguer perte d'information et simple conversion incorrecte de coordonnées.

## Échecs et diagnostic

Boxes correctes avant posttraitement mais sorties manquantes : inspecter seuils/NMS. Loss bonne mais rappel faible : vérifier assignation, labels, stride, échelle et protocole avant de changer le backbone.

## Alternatives et usages

Comparer architecture + recette + supervision + coût complet ; la catégorie one/two-stage seule ne prédit pas la qualité ni la latence.

## Sources et cartes

- [YOLOv3, §2.1 : anchors](https://arxiv.org/abs/1804.02767) et [YOLOX, §2.1 : passage anchor-free](https://arxiv.org/abs/2107.08430), exemples concrets de variantes.

- [Faster R-CNN, §3](https://arxiv.org/abs/1506.01497).
- [YOLO original, §2](https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html).
- [DETR, §§3.1–3.2](https://arxiv.org/abs/2005.12872).
- [Cartes associées](../82-detection-fasterrcnn-yolo-detr.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
