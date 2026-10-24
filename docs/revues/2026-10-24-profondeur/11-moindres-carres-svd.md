# Revue — Moindres carrés, SVD et conditionnement — 2026-10-24

## Synthèse

9 cartes examinées pour leur pertinence et leur développement ; 5 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : blanchiment, perte de rang et distinction ajustement–identifiabilité. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SVD-001 | Réponse conservée ; pas de nouvelle affirmation | raisonnement : distinguer résidu et identifiabilité | Noyau fini et erreurs bloquantes conservés | Fiche r5, unités/hypothèses explicites | Aucun écart éditorial retenu | Conserver : 184 mots lexicaux, déjà développée |
| CV-SVD-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comparaison : choisir QR ou équations normales | Noyau fini et erreurs bloquantes conservés | Fiche r5, unités/hypothèses explicites | Mineure | Développer : 172 → 217 mots lexicaux |
| CV-SVD-003 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | pratique : pondérer des résidus hétérogènes | Noyau fini et erreurs bloquantes conservés | Fiche r5, unités/hypothèses explicites | Mineure | Développer : 133 → 213 mots lexicaux |
| CV-SVD-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : distinguer outliers et rang déficient | Noyau fini et erreurs bloquantes conservés | Fiche r5, unités/hypothèses explicites | Mineure | Développer : 173 → 220 mots lexicaux |
| CV-SVD-005 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | algorithme : dérouler une estimation DLT | Noyau fini et erreurs bloquantes conservés | Fiche r5, unités/hypothèses explicites | Mineure | Développer : 169 → 217 mots lexicaux |
| CV-SVD-006 | Réponse conservée ; pas de nouvelle affirmation | raisonnement : relier normalisation et conditionnement de la DLT | Noyau fini et erreurs bloquantes conservés | Fiche r5, unités/hypothèses explicites | Aucun écart éditorial retenu | Conserver : 223 mots lexicaux, déjà développée |
| CV-SVD-007 | Réponse conservée ; pas de nouvelle affirmation | comprehension : situer Gauss-Newton et Levenberg-Marquardt | Noyau fini et erreurs bloquantes conservés | Fiche r5, unités/hypothèses explicites | Aucun écart éditorial retenu | Conserver : 204 mots lexicaux, déjà développée |
| CV-SVD-008 | Réponse conservée ; pas de nouvelle affirmation | pratique : régler l'échelle d'une perte robuste | Noyau fini et erreurs bloquantes conservés | Fiche r5, unités/hypothèses explicites | Aucun écart éditorial retenu | Conserver : 200 mots lexicaux, déjà développée |
| CV-SVD-009 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : interpréter une covariance d'estimation | Noyau fini et erreurs bloquantes conservés | Fiche r5, unités/hypothèses explicites | Mineure | Développer : 177 → 221 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/10-mathematiques-estimation/11-moindres-carres-svd.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/10-mathematiques-estimation/references/11-moindres-carres-svd.md) : révision 5, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [Ceres, Covariance Estimation](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) : Introduction, Rank of the Jacobian et Gauge Invariance, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
