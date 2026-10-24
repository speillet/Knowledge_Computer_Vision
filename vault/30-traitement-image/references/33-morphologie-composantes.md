---
id: CV-MORPHO
type: methode
domaine: d03
poles: [A, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 3
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d03]
---
# Morphologie et composantes connexes

## Problème, données et hypothèses

Modifier une géométrie binaire et regrouper ses régions selon une connectivité. Entrées : masque avec polarité définie, structurant, ancrage et bord ; sorties : masque transformé ou labels. Un label de composante n'est ni une classe sémantique ni une identité temporelle.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

L'érosion retire les points sans voisinage compatible ; la dilatation étend le support. Ouverture et fermeture composent ces opérations dans des ordres différents. Les composantes connexes regroupent ensuite des pixels reliés selon 4 ou 8 voisins.

## Mathématiques, conventions et unités

Pour un structurant symétrique B centré, $A\ominus B=\{x:x+B\subseteq A\}$ et $A\oplus B=\{a+b:a\in A,b\in B\}$. Une ouverture est $(A\ominus B)\oplus B$. B exprime une échelle en pixels : une variation de résolution change son sens physique.

## Paramètres et propriétés

Fixer taille/forme de B, itérations, connectivité et traitement des trous. Deux régions en contact peuvent fusionner ; une opération utile contre le bruit peut supprimer un vrai petit défaut.

## Coût et implémentation

Le coût dépend de l'image, du structurant et de l'algorithme. Les labels sont internes à une image et peuvent être renumérotés. Pseudocode illustratif : nettoyer → étiqueter → mesurer → contrôler objets manquants ; aucune exécution image annoncée.

## Évaluation et variation contrôlée

Variation analytique : deux pixels qui se touchent seulement en diagonale sont deux composantes en 4-connectivité et une en 8-connectivité. Sur image réelle, mesurer erreurs de fusion/séparation avant de filtrer les petites régions.

## Échecs et diagnostic

Comptage trop faible : regarder les ponts ajoutés par dilatation/fermeture et la connectivité. Comptage trop élevé : inspecter fragments, bruit et structurant ; ne pas considérer la taille comme vérité sémantique.

## Alternatives et usages

Watershed à marqueurs pour séparer des objets joints ; segmentation d'instances si l'apparence et les contacts dépassent un modèle géométrique simple.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent support géométrique, topologie et convention de connectivité. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-MORPHO-001

**Question de travail** : Quel effet géométrique distingue ouverture et fermeture binaires, et pourquoi choisir la taille du structurant avec la tâche ?

**Réponse de référence** : L’ouverture érode puis dilate et peut retirer de petites structures de premier plan ; la fermeture dilate puis érode et peut combler des trous ou intervalles. Choisir le structurant selon les tailles et formes à conserver.

**Explication géométrique** : l'érosion exige que le structurant tienne dans le premier plan ; elle retire donc des positions proches de certaines frontières. La dilatation étend ensuite les positions conservées. Dans une ouverture, une structure trop étroite pour survivre à l'érosion ne réapparaît pas simplement parce qu'une dilatation suit. Dans une fermeture, des intervalles suffisamment petits peuvent être comblés.

**Choix d'échelle** : une taille en pixels représente une taille physique seulement si résolution et géométrie sont connues. Un structurant utile sur une caméra peut effacer les défauts recherchés après un changement de résolution. Dans un exemple construit, comparer un défaut fin et une poussière de taille voisine montre que la morphologie ne possède aucune information sémantique pour les départager. Évaluer donc suppressions et fusions sur les cas critiques, avec polarité du masque, forme du structurant et traitement du bord explicités.

### Cas lié à CV-MORPHO-003

**Question de travail** : Après fermeture morphologique, deux pièces proches sont comptées comme une seule. Quelle hypothèse vérifier ?

**Réponse de référence** : Le structurant peut avoir créé un pont ; inspecter le masque avant/après et la distance entre objets.

**Mécanisme de l'erreur** : la dilatation peut joindre deux régions séparées par un intervalle plus petit que l'échelle du structurant. L'érosion suivante ne restaure pas nécessairement cet intervalle ; la fermeture peut conserver une région commune. L'étiquetage connexe compte alors correctement un seul ensemble relié, mais cet ensemble ne représente plus un seul objet du monde.

**Contrôle construit** : afficher les pixels ajoutés entre les masques avant et après, puis faire varier la taille et l'orientation du structurant à image fixe. Si le nombre d'objets change quand le pont apparaît, la cause est localisée. Un filtrage par aire après fusion ne retrouve pas les deux pièces : il agit sur la région déjà regroupée. Selon la scène, préserver l'intervalle, utiliser des marqueurs de séparation ou une segmentation d'instances. Toute correction doit aussi être évaluée sur des objets réellement jointifs, pour éviter de résoudre un cas en fragmentant les autres.

**Repère documentaire de cette passe** : [OpenCV 4.13, Morphological Transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html), erosion, dilation, opening, closing. Les autres développements figurent dans les [cartes associées](../33-morphologie-composantes.md).

## Sources et cartes

- [OpenCV 4.13.0, connectedComponents, paramètres connectivity et labels](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html).

Pour la morphologie ensembliste avec les conventions annoncées, l’ouverture est anti-extensive et la fermeture extensive : elles peuvent supprimer de petites structures de premier plan ou combler de petits intervalles. Sur une image finie, le traitement des bords doit rester explicite.

- [OpenCV, morphological transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html).
- [Cartes associées](../33-morphologie-composantes.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
