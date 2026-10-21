---
id: CV-ECC
type: methode
domaine: d04
poles: [B, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-HOMOGRAPHIE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# Recalage par intensités et ECC

## Problème, données et hypothèses

Aligner des images en optimisant un critère photométrique sous un modèle de mouvement. Entrées : images compatibles, masque éventuel et initialisation ; sortie : paramètres de warp. Ce n'est pas un matcher de descripteurs locaux.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

L'optimiseur déforme une image pour améliorer la corrélation avec l'autre. Le centrage et la normalisation rendent la corrélation inchangée sous un gain positif et un offset globaux sur un support fixé, de variance non nulle (déduction algébrique). Cela ne garantit pas une convergence du recalage ECC. Une pyramide peut améliorer l'initialisation sans garantir un optimum global.

## Mathématiques, conventions et unités

Un warp $W(x;\theta)$ transforme les coordonnées selon le modèle choisi. Une corrélation normalisée compare des intensités centrées/normées sur la zone commune ; $\theta$ n'a pas les mêmes dimensions pour translation, affine et homographie. Préciser le sens du warp et l'usage de sa réciproque à l'affichage.

## Paramètres et propriétés

Modèle, critère d'arrêt, masque et échelle doivent correspondre au mouvement. Texture, recouvrement et initialisation sont essentiels. Robustesse à un gain simple ne couvre pas ombres, occultations ou géométrie 3D arbitraire.

## Coût et implémentation

Chaque itération évalue et dérive le critère sur des pixels ; résolution et pyramide comptent. Aucun appel `findTransformECC` exécuté ; ne pas transformer convergence en garantie de recalage.

## Évaluation et variation contrôlée

Variation proposée : translation connue puis initialisation de plus en plus éloignée. Mesurer erreur de warp sur points réservés et taux de convergence ; un score photométrique seul peut favoriser un motif répétitif.

## Échecs et diagnostic

Échec malgré des images proches : vérifier plage/type, sens de transformation, recouvrement et perturbation photométrique réelle.

## Alternatives et usages

Features + RANSAC pour grandes transformations avec points distinctifs ; recalage par intensités pour raffinement approprié. Comparer sur précision et bassin utile.

## Sources et cartes

- [OpenCV findTransformECC, motion and criteria](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html).
- [Cartes associées](../45-recalage-ecc.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
