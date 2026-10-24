# Revue — Stéréo rectifiée, SGM et profondeur — 2026-10-24

## Synthèse

4 cartes examinées pour leur pertinence et leur développement ; 4 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : disparité, incertitude de profondeur et géométrie rectifiée. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-STEREO-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : calculer une profondeur rectifiée | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 51 → 195 mots lexicaux |
| CV-STEREO-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : interpréter l’incertitude de profondeur | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 51 → 189 mots lexicaux |
| CV-STEREO-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : décoder une disparité fixe | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 50 → 180 mots lexicaux |
| CV-STEREO-004 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comparaison : séparer rectification et matching | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 48 → 194 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/60-vision-3d/61-stereo-profondeur.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/60-vision-3d/references/61-stereo-profondeur.md) : révision 3, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [OpenCV 4.13, Depth Map from Stereo Images](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html) : relation profondeur–disparité et correspondance, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
