# Revue — Déploiement edge, compression et surveillance — 2026-10-20

## Synthèse

4 cartes auditées. Trois manques importants de justification corrigés ; dérivation et limites du modèle explicitées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 3 importante, 1 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DEPLOIEMENT-001 | Calcul analytique confirmé | borner un gain de système. | 44 mots à l’entrée ; Un calcul sous hypothèses explicites | Fiche et format contrôlés | important | Remplacer citation inadéquate |
| CV-DEPLOIEMENT-002 | Confirmé avec source ajoutée | relier compression et accélération. | 49 mots à l’entrée ; Une dépendance matérielle précise | Fiche et format contrôlés | important | Citer Sparsity |
| CV-DEPLOIEMENT-003 | Confirmé ; source datée et ciblée | versionner un système complet. | 48 mots à l’entrée ; Noyau fini, objectif conservé | Fiche et format contrôlés | mineur | Préciser source |
| CV-DEPLOIEMENT-004 | Mécanisme confirmé ; diagnostic proposé | tester le régime edge. | 42 mots à l’entrée ; Traces discriminantes finies | Fiche et format contrôlés | important | Ajouter source thermique |

### Affirmations de la fiche et des cartes

- Calcul confirmé : temps initial normalisé à 1, temps nouveau 0,9+0,1/2=0,95, gain 1,0526316. Modèle séquentiel sans surcoût, pas une règle de p99 ni de pipeline recouvrant les calculs.
- Confirmé : TensorRT 8.6.1 documente des motifs 2:4 et précise que des tactiques denses peuvent rester plus rapides. Exemple versionné, pas une annonce du support universel actuel.
- Confirmé : Hinton propose la supervision d'un modèle compact par sorties du modèle enseignant ; aucune réduction automatique des transferts ne s'en déduit.
- Confirmé : ML Test Score traite reproductibilité, intégration, rollback et surveillance. La liste d'artefacts de la carte est une adaptation du projet.
- Confirmé : Jetson r36.4 documente surveillance thermique et réduction des fréquences ; l'identification de la cause exige toujours les traces proposées. Aucun appareil mesuré ni modifié.

## Corrections appliquées

Fiche révisée, sources d’Amdahl/sparsité/distillation/thermique ajoutées ; sources des quatre cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, comprehension, conception, evaluation. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Amdahl (1967), p. 483](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf) : limite de la partie non accélérée ; calcul numérique dérivé par le projet.

- [ML Test Score, introduction, Model tests, Infra tests](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf).
- [TensorRT 8.6.1, §6.10 Sparsity](https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt-861/developer-guide/index.html#structured-sparsity).
- [Hinton et al., introduction et soft targets](https://arxiv.org/abs/1503.02531).
- [Jetson Linux r36.4, Thermal Management](https://docs.nvidia.com/jetson/archives/r36.4/DeveloperGuide/SD/PlatformPowerAndPerformance/JetsonOrinNanoSeriesJetsonOrinNxSeriesAndJetsonAgxOrinSeries.html).
- [TensorRT, Support Matrix, portabilité](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html), consultée le 20 octobre 2026.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
