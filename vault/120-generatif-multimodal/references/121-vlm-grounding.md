---
id: CV-VLM
type: comparaison
domaine: d12
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
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

L'entrée est convertie en tokens/features visuels et textuels selon la méthode ; leur nombre, la résolution et le contexte conditionnent le coût. L’entraînement génératif optimise un objectif sur les tokens ; le décodage produit ensuite une séquence selon une stratégie de recherche ou d’échantillonnage. Aucun de ces objectifs ne constitue une preuve de vérité visuelle. Un score de vraisemblance texte ne remplace pas une annotation de boîte ou de masque.

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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent connecteur, ancrage visuel et test de dépendance à l’image. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-VLM-001

**Question de travail** : Que distingue CLIP utilisé pour comparer image et texte, un VLM génératif et un VLA ?

**Réponse de référence** : CLIP compare des représentations image–texte ; un VLM génère des sorties conditionnées par vision/langage ; un VLA produit une interface d’action selon sa conception.

**Définir l'interface** : comparer des embeddings sert à classer ou rechercher parmi des candidats ; générer du texte produit une séquence conditionnée ; produire des actions engage une autre représentation et un autre environnement d'évaluation. Une architecture peut partager des briques sans que ces contrats deviennent interchangeables.

**Exemple construit** : « une pièce est présente » peut être une description plausible, mais ne fournit ni une boîte validée ni une commande robotique correctement référencée. Pour une application, préciser format de sortie, temps de validité et référence attendue, puis mesurer omissions et fausses assertions. Si des actions sont étudiées, distinguer connaissance de l'interface et validation d'une politique en boucle fermée. Le parcours couvre ici la perception et ses limites ; le passage à la commande ne se déduit pas d'une réponse verbale convaincante ni d'un score de génération élevé. Les preuves doivent correspondre à ce que le système promet réellement.

### Cas lié à CV-VLM-004

**Question de travail** : Cas D — diagnostic : un VLM décrit des objets absents sur des images industrielles. Quelle enquête mène à une correction vérifiable ?

**Réponse de référence** : Vérifier image réellement reçue, résolution/prompt, distribution, négatifs et référence ; classer hallucinations et omissions puis tester une intervention à la fois.

**Ablation discriminante** : garder l'image et les labels de référence, modifier uniquement la formulation sur validation, puis comparer à une chaîne visuelle structurée. Tester aussi des images sans objet cible et des variations de résolution. Cela aide à distinguer une information mal transmise d'une tendance à compléter linguistiquement une scène familière.

**Critère de correction** : chercher une baisse mesurée des assertions fausses sans augmenter silencieusement les omissions. Une consigne de prudence peut changer le style des réponses sans rendre leur contenu plus exact. Conserver une politique de refus, les entrées réellement traitées et le checkpoint pour reproduire les erreurs. Toute amélioration reste liée au protocole ; aucun prompt ne constitue ici une garantie générale de supprimer les hallucinations sur tous les nouveaux produits.

**Repère documentaire de cette passe** : [BLIP-2](https://arxiv.org/html/2301.12597v3), §3, connecteur visuel et entraînement. Les autres développements figurent dans les [cartes associées](../121-vlm-grounding.md).

## Sources et cartes

- [Florence-2, résumé](https://arxiv.org/abs/2311.06242) : représentation par prompts pour plusieurs tâches.
- [RT-2, résumé et fig. 1](https://arxiv.org/abs/2307.15818) et [π0, résumé](https://arxiv.org/abs/2410.24164) : interface vision–langage–action, sans validation robotique du projet.

- [BLIP-2, architecture](https://arxiv.org/abs/2301.12597).
- [LLaVA original](https://arxiv.org/abs/2304.08485).
- [Flamingo](https://arxiv.org/abs/2204.14198).
- [OpenVLA, interface actions](https://openvla.github.io/).
- [Cartes associées](../121-vlm-grounding.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
