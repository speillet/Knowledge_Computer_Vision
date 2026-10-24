# Revue — FAST et BRIEF — détecter un coin puis décrire son voisinage — 2026-10-24

## Synthèse

5 cartes examinées pour leur pertinence et leur développement ; 5 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : test de segment et signature binaire sous transformations. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FAST-BRIEF-001 | Protocole proposé sous hypothèses ; noyau antérieur conservé | algorithme : expliquer le test FAST | Noyau fini et erreurs bloquantes conservés | Fiche r2, unités/hypothèses explicites | Mineure | Développer : 100 → 222 mots lexicaux |
| CV-FAST-BRIEF-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : calculer une distance binaire | Noyau fini et erreurs bloquantes conservés | Fiche r2, unités/hypothèses explicites | Mineure | Développer : 72 → 200 mots lexicaux |
| CV-FAST-BRIEF-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comparaison : séparer FAST BRIEF et ORB | Noyau fini et erreurs bloquantes conservés | Fiche r2, unités/hypothèses explicites | Mineure | Développer : 80 → 201 mots lexicaux |
| CV-FAST-BRIEF-004 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | diagnostic : isoler un échec sous rotation | Noyau fini et erreurs bloquantes conservés | Fiche r2, unités/hypothèses explicites | Mineure | Développer : 91 → 220 mots lexicaux |
| CV-FAST-BRIEF-005 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : mesurer le compromis calcul répétabilité | Noyau fini et erreurs bloquantes conservés | Fiche r2, unités/hypothèses explicites | Mineure | Développer : 84 → 206 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/40-features-matching/47-fast-brief.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/40-features-matching/references/47-fast-brief.md) : révision 2, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [Rosten et Drummond 2006](https://www.edwardrosten.com/work/rosten_2006_machine.pdf) : §§2–3, test FAST et apprentissage de l’arbre, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Calonder et al., BRIEF, §2, a aussi été ouvert ; aucun benchmark de vitesse n’est extrapolé.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
