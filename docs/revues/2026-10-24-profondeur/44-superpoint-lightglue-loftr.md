# Revue — SuperPoint, LightGlue et LoFTR — 2026-10-24

## Synthèse

5 cartes examinées pour leur pertinence et leur développement ; 5 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : compatibilité features–matcher, résolution et validation. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MATCH-APPRIS-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comprehension : attribuer le rôle des composants | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 41 → 185 mots lexicaux |
| CV-MATCH-APPRIS-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comparaison : distinguer detector-free et flot dense | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 52 → 199 mots lexicaux |
| CV-MATCH-APPRIS-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | pratique : garder des features compatibles | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 41 → 190 mots lexicaux |
| CV-MATCH-APPRIS-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : construire une baseline comparable | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 56 → 198 mots lexicaux |
| CV-MATCH-APPRIS-005 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : contrôler les coordonnées du matching | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 46 → 191 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/40-features-matching/44-superpoint-lightglue-loftr.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/40-features-matching/references/44-superpoint-lightglue-loftr.md) : révision 3, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [LightGlue, dépôt officiel](https://github.com/cvg/LightGlue) : README, Usage et extracteurs compatibles, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- SuperPoint §3/§5 et LoFTR §3 ont aussi été ouverts. Le site projet LightGlue était inaccessible ; le README officiel sert de repli, sans exécution de checkpoint.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
