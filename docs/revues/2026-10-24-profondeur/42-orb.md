# Revue — ORB — détection et descripteur binaire orienté — 2026-10-24

## Synthèse

6 cartes examinées pour leur pertinence et leur développement ; 6 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : séparer détection, orientation, représentation et norme. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ORB-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | algorithme : reconstruire le mécanisme d'ORB | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 97 → 216 mots lexicaux |
| CV-ORB-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : relier représentation et distance | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 106 → 219 mots lexicaux |
| CV-ORB-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | pratique : choisir la norme après changement de variante | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 103 → 217 mots lexicaux |
| CV-ORB-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comparaison : distinguer deux filtres de correspondances | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 96 → 220 mots lexicaux |
| CV-ORB-005 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : diagnostiquer une perte de répétabilité | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 104 → 229 mots lexicaux |
| CV-ORB-006 | Protocole proposé sous hypothèses ; noyau antérieur conservé | conception : articuler contrainte de calcul et réussite de tâche | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 111 → 227 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/40-features-matching/42-orb.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/40-features-matching/references/42-orb.md) : révision 4, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [OpenCV 4.13, ORB](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html) : Theory, orientation et BRIEF tourné, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Normes et WTA_K confrontés aussi à OpenCV 4.13, Feature Matching, et Context7. Le PDF original de Rublee n’était pas accessible pendant cette passe : ses benchmarks ne sont pas revalidés ici.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
