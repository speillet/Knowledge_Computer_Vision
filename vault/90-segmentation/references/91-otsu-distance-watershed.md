---
id: CV-WATERSHED
type: pipeline
domaine: d09
poles: [A, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-MORPHO"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d09]
---
# Otsu, distance transform et watershed

## Problème, données et hypothèses

Séparer des objets au contact à partir d'un modèle classique d'intensité et de marqueurs. Entrées : image, masque et polarité ; sorties successives : partition binaire, distances puis labels d'instances. Ce sont des étapes différentes, pas trois noms d'un même algorithme.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-MORPHO](../../30-traitement-image/references/33-morphologie-composantes.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Otsu choisit un seuil selon les distributions d'intensité. La distance transform mesure la distance d'un pixel du masque au fond. Ses maxima peuvent fournir des marqueurs ; watershed propage des bassins selon une topographie/implémentation. De bons marqueurs importent autant que le seuillage.

## Mathématiques, conventions et unités

Otsu maximise $\omega_0\omega_1(\mu_0-\mu_1)^2$ pour un seuil, poids de classes et moyennes, équivalent à minimiser la variance intra-classe pondérée. La distance $D(p)=\min_{q\in fond}\|p-q\|$ dépend de la métrique et de la résolution. Elle ne mesure pas directement une identité ou classe d'objet.

## Paramètres et propriétés

Seuil, éclairage, morphologie, maxima et connectivité. Dans watershed OpenCV documenté, image 8 bits 3 canaux et marqueurs int32 : inconnu 0, labels positifs, frontières finales −1 ; le tableau de marqueurs est modifié. Le fond connu est distinct de l'inconnu.

## Coût et implémentation

Coût de segmentation et de propagation lié à l'image/marqueurs. Aucun appel OpenCV exécuté ; un calcul Otsu sur histogramme jouet est proposé dans les exemples arithmétiques, pas une validation image.

## Évaluation et variation contrôlée

Baseline : objets disjoints puis contact contrôlé ; comparer composantes seules et watershed à marqueurs. Prédire qu'un marqueur fusionné peut maintenir la sous-segmentation. Mesurer erreurs d'instances, pas seulement recouvrement du masque global.

## Échecs et diagnostic

Deux grains restent fusionnés : inspecter marqueurs et topographie. Trop de fragments : inspecter bruit et maxima parasites. Un bon histogramme bimodal ne prouve pas une bonne séparation sémantique.

## Alternatives et usages

Seuillage local pour éclairage variable, GrabCut pour interaction, modèle d'instances si variations dépassent les hypothèses simples.

## Sources et cartes

- [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html).
- [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
- [Cartes associées](../91-otsu-distance-watershed.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
