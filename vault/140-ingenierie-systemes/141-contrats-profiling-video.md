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

**Deux quantités distinctes** : un débit compte les sorties par seconde ; l'âge d'une frame compare son instant de capture à celui où sa décision est disponible. Un système peut traiter beaucoup d'images tout en accumulant une attente importante avant le calcul. Le terme temps réel doit donc être lié à un délai utile défini.

**Exemple construit** : une file contient déjà plusieurs secondes d'images lorsque le moteur atteint son débit nominal. Les sorties arrivent régulièrement, mais décrivent un passé trop ancien pour l'action aval. Mesurer attente et fraîcheur, puis choisir une politique de charge cohérente avec le besoin. Abandonner de vieilles frames peut réduire l'ancienneté, mais affecte tracking et événements courts ; traiter toutes les frames peut préserver la complétude en violant le délai. Le bon compromis ne se déduit pas du FPS seul : il appartient au contrat produit et doit être testé sous charge.

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

**Ordre de grandeur analytique** : dans le modèle constant annoncé, quarante frames supplémentaires s'accumulent chaque seconde. Un buffer peut absorber un pic temporaire, mais pas une surcharge durable sans autre changement. Sa capacité modifie le moment où l'on manque de mémoire ou où l'on bloque, pas l'écart de capacité soutenable.

**Décision proposée** : définir si le produit privilégie toutes les observations ou leur fraîcheur, puis comparer réduction de charge, capacité supplémentaire, admission et abandon contrôlé. Mesurer les effets sur les erreurs temporelles et les pertes de tracking. Si un producteur est bloqué, vérifier aussi ce qui se passe dans les buffers amont de caméra ou de décodage. Une file bornée ne garantit pas à elle seule une bonne latence de bout en bout. La stabilité se juge sur le flux réel, ses variations et la politique complète, pas seulement sur le réglage d'un buffer isolé.

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

**Périmètre de mesure** : le moteur peut mesurer uniquement une partie du calcul, avec entrées déjà en mémoire ou transferts exclus selon les options. La caméra réelle ajoute acquisition, transport, décodage et attente. Une opération asynchrone peut aussi être seulement lancée lorsque le chronomètre s'arrête.

**Protocole proposé** : associer chaque résultat à l'instant de capture de sa frame et mesurer jusqu'à la sortie utile, avec une horloge ou une synchronisation cohérente. Conserver aussi des mesures par étape pour localiser le coût. Tester charge, taille de batch, objets et durée représentatifs. Une distribution de latences et des drops décrivent mieux le service qu'un unique temps moyen de kernel. Les outils de benchmark restent utiles pour comparer un composant ; leurs options et versions définissent ce qu'ils mesurent. Il faut donc relier leur sortie au contrat du produit plutôt que lui attribuer implicitement toutes les étapes.

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

**Dimensionnement proposé** : commencer par une baseline à un flux pour vérifier contrats et instrumentation, puis augmenter la charge jusqu'aux huit flux simultanés. Observer quelle ressource et quelle file saturent, en conservant modèle, précision et seuils. Le débit agrégé de 240 images/s ne dit pas si chaque flux reçoit un service équitable.

**Critère système** : comparer distributions par flux et âge des observations avec le budget de décision. Un p99 global peut masquer un flux défavorisé ; la somme des p99 d'étapes n'est pas en général le p99 du chemin complet. Inclure régime thermique, pics et redémarrage dans un protocole documenté. Ces mesures permettent de choisir une optimisation qui traite le goulet réel, plutôt que surdimensionner ou compresser aveuglément le seul réseau.

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

**Interprétation des traces** : un GPU peu occupé peut attendre des images décodées, des copies ou une dépendance entre étapes. Une moyenne d'utilisation masque les alternances de calcul et d'attente ; elle ne dit pas directement quel composant doit être accéléré.

**Ablation proposée** : instrumenter la chronologie, puis remplacer temporairement le décodage par des entrées préparées ou comparer un transfert isolé, avec un objectif de mesure explicite. Réintroduire ensuite la chaîne complète pour vérifier le gain produit. Contrôler aussi taille des lots et files, car réduire un coût peut déplacer le goulet. La qualité des entrées et des sorties doit rester identique. Cette démarche relie une hypothèse à une mesure discriminante et évite de modifier architecture ou précision alors que le modèle ne constitue qu'une fraction du délai observé. Les essais décrits sont proposés, sans trace matérielle exécutée ici.

**Erreurs bloquantes** : Optimiser le réseau sans mesurer les autres étapes.
Source: [[140-ingenierie-systemes/references/141-contrats-profiling-video|Fiche complète]] ; Diagnostic proposé par le projet ; [TensorRT, Reported Performance Metrics et profiling](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html), consulté le 2026-10-20.
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-PIPELINE-005 provenance::agent pole::C pole::E pole::F
END
