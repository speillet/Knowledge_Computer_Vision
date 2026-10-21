---
id: CV-HOMOGRAPHIE
type: methode
domaine: d05
poles: [B, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: []
revision: 3
tags: [cv/d05, geometrie, ransac, matching]
---
# RANSAC appliqué à une homographie

## Problème, contrat et prérequis

Estimer une transformation projective entre deux plans images malgré des
correspondances fausses. Une homographie décrit notamment un plan observé depuis
deux positions, ou une rotation pure de caméra dans le modèle perspective idéal.
Une translation devant une scène avec relief introduit généralement de la
parallaxe, incompatible avec une seule homographie globale. [OpenCV, géométrie][tutorial]

Entrées : $n$ paires de points 2D en pixels dans les repères source et destination,
avec unités et prétraitements connus. Sorties : matrice $H$ et masque d'inliers
selon le résidu retenu. Des images très distordues peuvent nécessiter une
correction avant ce modèle projectif.

**Prérequis obligatoires** : [points homogènes et résidus](../../01-Parcours/Pre-requis.md).
**Connexions** : [SIFT](../../40-features-matching/references/41-sift.md), [ORB](../../40-features-matching/references/42-orb.md), [calibration](52-calibration-zhang.md).
**Compétences** : estimer, interpréter le consensus, diagnostiquer les dégénérescences.

## Intuition et déroulement

Les moindres carrés sur tous les matches peuvent être dominés par les outliers.
RANSAC propose de petites hypothèses et recherche celle qui explique un consensus.
Il faut distinguer l'algorithme robuste du modèle choisi : remplacer le modèle
par une fondamentale ou une pose change le problème et la taille minimale.
[Fischler et Bolles, §II][ransac]

Pseudocode **non exécuté**, variante pédagogique :

```text
répéter jusqu'au budget ou au critère d'arrêt :
    tirer quatre paires en position générale
    estimer une homographie candidate
    calculer le résidu de chaque paire dans le repère destination
    retenir le consensus associé au seuil et au score choisis
réestimer sur les inliers du meilleur candidat
recalculer et inspecter les résidus et la couverture
```

L'implémentation peut employer d'autres scores, tirages guidés et raffinements.
Ne pas attribuer à tout appel `findHomography` les propriétés d'une autre variante.

## Modèle et résidu

$$
\tilde x'_i\sim H\tilde x_i,\qquad
e_i=\|x'_i-\pi(H\tilde x_i)\|_2.
$$

$x_i,x'_i\in\mathbb R^2$ sont des points euclidiens ; $\tilde x_i$ leur
représentation homogène ; $\pi$ divise par la troisième composante.
$H\in\mathbb R^{3\times3}$, inversible, est définie à un facteur non nul,
soit huit degrés de liberté. $e_i$ est ici une distance **en pixels destination**.
Un point est inlier si son résidu respecte le seuil choisi ; préciser l'inégalité
de l'implémentation si la valeur frontière compte. [OpenCV `findHomography`][api]

Quatre paires en position générale suffisent au cas minimal : pas de triplet
colinéaire dans chaque ensemble minimal. Des points presque alignés ou regroupés
sur une petite zone peuvent rendre l'estimation mal conditionnée. Normaliser les
coordonnées améliore le calcul linéaire ; cela ne répare pas la dégénérescence.

## Budget de tirages et paramètres

$$
N=\left\lceil\frac{\log(1-p)}{\log(1-w^m)}\right\rceil.
$$

$p\in(0,1)$ est la probabilité nominale visée d'avoir tiré au moins un
échantillon entièrement inlier, $w\in(0,1)$ la proportion d'inliers supposée,
et $m=4$ la taille minimale pour ce modèle. Avec des tirages indépendants
modélisés ainsi, un échantillon est tout-inlier avec probabilité $w^m$.
Pour $w=0,5$, $p=0,99$, le budget vaut 72 ; à $w=0,8$, il vaut 9.
Résultats exécutés dans `examples/pilot_math.py`.

Ce n'est pas la probabilité que la transformation finale soit physiquement
correcte. Mauvais $w$, échantillons dégénérés et structure répétitive peuvent
invalider l'interprétation simplifiée. [Fischler et Bolles, §II][ransac]

Un seuil trop large absorbe des erreurs ; trop faible, il exclut des observations
compatibles avec leur bruit. Changer la résolution impose de reconsidérer un
seuil en pixels. La confiance, le budget et le score ne remplacent pas le contrôle
du modèle et de la répartition spatiale.

## Coût, implémentation et évaluation

L'évaluation naïve de $N$ candidats sur $n$ paires a un coût de l'ordre de $Nn$
résidus, auquel s'ajoutent estimation et raffinement. Les arrêts adaptatifs changent
ce coût. Le filtrage en amont et une meilleure proportion d'inliers peuvent aider.

Extrait **illustratif non exécuté**, OpenCV 4.13 :

```python
H, inliers = cv.findHomography(src_xy, dst_xy, cv.RANSAC, 3.0)
# Vérifier H/inliers non absents, puis les points réservés et la zone utile.
```

`src_xy` et `dst_xy` contiennent les paires dans leurs repères respectifs ;
3,0 est un seuil illustratif en pixels destination, pas une recommandation.
L'appel seul n'atteste pas la qualité géométrique. [API][api]

**Baseline analytique proposée, non exécutée ici** : transformation connue de points d'un plan. Observer
résidu, proportion d'inliers et erreur sur des points non utilisés.
**Variation proposée, non exécutée sur images** : ajouter progressivement des
outliers puis une seconde profondeur sous translation. Prédiction : le premier
facteur exige davantage de tirages ; le second peut rendre le modèle faux.
Le taux d'inliers ne distingue pas seul ces deux situations.

## Diagnostic et décision industrielle

| Symptôme | Hypothèses à distinguer | Vérification |
| --- | --- | --- |
| Excellent consensus sur un petit logo, coins projetés loin | Extrapolation, points mal répartis | Carte des inliers, points réservés en périphérie, sensibilité aux sous-échantillons |
| Résidus opposés entre premier et arrière-plan | Parallaxe, plusieurs plans | Colorer les résidus par profondeur/zone ; comparer un modèle multivue adapté |
| Résultat change fortement entre essais | Faible proportion d'inliers, dégénérescence, budget court | Consigner seed/variante, distribution des points et budgets |

Pour recaler une carte plane, une homographie est une hypothèse raisonnable à
tester. Pour localiser une caméra dans une scène 3D connue, examiner PnP ;
pour deux vues d'une scène 3D inconnue, examiner géométrie épipolaire et pose.
Calibration, pose et recalage répondent à des objectifs distincts.

## Sources et cartes

- [Fischler et Bolles, 1981][ransac] : §II, consensus et budget nominal.
- [Tutoriel officiel homographie][tutorial] : géométrie et conditions.
- [OpenCV 4.13 `findHomography`][api] : résidu et paramètres d'implémentation.
- [Cartes homographie](../51-ransac-homographie.md).

[ransac]: https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf
[tutorial]: https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html
[api]: https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html
