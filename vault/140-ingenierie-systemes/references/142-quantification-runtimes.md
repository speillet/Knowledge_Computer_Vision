---
id: CV-QUANT
type: methode
domaine: d14
poles: [A, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-PIPELINE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d14]
---
# PTQ, QAT, INT8/FP8 et runtimes

## Problème, données et hypothèses

Réduire coût d'inférence tout en préservant l'erreur utile au produit. Entrées : modèle, données de calibration/validation, backend et matériel ; sortie : modèle/moteur compatible et mesures qualité–performance. Un format de fichier n'est pas une garantie d'accélération.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-PIPELINE](141-contrats-profiling-video.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

PTQ choisit des paramètres après entraînement ; QAT expose l'apprentissage à une simulation de quantification. Q/DQ explicites, granularité, couverture des opérateurs et kernels définissent l'exécution réelle. TensorRT, ONNX Runtime, OpenVINO et LiteRT ont des matrices de support distinctes.

## Mathématiques, conventions et unités

Quantification affine schématique : $q=clip(round(x/s)+z)$ et $\hat x=s(q-z)$, échelle s>0 et zero-point z. Plages, saturation et granularité per-tensor/per-channel comptent. INT8 entier et FP8 flottant ont des représentations/contraintes différentes ; ils ne sont pas interchangeables par une simple étiquette.

## Paramètres et propriétés

Distribution de calibration, couches sensibles, précision mixte, formes dynamiques et opérateurs. Vérifier runtime/version/GPU ou NPU avant d'annoncer support PTQ/QAT ou gain ; un moteur sérialisé n'est pas universellement portable.

## Coût et implémentation

Conversions, fallbacks, transferts et goulots non réseau peuvent annuler le gain. Aucun moteur construit ni accélération mesurée ; sources runtime vérifiées le 2026-10-18, pas de commande universelle figée.

## Évaluation et variation contrôlée

Baseline float puis même test, acquisition et point d'exploitation après quantification. Varier représentativité de calibration et précision ; mesurer petits objets, sous-groupes, latence/mémoire et coût complet.

## Échecs et diagnostic

Pas de gain après INT8 : inspecter opérateurs réellement quantifiés, fallback CPU, copies et prétraitement. Perte de rappel : inspecter saturation/distributions et couches critiques avant de changer le seuil métier.

## Alternatives et usages

Précision mixte, distillation, compression structurée et optimisation du pipeline selon le goulot ; la taille du fichier ne prédit pas le temps de traitement.

## Sources et cartes

- [TensorRT, quantization workflows](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html).
- [TensorRT, support matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
- [Cartes associées](../142-quantification-runtimes.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
