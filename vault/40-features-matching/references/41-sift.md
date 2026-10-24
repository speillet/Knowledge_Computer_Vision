---
id: CV-SIFT
type: methode
domaine: d04
poles: [B, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: []
revision: 4
tags: [cv/d04, matching, sift]
---
# SIFT — points locaux et description à plusieurs échelles

## Problème et contrat des données

SIFT (*Scale-Invariant Feature Transform*) fournit des points caractéristiques
et des descripteurs pour rechercher des correspondances entre images. Il ne
produit ni une transformation globale ni une identité d'objet à lui seul.
Entrée du pilote : image 2D en gris ; sortie : positions $(x,y)$ en pixels,
échelles, orientations et vecteurs de 128 composantes pour la variante classique.
Les coordonnées retournent dans le repère de l'image fournie : conserver le
resize/crop appliqué avant extraction. [Lowe, §§3–6][lowe]

**Compétences** : expliquer le pipeline, interpréter les invariances, choisir
une distance, diagnostiquer les matches.
**Prérequis obligatoires** : [gradients, distances et repères](../../01-Parcours/Pre-requis.md).
**Connexions** : [ORB](42-orb.md), [RANSAC/homographie](../../50-calibration-geometrie/references/51-ransac-homographie.md).

## Intuition et déroulement

Un détail visuel doit être retrouvé à une échelle comparable avant de décrire
son voisinage. SIFT recherche des extrema dans un espace d'échelles, rejette
les localisations instables, choisit une orientation locale, puis décrit la
distribution spatiale des directions de gradient.

1. Construire une pyramide gaussienne et des différences de gaussiennes (DoG).
2. Comparer un candidat à ses 26 voisins spatiaux et d'échelle.
3. Affiner sa localisation ; rejeter faible contraste et réponses dominées par
   une arête, dont la position est mal définie dans une direction.
4. Attribuer une ou plusieurs orientations dominantes.
5. Accumuler les gradients dans des cellules orientées ; normaliser le vecteur.
6. Proposer des matches avec une distance adaptée, puis filtrer les ambiguïtés.
7. Vérifier un modèle géométrique si le problème en exige un. [Lowe, §§3–7][lowe]

Les étapes 6–7 appartiennent au pipeline de matching ; une homographie n'est
pas une composante obligatoire du descripteur SIFT.

## Mathématiques expliquées

$$
L(x,y,\sigma)=(G_\sigma*I)(x,y),\qquad
D(x,y,\sigma)=L(x,y,k\sigma)-L(x,y,\sigma).
$$

$I$ est l'image, $G_\sigma$ un noyau gaussien normalisé, $*$ la convolution,
$\sigma>0$ l'échelle de lissage en pixels et $k>1$ le rapport entre deux
échelles successives. La DoG compare deux niveaux voisins ; elle approxime
un Laplacien normalisé en échelle lorsque leur espacement est adapté.
Dans une octave, $k=2^{1/s}$ pour $s$ intervalles : doubler $\sigma$ définit
une octave. Les valeurs d'intensité et les seuils doivent rester cohérents.

Le descripteur classique regroupe $4\times4$ cellules et huit orientations,
soit 128 composantes. Pondération et interpolation réduisent les changements
brusques dus au déplacement des gradients. Normalisation, écrêtage puis
renormalisation atténuent certaines variations photométriques ; elles ne
compensent ni saturation ni ombres arbitraires. [Lowe, §§3 et 6][lowe]

Pour une requête, $d_1\le d_2$ sont les distances aux deux meilleurs candidats.
Accepter $d_1<\tau d_2$, avec $0<\tau<1$, rejette un match dont le voisin
suivant est presque aussi plausible. Une petite distance absolue ne suffit
donc pas. Si les deux distances sont nulles, l'ambiguïté ne doit pas être
acceptée aveuglément. [Lowe, §7.1][lowe]

## Hypothèses, propriétés et paramètres

- Échelle et rotation : mécanismes de normalisation, soumis à l'échantillonnage,
  au bruit et à la répétabilité de détection ; aucune garantie pour toute image.
- Perspective : robustesse limitée, sans invariance projective générale.
- Texture : nécessaire pour former des voisinages localement distinctifs.
- Paramètres : densité des octaves, seuil de contraste, rejet des arêtes,
  nombre de points retenus et seuil du ratio. Ne modifier qu'un facteur à la
  fois sur un jeu de validation représentant le problème industriel.

Un seuil de ratio plus strict réduit généralement les matches conservés ;
il faut mesurer si le rappel géométrique et la couverture spatiale en souffrent.
Le seuil historique 0,8 de Lowe dépend de ses expériences, sans valeur universelle.

## Coût et implémentation

Pyramide, détection et description dépendent de la résolution, des niveaux et
du nombre de points. Un matching exhaustif de $n$ et $m$ vecteurs de dimension
$d$ coûte de l'ordre de $nmd$ comparaisons scalaires ; FLANN change le compromis
temps/rappel. Aucun gain de vitesse matériel n'est présumé ici.

Extrait **illustratif non exécuté**, API OpenCV 4.13 vérifiée :

```python
sift = cv.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(gray, None)
matcher = cv.BFMatcher(cv.NORM_L2, crossCheck=False)
# knnMatch exige de traiter le cas sans descripteurs ou avec moins de 2 voisins.
pairs = matcher.knnMatch(descriptors_a, descriptors_b, k=2)
good = [a for pair in pairs if len(pair) == 2
        for a, b in [pair] if a.distance < 0.75 * b.distance]
```

`gray`, `descriptors_a` et `descriptors_b` sont des entrées préparées, pas des
variables créées par cet extrait. Le ratio 0,75 est illustratif.
La norme découle du sens du descripteur, pas seulement de son type mémoire.
[OpenCV, matching][opencv]

## Évaluation, variation et diagnostic

**Baseline proposée, pas une expérience image exécutée** : deux prises de
vue d'une étiquette plane avec géométrie connue. Comparer les correspondances
à la transformation vraie, leur couverture et l'erreur de projection ; mesurer
la latence du pipeline complet sur la machine cible.

**Variation contrôlée proposée** : rotation seule, puis changement d'échelle,
puis ajout de flou séparément. Prédiction : orientation/échelle aident dans
leur domaine de fonctionnement ; le flou peut détruire les détails nécessaires.
Le résultat réel reste à mesurer, sans annoncer une performance numérique.

| Symptôme | Causes à départager | Vérification discriminante |
| --- | --- | --- |
| Beaucoup de matches sur des motifs répétés | Descripteurs ambigus, modèle géométrique incorrect | Distribution des ratios, localisation des inliers, validation sur points réservés |
| Quasi aucun point après flou | Détails supprimés, seuil de contraste trop strict | Inspecter pyramide et détections avant de changer le matcher |
| Bon consensus dans un coin, projection fausse ailleurs | Mauvaise couverture, extrapolation instable | Résidus et positions sur toute la zone utile |

**Cas industriel** : recalage d'une étiquette sous rotation avec budget CPU.
SIFT est une baseline à comparer à ORB et aux méthodes apprises sur succès,
robustesse et coût total, sans le déclarer gagnant a priori.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent normalisations, ambiguïté du ratio et couverture géométrique. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-SIFT-001

**Question de travail** : Pour recaler deux photos d'une étiquette plane, que fournit SIFT et quelles étapes restent nécessaires pour obtenir une transformation fiable ?

**Réponse de référence** : SIFT fournit des keypoints et leurs descripteurs locaux. Le matcher propose des paires ; un filtrage limite les ambiguïtés ; une estimation géométrique teste une transformation adaptée au plan. Les matches ne sont pas une preuve de recalage.

**Chaîne de décision construite** : pour une étiquette connue plane, conserver les coordonnées des keypoints dans chaque image, calculer les candidats et inspecter leur distribution avant d'estimer le warp. Quatre correspondances mal placées ou plusieurs paires ambiguës ne deviennent pas fiables parce qu'elles proviennent de SIFT. Un consensus concentré dans un coin peut également mal contraindre l'extrapolation vers l'autre bord.

**Interprétation du résultat** : contrôler une géométrie sur des points non utilisés pour son ajustement et dans la zone où le produit doit agir. Une pièce en relief peut exiger un autre modèle qu'une homographie unique. La responsabilité de SIFT est la représentation locale ; celle du pipeline est d'établir qu'une transformation explique suffisamment bien les observations pour l'usage annoncé.

### Cas lié à CV-SIFT-007

**Question de travail** : Pour choisir SIFT ou ORB sur une ligne industrielle avec recalage de pièces, quelles mesures rendent la comparaison utile au produit ?

**Réponse de référence** : utiliser les mêmes paires représentatives et une géométrie de référence ; mesurer succès de recalage, erreurs, couverture et coût complet sur le matériel cible. Régler sur validation puis figer pour le test.

**Critère produit proposé** : convertir l'erreur de recalage en conséquence métier, par exemple une région d'inspection décalée par rapport au défaut. Fixer une tolérance et compter les succès, refus et erreurs dangereuses. Deux méthodes aux résidus moyens voisins peuvent différer fortement sur les vues obliques ou les pièces peu texturées.

**Mesure complète** : consigner résolution, nombre de points et mêmes étapes incluses dans le chronométrage. Un extracteur plus rapide qui produit beaucoup de candidats ambigus peut déplacer le coût vers le matching et RANSAC. Examiner aussi mémoire et latence des cas difficiles. La bonne décision dépend du compromis observé sur le matériel cible et des conséquences d'un échec, pas d'une préférence générale pour une méthode classique ou binaire.

**Repère documentaire de cette passe** : [Lowe 2004](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf), §§3–7.1, détection, orientation, descripteur et matching. Les autres développements figurent dans les [cartes associées](../41-sift.md).

## Sources et cartes

- [Lowe 2004][lowe] : §§3–4 détection, §5 orientation, §6 description,
  §7.1 matching. Source scientifique de la méthode classique.
- [OpenCV 4.13, matching][opencv] : norme et API ; source d'implémentation.
- [Cartes SIFT](../41-sift.md).

[lowe]: https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf
[opencv]: https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html
