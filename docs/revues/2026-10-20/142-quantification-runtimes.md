# Revue — PTQ, QAT, INT8/FP8 et runtimes — 2026-10-20

## Synthèse

5 cartes auditées. Portée de la formule entière et sources de support précisées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 4 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-QUANT-001 | Confirmé ; source datée et ciblée | distinguer PTQ et QAT. | 52 mots à l’entrée ; Noyau fini, objectif conservé | Fiche et format contrôlés | mineur | Préciser source |
| CV-QUANT-002 | Confirmé ; source datée et ciblée | interpréter échelle et saturation. | 44 mots à l’entrée ; Noyau fini, objectif conservé | Fiche et format contrôlés | mineur | Préciser source |
| CV-QUANT-003 | Confirmé avec source complémentaire | vérifier le support d’un runtime. | 38 mots à l’entrée ; Contrat de support fini | Fiche et format contrôlés | important | Ajouter ONNX Runtime |
| CV-QUANT-004 | Déduction du projet explicite | diagnostiquer une absence de gain INT8. | 80 mots à l’entrée ; Hypothèses et critères de mesure finis | Fiche et format contrôlés | mineur | Attribuer le raisonnement |
| CV-QUANT-005 | Déduction du projet explicite | contrôler qualité et performance ensemble. | 54 mots à l’entrée ; Hypothèses et critères de mesure finis | Fiche et format contrôlés | mineur | Attribuer le raisonnement |

### Affirmations de la fiche et des cartes

- Confirmé : PTQ après entraînement avec données représentatives ; QAT simule les effets pendant l'entraînement. La fiche ne reprend pas une supériorité universelle de QAT.
- Formule précisée : quantification affine entière avec bornes et arrondi contractuel ; ONNX QuantizeLinear-21 explicite saturation et nearest-even. Le FP8 reste une représentation distincte.
- Confirmé : ONNX Runtime affecte les opérateurs/sous-graphes aux Execution Providers selon GetCapability ; le format d'échange ne promet pas un unique graphe matériel optimisé.
- Confirmé : support TensorRT distingue plateformes, versions compatibles et modes de compatibilité matérielle ; aucune portabilité universelle ni absence universelle de compatibilité n'est affirmée.
- OpenVINO/LiteRT sont nommés comme runtimes, mais aucune matrice complète de support de ces produits n'a été auditée. Aucune commande ni accélération chiffrée annoncée.
- Diagnostics et protocole qualité/coût : propositions du projet.

## Corrections appliquées

Fiche révisée, formule annotée ; sources des cinq cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, comprehension, conception. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [TensorRT, Quantization Workflows : PTQ/QAT, granularités et Q/DQ](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html).
- [TensorRT, Support Matrix : portability and compatibility](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
- [ONNX QuantizeLinear, version 21, Summary](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-21).
- [ONNX Runtime, Execution Providers et GetCapability](https://onnxruntime.ai/docs/execution-providers/).
- [TensorRT, benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API. Pages latest consultées le 20 octobre 2026 ; leur contenu peut évoluer. Aucun environnement de runtime construit.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
