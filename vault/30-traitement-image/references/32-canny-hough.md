---
id: CV-CANNY-HOUGH
type: methode
domaine: d03
poles: [B, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 3
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d03]
---
# Canny et Hough : contours, droites et segments

## Problème, données et hypothèses

Localiser des contours puis rechercher une structure géométrique. Canny sort une carte de contours ; Hough accumule des votes pour une famille de primitives. Une frontière photométrique n'est pas automatiquement un bord d'objet, et une droite n'est pas un segment.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Canny exploite gradients, suppression locale des non-maxima et hystérésis entre deux seuils. Un lissage est une étape de conception à expliciter. Hough transforme chaque point de contour en votes dans un espace de paramètres, puis recherche des maxima.

## Mathématiques, conventions et unités

Pour une droite, $\rho=x\cos\theta+y\sin\theta$, avec x,y et $\rho$ en pixels et $\theta$ en radians dans la convention choisie. La discrétisation de l'accumulateur détermine sa résolution. Le gradient combine dérivées spatiales ; sa norme L1 ou L2 n'est pas le même score.

## Paramètres et propriétés

Deux seuils Canny, échelle de gradient, pas rho/theta, votes, longueur minimale et écart maximal pour une variante segment. Ne pas promettre un lissage gaussien 5×5 interne à chaque API Canny.

## Coût et implémentation

Le nombre de points actifs et de bins domine le coût de Hough naïf ; une variante probabiliste réduit le travail sous ses hypothèses. Aucun appel de bibliothèque ni image réelle exécuté.

## Évaluation et variation contrôlée

Variation proposée : ajouter texture et flou séparément à une pièce à arêtes connues. Prédire contours parasites ou perdus ; mesurer répétabilité et erreur de ligne, pas seulement densité de contours.

## Échecs et diagnostic

Trop de lignes sur texture : contrôler d'abord les contours, la région utile et les bins. Contour interrompu : vérifier contraste et hystérésis avant de baisser tous les seuils.

## Alternatives et usages

LSD, ajustement robuste et modèles appris selon continuité, bruit et besoin de segment. Une contrainte géométrique métier peut limiter les faux positifs.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent relier contours, votes et validation géométrique. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-CANNY-HOUGH-001

**Question de travail** : Pourquoi Canny utilise-t-il deux seuils plutôt qu’un simple seuil de gradient ?

**Réponse de référence** : Les contours forts amorcent des structures ; des réponses plus faibles peuvent être retenues lorsqu’elles sont reliées aux fortes selon l’hystérésis.

**Déroulement interprété** : le gradient mesure une variation locale d'intensité. La suppression des non-maxima conserve les crêtes dans la direction du gradient afin d'éviter des bandes épaisses. L'hystérésis décide ensuite quelles crêtes faibles prolongent une structure suffisamment forte. Le seuil bas permet une continuité conditionnelle ; il ne rend pas toutes les réponses faibles admissibles.

**Exemple construit** : une arête éclairée de façon inégale comporte une portion contrastée et une portion faible. Un seuil unique élevé fragmente l'arête ; un seuil unique bas retient aussi beaucoup de texture. Les deux seuils permettent de conserver certaines portions faibles reliées à la portion forte. Si tout le contour est faible et sans amorce forte, il peut rester absent. Le réglage dépend de l'échelle de lissage, du contraste et de la définition du gradient ; aucune de ces étapes ne distingue à elle seule arête de pièce et texture du fond.

### Cas lié à CV-CANNY-HOUGH-004

**Question de travail** : Hough produit beaucoup de droites sur une surface texturée. Quel contrôle évite un réglage aveugle du seuil de vote ?

**Réponse de référence** : Inspecter carte Canny, distribution angulaire, région utile et support spatial des candidats.

**Enquête proposée** : superposer les droites et leurs points de support à l'image. Si les votes proviennent de stries répétées, le détecteur répond peut-être correctement à des contours qui ne sont simplement pas ceux de la pièce. Examiner ensuite la distribution des angles et le nombre de fragments : cela distingue une texture structurée d'un bruit dispersé.

**Ablation construite** : fixer les bins et seuils, restreindre une région d'intérêt, puis modifier séparément le lissage et la contrainte d'orientation attendue. Mesurer lignes métier trouvées, faux candidats et erreur de position. Augmenter seulement le seuil de vote peut éliminer une arête utile peu contrastée tout en conservant une texture longue et répétitive. Une contrainte géométrique aide uniquement si elle reste valable pour les orientations réellement rencontrées. L'accumulateur compte un support photométrique ; la validation du modèle de pièce est une décision supplémentaire du pipeline.

**Repère documentaire de cette passe** : [OpenCV 4.13, Hough Line Transform](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html), paramétrisation polaire et votes. Les autres développements figurent dans les [cartes associées](../32-canny-hough.md).

## Sources et cartes

Le tutoriel décrit une chaîne avec lissage ; ses explications ne constituent pas une preuve d’un lissage interne à chaque surcharge API. La carte de contours et les contraintes métier du cas de texture sont un diagnostic construit.

- [OpenCV Canny, Theory](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html).
- [OpenCV Hough, Theory](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html).
- [Cartes associées](../32-canny-hough.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
