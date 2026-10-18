---
id: CV-ASSOCIATION
type: comparaison
domaine: d11
poles: [C, D, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-SORT"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# DeepSORT, ByteTrack et association multiobjet

## Problème, données et hypothèses

Améliorer l'association au-delà de SORT sous occultations, scores variables et apparence. Entrées : détections, timestamps, éventuellement embeddings et historique ; sortie : pistes avec IDs selon cycle de vie. La qualité du détecteur reste déterminante.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SORT](111-sort.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

DeepSORT combine mouvement, gating Mahalanobis, distance d'apparence et cascade d'association. ByteTrack associe d'abord les détections de score élevé, puis les faibles aux pistes restantes selon la méthode ; les faibles non associées ne créent pas indistinctement de nouvelles pistes.

## Mathématiques, conventions et unités

Une distance d'apparence cosinus peut écrire $1-a^Tb$ pour vecteurs unitaires. Elle n'est pas la même mesure que l'IoU ou le résidu Mahalanobis de mouvement. Mélanger leurs seuils sans normalisation/protocole n'est pas une fusion de probabilités justifiée.

## Paramètres et propriétés

Seuils haut/bas, gating, mémoire d'apparence, confirmation et durée de perte. Le ReID piéton original peut mal transférer à des pièces identiques. Le suivi 3D, par exemple AB3DMOT, exige en plus un contrat de repère/boîte et de mouvement 3D, pas un simple renommage du tracker 2D.

## Coût et implémentation

Embeddings ajoutent extraction et mémoire ; détecteur, NMS, association et transferts doivent être comptés. Aucun tracker exécuté ni amélioration de score prétendue.

## Évaluation et variation contrôlée

Baseline SORT à détecteur fixe ; varier occultation et calibrage des scores séparément. Mesurer ID switches, fragments et métriques d'association, avec split par séquence et paramètres figés.

## Échecs et diagnostic

IDs échangés malgré apparence : vérifier domaines ReID, crops, normalisation et association. Fausses pistes : inspecter création et seuils ; ne pas baisser tous les seuils sans traces frame par frame.

## Alternatives et usages

Associer mouvement et apparence selon ambiguïtés ; compenser ego-motion si nécessaire. Les trackers monoobjet et ReID seul remplissent des contrats distincts.

## Sources et cartes

- [DeepSORT, §§2.1–2.3](https://arxiv.org/abs/1703.07402).
- [ByteTrack, §3 Algorithm1](https://arxiv.org/abs/2110.06864).
- [AB3DMOT, contrat 3D](https://arxiv.org/abs/2008.08063).
- [Cartes associées](../112-deepsort-bytetrack.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
