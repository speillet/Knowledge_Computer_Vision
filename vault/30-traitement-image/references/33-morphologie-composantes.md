---
id: CV-MORPHO
type: methode
domaine: d03
poles: [A, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 2
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d03]
---
# Morphologie et composantes connexes

## Problème, données et hypothèses

Modifier une géométrie binaire et regrouper ses régions selon une connectivité. Entrées : masque avec polarité définie, structurant, ancrage et bord ; sorties : masque transformé ou labels. Un label de composante n'est ni une classe sémantique ni une identité temporelle.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

L'érosion retire les points sans voisinage compatible ; la dilatation étend le support. Ouverture et fermeture composent ces opérations dans des ordres différents. Les composantes connexes regroupent ensuite des pixels reliés selon 4 ou 8 voisins.

## Mathématiques, conventions et unités

Pour un structurant symétrique B centré, $A\ominus B=\{x:x+B\subseteq A\}$ et $A\oplus B=\{a+b:a\in A,b\in B\}$. Une ouverture est $(A\ominus B)\oplus B$. B exprime une échelle en pixels : une variation de résolution change son sens physique.

## Paramètres et propriétés

Fixer taille/forme de B, itérations, connectivité et traitement des trous. Deux régions en contact peuvent fusionner ; une opération utile contre le bruit peut supprimer un vrai petit défaut.

## Coût et implémentation

Le coût dépend de l'image, du structurant et de l'algorithme. Les labels sont internes à une image et peuvent être renumérotés. Pseudocode illustratif : nettoyer → étiqueter → mesurer → contrôler objets manquants ; aucune exécution image annoncée.

## Évaluation et variation contrôlée

Variation analytique : deux pixels qui se touchent seulement en diagonale sont deux composantes en 4-connectivité et une en 8-connectivité. Sur image réelle, mesurer erreurs de fusion/séparation avant de filtrer les petites régions.

## Échecs et diagnostic

Comptage trop faible : regarder les ponts ajoutés par dilatation/fermeture et la connectivité. Comptage trop élevé : inspecter fragments, bruit et structurant ; ne pas considérer la taille comme vérité sémantique.

## Alternatives et usages

Watershed à marqueurs pour séparer des objets joints ; segmentation d'instances si l'apparence et les contacts dépassent un modèle géométrique simple.

## Sources et cartes

- [OpenCV 4.13.0, connectedComponents, paramètres connectivity et labels](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html).

Pour la morphologie ensembliste avec les conventions annoncées, l’ouverture est anti-extensive et la fermeture extensive : elles peuvent supprimer de petites structures de premier plan ou combler de petits intervalles. Sur une image finie, le traitement des bords doit rester explicite.

- [OpenCV, morphological transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html).
- [Cartes associées](../33-morphologie-composantes.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
