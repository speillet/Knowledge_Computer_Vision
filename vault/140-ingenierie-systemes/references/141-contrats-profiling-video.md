---
id: CV-PIPELINE
type: pipeline
domaine: d14
poles: [C, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 1
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

Mesurer temps moteur et transferts séparément, puis système complet ; Nsight peut aider selon matériel. Aucun benchmark exécuté. Les commandes et défauts de `trtexec` évoluent : consulter la version avant de supposer ce qui est inclus.

## Évaluation et variation contrôlée

Baseline : un flux puis charge croissante à modèle figé ; mesurer p50/p99, âge de frame, drops, débit et mémoire. La variation de charge teste files et concurrence, pas uniquement le kernel moyen.

## Échecs et diagnostic

FPS stables mais frames vieilles : inspecter files/backpressure et timestamps. GPU peu occupé : profiler CPU/décodage/transferts. Ne pas conclure que le modèle est trop petit ou trop grand sans trace.

## Alternatives et usages

GStreamer/DeepStream/NVDEC selon environnement ; ROS 2 pour interfaces robot avec contrat QoS/horloges. Une politique de fraîcheur peut abandonner de vieilles frames mais doit être cohérente avec tracking et temporalité.

## Sources et cartes

- [TensorRT, performance benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/latest/performance/benchmarking.html).
- [GStreamer queue, limites et leaky](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html).
- [Cartes associées](../141-contrats-profiling-video.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
