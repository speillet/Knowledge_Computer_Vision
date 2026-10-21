---
id: CV-BIOMETRIE
type: comparaison
domaine: d07
poles: [E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 2
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# Reconnaissance biométrique, ArcFace et PAD

## Problème, données et hypothèses

Comparer des identités visuelles selon un protocole, sans confondre vérification 1:1, identification 1:N et détection de présentation. Entrées : acquisitions et embeddings ; sorties : scores/décisions conditionnées au seuil. Cette fiche n'établit aucune conformité réglementaire.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

ArcFace apprend une séparation angulaire de représentations d'identité. Une comparaison d'embeddings ne détecte pas automatiquement une photo, un écran ou autre attaque par présentation ; PAD est un autre problème avec son protocole.

## Mathématiques, conventions et unités

FMR/FNMR décrivent des erreurs de comparaison sous un seuil ; FAR/FRR système dépendent aussi de la procédure et des échecs d'acquisition. Un EER est un point d'équilibre d'un protocole, pas le résultat à très faible taux de fausse acceptation. Les similarités restent dépendantes du domaine.

## Paramètres et propriétés

Qualifier populations, qualité, enrolment, seuil et données ; évaluer sous-groupes et conditions d'acquisition. Une référence de standard PAD doit être versionnée lors d'une étude dédiée ; aucune certification n'est déduite d'un modèle.

## Coût et implémentation

Encoder, rechercher et maintenir la galerie ont des coûts différents entre 1:1 et 1:N. Aucun visage réel ni système biométrique exécuté.

## Évaluation et variation contrôlée

Variation proposée : qualité/pose puis taille de galerie séparément. Mesurer au seuil métier et intervalles selon protocole, pas seulement une accuracy globale ou l'EER.

## Échecs et diagnostic

Bon score moyen mais échecs sur une condition : stratifier acquisition et comparaison, inspecter seuil et données. Une détection de visage correcte n'atteste ni identité ni liveness.

## Alternatives et usages

Vérification, identification, qualité et PAD exigent sorties et références distinctes ; documenter les limites de généralisation.

## Sources et cartes

- [Ngan et al. 2023, NISTIR 8491, résumé PAD](https://www.nist.gov/publications/face-analysis-technology-evaluation-fate-part-10-performance-passive-software-based)

- [ArcFace, objectif et évaluation](https://arxiv.org/abs/1801.07698).
- [NIST FRTE 1:1, FMR/FNMR](https://pages.nist.gov/frvt/html/frvt11.html).
- [Cartes associées](../75-embeddings-biometrie.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
