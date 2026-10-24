# Revue — SO(3), SE(3) et conventions de transformation — 2026-10-24

## Synthèse

6 cartes examinées pour leur pertinence et leur développement ; 5 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : composition des repères et perturbations gauche/droite. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SE3-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : composer avec des repères nommés | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 140 → 206 mots lexicaux |
| CV-SE3-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | pratique : inverser une pose rigide | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 44 → 195 mots lexicaux |
| CV-SE3-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comparaison : distinguer perturbations locale et globale | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 159 → 206 mots lexicaux |
| CV-SE3-004 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | diagnostic : contrôler un quaternion | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 151 → 212 mots lexicaux |
| CV-SE3-005 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | evaluation : mesurer un écart de rotation | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 175 → 222 mots lexicaux |
| CV-SE3-006 | Réponse conservée ; pas de nouvelle affirmation | diagnostic : convertir entre conventions d'axes caméra | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Aucun écart éditorial retenu | Conserver : 240 mots lexicaux, déjà développée |

## Corrections appliquées

- [Réponses](../../../vault/10-mathematiques-estimation/12-rotations-se3.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/10-mathematiques-estimation/references/12-rotations-se3.md) : révision 6, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [Solà et al., micro Lie theory](https://arxiv.org/html/1812.01537v9) : §II, perturbations et incertitudes ; annexe D, SE(3), passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
