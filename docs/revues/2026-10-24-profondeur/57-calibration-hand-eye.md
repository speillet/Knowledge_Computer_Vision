# Revue — Hand-eye calibration — résoudre AX = XB sans mélanger les repères — 2026-10-24

## Synthèse

5 cartes examinées pour leur pertinence et leur développement ; 5 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : conventions AX=XB, excitation et validation indépendante. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HANDEYE-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : dériver les mouvements relatifs | Noyau fini et erreurs bloquantes conservés | Fiche r2, unités/hypothèses explicites | Mineure | Développer : 82 → 194 mots lexicaux |
| CV-HANDEYE-002 | Protocole proposé sous hypothèses ; noyau antérieur conservé | pratique : respecter le sens des poses API | Noyau fini et erreurs bloquantes conservés | Fiche r2, unités/hypothèses explicites | Mineure | Développer : 91 → 214 mots lexicaux |
| CV-HANDEYE-003 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | conception : exciter les directions observables | Noyau fini et erreurs bloquantes conservés | Fiche r2, unités/hypothèses explicites | Mineure | Développer : 89 → 202 mots lexicaux |
| CV-HANDEYE-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : tester la fermeture de la chaîne | Noyau fini et erreurs bloquantes conservés | Fiche r2, unités/hypothèses explicites | Mineure | Développer : 113 → 220 mots lexicaux |
| CV-HANDEYE-005 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comparaison : distinguer eye-in-hand et eye-to-hand | Noyau fini et erreurs bloquantes conservés | Fiche r2, unités/hypothèses explicites | Mineure | Développer : 94 → 217 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/50-calibration-geometrie/57-calibration-hand-eye.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/50-calibration-geometrie/references/57-calibration-hand-eye.md) : révision 2, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [OpenCV 4.13, calibrateHandEye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) : calibrateHandEye, transformations et mouvements minimums, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Convention et exigences de mouvement confrontées aussi via Context7 ; aucune séquence robot exécutée.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
