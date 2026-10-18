# PTQ, QAT, INT8/FP8 et runtimes — cartes

Fiche : [[140-ingenierie-systemes/references/142-quantification-runtimes|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::140-ingenierie-systemes

## CV-QUANT-001

Objectif : distinguer PTQ et QAT. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-QUANT-001
Question: Qu’est-ce qui distingue PTQ de QAT, au-delà du format numérique final ?
Reponse: **Noyau attendu** : PTQ intervient après entraînement ; QAT adapte l’apprentissage à un modèle de quantification.

**Approfondissement** : La granularité, le backend, les données et les opérateurs déterminent la qualité finale ; QAT n’est pas automatiquement nécessaire ni supérieur pour toute tâche.

**Erreurs bloquantes** : Assimiler le mot INT8 à une méthode d’apprentissage unique.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Fiche complète]] ; [TensorRT, quantization workflows](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html) ; [TensorRT, support matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
Tags: cv::pilote cv::d14 famille::comparaison cv_id::CV-QUANT-001 provenance::agent pole::A pole::F
END

## CV-QUANT-002

Objectif : interpréter échelle et saturation. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-QUANT-002
Question: Quel risque introduit une échelle de quantification estimée sur un jeu qui ne représente pas les images d’exploitation ?
Reponse: **Noyau attendu** : Saturation ou résolution numérique inadéquate pour les activations réelles, avec erreurs sensibles sur certaines sorties.

**Approfondissement** : Mesurer distributions et performance par cas critique ; ne pas seulement regarder la moyenne de calibration.

**Erreurs bloquantes** : Supposer que quelques images arbitraires donnent une calibration universelle.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Fiche complète]] ; [TensorRT, quantization workflows](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html) ; [TensorRT, support matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
Tags: cv::pilote cv::d14 famille::raisonnement cv_id::CV-QUANT-002 provenance::agent pole::A pole::F
END

## CV-QUANT-003

Objectif : vérifier le support d’un runtime. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-QUANT-003
Question: Pourquoi exporter un modèle ONNX ne suffit-il pas à garantir sa même précision et son accélération sur tout runtime ?
Reponse: **Noyau attendu** : Opérateurs, formes, kernels, précisions et matériel supportés diffèrent ; conversions/fallbacks et prétraitements doivent être validés.

**Approfondissement** : Versionner export, runtime, cible et mesures ; inspecter le graphe exécuté.

**Erreurs bloquantes** : Assimiler format d’échange et exécution optimisée universelle.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Fiche complète]] ; [TensorRT, quantization workflows](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html) ; [TensorRT, support matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
Tags: cv::pilote cv::d14 famille::pratique cv_id::CV-QUANT-003 provenance::agent pole::A pole::F
END

## CV-QUANT-004

Objectif : diagnostiquer une absence de gain INT8. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-QUANT-004
Question: Cas F — diagnostic : INT8 ne réduit pas la latence totale d’un pipeline vision. Comment départager les causes ?
Reponse: **Noyau attendu** : Profiler moteur et pipeline complet, opérateurs/précisions effectives, fallback, prétraitement CPU et transferts.

**Approfondissement** : Comparer même charge et qualité ; une accélération d’un petit étage peut être invisible à l’échelle du système. Corriger le goulot observé avant une nouvelle compression.

**Erreurs bloquantes** : Conclure que la quantification est toujours inutile ou toujours mal implémentée.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Fiche complète]] ; [TensorRT, quantization workflows](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html) ; [TensorRT, support matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-QUANT-004 provenance::agent pole::A pole::F cas_pole::F::diagnostic
END

## CV-QUANT-005

Objectif : contrôler qualité et performance ensemble. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-QUANT-005
Question: Quelles mesures associer à une réduction de mémoire après quantification d’un détecteur ?
Reponse: **Noyau attendu** : Qualité sur données réservées et cas critiques, plus latence/débit/mémoire du système complet au point d’exploitation fixé.

**Approfondissement** : Contrôler petits objets, domaines et saturation ; une taille de modèle réduite n’établit pas une mise en service acceptable.

**Erreurs bloquantes** : Rapporter seulement le nombre de bits ou le poids du fichier.
Source: [[140-ingenierie-systemes/references/142-quantification-runtimes|Fiche complète]] ; [TensorRT, quantization workflows](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-workflows.html) ; [TensorRT, support matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
Tags: cv::pilote cv::d14 famille::evaluation cv_id::CV-QUANT-005 provenance::agent pole::A pole::F
END
