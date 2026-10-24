---
id: CV-OPENVOC
type: methode
domaine: d08
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent vocabulaire variable, protocole et sortie localisée. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-OPENVOC-001

**Question de travail** : Pourquoi un classement CLIP d’une image ne remplace-t-il pas directement un détecteur open-vocabulary ?

**Réponse de référence** : Le classement image porte sur l’image globale ; la détection doit aussi localiser les instances avec un protocole de sortie adapté.

**Décomposition de la sortie** : une similarité globale image–texte peut indiquer qu'un contenu est compatible avec une description. Un détecteur doit en plus proposer des positions et distinguer plusieurs occurrences, avec leurs classes ou relations au texte. Un score sur l'image entière ne détermine ni ces boîtes ni leur nombre.

**Exemple construit** : une scène avec deux tasses et une assiette peut bien correspondre au texte « tasse » sans fournir la localisation de chaque tasse. L'évaluation de détection doit vérifier instances, coordonnées et objets manqués, y compris lorsque le prompt est absent de l'image. Un grounding référentiel peut demander encore une autre sortie, comme « la tasse à gauche de l'assiette ». Définir annotations, négatifs, seuils et métriques selon ce contrat. Le langage élargit l'interface des candidats ; il ne dispense pas de vérifier la précision spatiale et les confusions du domaine.

### Cas lié à CV-OPENVOC-003

**Question de travail** : Un prompt large donne des boîtes sur des objets apparentés mais hors cible. Que tester ?

**Réponse de référence** : Définition de classe, formulations/négatifs et score de région sur validation ; inspecter les confusions et annotations.

**Pourquoi le texte peut être en cause** : une description générale peut correspondre à plusieurs catégories visuelles que la taxonomie industrielle sépare. Un modèle peut donc retourner une région plausible pour le langage courant mais incorrecte pour le besoin. Un seuil unique ne résout pas nécessairement cette ambiguïté.

**Enquête construite** : consigner les classes visées et exclues, comparer des formulations plus précises et des négatifs proches sur validation, puis inspecter les régions et annotations. Séparer défaut de localisation et confusion de vocabulaire. Évaluer aussi l'absence de cible, car choisir le meilleur candidat ne prouve pas sa présence. Une nouvelle formulation doit être figée avant le test final. Si le domaine ne fournit pas d'indice discriminant visible, un meilleur prompt peut rester insuffisant ; l'interface doit alors permettre refus ou vérification plutôt que garantir une catégorie exacte.

**Repère documentaire de cette passe** : [Grounding DINO](https://arxiv.org/html/2303.05499v4), méthode et protocole open-set. Les autres développements figurent dans les [cartes associées](../83-detection-open-vocabulary.md).

## Sources et cartes

- [OWL-ViT, méthode](https://arxiv.org/abs/2205.06230).
- [Grounding DINO, méthode](https://arxiv.org/abs/2303.05499).
- [Cartes associées](../83-detection-open-vocabulary.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
