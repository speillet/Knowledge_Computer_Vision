---
id: CV-FLANN
type: methode
domaine: d04
poles: ["B", "E", "F"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
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

## Sources et cartes

- [Muja et Lowe 2009, §§2–3, recherche approchée et configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf).
- [OpenCV 4.13, Feature Matching, BF et FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html).
- [Cartes associées](../48-flann.md) : CV-FLANN-001 à 004.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
