# Revue — Calibration caméra sur mire — méthode de Zhang — 2026-10-24

## Synthèse

7 cartes examinées pour leur pertinence et leur développement ; 7 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : contraintes des vues, resize et contrôle hors apprentissage. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ZHANG-001 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comprehension : distinguer trois objectifs géométriques | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 104 → 225 mots lexicaux |
| CV-ZHANG-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : interpréter les conventions de projection | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 124 → 241 mots lexicaux |
| CV-ZHANG-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | raisonnement : expliquer les contraintes multi-vues | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 109 → 229 mots lexicaux |
| CV-ZHANG-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : interpréter un RMS sans conclusion abusive | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 111 → 230 mots lexicaux |
| CV-ZHANG-005 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | pratique : propager une transformation pixel | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 105 → 217 mots lexicaux |
| CV-ZHANG-006 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : diagnostiquer l'observabilité | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 107 → 227 mots lexicaux |
| CV-ZHANG-007 | Protocole proposé sous hypothèses ; noyau antérieur conservé | conception : construire une collecte et une validation cohérentes | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 102 → 216 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/50-calibration-geometrie/52-calibration-zhang.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/50-calibration-geometrie/references/52-calibration-zhang.md) : révision 4, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [Zhang, rapport TR98-71](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) : §§2–4, projection, estimation et raffinement, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
