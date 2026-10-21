---
id: CV-SAM
type: methode
domaine: d09
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-SEGMENTATION"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d09]
---
# SAM, SAM 2 et segmentation guidée en vidéo

## Problème, données et hypothèses

Produire des masques conditionnés par points, boîtes ou masques selon le modèle. SAM traite la segmentation promptable d'image ; SAM 2 ajoute mémoire/propagation vidéo. Ni classes sémantiques ni détection automatique de toutes identités ne sont garanties par ces sorties.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SEGMENTATION](93-semantique-instances-panoptique.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Un encodeur image et un encodeur de prompt conditionnent un décodeur de masque ; SAM peut représenter une ambiguïté par plusieurs propositions. SAM 2 exploite informations mémorisées pour propager des masklets avec prompts et corrections.

## Mathématiques, conventions et unités

Une carte de masque et son score prédit restent conditionnés par le prompt et le modèle ; ils ne constituent pas une annotation de classe. Le temps d'un prompt inclut encodage, cache et décodage selon usage. En vidéo, le protocole doit dire si des frames futures ou corrections rétroactives sont autorisées.

## Paramètres et propriétés

Checkpoint, résolution, politique de prompts, sélection de masque et mémoire vidéo. Le prototype text-to-mask du papier SAM n'est pas le contrat automatique de son checkpoint/API standard.

## Coût et implémentation

Cache de l'encodeur amortissable sur plusieurs prompts ; vidéo et mémoire ont un coût. Aucun modèle exécuté ni performance mobile annoncée.

## Évaluation et variation contrôlée

Baseline : mêmes prompts/budget d'interaction puis propagation sur vidéo annotée. Varier occultation et mouvement ; mesurer qualité des masques, corrections et délai en protocole causal ou offline explicite.

## Échecs et diagnostic

Un masque suit le mauvais objet après croisement : inspecter prompts, mémoire, visibilité et identité ; ne pas assimiler une bonne segmentation d'une frame au bon suivi temporel.

## Alternatives et usages

Segmentation supervisée fermée, annotation assistée ou modèle promptable selon labels et interaction disponibles. La classification/association peut nécessiter d'autres composants.

## Sources et cartes

- [SAM, §3 et prototype texte §7.5](https://arxiv.org/abs/2304.02643).
- [SAM 2, architecture et mémoire](https://arxiv.org/abs/2408.00714).
- [Cartes associées](../94-sam-sam2.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
