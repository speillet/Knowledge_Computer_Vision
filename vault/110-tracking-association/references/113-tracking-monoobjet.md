---
id: CV-SOT
type: comparaison
domaine: d11
poles: [C, D, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# Tracking monoobjet : corrélation, siamois et MeanShift

## Problème, données et hypothèses

Suivre une cible initialisée dans une séquence, sans supposer un détecteur multiobjet ni une identité globale. Entrées : cible initiale et frames ; sortie : localisation de cette cible avec confiance/visibilité selon méthode.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

MeanShift cherche un mode d'une distribution d'apparence locale ; CamShift adapte sa fenêtre selon sa conception. Filtres de corrélation et réseaux siamois comparent modèle de cible et zone de recherche. Mise à jour du template et recherche locale créent un compromis adaptation/dérive.

## Mathématiques, conventions et unités

Une réponse de corrélation élevée est un score relatif entre template et recherche, pas une probabilité d'identité. Le déplacement maximal observable dépend de la région de recherche et de la cadence. Sans observation discriminante après occultation, l'identité peut rester ambiguë.

## Paramètres et propriétés

Taille de recherche, échelle, fréquence de mise à jour, confiance et politique de perte. Une mise à jour sur un distracteur peut contaminer le modèle. Détection de présence et localisation doivent être distinguées.

## Coût et implémentation

Template, recherche et calcul multiéchelle dominent. Aucun tracker monoobjet exécuté ; les familles sont comparées au niveau du contrat, sans FPS universel.

## Évaluation et variation contrôlée

Baseline avec cible unique et perturbations séparées : occultation, distracteur, sortie de champ. Mesurer précision, robustesse, pertes et politique de réinitialisation plutôt que seuls frames réussis.

## Échecs et diagnostic

Dérive progressive : inspecter ce qui est intégré au template et la présence réelle de la cible. Un score haut sur un distracteur n'est pas une preuve de persistance.

## Alternatives et usages

Détecteur + association si plusieurs cibles et entrées/sorties sont attendues ; suivi de point si la sortie utile est un point. Définir le contrat avant la famille de modèle.

## Sources et cartes

- [OpenCV, Meanshift/Camshift](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
- [SiamFC, méthode](https://arxiv.org/abs/1606.09549).
- [Cartes associées](../113-tracking-monoobjet.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
