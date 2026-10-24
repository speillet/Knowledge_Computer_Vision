---
id: CV-MATCHING
type: methode
domaine: d04
poles: [B, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-SVD"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# Détecteurs locaux, descripteurs et matchers

## Problème, données et hypothèses

Séparer les responsabilités d'un pipeline local. Détecteur : points et score de localisation ; descripteur : vecteur du patch ; matcher : candidats ; estimation géométrique : cohérence des paires. Les entrées conservent résolution, coordonnées et type de représentation.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Harris cherche une variation d'intensité dans deux directions ; Shi–Tomasi utilise la plus petite valeur propre de la matrice locale. FAST utilise des comparaisons sur un cercle. BRIEF décrit par tests binaires sans être un détecteur. AKAZE construit une représentation multiéchelle non linéaire ; sa variante de descripteur doit être nommée.

## Mathématiques, conventions et unités

La matrice locale $M=\sum w\nabla I\nabla I^T$ décrit l'information de gradient. Deux valeurs propres élevées contraignent deux directions ; une seule donne une ambiguïté le long d'un bord. Le score Harris $\det(M)-k\operatorname{tr}(M)^2$ dépend de son paramètre k et des échelles ; ce n'est pas une probabilité.

## Paramètres et propriétés

Nombre de points, NMS locale, seuils, échelle, norme et filtrage doivent être cohérents. BF compare exhaustivement ; FLANN approxime une recherche avec index et paramètres compatibles. La métrique vient du descripteur, pas du nom du matcher.

## Coût et implémentation

BF coûte environ n×m comparaisons ; un index modifie coût de construction, mémoire et rappel. Aucun exemple de bibliothèque n'est exécuté. Comparer extraction + matching + validation.

## Évaluation et variation contrôlée

Variation analytique : patch d'arête puis coin. Prédire une direction de déplacement mal contrainte sur l'arête. En pratique, mesurer répétabilité et succès géométrique sous bruit, sans assimiler score de coin et précision de recalage.

## Échecs et diagnostic

Beaucoup de points inutiles : inspecter distribution spatiale et répétition. Matches absents : vérifier norme/type, seuils et nombre réel de voisins avant de changer le détecteur.

## Alternatives et usages

SIFT/ORB sont des références complètes ; méthodes apprises si elles améliorent le protocole cible. Une comparaison doit conserver les conditions d'acquisition.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent contrats des étapes et diagnostic avant changement de méthode. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-MATCHING-001

**Question de travail** : Pourquoi un coin localise-t-il mieux un déplacement 2D qu’une arête seule dans un modèle par gradients ?

**Réponse de référence** : Deux directions de variation contraignent le mouvement ; sur une arête, le déplacement tangent est peu observable.

**Modèle local** : pour un petit déplacement $d$, la variation photométrique se rapproche d'une forme quadratique $d^TMd$. La matrice $M$ rassemble les produits des gradients dans le voisinage. Ses directions propres indiquent les directions de déplacement qui changent beaucoup ou peu l'apparence.

**Exemple construit** : sur un bord vertical uniforme, déplacer le patch horizontalement change son contenu ; le déplacer le long du bord peut presque le laisser identique. Un coin visible présente au contraire des changements dans deux directions, ce qui aide à localiser un déplacement. Cela n'implique pas qu'il soit unique dans l'image : les coins d'une grille peuvent tous se ressembler. Distinguer donc information locale de localisation et ambiguïté d'association entre images. Une fenêtre mal éclairée, occultée ou trop grande peut également invalider le petit modèle photométrique malgré des valeurs propres favorables.

### Cas lié à CV-MATCHING-004

**Question de travail** : Deux logos répétés produisent des descripteurs proches. Quel composant permet de tester le modèle physique des correspondances ?

**Réponse de référence** : Une vérification géométrique adaptée à la scène, avec résidus, seuils et couverture ; le matcher seul ne le garantit pas.

**Ce que teste la géométrie** : une homographie pour un plan, ou une contrainte multivue appropriée, relie les positions des candidats dans les images. Le résidu exprime leur désaccord avec ce modèle dans une unité définie. Un matcher choisit des voisins dans une représentation d'apparence ; ces deux problèmes sont différents.

**Limite construite** : deux logos identiques sur un même support peuvent produire un groupe de matches et une transformation cohérents mais correspondant au mauvais logo. Un modèle géométrique ne résout pas nécessairement une symétrie de la scène. Chercher une marque unique, une position attendue ou une observation supplémentaire qui distingue les hypothèses. Contrôler aussi le support spatial des points et des observations réservées. Cette étape fournit des raisons d'accepter une transformation pour un usage précis, sans transformer automatiquement le consensus en preuve d'identité de l'objet.

**Repère documentaire de cette passe** : [OpenCV 4.13, Feature Matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), Brute-Force Matcher, normes et FLANN. Les autres développements figurent dans les [cartes associées](../43-detecteurs-matchers.md).

## Sources et cartes

- [OpenCV 4.13.0, FAST, Feature Detection](https://docs.opencv.org/4.13.0/df/d0c/tutorial_py_fast.html)
- [OpenCV 4.13.0, BRIEF, Theory](https://docs.opencv.org/4.13.0/dc/d7d/tutorial_py_brief.html)
- [OpenCV 4.13.0, AKAZE, Detailed Description et DescriptorType](https://docs.opencv.org/4.13.0/d8/d30/classcv_1_1AKAZE.html)

- [OpenCV Harris, théorie](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html).
- [OpenCV Shi–Tomasi](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html).
- [OpenCV matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html).
- [Cartes associées](../43-detecteurs-matchers.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
