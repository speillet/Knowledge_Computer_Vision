# Revue — DeepSORT, ByteTrack et association multiobjet — 2026-10-24

## Synthèse

4 cartes examinées pour leur pertinence et leur développement ; 4 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : gating, apparence et association des scores faibles. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ASSOCIATION-001 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comparaison : identifier l’ajout de DeepSORT | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 44 → 184 mots lexicaux |
| CV-ASSOCIATION-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | algorithme : comprendre l’usage des faibles scores ByteTrack | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 62 → 207 mots lexicaux |
| CV-ASSOCIATION-003 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | diagnostic : contrôler le transfert ReID | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 48 → 186 mots lexicaux |
| CV-ASSOCIATION-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : séparer détecteur et association | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 49 → 195 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/110-tracking-association/112-deepsort-bytetrack.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/110-tracking-association/references/112-deepsort-bytetrack.md) : révision 3, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [ByteTrack](https://arxiv.org/html/2110.06864v3) : algorithme de deuxième association, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- DeepSORT 1703.07402v1 a aussi été ouvert ; la chronologie d’occultation est construite pour distinguer les causes.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
