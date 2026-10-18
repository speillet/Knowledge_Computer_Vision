---
id: CV-IOU-AP
type: metrique-protocole
domaine: d13
poles: [A, C, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: []
revision: 2
tags: [cv/d13, evaluation, iou, ap]
---
# IoU et AP — protocole COCO de détection

## Problème et données

L'IoU mesure un recouvrement ; l'AP mesure le compromis précision/rappel d'une
liste de détections classées dans un protocole donné. Ni l'une ni l'autre ne
mesure à elle seule identité temporelle, latence ou gravité métier d'une erreur.
Cette fiche est une référence de **métrique/protocole**, pas un algorithme
d'extraction de features. [COCO, évaluation][cocodoc]

Entrées : prédictions avec image, catégorie, boîte/masque et score ; annotations
avec catégories, aire, ignore/crowd selon le protocole. Les résultats bbox COCO
utilisent `xywh`. Garder même repère et mêmes transformations que les annotations.
Les identifiants de catégorie ne sont pas nécessairement des indices contigus.
[Format des résultats][format]

**Prérequis obligatoires** : [boîtes et repères](../../01-Parcours/Pre-requis.md).
**Connexions** : [NMS](../../80-detection-pose/references/81-nms.md), [SORT](../../110-tracking-association/references/111-sort.md), segmentation.
**Compétences** : calculer, interpréter, comparer seulement des protocoles compatibles.

## IoU : définition et limites

$$
\operatorname{IoU}(A,B)=\frac{|A\cap B|}{|A|+|B|-|A\cap B|}.
$$

$A,B$ sont deux régions d'aire positive ; $|\cdot|$ mesure une aire, en pixels
carrés si les coordonnées sont en pixels. L'IoU est sans unité et entre 0 et 1.
Pour des boîtes continues `xyxy`, l'intersection multiplie largeur et hauteur
de recouvrement tronquées à zéro ; ne pas ajouter `+1` à une convention continue.
Une boîte dégénérée doit être traitée explicitement, pas masquée par un epsilon.

Une même translation en pixels pénalise davantage une petite boîte : l'IoU
n'est pas une erreur métrique absolue. Pour des masques, le calcul porte sur
les régions segmentées, pas leurs rectangles englobants. Une mIoU de segmentation
sémantique et une AP d'instances répondent à des protocoles différents.

## De l'affectation à précision/rappel

À un seuil IoU et pour une catégorie, ordonner les prédictions par score.
Les règles du protocole déterminent l'appariement à la GT. Une GT ordinaire
déjà associée ne donne pas un second TP : un doublon peut donc devenir FP.
Dans le code COCO, GT ignorées/crowds exigent un traitement particulier.
[Implémentation, `evaluateImg`][code]

Après accumulation, $P=TP/(TP+FP)$ et $R=TP/N_{GT}$ : $N_{GT}$ compte
les GT valides de la catégorie et du sous-ensemble évalué. Le classement global
des détections de cette catégorie entre images importe ; une transformation
des scores qui change ce classement peut changer l'AP.

## AP COCO : moyenne et interpolation

À chaque seuil IoU, former l'enveloppe de précision
$P_{interp}(r)=\max_{\tilde r\ge r}P(\tilde r)$, avec zéro pour les rappels
inatteignables. Le code échantillonne 101 rappels $r\in\{0,0{,}01,\ldots,1\}$.
L'AP principale moyenne aussi dix seuils IoU de 0,50 à 0,95 par pas de 0,05,
et les catégories valides. AP50 fixe 0,50 ; AP75 fixe 0,75.
Ce n'est ni une précision à un seul seuil de score ni une moyenne des IoU.
[COCO][cocodoc], [code `accumulate`][code]

Une catégorie avec GT valide mais sans détection a AP nulle ; sans GT valide,
elle est indéfinie et exclue de la moyenne dans cette référence. Rapporter
catégories, tailles, nombre maximal de détections et type bbox/segm.

## Coins du protocole à ne pas effacer

La référence Python épinglée `8c9bcc3` avec `useCats=1` applique `maxDets=100`
**par image et catégorie** avant accumulation. La page descriptive COCO
annonce un plafond global toutes classes ; un wrapper ou serveur peut aussi
effectuer ce filtrage global. Cette divergence est explicitée : comparer
seulement des exécutions dont version et préfiltrage sont connus.
[Code, `evaluateImg` et `Params`][code]

Pour une crowd, plusieurs prédictions peuvent être absorbées et ignorées ;
le recouvrement utilisé peut être $|D\cap G|/|D|$ pour une détection $D$ et une
région crowd $G$, au lieu de l'IoU ordinaire. Les prédictions non associées
hors plage d'aire peuvent aussi être ignorées. Ne pas remplacer ces règles
par un simple matching un-à-un maison pour annoncer une « AP COCO ».
[Implémentation de recouvrement][mask]

## Exemple exécuté, baseline et variation

Exemple analytique sans ignore/crowd, une catégorie et un seuil IoU fixés :
deux GT valides ; détections classées TP, FP doublon, TP. Les rappels sont
$0,5;0,5;1$ et les précisions $1;0,5;2/3$. L'enveloppe donne

$$
AP_{101}=\frac{51\times1+50\times(2/3)}{101}\approx0,834983.
$$

Il y a 51 seuils de rappel de 0 à 0,50 inclus. Le FP intermédiaire fait baisser
la précision aux rappels supérieurs. Si l'on ne détecte qu'une des deux GT,
$AP_{101}=51/101\approx0,504950$ : ce n'est pas une AP de 1 malgré une précision
de 1 pour l'unique prédiction. Calculs exécutés dans `examples/pilot_math.py` ;
ce programme n'est pas un réimplémentation complète de pycocotools.

**Variation contrôlée** : placer le doublon après les deux TP au lieu d'entre
eux. Dans ce cas construit, l'enveloppe peut garder une AP de 1 ; cela montre
que le rang d'une erreur compte. Ce n'est pas la preuve que les FP tardifs sont
sans coût à un seuil d'exploitation donné.

## Coût, évaluation et diagnostic

Le tri et les comparaisons aux GT dépendent du nombre de prédictions et des
seuils/catégories. Fixer le filtrage de score, NMS, top-k, versions et split.
Aucun entraînement ni appel pycocotools sur un jeu réel n'est exécuté ici.

| Symptôme | Explication possible | Vérification |
| --- | --- | --- |
| AP50 bonne, AP75 faible | Localisation imprécise, coordonnées transformées incorrectement | Erreurs de boîtes et résultats par taille, repère après resize/padding |
| Écart entre deux évaluateurs | maxDets, ignore/crowd, interpolation, catégories | Même fichier de résultats, version et paramètres explicites |
| AP bonne, défauts critiques ratés | Moyenne masquant classes/tailles rares, seuil métier inadapté | Sous-groupes et courbe au point d'exploitation |

## Sources et cartes

- [Description officielle COCO][cocodoc] et [format][format].
- [Code officiel `cocoeval.py`, commit 8c9bcc3][code] : `evaluateImg` L235,
  `accumulate` L353, `Params` L502 ; version vérifiée le 2026-10-18.
- [Code des recouvrements, même commit][mask] : `bbIou` et crowd.
- [Cartes IoU/AP](../131-iou-ap-coco.md).

[cocodoc]: https://cocodataset.org/#detection-eval
[format]: https://cocodataset.org/#format-results
[code]: https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py
[mask]: https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/common/maskApi.c
