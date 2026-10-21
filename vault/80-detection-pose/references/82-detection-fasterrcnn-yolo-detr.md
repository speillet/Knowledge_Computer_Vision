---
id: CV-DETECTEURS
type: methode
domaine: d08
poles: [A, C, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 5
prerequis: ["CV-IOU-AP", "CV-NMS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d08]
---
# Détection : Faster R-CNN, familles YOLO et DETR

## Problème, données et hypothèses

Localiser et classer des objets selon boîtes, scores et labels. Entrées : images et annotations avec repères/tailles ; sorties : ensemble de détections. Les particularités sont affectation, localisation et posttraitements, au-delà des bases DL déjà acquises.

### Plusieurs instances, plusieurs classes, plusieurs labels

Le nombre d'objets et le nombre de classes sont deux dimensions distinctes.
Détecter trois voitures et deux vélos demande cinq localisations d'instances,
réparties sur deux catégories présentes dans l'image. Un modèle de détection
multiclasse peut donc produire plusieurs objets de chaque classe ; il ne se
réduit ni à un label pour l'image entière ni à une boîte par classe.

La classification **multi-étiquette** concerne plusieurs labels valides pour
une même instance, si la taxonomie le prévoit. Par exemple, un contrat peut
retenir à la fois « véhicule » et « voiture » ; d'autres jeux n'annotent que
la catégorie la plus spécifique. Deux labels exclusifs proposés sur le même
objet représentent une ambiguïté à résoudre, pas automatiquement deux objets.
Les cas et leur politique d'annotation sont des exemples du projet.

YOLOv3 §2.2 illustre la distinction : ses classifieurs logistiques indépendants
permettent une formulation multi-étiquette, contrairement à un softmax modélisant
des classes exclusives. Cela ne suffit pas à déterminer les
labels finaux : supervision, seuils, éventuel choix de la meilleure classe et
posttraitement doivent suivre le contrat. Ne pas attribuer ce choix à toutes
les versions YOLO. [YOLOv3 v1, §2.2](https://arxiv.org/html/1804.02767v1)

Pour l'inférence et l'évaluation, conserver le triplet boîte, score et classe
pour chaque hypothèse, ainsi que son image d'origine. Distinguer ensuite :
plusieurs hypothèses d'une instance, plusieurs instances de même classe et
objets de classes différentes qui se recouvrent. Les
[cas NMS multiclasses et multi-instances](81-nms.md#détections-multiples-classes-et-tailles-de-boîtes)
montrent pourquoi le recouvrement seul ne tranche pas cette identité.

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

### Expérience proposée : ne faire varier que la résolution

Ce protocole du projet est **à exécuter** ; aucun résultat sur images n'est disponible.

1. **Baseline** : choisir un checkpoint et un backend acceptant les deux tailles, figer poids, classes et jeu de validation annoté, séparé de l'entraînement par scène. Consigner les versions et la politique d'annotation. Utiliser une entrée letterbox $1280\times1280$.
2. **Variation** : passer à $640\times640$, sans réentraînement. Garder interpolation, normalisation, politique de padding, seuil de score, NMS éventuelle et plafonds de détections identiques. Seules les dimensions et les transformations de coordonnées qui en découlent changent. Archiver les prédictions décodées avant filtrage, après seuil de score, puis après NMS ou le posttraitement propre au modèle.
3. **Prédiction à confronter** : les petits objets pourraient perdre des détails ou être moins bien localisés ; le coût du réseau pourrait baisser. Ce sont des hypothèses, ni une baisse d'AP nécessaire ni une promesse de latence totale.
4. **Mesures** : remettre toutes les boîtes dans l'image d'origine. Comparer AP50, AP75, AP par taille et rappel à score/IoU fixés, avec les mêmes règles d'ignore/crowd et de plafonnement. Définir les strates de taille une seule fois depuis les annotations d'origine, selon le protocole choisi ; ne pas déplacer un objet de strate parce qu'on a réduit l'entrée. Pour chaque étape de filtrage, mesurer la couverture des mêmes GT, de bonne classe et au même seuil IoU, sans compter les doublons comme des objets supplémentaires.
5. **Diagnostic et coût** : examiner les erreurs par classe, taille, densité et étape, ainsi que les images correspondantes. Chronométrer décodage, resize/transferts, réseau et posttraitement sur le même matériel, précision et batch, avec échauffement et répétitions documentés ; rapporter latence complète et dispersion. Un cas où la GT n'est plus couverte après NMS distingue un problème de sélection d'une absence de proposition correcte.
6. **Conclusion limitée** : formuler une hypothèse à partir des cas et tester ensuite une seule correction sur validation. Figer les choix avant test. Un gain sur ce jeu et ce checkpoint ne classe pas universellement Faster R-CNN, YOLO et DETR.

Le cadre AP est celui de la [fiche IoU/AP](../../130-evaluation-fiabilite/references/131-iou-ap-coco.md) ; les seuils de score, de NMS et d'évaluation restent distincts.

## Échecs et diagnostic

Boxes correctes avant posttraitement mais sorties manquantes : inspecter seuils/NMS. Loss bonne mais rappel faible : vérifier assignation, labels, stride, échelle et protocole avant de changer le backbone.

### Lire les erreurs au-delà de l'AP globale

TIDE §2.2 sépare six familles. Dans les cas simples sans ignore/crowd, les seuils $t_b=0{,}1$ et $t_f=0{,}5$ servent ici d'illustration, comme dans l'article ; ils ne sont pas universels. Le tableau évite les égalités aux seuils et les conflits entre plusieurs GT, qui demandent les règles complètes de l'outil.

| Famille | Lecture d'un cas simple | Vérification proposée par le projet |
| --- | --- | --- |
| Classification | Bonne localisation, mauvaise classe | Classes proches, définition des labels et annotations |
| Localisation | Bonne classe, recouvrement intermédiaire entre $t_b$ et $t_f$ | Repère, cibles, précision des boîtes et échelle |
| Classification et localisation | Mauvaise classe et recouvrement intermédiaire | Examiner conjointement image, label et boîte |
| Doublon | Bonne classe et recouvrement suffisant, GT déjà associée à une détection mieux scorée | Classe, scores et posttraitement ; ne pas compter deux TP |
| Fond | Recouvrement inférieur à $t_b$ avec toutes les GT | Faux objet ou objet réel non annoté |
| GT manquée | GT non détectée et non déjà expliquée par les erreurs de classification/localisation | Couverture avant/après filtrage, échelle, occultation et données |

Trois situations indépendantes avec une seule GT « voiture » : IoU $0{,}8$ et classe « camion » donnent une erreur de classification ; IoU $0{,}3$ et classe « voiture », une erreur de localisation ; une seconde boîte « voiture » d'IoU $0{,}8$ après une boîte mieux scorée déjà associée, un doublon. Ces classifications utilisent les hypothèses du cas, pas une causalité déduite d'un score agrégé.

Le nombre brut d'erreurs ne mesure pas leur effet sur l'AP : leur rang par score compte. TIDE estime des effets par corrections oracles appliquées séparément à la même baseline (§§2.2–2.3). Ces gains ne s'additionnent pas en général (annexe A.1) et ne prédisent pas le gain d'un réentraînement réel. Les contrôles proposés ci-dessus sont des pistes, pas des causes prouvées par la taxonomie.

### Qualité des annotations

Une détection non associée à une GT et non ignorée est comptée FP par le protocole, même si une inspection confirme un objet réel omis. Un score élevé ne suffit pas à trancher : vérifier l'image, la classe attendue, les objets partiels, les conventions de boîte, les exclusions et le traitement crowd/ignore. TIDE §3.4 et annexe D montrent des exemples d'annotations manquantes ou ambiguës ; l'annexe E montre aussi que la gestion des détections ignorées influence le diagnostic.

Protocole proposé par le projet : examiner un échantillon documenté sans privilégier un modèle, appliquer des règles d'annotation stables, faire arbitrer les cas ambigus, puis versionner les corrections. Réévaluer tous les modèles comparés sur cette même version, en conservant les résultats antérieurs. Ne pas retirer sélectivement les FP d'un modèle pour améliorer son score. Une omission d'objet est différente d'une exclusion intentionnelle par la politique du jeu.

### Tailles, rapports d'aspect et précision des boîtes

Une même image peut contenir simultanément de petites et grandes boîtes,
carrées ou allongées. Une taille d'entrée fixe n'impose pas des dimensions de
boîtes fixes : les coordonnées sont régressées ; niveaux de features et,
selon la méthode, formes d'anchors organisent les prédictions. YOLOv3 décrit
par exemple sa régression au §2.1 et ses prédictions à plusieurs échelles
au §2.3 ; FCOS utilise les distances et plages déjà présentées ici.

La taille relative des boîtes compte aussi **après** la prédiction. Une inclusion
peut avoir une faible IoU : voir le [calcul NMS](81-nms.md#inclusion-et-boîtes-de-tailles-très-différentes).
À l'évaluation, une même erreur absolue peut pénaliser très différemment les
objets. Cas analytiques du projet, rectangles alignés sur les axes, coordonnées
continues dans un même repère en pixels,
boîte prédite de même largeur/hauteur que sa GT mais translatée :

| Taille GT et prédiction | Translation $(\Delta x,\Delta y)$ | Intersection / union | IoU |
| --- | --- | --- | --- |
| $4\times4$ | $(2,0)$ pixels | $8/24$ | $1/3$ |
| $40\times40$ | $(2,0)$ pixels | $1520/1680$ | $19/21\approx0{,}905$ |
| $40\times4$ | $(2,0)$ pixels | $152/168$ | $19/21\approx0{,}905$ |
| $40\times4$ | $(0,2)$ pixels | $80/240$ | $1/3$ |

Deux pixels d'erreur représentent une fraction différente de la dimension
concernée. Une boîte allongée est ici bien plus sensible au déplacement sur
son axe court. Ce n'est pas une contradiction avec l'invariance d'IoU lorsque
l'on redimensionne **ensemble** les deux boîtes : ici l'erreur reste fixée à
deux pixels. Dérivation de la définition d'IoU, [GIoU v2, §3, équation 1](https://arxiv.org/html/1902.09630v2), calculs vérifiés sans détecteur exécuté.

Dans le protocole proposé, croiser classe, taille, rapport d'aspect et densité
sur les mêmes annotations, puis inspecter les distributions de scores et les
pertes avant/après posttraitement. Ne pas conclure qu'un réglage est bon pour
les petites boîtes à partir de la seule AP moyenne ; ne pas changer de repère
ou de convention d'aire entre tailles.

### Cas analytique : resize, padding et NMS

Pour une image de largeur 1920 et hauteur 1080 redimensionnée sans déformation dans $640\times640$, le facteur est $1/3$. L'image utile devient $640\times360$ ; le padding centré ajoute 140 pixels en haut et en bas. Avec coordonnées continues, origine en haut à gauche : $x'=x/3$, $y'=y/3+140$ ; l'inverse est $x=3x'$, $y=3(y'-140)$.

La boîte GT $(900,450,912,459)$, de taille $12\times9$, devient $G=(300,290,304,293)$, de taille $4\times3$. L'aller-retour doit restituer exactement la boîte d'origine. Cette géométrie ne prouve pas à elle seule pourquoi un modèle échoue : il faut examiner ses sorties aux différentes étapes.

Exemple construit, une GT, une classe, aucune zone ignorée, deux candidates seulement, seuil de score $0{,}1$, hard NMS pour IoU $>0{,}4$, évaluation à IoU $0{,}5$ :

| Candidate dans l'entrée | Score | IoU avec $G$ | Avant NMS | Après NMS |
| --- | --- | --- | --- | --- |
| $P=(300,290,304,293)$ | $0{,}8$ | 1 | Couvre la GT | Supprimée |
| $Q=(301{,}5,290,305{,}5,293)$ | $0{,}9$ | $5/11\approx0{,}455$ | Ne couvre pas la GT au seuil d'évaluation | Conservée |

Les deux candidates passent le seuil de score. Leur IoU mutuelle vaut $5/11>0{,}4$ : Q, mieux scorée, supprime P. Le rappel de cette GT passe de 1 à 0 ; ici, la perte se situe dans le posttraitement, car une proposition correcte existait à cette résolution. Cela ne démontre pas que toute baisse d'AP après resize vient de NMS. Si aucune candidate correcte n'existe avant filtrage, examiner plutôt la taille effective, les features, les données et l'assignation d'entraînement. Le mécanisme de suppression est documenté par Soft-NMS §4 ; les nombres sont un calcul du projet, sans inférence réseau.

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
- [TIDE, version 2, §§2.2–2.3, 3.4 et annexes A.1, D–E : erreurs, oracles et annotations](https://arxiv.org/html/2008.08115v2).
- [Soft-NMS, §4 : interaction scores, suppression et qualité de localisation](https://arxiv.org/html/1704.04503), consulté le 2026-10-21.
- [YOLOv3, version 1, §§2.1–2.3 : régression, classes et échelles](https://arxiv.org/html/1804.02767v1), complément consulté le 2026-10-21.
- [Cartes associées](../82-detection-fasterrcnn-yolo-detr.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.

Enrichissement du 2026-10-21 : cartes CV-DETECTEURS-006 à 010, mécanismes d’apprentissage et FPN. Sources scientifiques consultées ; calculs synthétiques vérifiés, sans entraînement ni benchmark.

Enrichissement du diagnostic du 2026-10-21 : cartes CV-DETECTEURS-011 et 012, cas 004 précisé et protocole de variation de résolution proposé. Cas géométrique/NMS calculé ; expérience sur images non exécutée.

Complément du 2026-10-21 : distinction instances/classes/étiquettes, carte CV-DETECTEURS-013, tailles et rapports d’aspect ; renvois vers les cas NMS multiclasses et imbriqués. Calculs synthétiques, sans mesure sur images.
