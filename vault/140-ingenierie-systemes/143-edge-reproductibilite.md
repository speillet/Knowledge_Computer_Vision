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
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Fiche complète]] ; Dérivation algébrique du projet pour le modèle séquentiel de la fiche : temps normalisé après changement $(1-f)+f/s$, soit $0,9+0,1/2=0,95$ ; [Amdahl (1967), p. 483](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf) pour la limite imposée par la partie non accélérée.
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
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Fiche complète]] ; [TensorRT 8.6.1, §6.10 Sparsity](https://docs.nvidia.com/deeplearning/tensorrt/archives/tensorrt-861/developer-guide/index.html#structured-sparsity) : les tactiques creuses ne sont pas systématiquement sélectionnées car elles peuvent être plus lentes.
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
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Fiche complète]] ; [The ML Test Score, Model/Infra tests et rollback](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf) ; liste de contrats adaptée par le projet.
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
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Fiche complète]] ; Diagnostic proposé par le projet ; [Jetson Linux r36.4, Thermal Management](https://docs.nvidia.com/jetson/archives/r36.4/DeveloperGuide/SD/PlatformPowerAndPerformance/JetsonOrinNanoSeriesJetsonOrinNxSeriesAndJetsonAgxOrinSeries.html) pour le mécanisme thermique, sans supposer cette plateforme dans tous les déploiements.
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-DEPLOIEMENT-004 provenance::agent pole::A pole::C pole::E pole::F
END
