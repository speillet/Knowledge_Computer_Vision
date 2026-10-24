# Revue — Contrats de données, profiling et pipelines vidéo — 2026-10-24

## Synthèse

5 cartes examinées pour leur pertinence et leur développement ; 5 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : contrats, files et âge de l’information. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-PIPELINE-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comparaison : séparer latence débit et fraîcheur | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 43 → 191 mots lexicaux |
| CV-PIPELINE-002 | Protocole proposé sous hypothèses ; noyau antérieur conservé | raisonnement : raisonner sur une file vidéo | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 48 → 196 mots lexicaux |
| CV-PIPELINE-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | pratique : définir un benchmark complet | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 44 → 190 mots lexicaux |
| CV-PIPELINE-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | conception : dimensionner huit flux sous p99 | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 95 → 218 mots lexicaux |
| CV-PIPELINE-005 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : localiser un goulot par trace | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 49 → 188 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/140-ingenierie-systemes/141-contrats-profiling-video.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/140-ingenierie-systemes/references/141-contrats-profiling-video.md) : révision 3, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [GStreamer, queue](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html) : limites, blocage, leaky et niveaux courants, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Le comportement de file est documenté ; les décompositions de latence et choix de politique sont des propositions sous contraintes, pas des mesures matérielles.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
