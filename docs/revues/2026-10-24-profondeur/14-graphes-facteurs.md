# Revue — Graphes de facteurs et optimisation incrémentale — 2026-10-24

## Synthèse

5 cartes examinées pour leur pertinence et leur développement ; 4 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : graphe, jauge et coût d’une élimination. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FACTEURS-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comprehension : séparer représentation et solveur | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 158 → 208 mots lexicaux |
| CV-FACTEURS-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : expliquer une jauge | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 125 → 206 mots lexicaux |
| CV-FACTEURS-003 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | diagnostic : vérifier une fermeture de boucle | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 162 → 211 mots lexicaux |
| CV-FACTEURS-004 | Réponse conservée ; pas de nouvelle affirmation | comparaison : choisir un back-end robuste aux fausses boucles | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Aucun écart éditorial retenu | Conserver : 215 mots lexicaux, déjà développée |
| CV-FACTEURS-005 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | algorithme : expliquer la mise à jour incrémentale d'iSAM2 | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 175 → 228 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/10-mathematiques-estimation/14-graphes-facteurs.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/10-mathematiques-estimation/references/14-graphes-facteurs.md) : révision 6, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [GTSAM, Introduction](https://gtsam.org/tutorials/intro.html) : factor graph, Values et prior, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Les propriétés d’élimination sont rapprochées de Ceres, Non-linear Least Squares Solving, Schur solvers ; iSAM2 : Kaess et al. 2012, §§3–4.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
