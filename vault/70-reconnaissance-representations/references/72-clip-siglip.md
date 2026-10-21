---
id: CV-CLIP
type: methode
domaine: d07
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-REPRESENTATIONS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# CLIP, SigLIP et reconnaissance par texte

## Problème, données et hypothèses

Relier images et descriptions dans un espace commun pour retrieval ou classification à vocabulaire défini au moment de l'usage. Entrées : images, textes et preprocessing du modèle ; sortie : similarités ou décisions sous protocole. Un encodeur contrastif ne génère pas à lui seul une explication textuelle.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-REPRESENTATIONS](71-representations-transfert.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

CLIP rapproche les paires positives et compare les candidats par un objectif contrastif. SigLIP utilise un objectif sigmoid par paire avec température/biais appris. Le zero-shot construit des descriptions de classes puis les compare aux images.

## Mathématiques, conventions et unités

Une similarité peut écrire $s_{ij}=\tau\langle v_i/\|v_i\|,t_j/\|t_j\|\rangle$, température inverse $\tau$ selon convention. Le softmax sur un ensemble de candidats est relatif à cet ensemble. Ajouter un candidat change les valeurs normalisées ; celles-ci ne sont pas une preuve de probabilité de vérité calibrée.

## Paramètres et propriétés

Version/checkpoint, prompts, langues, ensemble de labels, résolution et normalisation. Tester synonymes et négatifs difficiles. Sigmoid ne garantit pas non plus une calibration hors distribution.

## Coût et implémentation

Encoder/indexer des textes peut être amorti ; images, taille du vocabulaire et recherche de voisins ont un coût. Aucun modèle exécuté ; les résultats de papiers ne valent pas validation sur le domaine cible.

## Évaluation et variation contrôlée

Baseline : classifieur fermé sur catégories connues face à classification par texte. Varier prompts puis vocabulaire séparément ; mesurer erreurs, rejets et classes non représentées avec labels de référence.

## Échecs et diagnostic

Un objet absent reçoit un score fort : vérifier candidats, biais de descriptions et hors-distribution ; prévoir décision de rejet mesurée, sans inventer un seuil universel.

## Alternatives et usages

Classification fermée si taxonomie stable et données suffisantes ; open-vocabulary pour un autre compromis. Retrieval, grounding et génération textuelle nécessitent des sorties et évaluations distinctes.

## Sources et cartes

- [CLIP, §§2.3,3 et limites §6](https://arxiv.org/abs/2103.00020).
- [SigLIP, §3 et Algorithm1](https://arxiv.org/abs/2303.15343).
- [Cartes associées](../72-clip-siglip.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
