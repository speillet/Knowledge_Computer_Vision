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

**Exemple de responsabilité** : au croisement de deux personnes, deux mesures peuvent être géométriquement plausibles pour une piste. Le filtre prédit des états et leurs incertitudes ; l'affectation choisit les couples effectivement utilisés pour la correction. Si ce choix échange les personnes, un état lisse peut suivre avec assurance la mauvaise identité.

**Diagnostic proposé** : conserver pour chaque frame les boîtes avant association, les prédictions, les coûts et les événements de création ou suppression. Une superposition finale sans cette chronologie ne permet pas de localiser l'erreur. Le schéma causal sépare ces fonctions pour choisir un correctif : améliorer le détecteur, la prédiction, l'association ou le cycle de vie selon la trace observée, plutôt qu'attribuer tout problème à Kalman.

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

**Pourquoi les unités importent** : un déplacement de centre par frame change de signification si l'intervalle entre appels change. Deux frames consécutives à dix images/s sont plus éloignées dans le temps qu'à trente images/s. Le modèle et son bruit doivent correspondre à cette convention, ou être adaptés avec un pas temporel explicite.

**Contrôle construit** : conserver une même séquence horodatée et comparer un traitement sans saut puis avec sous-échantillonnage. Vérifier mouvements prédits, erreurs d'association et durée physique de persistance des pistes. Un paramètre d'âge en nombre de frames ne conserve pas automatiquement sa durée en secondes. Ces éléments expliquent pourquoi un simple changement de cadence peut modifier la continuité des IDs sans changement du détecteur.

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

**Intuition de pondération** : le gain est sans unité et se situe ici entre zéro et un pour des variances positives. La correction est une fraction de l'innovation de dix pixels. Une mesure déclarée moins précise apporte moins d'information et déplace moins l'estimation ; elle réduit aussi moins son incertitude.

**Limite du calcul** : les valeurs supposent modèle linéaire, bruits compatibles et mesure correctement associée. Diminuer artificiellement $R$ rend le filtre plus réactif mais peut le rendre surconfiant face à une mauvaise mesure. Une covariance plus faible ne prouve pas une meilleure position réelle. L'exemple aide donc à comprendre le compromis prédiction/observation, avant le problème séparé de l'association d'objets.

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

**Chronologie à expliciter** : mémoriser une piste permet de la réassocier plus tard, tandis qu'émettre une boîte décrit ce que le consommateur reçoit dans la frame courante. Ces deux décisions suivent des conditions distinctes dans la référence. Une absence à l'écran ne démontre donc pas à elle seule que la piste a déjà été détruite.

**Test construit** : préparer une détection, une frame vide, puis un retour de détection, et tracer âge, hits, ID interne et sortie émise. Refaire avec deux frames vides et avec une cadence différente. Ne pas interpréter un âge en frames comme une durée universelle. Le résultat attendu concerne le commit épinglé ; une autre bibliothèque ou variante peut adopter un cycle différent.

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

**Différence d'objectif** : optimiser une somme de similarités favorise une très bonne paire même si l'autre paire est ensuite inutilisable. Maximiser d'abord le nombre de couples admissibles exprime une autre préférence, qui peut conserver deux paires de qualité moyenne. Aucun nom d'algorithme d'affectation ne dispense de définir ce que le coût et les contraintes représentent.

**Usage du contre-exemple** : tester séparément couples impossibles, choix de non-affectation et seuils, puis regarder les conséquences sur les IDs. Changer seulement le solveur sans modifier la formulation peut conserver le même comportement. La matrice jouet démontre une différence logique entre deux problèmes ; elle ne dit pas lequel produit les meilleures trajectoires sur toutes les scènes.

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

**Enquête temporelle** : repérer la dernière frame correctement associée, la première frame manquée, le moment éventuel de suppression et la première réapparition. Si la piste existe encore mais qu'une autre détection est choisie, le problème diffère d'une création normale après expiration.

**Ablation proposée** : fixer les détections et changer uniquement le cycle de vie, puis fixer ce cycle et examiner une autre information d'association. Vérifier les conséquences sur les faux maintiens de pistes et les erreurs après croisement. Une durée de persistance plus longue peut aider une courte absence mais conserver une hypothèse devenue fausse. Le diagnostic doit expliquer l'événement observé et ses compromis, sans appliquer systématiquement le même paramètre à toute perte d'identité.

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

**Exemple construit** : un détecteur fournit les bonnes boîtes à chaque frame mais leur ordre est permuté au croisement. L'AP reste excellente si chaque boîte correspond bien à un objet, tandis qu'une association naïve par indice échange les identités. Un score spatial ne mesure pas cette erreur temporelle.

**Évaluation proposée** : conserver la même séquence et examiner détection, association et gestion des disparitions séparément. Ajouter des occultations et des objets d'apparence proche pour observer les informations manquantes. Les composants peuvent être nécessaires sans être suffisants : une représentation ReID discriminante ne crée pas une boîte absente, et un flot précis ne décide pas seul la naissance d'une piste. Choisir la métrique selon la sortie promise par le système.

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

**Ancienneté des observations** : le tracker peut être rapide tout en recevant des détections calculées sur des images anciennes. Une file d'attente ou une politique de batch peut augmenter le déplacement réel entre l'état estimé et la décision utilisée. Cela peut affecter simultanément latence et qualité d'association.

**Mesure proposée** : horodater capture, entrée de chaque étape et sortie, puis stratifier les délais et erreurs par densité d'objets. Comparer charge habituelle, pics et pertes de frames avec la même politique de file. Les performances publiées pour l'association seule ne remplacent pas cette trace. Un système exploitable doit tenir son budget temporel et sa qualité de pistes dans les mêmes conditions, avec une politique explicite lorsque la charge dépasse la capacité.

**Erreurs bloquantes** : présenter la fréquence du composant comme celle du système complet ou ignorer les échanges d'ID dans l'évaluation.
Source: [[110-tracking-association/references/111-sort|Fiche SORT]] ; [SORT, §4](https://arxiv.org/abs/1602.00763).
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-SORT-008 provenance::agent pole::C pole::D pole::E
END
