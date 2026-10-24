# Revue — Kalman, EKF, UKF et ESKF pour la fusion — 2026-10-24

## Synthèse

6 cartes examinées pour leur pertinence et leur développement ; 5 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : innovations, covariance et réinitialisation de l’ESKF. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FUSION-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comprehension : distinguer variantes de filtre | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 142 → 203 mots lexicaux |
| CV-FUSION-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : interpréter une innovation normalisée | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 171 → 224 mots lexicaux |
| CV-FUSION-003 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | diagnostic : préserver la covariance ESKF | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 166 → 216 mots lexicaux |
| CV-FUSION-004 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | pratique : traiter temps et données manquantes | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 152 → 205 mots lexicaux |
| CV-FUSION-005 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : justifier la formulation à état d'erreur | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 166 → 233 mots lexicaux |
| CV-FUSION-006 | Réponse conservée ; pas de nouvelle affirmation | diagnostic : stabiliser la mise à jour de covariance | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Aucun écart éditorial retenu | Conserver : 231 mots lexicaux, déjà développée |

## Corrections appliquées

- [Réponses](../../../vault/10-mathematiques-estimation/13-kalman-ekf-eskf.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/10-mathematiques-estimation/references/13-kalman-ekf-eskf.md) : révision 6, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [Solà, Quaternion kinematics for the error-state Kalman filter](https://arxiv.org/html/1711.02508v1) : §6.3, injection et reset de l’erreur, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- La forme de Joseph est aussi confrontée au rapport JPL 42-233A, §III.A ; les cas de gating et de bruit restent des raisonnements conditionnels.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
