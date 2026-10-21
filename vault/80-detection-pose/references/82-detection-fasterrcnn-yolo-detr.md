---
id: CV-DETECTEURS
type: methode
domaine: d08
poles: [A, C, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 3
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

### Assignation dense : exemple FCOS

Dans FCOS décrit aux §§3.1–3.2 de l'article, les sites de prédiction remplacent les anchors, mais doivent toujours recevoir une supervision. Un site est admissible pour une boîte s'il est à l'intérieur et si sa plus grande distance aux quatre bords appartient à la plage du niveau FPN. Parmi plusieurs boîtes admissibles, celle de plus petite aire est retenue ; sans boîte admissible, le site est négatif. Le filtrage par taille réduit les ambiguïtés entre objets superposés. Ce mécanisme n'est ni une NMS ni une règle commune à tous les détecteurs anchor-free ; les variantes avec center sampling modifient la sélection des sites.

### Pyramide de features : FPN

Le chemin descendant propage les représentations sémantiques profondes vers des résolutions plus fines. Les connexions latérales ajoutent les features du backbone, moins sous-échantillonnées et mieux localisées. Dans la construction originale, une projection $1\times1$ aligne les canaux, puis une addition fusionne les cartes de même taille ; une convolution $3\times3$ suit la fusion. La pyramide ainsi construite à partir d'une image aide à traiter plusieurs échelles, notamment les petits objets, sans constituer une garantie de rappel. Simplement agrandir la dernière feature map ne restitue pas l'information des niveaux fins. Aucune pyramide ne garantit la récupération des détails supprimés dans l'image d'entrée.

## Mathématiques, conventions et unités

Une loss combine termes de classe et localisation selon l'affectation. Pour DETR, choisir une bijection de coût minimal lie cibles et requêtes ; les requêtes sans cible apprennent no-object. Ce matching d'apprentissage n'est ni la NMS ni le matching d'évaluation. Les boîtes normalisées doivent être restituées dans le bon repère.

### Cibles de boîtes en distances

Pour FCOS, utiliser des coordonnées continues dans l'image d'entrée : origine en haut à gauche, $x$ vers la droite, $y$ vers le bas, unités en pixels. Au site $(x,y)$ associé à la boîte $(x_0,y_0,x_1,y_1)$, les cibles sont

$$
(l,t,r,b)=(x-x_0,\;y-y_0,\;x_1-x,\;y_1-y).
$$

Le décodage restitue $(x-l,y-t,x+r,y+b)$. Il faut d'abord ramener le site de la feature map dans le repère image ; une éventuelle normalisation par le stride doit être inversée. Exemple analytique du projet : site $(40,30)$ et boîte $(20,10,90,70)$ donnent $(20,20,50,40)$ pixels, puis exactement la boîte initiale au décodage. Les largeurs continues n'utilisent pas de terme $+1$.

### Classification dense : Focal Loss

Avec $p_t$ la probabilité attribuée au label binaire correct, la forme pondérée est

$$
\mathrm{FL}(p_t)=-\alpha_t(1-p_t)^\gamma\log p_t.
$$

$\alpha_t$ pondère la classe ; $\gamma\geq0$ module la contribution selon la difficulté. Pour $\gamma=0$, on retrouve l'entropie croisée pondérée. Pour $\gamma>0$, les exemples déjà bien classés pèsent moins, ce qui limite l'accumulation des nombreux négatifs faciles en détection dense. À $\gamma=2$, les facteurs multiplicatifs valent $0{,}01$ pour $p_t=0{,}9$ et $0{,}81$ pour $p_t=0{,}1$ ; ils modulent la loss, pas directement son gradient. La méthode ne supprime pas les négatifs et n'est pas conçue pour neutraliser les annotations erronées parmi les cas difficiles.

### Localisation sans recouvrement : GIoU

Pour deux boîtes rectangulaires alignées sur les axes, d'aires positives, $A$ et $B$, soit $C$ le plus petit rectangle aligné sur les axes qui les contient. Avec $|\cdot|$ l'aire,

$$
\operatorname{GIoU}(A,B)=\operatorname{IoU}(A,B)-\frac{|C\setminus(A\cup B)|}{|C|},\qquad L_{\mathrm{GIoU}}=1-\operatorname{GIoU}(A,B).
$$

Si les boîtes restent strictement disjointes, $1-\operatorname{IoU}$ reste à 1 : ce terme seul n'indique pas comment les rapprocher. GIoU ajoute une pénalité géométrique sur la partie vide du rectangle englobant. Exemple analytique en coordonnées continues : $A=(0,0,2,2)$ et $B=(3,0,5,2)$ ont une union d'aire 8 et un rectangle $C$ d'aire 10, d'où GIoU $=-0{,}2$ et loss $=1{,}2$. Déplacer $B$ en $(2{,}5,0,4{,}5,2)$ réduit la loss à $10/9$, alors qu'IoU reste nul. Cela illustre le signal supplémentaire, sans garantir une convergence ou une AP supérieure pour toute recette.

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
- [FCOS, version 5, §§3.1–3.3 : sites, distances, niveaux et variantes de sélection](https://arxiv.org/html/1904.01355v5).
- [Focal Loss, version 2, §§2 et 3.1–3.2 : déséquilibre, pondération et difficulté](https://arxiv.org/html/1708.02002v2).
- [GIoU, version 2, §3 et algorithmes 1–2 : géométrie et loss](https://arxiv.org/html/1902.09630v2).
- [FPN, version 2, §3 et figure 3 : chemins descendant et latéraux](https://arxiv.org/html/1612.03144v2).
- [Cartes associées](../82-detection-fasterrcnn-yolo-detr.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.

Enrichissement du 2026-10-21 : cartes CV-DETECTEURS-006 à 010, mécanismes d’apprentissage et FPN. Sources scientifiques consultées ; calculs synthétiques vérifiés, sans entraînement ni benchmark.
