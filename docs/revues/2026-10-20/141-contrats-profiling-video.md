# Revue — Contrats de données, profiling et pipelines vidéo — 2026-10-20

## Synthèse

5 cartes auditées. Noyaux confirmés ; sources datées et calculs/protocoles distingués.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 5 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-PIPELINE-001 | Déduction du projet explicite | séparer latence débit et fraîcheur. | 43 mots à l’entrée ; Hypothèses et critères de mesure finis | Fiche et format contrôlés | mineur | Attribuer le raisonnement |
| CV-PIPELINE-002 | Déduction du projet explicite | raisonner sur une file vidéo. | 48 mots à l’entrée ; Hypothèses et critères de mesure finis | Fiche et format contrôlés | mineur | Attribuer le raisonnement |
| CV-PIPELINE-003 | Confirmé ; source datée et ciblée | définir un benchmark complet. | 44 mots à l’entrée ; Noyau fini, objectif conservé | Fiche et format contrôlés | mineur | Préciser source |
| CV-PIPELINE-004 | Déduction du projet explicite | dimensionner huit flux sous p99. | 95 mots à l’entrée ; Hypothèses et critères de mesure finis | Fiche et format contrôlés | mineur | Attribuer le raisonnement |
| CV-PIPELINE-005 | Déduction du projet explicite | localiser un goulot par trace. | 49 mots à l’entrée ; Hypothèses et critères de mesure finis | Fiche et format contrôlés | mineur | Attribuer le raisonnement |

### Affirmations de la fiche et des cartes

- Confirmé : TensorRT distingue Throughput, Host Latency, GPU Compute Time et transferts ; les exemples de timing synchronisent les opérations. Le périmètre d'une inférence n'est pas celui d'une caméra complète.
- Confirmé : GStreamer queue bloque à une limite et propose leaky pour abandonner nouveaux ou anciens buffers. La croissance non bornée de la fiche est un modèle de file sans limite, pas le comportement par défaut de cet élément borné.
- Calcul analytique : 8×30=240 images/s, déficit 40 images/s face à 200. La capacité ne corrige pas un déficit soutenu ; admission, rétropression ou abandon changent les hypothèses.
- Déduction statistique : les quantiles de sommes ne sont pas en général des sommes de quantiles. Aucun p99 réel ni régime thermique n'a été mesuré.
- Les cartes de conception/diagnostic définissent des critères, sans prescrire une machine ou garantir un débit.

## Corrections appliquées

Fiche révisée ; formulation « valeurs par défaut » et sources des cinq cartes précisées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, comprehension, evaluation. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [TensorRT, Measure End-to-End Performance, Reported Performance Metrics et timing CUDA](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), documentation latest consultée le 20 octobre 2026.
- [GStreamer queue, limites, blocage et leaky](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), consulté le 20 octobre 2026.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
