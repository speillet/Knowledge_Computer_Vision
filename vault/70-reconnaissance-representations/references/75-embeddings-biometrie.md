---
id: CV-BIOMETRIE
type: comparaison
domaine: d07
poles: [E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 3
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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent vérification, identification et point d’exploitation. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-BIOMETRIE-001

**Question de travail** : Un embedding ArcFace séparant bien les identités prouve-t-il qu’une présentation est authentique ?

**Réponse de référence** : Non : la comparaison d’identité et PAD ont des cibles et données d’évaluation distinctes.

**Différence des cibles** : la reconnaissance compare une acquisition à une identité de référence. La détection de présentation cherche à distinguer certains types d'acquisition ou d'attaque selon un autre protocole. Une reproduction peut conserver une apparence d'identité très proche sans être une présentation authentique.

**Exemple construit** : une photo nette peut produire un embedding proche de celui de la personne ; cette proximité répond à une question d'apparence, pas à la présence physique de cette personne au moment de l'acquisition. Définir et évaluer les deux sorties avec des données adaptées, puis leur intégration dans le système. Une détection de visage correcte ne résout pas non plus la vérification d'identité. Le propos reste un contrat technique de perception et d'évaluation ; aucune conformité, certification ou garantie de résistance à toute présentation n'est déduite du seul modèle d'embedding.

### Cas lié à CV-BIOMETRIE-002

**Question de travail** : Pourquoi l’EER ne suffit-il pas pour un système exploitant un seuil à très faible FMR ?

**Réponse de référence** : Il décrit un point d’équilibre qui peut différer fortement du seuil visé ; mesurer FNMR et autres erreurs au point requis.

**Lecture de la courbe** : déplacer le seuil modifie simultanément comparaisons acceptées à tort et identités rejetées à tort. L'EER désigne une égalité de ces taux dans un protocole donné ; un produit visant un très faible taux de fausse correspondance fonctionne généralement ailleurs sur la courbe.

**Évaluation proposée** : fixer le seuil sur des données de réglage, puis mesurer le taux de faux non-matches au niveau de FMR visé sur un test indépendant. Consigner qualité d'acquisition, population, enrôlement et taille des ensembles ; examiner les sous-groupes et l'incertitude statistique lorsqu'elle est pertinente. Des échecs de capture ajoutent encore des événements au niveau système. Une bonne valeur moyenne ne prédit donc pas toutes les conditions d'exploitation. Le point de fonctionnement et les unités de comparaison doivent rester visibles pour que deux résultats de reconnaissance soient interprétables.

**Repère documentaire de cette passe** : [NIST, FRTE 1:1 Verification](https://pages.nist.gov/frvt/html/frvt11.html), présentation de l’évaluation vérification et erreurs. Les autres développements figurent dans les [cartes associées](../75-embeddings-biometrie.md).

## Sources et cartes

- [Ngan et al. 2023, NISTIR 8491, résumé PAD](https://www.nist.gov/publications/face-analysis-technology-evaluation-fate-part-10-performance-passive-software-based)

- [ArcFace, objectif et évaluation](https://arxiv.org/abs/1801.07698).
- [NIST FRTE 1:1, FMR/FNMR](https://pages.nist.gov/frvt/html/frvt11.html).
- [Cartes associées](../75-embeddings-biometrie.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
