---
id: CV-PIPELINE
type: pipeline
domaine: d14
poles: [C, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 3
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d14]
---
# Contrats de données, profiling et pipelines vidéo

## Problème, données et hypothèses

Tenir une exigence de décision de bout en bout sous flux. Entrées : frames avec timestamps, métadonnées et contrats ; sortie : résultat dans le bon repère avant le délai utile. Latence, débit et fraîcheur ne sont pas la même quantité.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Décomposer acquisition, décodage, prétraitement, transferts, inférence, posttraitement et émission. Profiler CPU/GPU/queues avec horodatage cohérent. Batching et recouvrement peuvent augmenter le débit sans améliorer la latence individuelle ; une file accumule du retard si le service est insuffisant.

## Mathématiques, conventions et unités

Pour huit flux à 30 images/s, le débit entrant est 240 images/s. Cette moyenne ne donne pas un p99. Une file avec taux d'arrivée $\lambda$ supérieur au service soutenable $\mu$ croît sans borne dans un modèle sans abandon. Un budget p99 somme de p99 d'étapes n'est pas une identité statistique générale.

## Paramètres et propriétés

Batch, concurrence, cadence, politique de drop, buffers et point de mesure. Zero-copy décrit certains transferts évités, pas une absence universelle de copie. Décodage matériel et conversion couleur peuvent encore être des goulots.

## Coût et implémentation

Mesurer temps moteur et transferts séparément, puis système complet ; Nsight peut aider selon matériel. Aucun benchmark exécuté. Les commandes et valeurs par défaut de `trtexec` évoluent : consulter la version avant de supposer ce qui est inclus. Documentation `latest` consultée le 2026-10-20 ; aucune commande ni valeur par défaut universelle n’est fixée ici.

## Évaluation et variation contrôlée

Baseline : un flux puis charge croissante à modèle figé ; mesurer p50/p99, âge de frame, drops, débit et mémoire. La variation de charge teste files et concurrence, pas uniquement le kernel moyen.

## Échecs et diagnostic

FPS stables mais frames vieilles : inspecter files/backpressure et timestamps. GPU peu occupé : profiler CPU/décodage/transferts. Ne pas conclure que le modèle est trop petit ou trop grand sans trace.

## Alternatives et usages

GStreamer/DeepStream/NVDEC selon environnement ; ROS 2 pour interfaces robot avec contrat QoS/horloges. Une politique de fraîcheur peut abandonner de vieilles frames mais doit être cohérente avec tracking et temporalité.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent contrats, files et âge de l’information. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-PIPELINE-001

**Question de travail** : Un pipeline tient 240 images/s mais décide sur des frames vieilles. A-t-il forcément respecté son besoin temps réel ?

**Réponse de référence** : Non : le débit ne garantit ni l’âge de l’observation ni le délai par décision.

**Deux quantités distinctes** : un débit compte les sorties par seconde ; l'âge d'une frame compare son instant de capture à celui où sa décision est disponible. Un système peut traiter beaucoup d'images tout en accumulant une attente importante avant le calcul. Le terme temps réel doit donc être lié à un délai utile défini.

**Exemple construit** : une file contient déjà plusieurs secondes d'images lorsque le moteur atteint son débit nominal. Les sorties arrivent régulièrement, mais décrivent un passé trop ancien pour l'action aval. Mesurer attente et fraîcheur, puis choisir une politique de charge cohérente avec le besoin. Abandonner de vieilles frames peut réduire l'ancienneté, mais affecte tracking et événements courts ; traiter toutes les frames peut préserver la complétude en violant le délai. Le bon compromis ne se déduit pas du FPS seul : il appartient au contrat produit et doit être testé sous charge.

### Cas lié à CV-PIPELINE-005

**Question de travail** : GPU peu occupé et latence élevée : quelles mesures peuvent distinguer décodage CPU, transferts et files ?

**Réponse de référence** : Tracer temps CPU/GPU, H2D/D2H, attentes et âge des frames avec charge représentative.

**Interprétation des traces** : un GPU peu occupé peut attendre des images décodées, des copies ou une dépendance entre étapes. Une moyenne d'utilisation masque les alternances de calcul et d'attente ; elle ne dit pas directement quel composant doit être accéléré.

**Ablation proposée** : instrumenter la chronologie, puis remplacer temporairement le décodage par des entrées préparées ou comparer un transfert isolé, avec un objectif de mesure explicite. Réintroduire ensuite la chaîne complète pour vérifier le gain produit. Contrôler aussi taille des lots et files, car réduire un coût peut déplacer le goulet. La qualité des entrées et des sorties doit rester identique. Cette démarche relie une hypothèse à une mesure discriminante et évite de modifier architecture ou précision alors que le modèle ne constitue qu'une fraction du délai observé. Les essais décrits sont proposés, sans trace matérielle exécutée ici.

**Repère documentaire de cette passe** : [GStreamer, queue](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), limites, blocage, leaky et niveaux courants. Les autres développements figurent dans les [cartes associées](../141-contrats-profiling-video.md).

## Sources et cartes

- [TensorRT, performance benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html).
- [GStreamer queue, limites et leaky](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html).
- [Cartes associées](../141-contrats-profiling-video.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
