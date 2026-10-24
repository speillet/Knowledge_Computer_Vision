# Revue — IoU et AP — protocole COCO de détection — 2026-10-24

## Synthèse

7 cartes examinées pour leur pertinence et leur développement ; 7 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : appariement, classement et conventions COCO. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IOU-AP-001 | Protocole proposé sous hypothèses ; noyau antérieur conservé | pratique : calculer un recouvrement dans le bon contrat | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 98 → 212 mots lexicaux |
| CV-IOU-AP-002 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comprehension : distinguer mesure locale et protocole agrégé | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 124 → 240 mots lexicaux |
| CV-IOU-AP-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | algorithme : expliquer la pénalité d'un doublon | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 94 → 218 mots lexicaux |
| CV-IOU-AP-004 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : reconstruire une AP interpolée simple | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 110 → 225 mots lexicaux |
| CV-IOU-AP-005 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : comparer des évaluateurs avec prudence | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 113 → 228 mots lexicaux |
| CV-IOU-AP-006 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : diagnostiquer un écart selon l'exigence de localisation | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 103 → 219 mots lexicaux |
| CV-IOU-AP-007 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : relier moyenne benchmark et décision métier | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 103 → 226 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/130-evaluation-fiabilite/131-iou-ap-coco.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/130-evaluation-fiabilite/references/131-iou-ap-coco.md) : révision 4, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [COCO API, cocoeval.py au commit 8c9bcc3](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py) : evaluateImg, accumulate et summarize, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Le calcul de boîte et les exemples de rang sont des cas analytiques ; pas de benchmark dataset.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
