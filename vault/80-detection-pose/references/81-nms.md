---
id: CV-NMS
type: methode
domaine: d08
poles: [A, C, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: ["CV-IOU-AP"]
revision: 3
tags: [cv/d08, detection, nms]
---
# NMS — supprimer des détections redondantes

## Problème et données

Plusieurs hypothèses d'un détecteur peuvent désigner le même objet. La greedy
hard NMS (*Non-Maximum Suppression*) conserve successivement la boîte de meilleur
score et retire des candidates qui la recouvrent trop. Elle suppose que score
et recouvrement permettent de distinguer doublons et vrais voisins ; cette
hypothèse peut échouer dans une foule. [Soft-NMS, §4][paper]

Entrées : boîtes valides `xyxy` dans un repère commun, scores scalaires, classes
si l'on sépare les catégories. Sorties : indices conservés, pas boîtes fusionnées.
Les scores servent au classement ; leur calibration probabiliste n'est pas
une condition nécessaire au calcul. Les coordonnées normalisées ou pixels
peuvent convenir si toutes les boîtes partagent la même convention.

**Prérequis obligatoires** : [IoU](../../130-evaluation-fiabilite/references/131-iou-ap-coco.md).
**Connexions** : [SORT](../../110-tracking-association/references/111-sort.md), AP, détection dense et détecteurs par ensembles.
**Compétences** : dérouler l'algorithme et régler les seuils sans les confondre.

## Déroulement et paramètres

Pseudocode **pédagogique**, matérialisé par l'exemple Python du dépôt :

```text
trier les indices par score décroissant
tant que des candidats restent :
    conserver le premier
    retirer les autres si leur IoU avec lui dépasse le seuil
```

La variante du pilote supprime pour $\operatorname{IoU}>\tau_{nms}$.
L'égalité est conservée. En cas de scores égaux, elle utilise l'indice d'entrée
comme départage déterministe. Une autre implémentation peut ne pas garantir
le même choix CPU/GPU ; consigner le backend. [Torchvision NMS][api]

Les sources ne traitent pas l'égalité de la même façon : l'article écrit la
suppression pour $\operatorname{IoU}(M,b_i)\ge N_t$ [§4][paper], alors que
Torchvision et le code original suppriment pour une IoU strictement
supérieure. [Torchvision NMS][api] ; [code original][softcode] Le cas d'une
IoU exactement égale au seuil dépend donc de l'implémentation : le préciser
dans un test de frontière.

- Seuil de score : filtre la confiance avant/après le posttraitement choisi.
- Seuil NMS : décide la redondance entre deux prédictions.
- Seuil IoU d'évaluation : compare une prédiction à la vérité terrain.

Ces trois seuils n'ont ni la même paire d'objets ni le même rôle.
Une NMS séparée par classe évite une suppression interclasse, mais peut laisser
plusieurs labels incompatibles sur le même objet. La NMS globale a le compromis
inverse. Choisir selon la sémantique des annotations. [Batched NMS][batched]

## Exemple exécuté et variation

Boîtes continues $A=(0,0,10,10)$, $B=(2,0,12,10)$, $C=(20,0,30,10)$,
scores respectifs $0,9;0,8;0,7$. Intersection $A\cap B=80$ px², union 120 px²,
IoU $=2/3$. À $\tau_{nms}=0,5$, garder $A,C$ ; à 0,7, garder $A,B,C$.
Ce résultat est exécuté dans `examples/pilot_math.py`, sans reproduire un détecteur.

**Interprétation de la variation contrôlée** : augmenter le seuil conserve ici
davantage de boîtes ; cela peut sauver un vrai voisin ou conserver un doublon.
Les boîtes seules ne disent pas lequel : il faut les annotations de la tâche.
Une AP mesurée sur un vrai jeu reste nécessaire pour régler le compromis.

## Soft-NMS : alternative et limites

Soft-NMS diminue les scores au lieu d'éliminer immédiatement tout recouvrement
fort. Par exemple, la variante gaussienne utilise

$$
s_i\leftarrow s_i\exp\left(-\frac{\operatorname{IoU}(M,b_i)^2}{\sigma}\right).
$$

$M$ est la boîte sélectionnée, $b_i$ une candidate, $s_i$ son score et
$\sigma>0$ un paramètre sans unité. La pénalité gaussienne s'applique à toutes
les candidates restantes, sans seuil $N_t$. [Article, §4][paper] Rechercher à
nouveau le maximum parmi les scores pénalisés, comme le fait le code original.
Après chaque itération, les détections passées sous un seuil de score sont
écartées : « Soft-NMS ne supprime jamais » est faux. [Article, §5][paper] ;
[code original][softcode]

Le code original utilise des coordonnées inclusives avec `+1`, tandis que le
pilote utilise des coordonnées continues. Une comparaison numérique exige la
même convention. Le score d'une boîte ne devient pas une probabilité calibrée
par ce seul posttraitement. [Implémentation officielle][softcode]

## Coût, évaluation et diagnostic

Le tri coûte $O(n\log n)$ et la suppression naïve jusqu'à $O(n^2)$ comparaisons.
Un top-k amont réduit le coût mais peut perdre des objets ; consigner ce filtrage
dans le protocole AP. Aucun extrait Torchvision n'est exécuté dans ce lot.

Régler les seuils sur validation, figer avant test, analyser par classe, taille
et densité. Observer aussi l'effet sur le tracker aval : des boîtes supprimées
peuvent provoquer des pistes manquées.

| Symptôme | Causes à départager | Vérification |
| --- | --- | --- |
| Un piéton disparaît dans une foule | NMS trop agressive, détecteur n'ayant jamais proposé la boîte | Comparer sorties avant et après NMS avec GT |
| Plusieurs boîtes autour d'une pièce | Seuil trop permissif, classes différentes, convention fausse | Journal scores/classes/IoU et contrat de coordonnées |
| Résultats différents à scores égaux | Ordre ou backend non déterministe | Départage explicite, test ciblé sans conclure à un écart du réseau |

Un détecteur entraîné à produire un ensemble non redondant, comme DETR, peut
se passer de NMS : ne pas l'appliquer comme une obligation universelle.
[DETR, résumé][detr]

## Sources et cartes

- [Bodla et al., Soft-NMS 2017][paper] : §1 limites de la NMS, §4 hard/soft
  et fonctions de pénalité, §5 seuil de score après chaque itération.
- [Torchvision `nms`][api] et [catégories][batched] : convention d'API consultée
  le 2026-10-18 ; aucun benchmark logiciel revendiqué.
- [Code original Soft-NMS, commit b8e69bd][softcode] : coordonnées, recherche
  du maximum et seuil final.
- [Carion et al., DETR 2020][detr] : détection ensembliste sans NMS.
- [Cartes NMS](../81-nms.md).

[paper]: https://arxiv.org/abs/1704.04503
[api]: https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html
[batched]: https://docs.pytorch.org/vision/stable/generated/torchvision.ops.batched_nms.html
[softcode]: https://github.com/bharatsingh430/soft-nms/blob/b8e69bdf8df2ad53025c9d198ded909b50471d4f/lib/nms/cpu_nms.pyx
[detr]: https://arxiv.org/abs/2005.12872
