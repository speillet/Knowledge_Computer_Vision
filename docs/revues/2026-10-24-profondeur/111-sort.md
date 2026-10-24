# Revue — SORT — tracking multiobjet par mouvement et association — 2026-10-24

## Synthèse

8 cartes examinées pour leur pertinence et leur développement ; 8 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : filtrage, affectation et cycle de vie des pistes. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SORT-001 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comprehension : séparer les responsabilités du tracker | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 104 → 222 mots lexicaux |
| CV-SORT-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : interpréter un état et ses unités | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 119 → 239 mots lexicaux |
| CV-SORT-003 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : interpréter le poids d'une mesure | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 99 → 212 mots lexicaux |
| CV-SORT-004 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | algorithme : distinguer mémoire et émission | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 113 → 229 mots lexicaux |
| CV-SORT-005 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | pratique : comprendre le rejet après affectation | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 105 → 221 mots lexicaux |
| CV-SORT-006 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : établir un diagnostic discriminant | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 106 → 223 mots lexicaux |
| CV-SORT-007 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comparaison : distinguer les tâches temporelles | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 100 → 219 mots lexicaux |
| CV-SORT-008 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : définir une mesure de performance complète | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 106 → 228 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/110-tracking-association/111-sort.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/110-tracking-association/references/111-sort.md) : révision 4, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [SORT, code au commit 2236dff](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py) : associate_detections_to_trackers et Sort.update, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- L’article 1602.00763v2 a aussi été ouvert ; les cas de cadence et d’expiration sont des déductions du code, sans tracking exécuté.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
