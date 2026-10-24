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

**Calcul interprété** : normaliser le temps initial à un. La part non accélérée vaut 0,9 ; l'inférence passe de 0,1 à 0,05. Le temps total devient 0,95, soit une réduction de 5 %, et le facteur de vitesse est son inverse. L'étage accéléré n'occupait qu'une petite part du travail total.

**Conséquence produit** : profiler avant de compresser évite d'investir dans une optimisation dont le gain global est limité dans ce modèle. De nouveaux surcoûts de conversion peuvent même annuler le bénéfice. À l'inverse, réduire une ressource critique dans un système concurrent peut modifier les files d'une façon que ce calcul additif ne décrit pas. Il s'agit donc d'une borne de raisonnement sous hypothèses explicites, pas d'une prédiction de toute la distribution de latence. Confirmer le gain sur la même charge et le même contrat de qualité.

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

**Pourquoi le comptage ne suffit pas** : un poids nul n'est pas automatiquement une multiplication évitée par le kernel. Le motif de sparsité, la forme des tenseurs et les opérations disponibles déterminent si le matériel peut exploiter ce retrait. Une représentation creuse peut aussi ajouter indexation et transferts.

**Comparaison proposée** : inspecter le graphe réellement exécuté et mesurer la même tâche sur le matériel cible, avec qualité et mémoire. Distinguer pruning structuré, qui peut changer les dimensions du calcul, et sparsité non structurée, dont l'exploitation exige un support approprié. Vérifier les couches qui dominent réellement le temps. Une réduction du nombre de paramètres peut rester utile pour stockage ou distribution sans accélérer l'inférence. Les affirmations de vitesse doivent donc être accompagnées du schéma, du backend et du protocole, plutôt que déduites d'un pourcentage de zéros indépendant de l'implémentation.

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

**Exemple de régression** : des poids identiques peuvent produire une autre décision si l'entrée passe de RGB à BGR, si les boîtes sont décodées dans un autre repère ou si les indices de classes changent. Le modèle exploité est donc un ensemble de contrats et d'artefacts autour du réseau.

**Procédure proposée** : conserver une entrée témoin et des sorties de référence à plusieurs étapes, puis comparer une nouvelle version avant de la déployer. Versionner paramètres et dépendances qui changent ces sorties, avec le format attendu par le consommateur. Prévoir compatibilité et retour arrière de toute la chaîne, et pas seulement des poids. Une égalité exacte peut ne pas être réaliste entre toutes les cibles numériques ; définir une tolérance liée à l'usage et examiner les décisions proches du seuil. Ce contrôle facilite l'attribution d'une régression et la reproduction par un autre ingénieur.

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

**Pourquoi la durée compte** : l'état thermique, l'occupation mémoire et les files peuvent évoluer après le démarrage. Une mesure courte sur un appareil froid ne décrit donc pas nécessairement son régime soutenable. Une baisse de fréquence, une fuite ou une accumulation d'attente produisent des signatures différentes.

**Enquête proposée** : tracer simultanément température, fréquences, mémoire, débits par étape et âge des frames, sur une charge et une durée représentatives. Repérer quel changement précède la dégradation, puis modifier une hypothèse à la fois. Comparer par exemple une file bornée à la politique initiale sans changer le modèle, ou vérifier le régime thermique selon le dispositif. Confirmer ensuite qualité et délai complets. Une cause de calcul n'exclut pas une cause de données ; le système doit conserver entrées et configuration pour expliquer les échecs, sans annoncer un diagnostic unique depuis le seul FPS final.

**Erreurs bloquantes** : Déclarer le matériel suffisant sur un test froid isolé.
Source: [[140-ingenierie-systemes/references/143-edge-reproductibilite|Fiche complète]] ; Diagnostic proposé par le projet ; [Jetson Linux r36.4, Thermal Management](https://docs.nvidia.com/jetson/archives/r36.4/DeveloperGuide/SD/PlatformPowerAndPerformance/JetsonOrinNanoSeriesJetsonOrinNxSeriesAndJetsonAgxOrinSeries.html) pour le mécanisme thermique, sans supposer cette plateforme dans tous les déploiements.
Tags: cv::pilote cv::d14 famille::diagnostic cv_id::CV-DEPLOIEMENT-004 provenance::agent pole::A pole::C pole::E pole::F
END
