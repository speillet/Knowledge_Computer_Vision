# Déploiement edge, compression et surveillance — cartes

Fiche : [[140-ingenierie-systemes/references/143-edge-reproductibilite|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::140-ingenierie-systemes

## CV-DEPLOIEMENT-001

Objectif : borner un gain de système. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-001
Question: Si l’inférence représente 10 % du temps moyen et devient deux fois plus rapide sans autre coût, quel gain global idéal prévoir ?
Reponse: **Noyau attendu** : Environ 1/0,95 = 1,053×, selon le modèle d’Amdahl annoncé.

**Approfondissement** : Le p99 et les files peuvent réagir autrement ; vérifier par mesure complète plutôt qu’extrapoler le gain d’un kernel.

**Erreurs bloquantes** : Annoncer un pipeline deux fois plus rapide.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Fiche complète]] ; [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) ; [TensorRT, support et portabilité](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
Tags: cv::pilote cv::d14 famille::raisonnement cv_id::CV-DEPLOIEMENT-001 provenance::agent pole::A pole::C pole::E pole::F
END

## CV-DEPLOIEMENT-002

Objectif : relier compression et accélération. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-002
Question: Pourquoi moins de poids après pruning ne garantit-il pas une inférence plus rapide ?
Reponse: **Noyau attendu** : Le backend doit exploiter la structure de sparsité et les kernels disponibles ; conversions ou accès mémoire peuvent dominer.

**Approfondissement** : Mesurer graphe réel et matériel cible, qualité comprise ; taille disque et temps sont des grandeurs différentes.

**Erreurs bloquantes** : Déduire automatiquement vitesse et énergie du taux de poids nuls.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Fiche complète]] ; [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) ; [TensorRT, support et portabilité](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
Tags: cv::pilote cv::d14 famille::comparaison cv_id::CV-DEPLOIEMENT-002 provenance::agent pole::A pole::C pole::E pole::F
END

## CV-DEPLOIEMENT-003

Objectif : versionner un système complet. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-003
Question: Que faut-il versionner pour reproduire une sortie de vision au-delà des poids ?
Reponse: **Noyau attendu** : Prétraitements/repères, architecture, taxonomie, posttraitements/seuils, runtime et dépendances pertinentes, ainsi qu’une entrée de référence.

**Approfondissement** : Tester compatibilité et rollback avant déploiement ; une différence de resize ou BGR/RGB peut changer la décision.

**Erreurs bloquantes** : Considérer les poids comme l’unique artefact du modèle exploité.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Fiche complète]] ; [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) ; [TensorRT, support et portabilité](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
Tags: cv::pilote cv::d14 famille::pratique cv_id::CV-DEPLOIEMENT-003 provenance::agent pole::A pole::C pole::E pole::F
END

## CV-DEPLOIEMENT-004

Objectif : tester le régime edge. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-DEPLOIEMENT-004
Question: Un benchmark bref passe mais le débit chute après une heure sur edge. Quelles traces recueillir ?
Reponse: **Noyau attendu** : Température/fréquences, charge/mémoire, transferts et files, avec qualité et timestamps de bout en bout.

**Approfondissement** : Distinguer throttling, fuite ou accumulation de retard ; répéter le scénario représentatif après correction.

**Erreurs bloquantes** : Déclarer le matériel suffisant sur un test froid isolé.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Fiche complète]] ; [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) ; [TensorRT, support et portabilité](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html).
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-DEPLOIEMENT-004 provenance::agent pole::A pole::C pole::E pole::F
END
