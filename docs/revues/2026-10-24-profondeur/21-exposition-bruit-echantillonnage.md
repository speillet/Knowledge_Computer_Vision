# Revue — Exposition, bruit, couleur et échantillonnage — 2026-10-24

## Synthèse

4 cartes examinées pour leur pertinence et leur développement ; 4 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : exposition, bruit et échantillonnage reliés à la tâche. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ACQUISITION-001 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : calculer un flou simplifié | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 48 → 200 mots lexicaux |
| CV-ACQUISITION-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | comparaison : distinguer gain et exposition | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 252 → 329 mots lexicaux |
| CV-ACQUISITION-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : reconnaître aliasing et prétraitement incohérent | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 132 → 261 mots lexicaux |
| CV-ACQUISITION-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | pratique : contrôler une entrée image | Noyau fini et erreurs bloquantes conservés | Fiche r6, unités/hypothèses explicites | Mineure | Développer : 46 → 184 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/20-acquisition-images/21-exposition-bruit-echantillonnage.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md) : révision 6, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [EMVA 1288 Linear 4.0](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) : §§2.4, 2.6 et 2.7, modèle de bruit et signal, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Les cas de flou et d’aliasing sont des déductions du modèle de déplacement et de l’échantillonnage, sans mesure de capteur.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
