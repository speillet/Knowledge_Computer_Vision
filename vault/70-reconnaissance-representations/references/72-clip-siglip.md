---
id: CV-CLIP
type: methode
domaine: d07
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent contraste image–texte, candidats et décalage de domaine. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-CLIP-001

**Question de travail** : Comment CLIP peut-il classer une image avec des classes qu’on décrit par texte ?

**Réponse de référence** : Encoder image et descriptions, comparer dans un espace aligné puis appliquer une règle de décision sur ces candidats.

**Mécanisme de décision** : chaque description de classe définit un candidat textuel dans l'espace partagé. L'image est comparée à ces candidats, puis une règle choisit ou rejette une proposition. Le vocabulaire constitue donc une partie de la définition du classifieur, même sans entraînement d'une tête supplémentaire.

**Exemple construit** : proposer seulement « pièce correcte » et « pièce rayée » force une comparaison entre ces formulations, même si l'image montre une autre pièce ou un fond vide. Le meilleur candidat peut être le moins mauvais. Tester des descriptions alternatives sur validation, conserver des négatifs et définir une politique de rejet mesurée. La similarité image–texte peut servir à la recherche ou à une classification par descriptions ; elle ne fournit pas à elle seule une explication générée ni la localisation précise d'une rayure. L'interface et la métrique doivent correspondre à la sortie demandée.

### Cas lié à CV-CLIP-004

**Question de travail** : Comment tester un classifieur image–texte sans régler les prompts sur le test final ?

**Réponse de référence** : Créer des variantes sur validation, figer prompts et vocabulaire, puis mesurer erreurs et rejets sur test séparé par scène/domaine.

**Pourquoi les prompts sont des paramètres** : choisir une formulation en fonction de son score sur le test utilise indirectement ses labels pour régler le système. Même sans gradient, cette sélection peut suradapter la décision aux exemples censés fournir une mesure indépendante.

**Protocole proposé** : définir un ensemble de formulations et une règle de combinaison sur validation, conserver le vocabulaire et les seuils, puis ouvrir le test final une fois les choix figés. Séparer scènes ou domaines selon le futur usage et documenter les catégories absentes. Rapporter les erreurs et la sensibilité aux formulations sans ne garder que les cas favorables. Pour une nouvelle itération après analyse d'échecs, préparer une autre évaluation indépendante. Une bonne pratique de transfert conserve ainsi une distinction entre exploration du modèle et estimation de sa généralisation, même lorsque l'outil est qualifié de zero-shot.

**Repère documentaire de cette passe** : [CLIP](https://arxiv.org/html/2103.00020v1), §§2–3, apprentissage et évaluation zero-shot. Les autres développements figurent dans les [cartes associées](../72-clip-siglip.md).

## Sources et cartes

- [CLIP, §§2.3,3 et limites §6](https://arxiv.org/abs/2103.00020).
- [SigLIP, §3 et Algorithm1](https://arxiv.org/abs/2303.15343).
- [Cartes associées](../72-clip-siglip.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
