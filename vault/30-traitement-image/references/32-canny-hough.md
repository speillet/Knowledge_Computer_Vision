---
id: CV-CANNY-HOUGH
type: methode
domaine: d03
poles: [B, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 1
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

## Sources et cartes

- [OpenCV Canny, Theory](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html).
- [OpenCV Hough, Theory](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html).
- [Cartes associées](../32-canny-hough.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
