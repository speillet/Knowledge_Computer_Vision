# Revue — RANSAC appliqué à une homographie — 2026-10-24

## Synthèse

7 cartes examinées pour leur pertinence et leur développement ; 7 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : succès d’échantillonnage, couverture et validité du modèle. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HOMOGRAPHIE-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comparaison : choisir un modèle géométrique | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 103 → 218 mots lexicaux |
| CV-HOMOGRAPHIE-002 | Protocole proposé sous hypothèses ; noyau antérieur conservé | raisonnement : relier degrés de liberté et dégénérescence | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 93 → 207 mots lexicaux |
| CV-HOMOGRAPHIE-003 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | algorithme : reconstruire une itération robuste | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 111 → 229 mots lexicaux |
| CV-HOMOGRAPHIE-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | raisonnement : interpréter le budget nominal de RANSAC | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 122 → 239 mots lexicaux |
| CV-HOMOGRAPHIE-005 | Protocole proposé sous hypothèses ; noyau antérieur conservé | pratique : interpréter l'unité d'un seuil de résidu | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 117 → 232 mots lexicaux |
| CV-HOMOGRAPHIE-006 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | diagnostic : diagnostiquer un modèle extrapolé | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 95 → 210 mots lexicaux |
| CV-HOMOGRAPHIE-007 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : expliquer une incompatibilité de modèle | Noyau fini et erreurs bloquantes conservés | Fiche r4, unités/hypothèses explicites | Mineure | Développer : 100 → 221 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/50-calibration-geometrie/51-ransac-homographie.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/50-calibration-geometrie/references/51-ransac-homographie.md) : révision 4, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [Fischler et Bolles 1981](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf) : §II, consensus et échantillonnage, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- La projection plane est reliée à Zhang §§2–3 ; les cas de couverture sont construits et ne démontrent aucune performance image.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
