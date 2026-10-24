---
id: CV-FLANN
type: methode
domaine: d04
poles: ["B", "E", "F"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-MATCHING"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# FLANN — recherche approchée et contrat de distance

## Prérequis et compétences

**Prérequis obligatoires** : [CV-MATCHING](43-detecteurs-matchers.md).
**Compétences visées** : choisir recherche approchée ou exhaustive; préserver la métrique des descripteurs; évaluer une approximation de voisins; mesurer la courbe temps rappel.
Les notions connexes restent des alternatives, pas des dépendances implicites.

## Problème et contrat des données

Rechercher rapidement des voisins parmi de nombreux descripteurs. L’entrée comprend base, requêtes, métrique et budget de recherche ; la sortie contient des candidats avec leurs distances, sans garantie générale de voisin exact. Un index pour vecteurs flottants en L2 n’est pas interchangeable avec un index pour chaînes binaires en Hamming.

## Mécanisme, paramètres et coût

FLANN regroupe plusieurs structures de recherche et des choix de configuration, pas un seul algorithme de matching. Muja et Lowe étudient notamment forêts de kd-trees aléatoires et arbres de k-means hiérarchiques. L’index construit une organisation de la base ; la requête explore une fraction des candidats. Arbres et budget de visite échangent mémoire, construction, temps de requête et rappel. OpenCV 4.13 montre un kd-tree pour SIFT et un index LSH pour des descripteurs ORB binaires usuels. Ces configurations ne rendent pas toute métrique compatible.

## Mathématiques et conventions

Sur un échantillon, comparer le voisin approché $\hat n(q)$ au voisin exact $n^*(q)$ calculé avec la même distance. Le recall@1 est la fraction de requêtes dont le voisin exact est retrouvé ; traiter les ex æquo selon un protocole annoncé. Le coût amorti est $T_{construction}+N_qT_{requête}$ pour $N_q$ requêtes. La distance de chaque match conserve le sens de la métrique utilisée ; vérifier aussi distance ou distance au carré dans l’API avant tout ratio. La recherche des deux voisins doit être assez fiable pour un ratio test pertinent.

## Évaluation et variation contrôlée

Baseline proposée : recherche exhaustive sur un sous-ensemble représentatif. Faire varier le budget de recherche, en conservant base, requêtes et métrique ; mesurer recall@1/2, durée de construction, latence par lot, mémoire et inliers géométriques. Exemple construit : 2 s de construction plus 100 requêtes à 1 ms coûtent 2,1 s ; une brute force à 3 ms coûte 0,3 s. Avec 10 000 requêtes, les coûts deviennent 12 s contre 30 s. L’index ne gagne donc pas pour tout usage.

## Diagnostic et alternatives

Une erreur de type avec ORB n’autorise pas à convertir aveuglément les octets en float pour L2 : conserver la métrique de Hamming ou choisir un index adapté. Une baisse d’inliers après accélération peut venir du rappel des deux voisins, pas du détecteur. Une petite base peut favoriser la recherche exhaustive. Une base évolutive impose aussi de mesurer reconstruction et invalidation de l’index. Aucun benchmark FLANN exécuté ; les coûts ci-dessus sont hypothétiques.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent rappel des voisins, ratio et amortissement de l’index. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-FLANN-001

**Question de travail** : Pourquoi un index FLANN peut-il être moins intéressant qu’une recherche exhaustive sur une petite base utilisée une seule fois ?

**Réponse de référence** : Le coût de construction et la mémoire peuvent dépasser le gain sur les requêtes. Comparer $T_{construction}+N_qT_{requête}$ au coût exhaustif pour le nombre réel de requêtes, avec le même objectif de rappel.

**Exemple de coût amorti** : avec 2 s de construction et 1 ms par requête, cent requêtes coûtent environ 2,1 s, tandis qu'une recherche exhaustive à 3 ms chacune coûte 0,3 s. Pour dix mille requêtes sur la même base, les coûts hypothétiques deviennent 12 s et 30 s. Les valeurs illustrent un calcul, sans constituer un benchmark FLANN.

**Interprétation** : le nombre réel de réutilisations de l'index et sa durée de validité décident de l'amortissement. Une base reconstruite à chaque image peut perdre cet avantage. Comparer également la qualité des voisins : diminuer le temps en acceptant un rappel insuffisant n'est pas un gain à objectif constant. Le choix dépend du volume, du matériel, des lots et du protocole.

### Cas lié à CV-FLANN-004

**Question de travail** : Quelles mesures permettent de régler le budget d’une recherche approchée sans masquer une dégradation du pipeline ?

**Réponse de référence** : Mesurer rappel des voisins par rapport à une baseline exacte, latence, mémoire, construction et nombre/qualité des inliers finaux. Faire varier un budget à la fois sur des données réservées.

**Séparer trois mesures** : le rappel de voisins compare l'index à une recherche exacte dans un espace de descripteurs ; la précision des matches compare les paires à une vérité de correspondance ; le succès géométrique juge la transformation obtenue. Ces niveaux peuvent diverger sur des textures répétitives ou des régions mal réparties.

**Courbe de décision proposée** : pour plusieurs budgets, conserver base et requêtes puis reporter temps complet, mémoire, rappel des deux premiers voisins et erreurs du recalage final. Ajouter le coût d'entretien si la base évolue. Choisir une région de fonctionnement qui respecte les contraintes du produit, puis la vérifier sur un lot réservé. Ce résultat ne se résume pas à maximiser le rappel : une recherche exhaustive peut être inutilement chère, mais une approximation très rapide peut être insuffisante.

**Repère documentaire de cette passe** : [Muja et Lowe 2009](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf), §§2–3, index et compromis de recherche. Les autres développements figurent dans les [cartes associées](../48-flann.md).

## Sources et cartes

- [Muja et Lowe 2009, §§2–3, recherche approchée et configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf).
- [OpenCV 4.13, Feature Matching, BF et FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html).
- [Cartes associées](../48-flann.md) : CV-FLANN-001 à 004.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
