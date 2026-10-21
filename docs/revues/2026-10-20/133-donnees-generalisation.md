# Revue — Splits, annotations, calibration des scores et dérive — 2026-10-20

## Synthèse

5 cartes auditées. Sources directes sur sélection et décalage ajoutées ; noyaux conservés.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 2 importante, 3 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FIABILITE-001 | Confirmé ; source ciblée | choisir une unité de split. | 42 mots à l’entrée ; Objectif fini et autonome | Fiche et format contrôlés | mineur | Préciser la source |
| CV-FIABILITE-002 | Confirmé ; source ciblée | distinguer deux calibrations. | 50 mots à l’entrée ; Objectif fini et autonome | Fiche et format contrôlés | mineur | Préciser la source |
| CV-FIABILITE-003 | Confirmé avec source ajoutée | garder un test non adaptatif. | 55 mots à l’entrée ; Règle de séparation claire | Fiche et format contrôlés | important | Ajouter Cawley–Talbot |
| CV-FIABILITE-004 | Déduction de protocole explicite | diagnostiquer une dérive saisonnière. | 82 mots à l’entrée ; Cas métier fini | Fiche et format contrôlés | mineur | Attribuer le diagnostic |
| CV-FIABILITE-005 | Confirmé avec source ajoutée | éviter une certitude hors domaine. | 43 mots à l’entrée ; Conclusion limitée aux preuves | Fiche et format contrôlés | important | Ajouter Ovadia |

### Affirmations de la fiche et des cartes

- Confirmé : Roberts explique la sous-estimation de l'erreur par certains splits aléatoires de données structurées ; le blocking dépend du scénario visé et n'est pas automatiquement meilleur pour toute cible. La carte conserve cette condition.
- Confirmé : Guo §2 définit l'accord confiance/fréquence de correction ; ce n'est pas l'estimation d'intrinsèques/extrinsèques de Zhang. La précision au seuil dépend aussi de la prévalence (identité de Bayes).
- Source ajoutée : Cawley–Talbot traite du biais optimiste dû à la sélection ; l'application à un test adapté pendant l'active learning est une déduction du projet.
- Source ajoutée : Ovadia montre les limites de la calibration post-hoc sous décalage ; aucun softmax élevé ne devient une garantie hors domaine.
- Dérive saisonnière, critères de collecte et surveillance : protocoles proposés, sans résultat terrain.

## Corrections appliquées

Bibliographie de la fiche complétée ; sources des cinq cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Relier prévalence, rappel et précision au seuil | Éviter de transférer la précision d’un test enrichi à la production | raisonnement | 1 carte ; calcul Bayes sur deux prévalences | Guo et protocole probabiliste explicite |

Familles absentes : algorithme, comprehension, conception, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Roberts et al., résumé et discussion du blocking](https://doi.org/10.1111/ecog.02881), PDF lu via [dépôt de l’auteur](https://www.biom.uni-freiburg.de/mitarbeiter/dormann/roberts-et-al-2017-ecography.pdf/at_download/file).
- [Guo et al., §2 équation 1](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf).
- [Cawley–Talbot, résumé et introduction](https://www.jmlr.org/papers/volume11/cawley10a/cawley10a.pdf).
- [Ovadia et al., résumé et introduction](https://arxiv.org/abs/1906.02530).
- [The ML Test Score, résumé officiel](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/), seulement pour le rôle des tests/surveillance ; pas d’audit des 28 tests.
- Zhang, passages contrôlés dans la revue 52.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
