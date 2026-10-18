---
id: CV-ORB
type: methode
domaine: d04
poles: [B, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: []
revision: 2
tags: [cv/d04, matching, orb]
---
# ORB — détection et descripteur binaire orienté

## Problème, données et prérequis

ORB (*Oriented FAST and Rotated BRIEF*) recherche des features locales avec
une représentation binaire adaptée aux comparaisons rapides. Entrée : image
en gris, avec repère et résolution conservés. Sortie : keypoints et descripteurs ;
la variante classique comporte 256 bits par descripteur. Il faut encore un
matcher et une validation géométrique. [Rublee et al., §§3–4][orbpaper]

**Compétences** : reconstruire le pipeline, choisir la distance, comparer sous
budget, diagnostiquer un changement de paramètres.
**Prérequis obligatoires** : [repères/distances](../../01-Parcours/Pre-requis.md).
**Connexions** : [SIFT](41-sift.md), [homographie](../../50-calibration-geometrie/references/51-ransac-homographie.md).

## Intuition et étapes

1. Détecter avec FAST dans une pyramide d'images.
2. Classer les candidats, notamment avec le score Harris dans la méthode originale.
3. Estimer une orientation grâce au centre de masse des intensités du patch.
4. Orienter un motif de tests de comparaison d'intensité de type BRIEF.
5. Former le vecteur binaire à partir de tests discriminants et peu corrélés.

Le choix des tests rBRIEF est appris hors ligne dans l'article ; il ne signifie
pas qu'un réseau est entraîné sur les deux images à apparier. [Rublee, §4][orbpaper]

## Orientation et distance

$$
m_{pq}=\sum_{(x,y)\in P}x^p y^q I(x,y),\qquad
\theta=\operatorname{atan2}(m_{01},m_{10}).
$$

$P$ est le patch, $(x,y)$ des coordonnées **centrées sur le keypoint**,
$I$ l'intensité et $m_{pq}$ son moment d'ordre $p+q$. $\theta$ est une
orientation en radians. Un patch pauvre ou symétrique peut rendre cette
orientation peu stable ; elle n'ajoute pas d'information absente de l'image.

Pour deux positions de test $a,b$, un bit vaut $\mathbf1[I(a)<I(b)]$.
Le motif est tourné avec l'orientation. Avec deux choix par test, la distance
de Hamming compte les positions de bits différentes ; une distance L2 entre
les octets stockés ne mesure pas la même chose.

Exemple construit : octets `00000000` et `10000000`. Hamming = 1, alors que
la différence numérique entre les octets vaut 128. Le stockage `uint8` ne
justifie donc pas une distance euclidienne sur les octets.

## Paramètres et propriétés

OpenCV 4.13 propose `nfeatures`, `scaleFactor`, `nlevels`, `fastThreshold`,
`patchSize`, `edgeThreshold` et `WTA_K`. Modifier la pyramide change à la fois
la couverture des échelles et le coût. Les zones proches du bord peuvent être
exclues pour garantir un patch exploitable. [OpenCV ORB][opencv]

`WTA_K=2` produit des tests binaires : `NORM_HAMMING`. Pour `WTA_K=3` ou `4`,
l'indice gagnant est codé sur deux bits : `NORM_HAMMING2` compare ces symboles.
Ce n'est pas « Hamming au carré ». Cette variante est un choix d'implémentation
à consigner ; ne pas généraliser sa norme au descripteur original.

Rotation : compensation locale, sous réserve d'une orientation stable.
Échelle : couverture discrète par la pyramide, sans invariance parfaite.
Perspective, flou de mouvement et faibles contrastes restent des causes d'échec.
Les chiffres de vitesse de 2011 ne sont pas des garanties sur un appareil actuel.

## Implémentation et coût

Extrait **illustratif non exécuté**, OpenCV 4.13 :

```python
orb = cv.ORB_create(nfeatures=1000, WTA_K=4)
matcher = cv.BFMatcher(orb.defaultNorm(), crossCheck=True)
# Après detectAndCompute sur chaque image et contrôle des résultats non vides :
matches = matcher.match(descriptors_a, descriptors_b)
```

Ici le cross-check retient les plus proches voisins mutuels. Il traite une
incohérence de réciprocité ; il ne prouve pas que le match est physiquement juste.
Le ratio test compare plutôt l'ambiguïté entre voisins. Ne pas activer un
cross-check puis supposer un appel `knnMatch(k=2)` interchangeable.
[OpenCV matcher][matcher]

La mémoire des descripteurs binaires et les comparaisons XOR/popcount sont des
avantages potentiels. Mesurer aussi extraction, transfert, matching et estimation
géométrique ; le nombre de features peut dominer le coût aval.

## Référence, variation et diagnostic

**Proposition d'expérience non exécutée** : comparer ORB et SIFT sur les mêmes
paires annotées, avec une géométrie vraie et le même budget de validation.
Mesurer taux de recalage réussi, résidus, couverture spatiale, latence p50/p95
et mémoire. Ne pas comparer seulement le nombre brut de matches.

**Variation contrôlée** : changer uniquement `WTA_K` de 2 à 4, adapter la norme
et garder le reste du protocole fixe. Prédiction : résultats et coût peuvent
changer ; une ancienne norme incorrecte introduirait un facteur confondant.
Le résultat attendu n'est pas « 4 est toujours meilleur ».

| Symptôme | Causes possibles | Contrôle utile |
| --- | --- | --- |
| Dégradation après changement de `WTA_K` | Norme restée Hamming, autre modification simultanée | Lire `defaultNorm()`, consigner les paramètres |
| Échec au changement d'échelle | Plage de pyramide, détails disparus | Visualiser les niveaux et la répétabilité des keypoints |
| Beaucoup de matches mais géométrie fausse | Motifs répétitifs, parallaxe, modèle faux | Ratio/cross-check puis vérification spatiale et géométrique |

**Choix industriel** : sur CPU embarqué, démarrer par une baseline ORB si les
variations sont compatibles, puis mesurer SIFT ou une approche apprise si
le taux de succès est insuffisant. La contrainte de temps ne remplace pas
la validation de la tâche.

## Sources et cartes

- [Rublee et al., ICCV 2011][orbpaper] : §§3–4 mécanisme ; §5 évaluation.
- [OpenCV ORB 4.13][opencv] : paramètres et sémantique de `WTA_K`.
- [OpenCV matching][matcher] : distances et cross-check.
- [Cartes ORB](../42-orb.md).

[orbpaper]: https://doi.org/10.1109/ICCV.2011.6126544
[opencv]: https://docs.opencv.org/4.13.0/db/d95/classcv_1_1ORB.html
[matcher]: https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html
