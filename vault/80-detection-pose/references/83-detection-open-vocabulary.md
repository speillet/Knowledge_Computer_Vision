---
id: CV-OPENVOC
type: methode
domaine: d08
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-CLIP", "CV-DETECTEURS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d08]
---
# Détection open-vocabulary et grounding

## Problème, données et hypothèses

Localiser des régions liées à un texte ou à un vocabulaire évolutif. Distinguer classification image–texte, détection open-vocabulary et grounding référentiel. Entrées : image plus candidats/prompt ; sorties : boîtes ou régions avec scores selon le modèle.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-CLIP](../../70-reconnaissance-representations/references/72-clip-siglip.md) ; [CV-DETECTEURS](82-detection-fasterrcnn-yolo-detr.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Des méthodes telles qu'OWL-ViT et Grounding DINO relient représentations visuelles et langage pour produire des régions. Le vocabulaire textuel ne remplace pas un protocole d'annotation, les négatifs ni une politique de rejet.

## Mathématiques, conventions et unités

Une similarité région–texte et un seuil conduisent à une décision sous ensemble de candidats. La normalisation des scores dépend du modèle ; elle ne certifie pas présence, calibration ou absence d'objet hors vocabulaire.

## Paramètres et propriétés

Version, prompt, tokenisation, résolution et seuils. Tester synonymes, objets proches, négatifs et classes absentes ; « open » ne signifie pas taxonomie illimitée comprise parfaitement.

## Coût et implémentation

Encodage texte/image, nombre de candidats et posttraitements comptent. Aucun modèle exécuté et aucun gain de mise à jour mensuelle annoncé comme mesuré.

## Évaluation et variation contrôlée

Baseline : détecteur fermé réentraîné versus approche texte sur nouveaux produits séparés du réglage. Mesurer AP/rappel, rejets et coût des mises à jour ; figer les formulations avant test.

## Échecs et diagnostic

Faux positifs sur descriptions larges : analyser ambiguïté du texte et taxonomie. Un score haut n'est pas une preuve de grounding exact.

## Alternatives et usages

Combiner détecteur connu, embeddings et annotations ciblées selon fréquence de nouveauté et tolérance d'erreur. Une génération VLM n'est pas une détection évaluée par boîtes.

## Sources et cartes

- [OWL-ViT, méthode](https://arxiv.org/abs/2205.06230).
- [Grounding DINO, méthode](https://arxiv.org/abs/2303.05499).
- [Cartes associées](../83-detection-open-vocabulary.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
