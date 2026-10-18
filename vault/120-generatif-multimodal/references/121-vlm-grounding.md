---
id: CV-VLM
type: comparaison
domaine: d12
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-CLIP", "CV-VIDEO"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d12]
---
# VLM, grounding et frontière vision–action

## Problème, données et hypothèses

Relier observations visuelles et langage pour questions, descriptions ou sorties structurées. Distinguer un embedding image–texte, un VLM génératif et un VLA produisant des actions. La commande robotique reste hors du périmètre de cette préparation.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-CLIP](../../70-reconnaissance-representations/references/72-clip-siglip.md) ; [CV-VIDEO](../../100-mouvement-video/references/102-points-actions-video.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

BLIP-2 relie encodeur visuel et LLM via Q-Former ; LLaVA combine connecteur et instruction tuning selon version ; Flamingo traite des entrées multimodales entrelacées. Une réponse textuelle peut s'appuyer sur le langage sans être correctement ancrée dans l'image. Florence-2 est une entrée multitâche à approfondir, pas une sortie universelle interchangeable.

## Mathématiques, conventions et unités

L'entrée est convertie en tokens/features visuels et textuels selon la méthode ; leur nombre, la résolution et le contexte conditionnent le coût. Une génération maximise un objectif de tokens, qui n'est pas une preuve de vérité visuelle. Un score de vraisemblance texte ne remplace pas une annotation de boîte ou de masque.

## Paramètres et propriétés

Checkpoint, image processor, prompt, format de sortie, outils éventuels et accès au futur. RT-2/OpenVLA/π0 introduisent une interface d'action ; connaître cette interface ne vaut pas valider une politique robotique.

## Coût et implémentation

Encodage, tokens visuels, contexte vidéo et décodage ont des coûts distincts. Aucun modèle exécuté ni disponibilité matérielle présumée. Les variantes doivent être nommées quand on cite un connecteur ou une propriété précise.

## Évaluation et variation contrôlée

Baseline : pipeline détection/tracking/règles versus VLM, avec mêmes tâches annotées et données réservées. Varier prompt et négatifs contrôlés ; mesurer hallucinations, omissions, localisation et coût, pas seulement fluidité.

## Échecs et diagnostic

Description d'objet absent : inspecter résolution, prompt, hors-distribution et référence ; tester images négatives et formulations alternatives sans sélectionner le meilleur résultat sur test.

## Alternatives et usages

Un pipeline explicite peut offrir des sorties plus contrôlables pour des événements définis ; VLM peut aider sur des descriptions/contextes nouveaux sous évaluation. Grounding doit avoir son protocole.

## Sources et cartes

- [BLIP-2, architecture](https://arxiv.org/abs/2301.12597).
- [LLaVA original](https://arxiv.org/abs/2304.08485).
- [Flamingo](https://arxiv.org/abs/2204.14198).
- [OpenVLA, interface actions](https://openvla.github.io/).
- [Cartes associées](../121-vlm-grounding.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
