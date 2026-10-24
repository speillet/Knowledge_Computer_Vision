---
id: CV-GRABCUT
type: methode
domaine: d09
poles: [A, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d09]
---
# GrabCut, régions et modèles d’apparence

## Problème, données et hypothèses

Extraire un objet à partir d'une initialisation interactive et d'un modèle d'apparence. Entrées : image couleur et rectangle/labels ; sortie : masque selon labels sûrs/probables. Le modèle ne comprend pas automatiquement la sémantique de l'objet demandé.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

GrabCut alterne estimation des distributions de couleur par mélanges gaussiens et optimisation d'une énergie par graph cut. Les termes unaires suivent l'apparence, les relations voisines encouragent une cohérence adaptée aux contours.

## Mathématiques, conventions et unités

Une énergie schématique $E(L)=\sum_p U_p(L_p)+\lambda\sum_{p,q}V_{pq}(L_p,L_q)$ combine coût d'étiquette et régularisation spatiale. L est le masque de labels ; $\lambda$ règle un compromis propre à la variante. Une énergie minimisée n'est pas une preuve de masque métier correct.

## Paramètres et propriétés

Rectangle initial, coups de pinceau, labels certains/probables, itérations et espace couleur. Fond/objet de couleurs proches, trous et transparence peuvent rendre le modèle d'apparence insuffisant.

## Coût et implémentation

Mémoire du graphe et itérations dépendent de la résolution. Aucun appel GrabCut exécuté. Region growing ou contours actifs utilisent d'autres objectifs/initialisations ; ils ne sont ici qu'introduits comme alternatives.

## Évaluation et variation contrôlée

Variation proposée : même objet et initialisation, puis rendre le fond similaire en couleur. Mesurer erreurs de masque et coût d'interaction, avec référence réservée.

## Échecs et diagnostic

L'objet est tronqué : vérifier que des pixels utiles ne sont pas imposés comme fond sûr. Plus d'itérations ne contredit pas une contrainte initiale fausse.

## Alternatives et usages

Watershed pour marqueurs/topographie, méthodes apprises par prompt pour autre généralisation ; conserver coût d'interaction et hypothèses.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent optimisation conditionnelle et rôle des contraintes utilisateur. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-GRABCUT-001

**Question de travail** : Quelles deux opérations principales GrabCut alterne-t-il ?

**Réponse de référence** : Estimer les modèles d’apparence fond/objet puis optimiser les labels via graph cut dans l’énergie définie.

**Intuition de l'alternance** : les labels actuels donnent des exemples de couleur pour le fond et le premier plan ; les modèles d'apparence influencent ensuite le coût de chaque attribution. Les relations entre voisins ajoutent une préférence spatiale. La nouvelle partition sert à une nouvelle estimation, dans les contraintes de l'initialisation.

**Exemple de limite** : si une partie de la cible ressemble au fond, son coût d'apparence peut favoriser la mauvaise région. Une indication utilisateur peut apporter une information que la couleur seule ne fournit pas. Le procédé ne nomme pas automatiquement un objet selon une taxonomie et un minimum d'énergie n'est pas une preuve de vérité métier. Vérifier initialisation et labels sûrs avant d'augmenter les itérations. Pour comparer à une méthode promptable apprise, compter aussi les interventions, les échecs et le coût complet, et pas seulement le temps de la dernière optimisation.

### Cas lié à CV-GRABCUT-003

**Question de travail** : Pour extraire un objet avec couleurs proches du fond, pourquoi comparer coût d’interaction et hypothèses plutôt que seulement temps d’optimisation ?

**Réponse de référence** : Les labels ajoutés par l’utilisateur peuvent fournir l’information manquante ; une solution rapide peut demander beaucoup de corrections.

**Coût réellement payé** : un algorithme rapide peut demander plusieurs retouches si son modèle de couleur sépare mal cible et fond. Une méthode plus coûteuse par appel peut réduire l'interaction ; l'inverse est aussi possible. Les temps doivent inclure la procédure nécessaire pour atteindre une qualité définie.

**Protocole proposé** : fixer des images réservées, une règle d'initialisation et un budget de correction, puis mesurer qualité de masque, nombre d'interventions, temps total et taux d'échec. Ajouter séparément un fond plus proche de la cible pour tester l'hypothèse d'apparence. Conserver les cas non résolus dans le bilan. Un optimum de l'énergie indique que la procédure a satisfait son modèle ; il ne dit pas que ce modèle possède assez d'information pour distinguer l'objet utile. La comparaison doit donc relier hypothèses de la méthode et effort humain, sans choisir seulement sur la durée du solveur.

**Repère documentaire de cette passe** : [OpenCV 4.13, GrabCut](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html), modèle, graph cut et labels certains/probables. Les autres développements figurent dans les [cartes associées](../92-grabcut-regions.md).

## Sources et cartes

- [OpenCV GrabCut, théorie et masques](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
- [Cartes associées](../92-grabcut-regions.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
