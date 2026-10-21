# Contrats de données, profiling et pipelines vidéo — cartes

Fiche : [[140-ingenierie-systemes/references/141-contrats-profiling-video|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::140-ingenierie-systemes

## CV-PIPELINE-001

Objectif : séparer latence débit et fraîcheur. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-PIPELINE-001
Question: Un pipeline tient 240 images/s mais décide sur des frames vieilles. A-t-il forcément respecté son besoin temps réel ?
Reponse: **Noyau attendu** : Non : le débit ne garantit ni l’âge de l’observation ni le délai par décision.

**Approfondissement** : Mesurer timestamps de capture à sortie, distribution de latence, file et drops sous charge représentative.

**Erreurs bloquantes** : Valider le produit au seul FPS moyen.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Fiche complète]] ; Distinction de mesures du projet ; [TensorRT, Reported Performance Metrics](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html) et [GStreamer, queue](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), consultés le 2026-10-20.
Tags: cv::pilote cv::d14 famille::comparaison cv_id::CV-PIPELINE-001 provenance::agent pole::C pole::E pole::F
END

## CV-PIPELINE-002

Objectif : raisonner sur une file vidéo. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-PIPELINE-002
Question: Que prévoir si une entrée soutenue à 240 images/s dépasse le service à 200 images/s et qu’aucune frame n’est abandonnée ?
Reponse: **Noyau attendu** : Le retard et la taille de file croissent dans ce modèle ; un buffer plus grand retarde seulement la saturation.

**Approfondissement** : Choisir capacité, admission ou abandon selon fraîcheur/complétude et mesurer le comportement réel.

**Erreurs bloquantes** : Croire qu’augmenter la queue résout le déficit durable de débit.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Fiche complète]] ; Bilan de flux analytique du projet, 240−200 = 40 images/s de déficit ; [GStreamer queue, blocage et leaky](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), consulté le 2026-10-20, décrit les politiques d’une file bornée.
Tags: cv::pilote cv::d14 famille::raisonnement cv_id::CV-PIPELINE-002 provenance::agent pole::C pole::E pole::F
END

## CV-PIPELINE-003

Objectif : définir un benchmark complet. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-PIPELINE-003
Question: Pourquoi un temps GPU mesuré par un moteur d’inférence ne suffit-il pas à valider caméra→décision ?
Reponse: **Noyau attendu** : Décodage, pré/posttraitements, transferts, files et émission peuvent être exclus de cette mesure.

**Approfondissement** : Vérifier version/options du benchmark et mesurer le périmètre produit ; synchroniser correctement les opérations asynchrones.

**Erreurs bloquantes** : Comparer des durées GPU asynchrones à une latence utilisateur sans contrat.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Fiche complète]] ; [TensorRT, Measure End-to-End Performance, métriques et mesures synchronisées](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), consulté le 2026-10-20.
Tags: cv::pilote cv::d14 famille::pratique cv_id::CV-PIPELINE-003 provenance::agent pole::C pole::E pole::F
END

## CV-PIPELINE-004

Objectif : dimensionner huit flux sous p99. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-PIPELINE-004
Question: Cas F — conception : huit flux 1080p à 30 images/s sur module embarqué avec budget p99 défini. Quelle démarche rend le choix vérifiable ?
Reponse: **Noyau attendu** : Fixer fraîcheur, drops et qualité ; profiler chaque étage puis le flux complet à 240 images/s ; tester batch/concurrence/queues et scénarios de charge/thermique avant de choisir matériel ou optimisation.

**Approfondissement** : Conserver latence, débit, mémoire et qualité ensemble. Prévoir une surcharge explicite plutôt qu’un buffer infini ; aucun débit produit n’est garanti ici.

**Erreurs bloquantes** : Dimensionner sur un FPS isolé du modèle ou additionner mécaniquement des p99.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Fiche complète]] ; Cas de dimensionnement construit du projet ; [TensorRT benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html) et [GStreamer queue](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), consultés le 2026-10-20.
Tags: cv::pilote cv::d14 famille::conception cv_id::CV-PIPELINE-004 provenance::agent pole::C pole::E pole::F cas_pole::F::conception
END

## CV-PIPELINE-005

Objectif : localiser un goulot par trace. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-PIPELINE-005
Question: GPU peu occupé et latence élevée : quelles mesures peuvent distinguer décodage CPU, transferts et files ?
Reponse: **Noyau attendu** : Tracer temps CPU/GPU, H2D/D2H, attentes et âge des frames avec charge représentative.

**Approfondissement** : Modifier un étage à la fois et conserver le même contrat de qualité. Une occupation moyenne seule ne localise pas la cause.

**Erreurs bloquantes** : Optimiser le réseau sans mesurer les autres étapes.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Fiche complète]] ; Diagnostic proposé par le projet ; [TensorRT, Reported Performance Metrics et profiling](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), consulté le 2026-10-20.
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-PIPELINE-005 provenance::agent pole::C pole::E pole::F
END
