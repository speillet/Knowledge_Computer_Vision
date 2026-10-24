# Revue — Représentations visuelles, ViT, Swin, ConvNeXt et DINOv2 — 2026-10-24

## Synthèse

5 cartes examinées pour leur pertinence et leur développement ; 5 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : biais d’architecture, échelle et protocole de transfert. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-REPRESENTATIONS-001 | Protocole proposé sous hypothèses ; noyau antérieur conservé | raisonnement : estimer le coût des tokens | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 39 → 188 mots lexicaux |
| CV-REPRESENTATIONS-002 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comparaison : situer Swin et ConvNeXt | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 43 → 188 mots lexicaux |
| CV-REPRESENTATIONS-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comprehension : utiliser des features autosupervisées | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 47 → 185 mots lexicaux |
| CV-REPRESENTATIONS-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comparaison : choisir une adaptation | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 52 → 194 mots lexicaux |
| CV-REPRESENTATIONS-005 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : contrôler le prétraitement d’un backbone | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 43 → 181 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/70-reconnaissance-representations/71-representations-transfert.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/70-reconnaissance-representations/references/71-representations-transfert.md) : révision 3, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [ViT](https://arxiv.org/html/2010.11929v2) : §3, représentation par patches, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Swin §3 a aussi été ouvert ; ConvNeXt et DINOv2 ont été consultés au niveau résumé. Les comparaisons empiriques de ces modèles ne sont donc pas revalidées ici.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
