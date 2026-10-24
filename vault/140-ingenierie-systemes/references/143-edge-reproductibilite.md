---
id: CV-DEPLOIEMENT
type: pipeline
domaine: d14
poles: [A, C, E, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 4
prerequis: ["CV-PIPELINE", "CV-QUANT"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d14]
---
# Déploiement edge, compression et surveillance

## Problème, données et hypothèses

Livrer un système de vision reproductible et observable, avec mise à jour maîtrisée. Entrées : artefacts, contrats, versions et cible ; sortie : service testé avec politique de panne/retour. Déploiement implique plus que copier les poids.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-PIPELINE](141-contrats-profiling-video.md) ; [CV-QUANT](142-quantification-runtimes.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Versionner prétraitements, modèle, posttraitements et taxonomie ; tester sur entrées de référence puis charge réelle. Distillation transfère une supervision/structure de sorties ; pruning retire des composantes selon schéma. Serving, température et file vidéo font partie du système.

## Mathématiques, conventions et unités

Dans le modèle séquentiel additif, la loi d'Amdahl simplifiée borne un gain global à $1/((1-f)+f/s)$ si une fraction f du temps est accélérée d'un facteur s, sans nouveaux surcoûts. Accélérer un étage de 10 % du temps par 2 donne seulement environ 1,053× global dans ce modèle. Ne pas confondre moyenne et p99.

## Paramètres et propriétés

Artefacts/runtime, formes, seuils, démarrage à froid, thermique, consommation, observabilité et rollback. OTA et gestion de versions doivent conserver compatibilité des sorties et possibilité de retour, sans modifier ici un appareil personnel.

## Coût et implémentation

Un pruning non structuré n'accélère que si kernels/matériel exploitent sa sparsité ; distiller peut demander un entraînement mais ne change pas automatiquement les transferts. Aucun appareil/serveur modifié ni consommation mesurée.

## Évaluation et variation contrôlée

Baseline complète figée ; varier charge, durée et température ambiante sous protocole. Mesurer stabilité, qualité et files, y compris démarrage, déconnexion et restauration. Une exécution courte ne prouve pas un régime thermique stable.

## Échecs et diagnostic

Une régression après mise à jour peut venir de normalisation ou classes, pas seulement poids ; utiliser entrées de référence et traces pour comparer versions. Conserver erreurs terrain anonymisées sans données privées.

## Alternatives et usages

Serving central, edge ou hybride selon contraintes ; la surveillance de scores doit être liée à des retours étiquetés pour démontrer une dérive de qualité.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent goulot séquentiel, régime thermique et reproductibilité. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-DEPLOIEMENT-001

**Question de travail** : Si l’inférence représente 10 % du temps moyen et devient deux fois plus rapide sans autre coût, quel gain global idéal prévoir ?

**Réponse de référence** : Environ 1/0,95 = 1,053×, selon le modèle d’Amdahl annoncé.

**Calcul interprété** : normaliser le temps initial à un. La part non accélérée vaut 0,9 ; l'inférence passe de 0,1 à 0,05. Le temps total devient 0,95, soit une réduction de 5 %, et le facteur de vitesse est son inverse. L'étage accéléré n'occupait qu'une petite part du travail total.

**Conséquence produit** : profiler avant de compresser évite d'investir dans une optimisation dont le gain global est limité dans ce modèle. De nouveaux surcoûts de conversion peuvent même annuler le bénéfice. À l'inverse, réduire une ressource critique dans un système concurrent peut modifier les files d'une façon que ce calcul additif ne décrit pas. Il s'agit donc d'une borne de raisonnement sous hypothèses explicites, pas d'une prédiction de toute la distribution de latence. Confirmer le gain sur la même charge et le même contrat de qualité.

### Cas lié à CV-DEPLOIEMENT-004

**Question de travail** : Un benchmark bref passe mais le débit chute après une heure sur edge. Quelles traces recueillir ?

**Réponse de référence** : Température/fréquences, charge/mémoire, transferts et files, avec qualité et timestamps de bout en bout.

**Pourquoi la durée compte** : l'état thermique, l'occupation mémoire et les files peuvent évoluer après le démarrage. Une mesure courte sur un appareil froid ne décrit donc pas nécessairement son régime soutenable. Une baisse de fréquence, une fuite ou une accumulation d'attente produisent des signatures différentes.

**Enquête proposée** : tracer simultanément température, fréquences, mémoire, débits par étape et âge des frames, sur une charge et une durée représentatives. Repérer quel changement précède la dégradation, puis modifier une hypothèse à la fois. Comparer par exemple une file bornée à la politique initiale sans changer le modèle, ou vérifier le régime thermique selon le dispositif. Confirmer ensuite qualité et délai complets. Une cause de calcul n'exclut pas une cause de données ; le système doit conserver entrées et configuration pour expliquer les échecs, sans annoncer un diagnostic unique depuis le seul FPS final.

**Repère documentaire de cette passe** : [Amdahl 1967](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf), p. 483, fraction non accélérée. Les autres développements figurent dans les [cartes associées](../143-edge-reproductibilite.md).

## Sources et cartes

- [Amdahl (1967), p. 483 : limite due à la fraction non accélérée](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf). Le calcul numérique ci-dessus est une dérivation du projet.

- [TensorRT 8.6.1, §6.10 Sparsity](https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt-861/developer-guide/index.html#structured-sparsity) : exemple versionné de motifs supportés et tactiques parfois moins rapides.
- [Hinton et al., Distilling the Knowledge in a Neural Network, introduction](https://arxiv.org/abs/1503.02531) : supervision par sorties du modèle enseignant.
- [Jetson Linux r36.4, Thermal Management](https://docs.nvidia.com/jetson/archives/r36.4/DeveloperGuide/SD/PlatformPowerAndPerformance/JetsonOrinNanoSeriesJetsonOrinNxSeriesAndJetsonAgxOrinSeries.html) : exemple versionné de réduction des fréquences sous contrainte thermique.

- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
- [TensorRT, support et portabilité](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
- [Cartes associées](../143-edge-reproductibilite.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
