---
id: CV-SAM
type: methode
domaine: d09
poles: [A, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent prompts, ambiguïté de masque et mémoire temporelle. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-SAM-001

**Question de travail** : SAM attribue-t-il automatiquement une classe sémantique à chaque pixel ?

**Réponse de référence** : Non : son contrat central est le masque guidé par prompt, pas une taxonomie sémantique complète.

**Lecture de la condition** : un point, une boîte ou un masque guide la région d'intérêt. La segmentation répond à ce conditionnement ; attribuer ensuite un nom de classe demande une autre information ou un autre composant. Un masque très précis peut donc être utile pour annoter sans fournir directement une taxonomie complète.

**Exemple construit** : un utilisateur désigne une pièce parmi plusieurs objets. Le masque produit délimite une région candidate, mais ne démontre pas qu'il s'agit du bon type de pièce ni qu'aucun autre objet n'a été oublié. Évaluer qualité de frontière, ambiguïtés et effort de correction avec des prompts comparables. Si une pipeline ajoute un texte ou un détecteur, préciser cette nouvelle chaîne au lieu d'attribuer ses sorties à SAM seul. Le contrat dépend du checkpoint et de l'interface réellement utilisés ; une possibilité explorée dans un papier n'est pas automatiquement une fonction disponible de chaque modèle distribué.

### Cas lié à CV-SAM-003

**Question de travail** : Pourquoi une annotation vidéo interactive avec corrections sur des frames futures ne se compare-t-elle pas directement à un tracker causal ?

**Réponse de référence** : Elle dispose d’informations différentes ; budget d’interaction et accès temporel modifient la tâche.

**Différence d'information** : corriger un masque après avoir vu la suite peut résoudre une ambiguïté qui était réelle à l'instant de la frame. L'annotation finale profite alors d'observations et d'interventions indisponibles pour une décision immédiate. La qualité finale et la disponibilité à temps sont deux propriétés distinctes.

**Protocole proposé** : annoncer frames consultées, nombre de clics ou corrections, propagation autorisée et instant où chaque sortie devient disponible. Comparer soit à budget identique, soit comme un compromis explicitement différent. Conserver les pertes et ambiguïtés au lieu de les effacer par un reset non compté. Un outil interactif peut être excellent pour produire une vérité terrain sans être un tracker autonome déployable avec les mêmes performances. Cette distinction protège les conclusions du benchmark et relie le coût humain, le temps et la qualité au véritable usage du système.

**Repère documentaire de cette passe** : [SAM 2](https://arxiv.org/html/2408.00714v2), architecture, masklets, prompts et mémoire. Les autres développements figurent dans les [cartes associées](../94-sam-sam2.md).

## Sources et cartes

- [SAM, §3 et prototype texte §7.5](https://arxiv.org/abs/2304.02643).
- [SAM 2, architecture et mémoire](https://arxiv.org/abs/2408.00714).
- [Cartes associées](../94-sam-sam2.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
