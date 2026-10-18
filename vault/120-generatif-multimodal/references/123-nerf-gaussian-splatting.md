---
id: CV-RENDU3D
type: comparaison
domaine: d12
poles: [B, D]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-EPIPOLAIRE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d12]
---
# NeRF, 3D Gaussian Splatting et reconstruction

## Problème, données et hypothèses

Synthétiser des vues d'une scène et distinguer qualité de rendu et précision géométrique. Entrées : images et poses/calibration selon méthode ; sorties : représentation et nouvelles vues. Les méthodes de profondeur monoculaire ou DUSt3R/MASt3R relèvent d'autres contrats de reconstruction, à approfondir séparément.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

NeRF représente densité/radiance en fonction d'un point 3D et de la direction de vue, puis rend par intégration volumique. 3D Gaussian Splatting optimise des primitives anisotropes explicites, leur apparence et densification, puis effectue un rendu par splatting.

## Mathématiques, conventions et unités

L'intégration volumique pondère une couleur par densité et transmittance le long du rayon ; les coordonnées, unités et poses doivent être cohérentes. Une PSNR élevée sur vues voisines n'établit ni surface métrique exacte ni qualité sur angles non observés.

## Paramètres et propriétés

Couverture des vues, poses, fond, exposition et scène statique supposée ; nombre de primitives, régularisation et protocole d'entraînement. Les ambiguïtés de régions jamais observées restent réelles.

## Coût et implémentation

Entraînement/optimisation, stockage et rendu coûtent différemment. Les FPS des auteurs dépendent du matériel et des scènes. Aucun rendu ou entraînement exécuté.

## Évaluation et variation contrôlée

Baseline : vues et poses connues avec split d'angles réservé ; varier couverture et bruit de pose séparément. Mesurer synthèse de vues et référence géométrique distinctement si la géométrie importe.

## Échecs et diagnostic

Rendu bon mais surface flottante : vérifier vues réservées, poses, régions non contraintes et objectif. Un optimiseur peut expliquer les images avec une géométrie inadéquate à la mesure.

## Alternatives et usages

MVS/TSDF pour d'autres hypothèses et sorties ; reconstruction apprise pour une autre supervision. Aucun de ces noms ne garantit une échelle absolue sans contrat adapté.

## Sources et cartes

- [NeRF, page et papier des auteurs](https://www.matthewtancik.com/nerf).
- [3D Gaussian Splatting, auteurs](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/).
- [Cartes associées](../123-nerf-gaussian-splatting.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
