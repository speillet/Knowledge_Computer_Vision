# Revue — SAM, SAM 2 et segmentation guidée en vidéo — 2026-10-24

## Synthèse

3 cartes examinées pour leur pertinence et leur développement ; 3 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : prompts, ambiguïté de masque et mémoire temporelle. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SAM-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comprehension : définir la sortie SAM | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 51 → 205 mots lexicaux |
| CV-SAM-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comparaison : situer SAM 2 en vidéo | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 47 → 191 mots lexicaux |
| CV-SAM-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : contrôler le futur dans l’évaluation | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 42 → 181 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/90-segmentation/94-sam-sam2.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/90-segmentation/references/94-sam-sam2.md) : révision 3, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [SAM 2](https://arxiv.org/html/2408.00714v2) : architecture, masklets, prompts et mémoire, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Les budgets de correction et protocoles causaux sont proposés ; aucun modèle ni annotation interactive exécuté.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
