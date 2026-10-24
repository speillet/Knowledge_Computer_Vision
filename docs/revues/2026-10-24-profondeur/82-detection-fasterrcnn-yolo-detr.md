# Revue — Détection : Faster R-CNN, familles YOLO et DETR — 2026-10-24

## Synthèse

13 cartes examinées pour leur pertinence et leur développement ; 12 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : contrats d’architecture, appariement et décomposition des erreurs. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-001 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comprehension : situer le partage de features | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 50 → 200 mots lexicaux |
| CV-DETECTEURS-002 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comparaison : ne pas généraliser toute la famille YOLO | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 40 → 182 mots lexicaux |
| CV-DETECTEURS-003 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | algorithme : distinguer les trois affectations | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 57 → 201 mots lexicaux |
| CV-DETECTEURS-004 | Réponse conservée ; pas de nouvelle affirmation | diagnostic : analyser les petits objets après resize | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Aucun écart éditorial retenu | Conserver : 180 mots lexicaux, déjà développée |
| CV-DETECTEURS-005 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : comparer des pipelines de détection | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 48 → 195 mots lexicaux |
| CV-DETECTEURS-006 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | algorithme : reconstruire l'assignation des sites dans FCOS | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 105 → 219 mots lexicaux |
| CV-DETECTEURS-007 | Protocole proposé sous hypothèses ; noyau antérieur conservé | pratique : calculer les cibles de régression en distances | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 84 → 199 mots lexicaux |
| CV-DETECTEURS-008 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comprehension : expliquer la modulation des négatifs faciles par Focal Loss | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 117 → 229 mots lexicaux |
| CV-DETECTEURS-009 | Protocole proposé sous hypothèses ; noyau antérieur conservé | raisonnement : expliquer le signal de GIoU pour des boîtes disjointes | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 131 → 241 mots lexicaux |
| CV-DETECTEURS-010 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comprehension : expliquer l'apport des connexions latérales de FPN | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 103 → 225 mots lexicaux |
| CV-DETECTEURS-011 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : distinguer des erreurs de classe, de localisation et de doublon | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 100 → 215 mots lexicaux |
| CV-DETECTEURS-012 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : diagnostiquer un faux positif pouvant provenir d'une annotation manquante | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 124 → 231 mots lexicaux |
| CV-DETECTEURS-013 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comprehension : distinguer instances, classes et étiquettes par instance | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 129 → 236 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md) : révision 6, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [DETR](https://arxiv.org/html/2005.12872v3) : §3, prédiction d’ensemble et matching, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- FCOS 1904.01355v5, Focal Loss 1708.02002v2 et TIDE 2008.08115v2 ont aussi été ouverts. Pas de classement des détecteurs ni d’entraînement annoncé.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
