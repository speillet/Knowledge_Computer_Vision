# Revue — Détection open-vocabulary et grounding — 2026-10-20

## Synthèse

3 cartes auditées. Pas de défaut scientifique dans les noyaux ; attribution et précision des sources corrigées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

3 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 3 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OPENVOC-001 | Confirmé après précision de source | séparer les sorties multimodales. | 55 mots à l’entrée ; Noyau fini, objectif conservé | Fiche et format contrôlés | mineur | Cibler la source |
| CV-OPENVOC-002 | Raisonnement du projet explicité | choisir un système à catalogue évolutif. | 84 mots à l’entrée ; Critères finis ; cas non exécuté | Fiche et format contrôlés | mineur | Préciser attribution |
| CV-OPENVOC-003 | Raisonnement du projet explicité | vérifier la spécificité du texte. | 45 mots à l’entrée ; Critères finis ; cas non exécuté | Fiche et format contrôlés | mineur | Préciser attribution |

### Affirmations de la fiche et des cartes

- Confirmé : OWL-ViT adapte le modèle image–texte à des sorties régionales ; Grounding DINO conditionne la sélection des requêtes et son décodeur par le texte.
- Confirmé : classer l'image entière ne fournit pas à lui seul des localisations d'instances.
- Les négatifs, seuils figés, rejets et coûts de maintenance sont des exigences de validation proposées par le projet. Aucun taux de généralisation ni garantie de calibration n'est déduit des articles.
- Trois objectifs distincts : type de sortie, choix sous contrainte, diagnostic de confusion ; aucun doublon interne.

## Corrections appliquées

Sources des trois cartes ciblées, fiche révisée ; aucun objectif modifié.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, comprehension, evaluation, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [OWL-ViT, résumé et §§3.1–3.2](https://arxiv.org/abs/2205.06230).
- [Grounding DINO, §§3.1–3.3](https://arxiv.org/abs/2303.05499).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
