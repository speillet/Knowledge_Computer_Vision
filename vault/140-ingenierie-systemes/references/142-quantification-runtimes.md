---
id: CV-QUANT
type: methode
domaine: d14
poles: [A, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
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

Quantification affine entière schématique : $q=clip(round(x/s)+z, q_{min}, q_{max})$ et $\hat x=s(q-z)$, échelle $s>0$, zero-point entier $z$ et bornes du type $q_{min},q_{max}$. La règle d’arrondi dépend du contrat ; ce schéma entier ne définit pas la représentation FP8. Plages, saturation et granularité per-tensor/per-channel comptent. INT8 entier et FP8 flottant ont des représentations/contraintes différentes ; ils ne sont pas interchangeables par une simple étiquette.

## Paramètres et propriétés

Distribution de calibration, couches sensibles, précision mixte, formes dynamiques et opérateurs. Vérifier runtime/version/GPU ou NPU avant d'annoncer support PTQ/QAT ou gain ; un moteur sérialisé n'est pas universellement portable.

## Coût et implémentation

Conversions, fallbacks, transferts et goulots non réseau peuvent annuler le gain. Aucun moteur construit ni accélération mesurée ; documentation runtime `latest` consultée de nouveau le 2026-10-20, pas de commande universelle figée.

## Évaluation et variation contrôlée

Baseline float puis même test, acquisition et point d'exploitation après quantification. Varier représentativité de calibration et précision ; mesurer petits objets, sous-groupes, latence/mémoire et coût complet.

## Échecs et diagnostic

Pas de gain après INT8 : inspecter opérateurs réellement quantifiés, fallback CPU, copies et prétraitement. Perte de rappel : inspecter saturation/distributions et couches critiques avant de changer le seuil métier.

## Alternatives et usages

Précision mixte, distillation, compression structurée et optimisation du pipeline selon le goulot ; la taille du fichier ne prédit pas le temps de traitement.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent échelle, saturation et exécution réelle du runtime. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-QUANT-001

**Question de travail** : Qu’est-ce qui distingue PTQ de QAT, au-delà du format numérique final ?

**Réponse de référence** : PTQ intervient après entraînement ; QAT adapte l’apprentissage à un modèle de quantification.

**Lecture de la différence** : une PTQ estime des paramètres de quantification à partir du modèle déjà appris et d'une procédure adaptée. Une QAT simule certains effets numériques pendant l'apprentissage pour permettre une adaptation. Le format final ne révèle donc pas à lui seul comment les paramètres ont été obtenus.

**Choix proposé** : comparer d'abord une baseline flottante et une PTQ sur les mêmes données réservées, puis envisager la QAT si la perte de qualité et le budget le justifient. Vérifier représentation, granularité et support du backend réellement utilisé. Une simulation d'entraînement doit correspondre assez bien au contrat d'inférence pour être interprétable. Le gain dépend aussi des opérateurs exécutés et du matériel. Une meilleure robustesse à la quantification ne garantit ni accélération de toute la chaîne ni conservation des petits défauts : mesurer ces sorties au point de fonctionnement fixé fait partie de la décision.

### Cas lié à CV-QUANT-005

**Question de travail** : Quelles mesures associer à une réduction de mémoire après quantification d’un détecteur ?

**Réponse de référence** : Qualité sur données réservées et cas critiques, plus latence/débit/mémoire du système complet au point d’exploitation fixé.

**Différentes mémoires** : la taille des poids sur disque n'est pas toute la mémoire utilisée : activations, buffers, contexte du runtime et copies peuvent compter. Une compression des poids peut donc produire un gain de stockage sans réduire proportionnellement le pic mémoire en exploitation.

**Protocole proposé** : conserver données et seuils de décision, mesurer AP ou métriques utiles, cas critiques, mémoire maximale, latence et débit sur la même cible. Contrôler les défauts petits ou peu contrastés, car une variation numérique limitée peut changer une décision près du seuil. Rapporter conversions et éventuels opérateurs restant en autre précision. Le point de fonctionnement doit être comparable avant de décider que la compression améliore le produit. Un fichier plus petit est un résultat de ressource ; il ne démontre ni accélération, ni qualité suffisante, ni robustesse aux acquisitions que la calibration numérique n'a pas représentées.

**Repère documentaire de cette passe** : [ONNX, QuantizeLinear-21](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-21), Summary, échelle, zero-point et arrondi. Les autres développements figurent dans les [cartes associées](../142-quantification-runtimes.md).

## Sources et cartes

- [ONNX QuantizeLinear, version d’opérateur 21, Summary](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-21) : échelle, zero-point, saturation et arrondi.
- [ONNX Runtime, Execution Providers](https://onnxruntime.ai/docs/execution-providers/), consulté le 2026-10-20 : affectation d’opérateurs/sous-graphes selon les capacités.

- [TensorRT, Quantization Workflows, consulté le 2026-10-24](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html).
- [TensorRT, support matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
- [Cartes associées](../142-quantification-runtimes.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
