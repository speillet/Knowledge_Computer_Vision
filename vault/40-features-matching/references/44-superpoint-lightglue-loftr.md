---
id: CV-MATCH-APPRIS
type: pipeline
domaine: d04
poles: [B]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-SIFT", "CV-ORB", "CV-HOMOGRAPHIE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# SuperPoint, LightGlue et LoFTR

## Problème, données et hypothèses

Construire des correspondances avec des composants appris, sans confondre détecteur, descripteur et matcher. SuperPoint produit des points/descripteurs ; LightGlue apparie des features compatibles ; LoFTR propose des correspondances detector-free coarse-to-fine. Ces sorties ne sont pas automatiquement une pose correcte.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SIFT](41-sift.md) ; [CV-ORB](42-orb.md) ; [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

SuperPoint apprend détection et description avec adaptation homographique. LightGlue exploite contexte et interactions entre features, avec adaptation de calcul. LoFTR utilise contexte et correspondances grossières puis fines sans requérir un détecteur sparse explicite.

## Mathématiques, conventions et unités

Chaque paire $(x_i,x'_i)$ est dans deux repères image explicites. Après resize ou padding, revenir à des coordonnées comparables avant le résidu géométrique. Un score de matching appris est un score du modèle ; il n'est pas automatiquement une probabilité calibrée sur l'usine.

## Paramètres et propriétés

Choisir checkpoints compatibles avec le type de features, résolution, seuil et politique de calcul. Detector-free ne signifie ni flot pour chaque pixel ni absence d'erreurs. Ne pas comparer des poids ou licences comme s'ils formaient un seul produit.

## Coût et implémentation

Résolution, nombre de features, attention et vérification aval dominent coût/mémoire. Aucun checkpoint téléchargé ou exécuté. Les résultats des auteurs restent liés à leur protocole.

## Évaluation et variation contrôlée

Baseline proposée : SIFT/ORB + même géométrie et même jeu de paires. Faire varier texture puis éclairage séparément ; mesurer succès de recalage, couverture, latence complète et échecs. Prédire un effet possible du contexte, sans annoncer de gain mesuré.

## Échecs et diagnostic

Échec sur surfaces répétitives : inspecter correspondances, répétition et modèle géométrique. Changement de checkpoint : vérifier normalisation et extraction attendues avant de régler seulement le seuil.

## Alternatives et usages

Sparse appris pour points explicites ; LoFTR pour une autre stratégie de correspondances ; ECC quand l'objectif et l'initialisation d'un recalage par intensités sont adaptés.

## Sources et cartes

- [SuperPoint, méthode et Homographic Adaptation](https://arxiv.org/abs/1712.07629).
- [LightGlue, dépôt des auteurs](https://github.com/cvg/LightGlue).
- [LoFTR, §3](https://arxiv.org/abs/2104.00680).
- [Cartes associées](../44-superpoint-lightglue-loftr.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
