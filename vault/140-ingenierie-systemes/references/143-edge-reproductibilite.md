---
id: CV-DEPLOIEMENT
type: pipeline
domaine: d14
poles: [A, C, E, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
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

La loi d'Amdahl simplifiée borne un gain global à $1/((1-f)+f/s)$ si une fraction f du temps est accélérée d'un facteur s, sans nouveaux surcoûts. Accélérer un étage de 10 % du temps par 2 donne seulement environ 1,053× global dans ce modèle. Ne pas confondre moyenne et p99.

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

## Sources et cartes

- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
- [TensorRT, support et portabilité](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
- [Cartes associées](../143-edge-reproductibilite.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
