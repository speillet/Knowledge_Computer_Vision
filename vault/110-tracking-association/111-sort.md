# Cartes pilotes — SORT

Fiche : [[110-tracking-association/references/111-sort|SORT]]. Provenance : agent.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-SORT-001

Objectif : séparer les responsabilités du tracker. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-SORT-001
Question: Comment SORT transforme-t-il les détections successives en pistes, et pourquoi Kalman ne résout-il pas à lui seul l'identité ?
Reponse: **Noyau attendu** : prédire les pistes avec Kalman, associer les boîtes aux détections par IoU et affectation, corriger les associées, puis gérer créations et disparitions. L'association choisit la mesure d'une piste ; Kalman estime l'état après ce choix, sans vérifier l'identité physique.

**Approfondissement** : ![Pipeline causal SORT](../99-Ressources/cv-sort-pipeline.svg)

Schéma original du projet, agent, licence MIT. Un filtre peut corriger avec confiance une mesure mal associée. SORT original n'utilise pas d'apparence pour lever cette ambiguïté et ne remplace pas le détecteur.

**Erreurs bloquantes** : attribuer la réidentification à Kalman ou attribuer la production des détections au tracker SORT.
Source: [[110-tracking-association/references/111-sort|Fiche SORT]] ; [Bewley et al., §3](https://arxiv.org/abs/1602.00763).
Tags: cv::pilote cv::d11 famille::comprehension cv_id::CV-SORT-001 provenance::agent pole::C pole::D pole::E
END

## CV-SORT-002

Objectif : interpréter un état et ses unités. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-SORT-002
Question: Dans SORT original, que représentent les sept composantes d'état et quelles hypothèses temporelles faut-il vérifier quand la cadence change ?
Reponse: **Noyau attendu** : $[u,v,s,r,\dot u,\dot v,\dot s]^T$ contient centre, aire, rapport largeur/hauteur et trois vitesses. La mesure porte sur $[u,v,s,r]$ ; le rapport est constant dans le modèle déterministe. La référence prend une frame comme pas de temps.

**Approfondissement** : centre en pixels, aire en pixels carrés, rapport sans unité ; vitesses par frame. Appeler le tracker à chaque frame même sans détection. Baisse de cadence et frames sautées changent les déplacements et l'incertitude : vérifier modèle, fréquence des appels et unités avant de régler les seuils.

**Erreurs bloquantes** : prendre $s$ pour le score du détecteur, le rapport pour une vitesse ou supposer que le modèle s'adapte automatiquement au temps réel.
Source: [[110-tracking-association/references/111-sort|Fiche SORT]] ; [Article, §3.2](https://arxiv.org/abs/1602.00763) ; [référence, L94](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py#L94).
Tags: cv::pilote cv::d11 famille::raisonnement cv_id::CV-SORT-002 provenance::agent pole::C pole::D pole::E
END

## CV-SORT-003

Objectif : interpréter le poids d'une mesure. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-SORT-003
Question: Pour une correction Kalman scalaire, $u^-=100$ px, $P^-=25$ px², $z=110$ px et $R=9$ px². Vers quelle valeur va la position corrigée, et que change une mesure plus incertaine ?
Reponse: **Noyau attendu** : $K=P^-/(P^-+R)=25/34$, donc $u^+=u^-+K(z-u^-)\approx107,35$ px. Augmenter $R$ diminue le gain et rapproche l'estimation de la prédiction.

**Approfondissement** : $P^+=(1-K)P^-\approx6,62$ px². Avec $R=100$ px², la position vaut 102 px. C'est un exemple exécuté de correction linéaire scalaire, pas tout l'état SORT ni une preuve que la mesure appartient à la bonne personne. Une mauvaise association reste une autre source d'erreur.

**Erreurs bloquantes** : rapprocher davantage l'estimation d'une mesure quand sa variance augmente, ou confondre variance et écart-type.
Source: [[110-tracking-association/references/111-sort|Fiche SORT]] ; [référence Kalman de SORT](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py#L94).
Tags: cv::pilote cv::d11 famille::raisonnement cv_id::CV-SORT-003 provenance::agent pole::C pole::D pole::E
END

## CV-SORT-004

Objectif : distinguer mémoire et émission. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-SORT-004
Question: Dans la référence SORT épinglée avec `max_age=1`, que se passe-t-il après une puis deux frames consécutives sans détection associée, et une piste mémorisée est-elle forcément émise ?
Reponse: **Noyau attendu** : la suppression intervient si `time_since_update > max_age`. Une frame manquée peut laisser la piste mémorisée ; la deuxième la supprime. La référence émet seulement les pistes mises à jour dans la frame et respectant ses conditions de hits.

**Approfondissement** : `min_hits` filtre aussi les sorties avec une exception au démarrage global. Toujours appeler `update` avec un tableau vide de forme `(0, 5)`, par exemple `np.empty((0, 5))`, lorsque rien n'est détecté. Augmenter l'âge change le compromis entre continuité et maintien de fausses hypothèses ; cela ne crée pas une information de réidentification.

**Erreurs bloquantes** : confondre piste conservée et boîte affichée, ou annoncer une suppression dès que l'âge est égal au maximum.
Source: [[110-tracking-association/references/111-sort|Fiche SORT]] ; [référence, cycle de vie L199](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py#L199).
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-SORT-004 provenance::agent pole::C pole::D pole::E
END

## CV-SORT-005

Objectif : comprendre le rejet après affectation. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-SORT-005
Question: Une affectation maximise la somme des IoU $\begin{bmatrix}0.90&0.31\\0.31&0\end{bmatrix}$, puis rejette les paires sous 0,30. Pourquoi peut-elle garder moins de paires qu'une affectation visant d'abord leur admissibilité ?
Reponse: **Noyau attendu** : la diagonale donne 0,90, contre 0,62 pour les croisées ; elle est donc choisie pour le score brut. Après rejet du zéro, il reste une paire. Les deux associations croisées auraient pourtant chacune dépassé le seuil.

**Approfondissement** : maximiser le score puis rejeter n'est pas identique à un problème d'affectation avec contraintes d'admissibilité et objectif explicite de cardinalité. C'est un contre-exemple analytique, pas un résultat statistique sur SORT. Le code a aussi un raccourci lorsque les associations admissibles sont non ambiguës.

**Erreurs bloquantes** : affirmer que tout gating après affectation est équivalent au gating avant, sans vérifier la formulation.
Source: [[110-tracking-association/references/111-sort|Fiche SORT]] ; [association SORT, L154](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py#L154).
Tags: cv::pilote cv::d11 famille::pratique cv_id::CV-SORT-005 provenance::agent pole::C pole::D pole::E
END

## CV-SORT-006

Objectif : établir un diagnostic discriminant. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-SORT-006
Question: Une personne change d'identifiant après une occultation. Quelles observations permettent de distinguer détection manquée, piste expirée et mauvaise association ?
Reponse: **Noyau attendu** : suivre, frame par frame, détections, prédictions, matrice d'IoU, associations et âge des pistes. Vérifier d'abord si la boîte existe, si la piste était encore mémorisée et si une paire admissible a été choisie.

**Approfondissement** :
- Boîte absente : examiner détecteur et NMS.
- Piste supprimée : examiner durée d'absence et `max_age`.
- Pistes concurrentes : examiner mouvement et ambiguïté d'apparence.

Augmenter `max_age` aide seulement certaines absences ; une méthode avec apparence ou autre association peut être nécessaire. La cause n'est pas identifiable à partir du seul identifiant final.

**Erreurs bloquantes** : prescrire automatiquement un âge plus élevé ou attribuer tout échange d'ID au filtre de Kalman.
Source: [[110-tracking-association/references/111-sort|Fiche SORT]] ; [SORT, §§3.2–3.4](https://arxiv.org/abs/1602.00763).
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-SORT-006 provenance::agent pole::C pole::D pole::E
END

## CV-SORT-007

Objectif : distinguer les tâches temporelles. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-SORT-007
Question: Pourquoi un bon flot optique, une bonne AP de détection et une bonne réidentification ne suffisent-ils pas séparément à garantir un bon tracking multiobjet ?
Reponse: **Noyau attendu** : le flot décrit des déplacements de points/pixels ; l'AP évalue des détections sans identité temporelle ; la ReID compare l'apparence d'identités. Le tracking combine observations, association et cycle de vie dans le temps.

**Approfondissement** : des détections bien localisées peuvent être associées aux mauvaises pistes ; une apparence correcte peut manquer une détection ; un flot utile ne décide pas toujours entrées/sorties et occultations. Évaluer détection et association avec des métriques et séquences adaptées, sans substituer l'AP à un score d'identité.

**Erreurs bloquantes** : confondre ces sorties ou déduire la continuité d'identité de la seule AP.
Source: [[110-tracking-association/references/111-sort|Fiche SORT]] ; [SORT, §§2–4](https://arxiv.org/abs/1602.00763).
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-SORT-007 provenance::agent pole::C pole::D pole::E
END

## CV-SORT-008

Objectif : définir une mesure de performance complète. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-SORT-008
Question: Le tracker seul dépasse la cadence demandée, mais le produit manque sa latence et perd des identités. Quelles mesures manquent à cette validation ?
Reponse: **Noyau attendu** : mesurer acquisition, détection, NMS, transferts et tracking de bout en bout sur le matériel cible ; mesurer aussi les erreurs d'identité, les fragments et les dépendances aux détections sur des séquences représentatives.

**Approfondissement** : conserver latence et débit séparés, examiner les pics, densité d'objets et cadence. Des chiffres de vitesse du papier concernent son environnement et son composant. Utiliser des splits par séquence/scène, consigner seuils et versions, et ne pas annoncer de performance de tracking avec le seul temps de l'affectation.

**Erreurs bloquantes** : présenter la fréquence du composant comme celle du système complet ou ignorer les échanges d'ID dans l'évaluation.
Source: [[110-tracking-association/references/111-sort|Fiche SORT]] ; [SORT, §4](https://arxiv.org/abs/1602.00763).
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-SORT-008 provenance::agent pole::C pole::D pole::E
END
