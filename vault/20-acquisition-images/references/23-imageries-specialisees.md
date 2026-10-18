---
id: CV-IMAGERIES
type: comparaison
domaine: d02
poles: [E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 1
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d02]
---
# Line-scan, télédétection et volumes médicaux

## Problème, données et hypothèses

Comprendre des contrats d'acquisition spécialisés avant d'appliquer un réseau 2D. Comparaison d'entrées : lignes synchronisées au mouvement, bandes multispectrales/SAR, volumes avec espacement/orientation physique. La fiche introduit ces familles ; elle ne constitue pas une maîtrise de chaque modalité.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Line-scan reconstruit une image au fil du déplacement ; une optique télécentrique vise à limiter certains changements de grandissement sur sa plage conçue. Une image géoréférencée porte une transformation vers des coordonnées terrestres. Un volume médical possède axes, espacement et orientation ; l'ordre du tableau n'est pas le repère patient.

## Mathématiques, conventions et unités

Un espacement voxel $(s_x,s_y,s_z)$ en mm transforme un déplacement d'indices en longueur physique. Des pixels ou voxels anisotropes rendent des distances en indices trompeuses. Un affine géospatial ou volumique doit conserver axe, unité et convention ; une coordonnée latitude/longitude n'est pas une distance euclidienne en mètres.

## Paramètres et propriétés

Préciser calibration line-scan/encodeur, bandes et normalisation, résolution au sol, no-data, axes et espacement. DICOM/NIfTI sont des formats avec métadonnées, pas des garanties d'annotations cohérentes ou d'utilité clinique.

## Coût et implémentation

Grandes mosaïques et volumes nécessitent tuilage avec recouvrement et restitution des coordonnées. Aucun fichier patient ou géospatial réel n'est chargé ici ; aucun résultat clinique n'est revendiqué.

## Évaluation et variation contrôlée

Variation proposée : rééchantillonner un volume anisotrope ou modifier la vitesse du convoyeur. Prédire les erreurs si la transformation n'est pas propagée ; vérifier une longueur connue et les raccords de tuiles.

## Échecs et diagnostic

Distances de contour incohérentes : vérifier espacement et orientation. Artefacts aux raccords : contrôler padding, recouvrement et fusion. Dégradation saisonnière : distinguer acquisition et distribution des labels.

## Alternatives et usages

Choisir une représentation selon la tâche et les unités ; une bonne segmentation ne prouve ni géoréférencement exact ni précision de métrologie.

## Sources et cartes

- [NIfTI, standard et transformations](https://nifti.nimh.nih.gov/nifti-1/).
- [DICOM, standard courant](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html).
- [SpaceNet7, données multi-temporelles](https://spacenet.ai/spacenet-7-multi-temporal-urban-development-challenge/).
- [Cartes associées](../23-imageries-specialisees.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
