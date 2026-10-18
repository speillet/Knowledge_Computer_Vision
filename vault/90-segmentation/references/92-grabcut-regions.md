---
id: CV-GRABCUT
type: methode
domaine: d09
poles: [A, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d09]
---
# GrabCut, régions et modèles d’apparence

## Problème, données et hypothèses

Extraire un objet à partir d'une initialisation interactive et d'un modèle d'apparence. Entrées : image couleur et rectangle/labels ; sortie : masque selon labels sûrs/probables. Le modèle ne comprend pas automatiquement la sémantique de l'objet demandé.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

GrabCut alterne estimation des distributions de couleur par mélanges gaussiens et optimisation d'une énergie par graph cut. Les termes unaires suivent l'apparence, les relations voisines encouragent une cohérence adaptée aux contours.

## Mathématiques, conventions et unités

Une énergie schématique $E(L)=\sum_p U_p(L_p)+\lambda\sum_{p,q}V_{pq}(L_p,L_q)$ combine coût d'étiquette et régularisation spatiale. L est le masque de labels ; $\lambda$ règle un compromis propre à la variante. Une énergie minimisée n'est pas une preuve de masque métier correct.

## Paramètres et propriétés

Rectangle initial, coups de pinceau, labels certains/probables, itérations et espace couleur. Fond/objet de couleurs proches, trous et transparence peuvent rendre le modèle d'apparence insuffisant.

## Coût et implémentation

Mémoire du graphe et itérations dépendent de la résolution. Aucun appel GrabCut exécuté. Region growing ou contours actifs utilisent d'autres objectifs/initialisations ; ils ne sont ici qu'introduits comme alternatives.

## Évaluation et variation contrôlée

Variation proposée : même objet et initialisation, puis rendre le fond similaire en couleur. Mesurer erreurs de masque et coût d'interaction, avec référence réservée.

## Échecs et diagnostic

L'objet est tronqué : vérifier que des pixels utiles ne sont pas imposés comme fond sûr. Plus d'itérations ne contredit pas une contrainte initiale fausse.

## Alternatives et usages

Watershed pour marqueurs/topographie, méthodes apprises par prompt pour autre généralisation ; conserver coût d'interaction et hypothèses.

## Sources et cartes

- [OpenCV GrabCut, théorie et masques](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
- [Cartes associées](../92-grabcut-regions.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
