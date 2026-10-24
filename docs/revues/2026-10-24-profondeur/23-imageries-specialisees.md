# Revue — Line-scan, télédétection et volumes médicaux — 2026-10-24

## Synthèse

3 cartes examinées pour leur pertinence et leur développement ; 3 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : géométrie physique, line-scan et unité de généralisation. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IMAGERIES-001 | Protocole proposé sous hypothèses ; noyau antérieur conservé | pratique : propager les unités d’un volume | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 58 → 202 mots lexicaux |
| CV-IMAGERIES-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | diagnostic : contrôler une acquisition line-scan | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 48 → 196 mots lexicaux |
| CV-IMAGERIES-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : éviter une fuite géographique | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 46 → 189 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/20-acquisition-images/23-imageries-specialisees.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/20-acquisition-images/references/23-imageries-specialisees.md) : révision 3, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [DICOM, Image Plane Module](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html) : §C.7.6.2.1.1, position, orientation et pixel spacing, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Basler, Line Scan GigE Use Cases, et SpaceNet 7, Problem/Data, ont aussi été ouverts. Les risques de split sont des déductions du projet, sans audit des données du challenge.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
