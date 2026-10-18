---
id: CV-ANOMALIES
type: methode
domaine: d07
poles: [A, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-REPRESENTATIONS", "CV-ACQUISITION"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# Inspection : golden template, PatchCore et PaDiM

## Problème, données et hypothèses

Détecter des écarts au nominal lorsque les défauts sont rares. Entrées : images nominales de référence et acquisition ; sorties : score image et/ou carte de localisation. L'anomalie dépend de la distribution de référence : changement d'éclairage et défaut produit ne sont pas équivalents.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-REPRESENTATIONS](71-representations-transfert.md) ; [CV-ACQUISITION](../../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Golden template compare à une référence après recalage. PatchCore garde une banque de features de patches nominaux, réduite par coreset, et score par proximité. PaDiM modélise des distributions gaussiennes de features par position et utilise leurs corrélations.

## Mathématiques, conventions et unités

Un score de proximité simple est $a(p)=\min_{m\in M}\|f(p)-m\|_2$ pour feature f et banque M ; le papier PatchCore inclut une agrégation/repondération à distinguer de ce résumé. PaDiM utilise $\sqrt{(f-\mu)^T\Sigma^{-1}(f-\mu)}$ avec covariance estimée/régularisée. Ces scores ne sont pas des probabilités de défaut calibrées.

## Paramètres et propriétés

Sélection nominale, couches, échelle, coreset/covariance, alignement et seuil. Une contamination du nominal ou une variabilité non couverte change le résultat. La détection de tous défauts futurs n'est pas garantie.

## Coût et implémentation

Banque et recherche de voisins consomment mémoire/calcul ; covariance et carte ont un autre coût. Aucun modèle ni jeu industriel exécuté.

## Évaluation et variation contrôlée

Comparer une baseline template et les méthodes avec mêmes splits par pièce/lot. Varier éclairage ou orientation séparément ; mesurer taux de faux rejets, défauts manqués et localisation, pas seulement AUROC image.

## Échecs et diagnostic

Scores élevés sur toutes les pièces d'une nouvelle caméra : vérifier acquisition, domaine nominal et recalage avant de réétiqueter tout comme défaut. Un fond dominant peut masquer une petite anomalie dans une métrique pixel globale.

## Alternatives et usages

Détection supervisée si défauts connus annotables ; hybride classique/appris selon variation et tolérance métier. Conserver procédure d'analyse des faux positifs.

## Sources et cartes

- [PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265).
- [PaDiM, §III](https://arxiv.org/abs/2011.08785).
- [Cartes associées](../73-patchcore-padim.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
