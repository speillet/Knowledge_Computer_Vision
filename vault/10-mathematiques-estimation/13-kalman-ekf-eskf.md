# Kalman, EKF, UKF et ESKF pour la fusion — cartes

Fiche : [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-FUSION-001

Objectif : distinguer variantes de filtre. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-FUSION-001
Question: Comment distinguer EKF, UKF et ESKF sans les classer en précision absolue ?
Reponse: **Noyau attendu** : l'EKF linéarise modèles et mesures autour de l'estimée courante. L'UKF propage $2n+1$ sigma-points choisis de façon déterministe à travers les fonctions non linéaires, sans jacobienne. L'ESKF intègre un état nominal non linéaire et estime une petite erreur autour de lui, avec les équations de prédiction et de correction d'un EKF appliquées à cette erreur. Ces noms décrivent donc des choix qui se combinent, pas trois catégories exclusives.

**Approfondissement** : selon Julier et Uhlmann, la transformée unscented calcule la moyenne avec un ordre de précision supérieur à l'EKF, mais la covariance au même ordre. Le résultat dépend du modèle, du bruit, de l'initialisation et de la cohérence temporelle ; une étiquette d'algorithme n'est pas un classement universel.

**Choix de conception** : commencer par la représentation de l'état, la non-linéarité des observations et le coût acceptable. Le filtre retenu doit être évalué sur des innovations et des erreurs de trajectoire cohérentes. Une meilleure approximation locale de propagation ne corrige pas une mauvaise extrinsèque, une association fausse ou une horloge décalée ; ces défauts appartiennent au modèle et aux données.

**Erreurs bloquantes** : dire qu'UKF est toujours meilleur ou qu'ESKF supprime la non-linéarité.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Fiche complète]] ; [Solà, §5.2, §6.1, équation 278, et annexe E, équations 439–440](https://arxiv.org/abs/1711.02508) ; [Julier et Uhlmann 1997, SPIE 3068, §3, équations 12–14](https://doi.org/10.1117/12.280797).
Tags: cv::pilote cv::d01 famille::comprehension cv_id::CV-FUSION-001 provenance::agent pole::B pole::C
END

## CV-FUSION-002

Objectif : interpréter une innovation normalisée. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FUSION-002
Question: Dans un filtre, $\nu$ désigne l’innovation mesure moins prédiction et $S$ sa covariance définie positive. Que mesure $\nu^TS^{-1}\nu$ dans un contrôle d’innovation ?
Reponse: **Noyau attendu** : c'est le carré de l'écart mesure/prédiction pondéré par son incertitude, une distance de Mahalanobis sans unité. Si le modèle, les bruits gaussiens et $S$ sont corrects, il suit une loi du $\chi^2$ à $m$ degrés de liberté, $m$ étant la dimension de la mesure. On rejette donc une mesure au-delà d'un quantile choisi, par exemple $\chi^2_{3;0{,}95}\approx7{,}81$.

**Approfondissement** : DeepSORT écarte ainsi les associations au-delà du quantile à 95 % pour une mesure de dimension 4, soit 9,4877. Le seuil dépend de $m$ et du risque accepté, pas des unités. Un rejet signale un écart entre prédiction, modèle stochastique et observation, sans dire lequel est en cause ; il ne prouve pas non plus l'identité du bon objet. Des valeurs trop souvent fortes ou faibles sur une séquence signalent un filtre sur- ou sous-confiant.

**Lecture du gating** : le test retire des associations trop incompatibles avec l'incertitude supposée. Il ne sélectionne pas forcément une association unique parmi les admissibles. Un filtre trop incertain peut accepter de nombreux candidats ; un filtre surconfiant peut rejeter la bonne mesure. L'affectation et la calibration statistique restent donc deux contrôles distincts.

**Erreurs bloquantes** : confondre grand résidu en pixels et grande incohérence statistique ; appliquer un même seuil quelle que soit la dimension de la mesure.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Fiche complète]] ; [Gamse et al. 2014, §2.2.2, équations 5–10, et §3.4.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/) ; [Wojke et al. 2017, DeepSORT, §2.2](https://arxiv.org/abs/1703.07402) ; quantiles recalculés par le projet.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-FUSION-002 provenance::agent pole::B pole::C
END

## CV-FUSION-003

Objectif : préserver la covariance ESKF. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FUSION-003
Question: Dans un ESKF caméra–IMU, juste après chaque correction, la covariance d'orientation tombe à presque zéro ; les mesures suivantes sont alors rejetées par le gating ou corrigent à peine l'état. Quelle erreur du reset rechercher en priorité, et quel traitement est correct ?
Reponse: **Noyau attendu** : chercher une remise à zéro de $P$ au moment où l'erreur moyenne est injectée puis remise à zéro. Le reset change seulement le point de référence de l'erreur, pas l'information disponible : on pose $\hat{\delta x}\leftarrow0$ mais $P\leftarrow GPG^T$, avec $G$ la jacobienne du reset.

**Approfondissement** : Dans la convention d’erreur angulaire locale de Solà, $R_{vrai}=R_{nom}\operatorname{Exp}(\delta\theta)$, $G$ vaut l’identité sauf sur le bloc d’orientation $G_\theta\approx I-[\hat{\delta\theta}/2]_\times$ au premier ordre. Prendre $G\approx I$ néglige cette petite correction de coordonnées, sans annuler $P$. Une convention d’erreur globale exige sa propre jacobienne. Pour départager d'un $R$ trop petit, regarder où chute $P$ : à l'instant du reset, c'est le reset ; pendant la mise à jour, c'est la pondération des mesures. Une covariance nulle déclare une connaissance parfaite fictive.

**Intuition géométrique** : après injection, la même incertitude est décrite autour d'un nouvel état nominal. Recentrer une distribution ne la rend pas ponctuelle. Tester séparément la correction et le reset sur une petite perturbation connue aide à localiser le défaut, en conservant toutes les corrélations entre orientation et autres variables.

**Erreurs bloquantes** : assimiler reset de représentation et disparition de l'incertitude.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Fiche complète]] ; [Solà, §6.3, équations 285–288](https://arxiv.org/abs/1711.02508) ; symptôme et test discriminant proposés par le projet.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-FUSION-003 provenance::agent pole::B pole::C
END

## CV-FUSION-004

Objectif : traiter temps et données manquantes. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-FUSION-004
Question: La caméra passe de 30 à 10 images/s avec une latence variable, tandis que l’IMU reste à 200 Hz. Quel contrat temporel la fusion doit-elle respecter ?
Reponse: **Noyau attendu** : propager état et covariance échantillon IMU par échantillon, avec le $\Delta t$ réel entre horodatages, car chaque terme de covariance en dépend. Appliquer chaque mesure caméra à son instant d’acquisition, pas de réception. Distinguer absence de mesure et mesure nulle.

**Approfondissement** : sur un pas $\Delta t$, Solà propage le terme dynamique par une exponentielle ; le bruit de mesure IMU y contribue en $\Delta t^2$, les marches aléatoires des biais en $\Delta t$. Un code qui propage une fois par image avec un $\Delta t$ figé, ou qui ignore des échantillons IMU perdus, prédit donc une mauvaise covariance. Une image en retard se traite par tampon d’états et re-propagation depuis son instant d’acquisition, ou se rejette explicitement. Vérifier horloges, délais et ordre de réception avant de retoucher le gain.

**Cas construit** : une image reçue tard peut correspondre à un état déjà dépassé par plusieurs intégrations IMU. La corriger comme si elle était actuelle mélange mouvement et délai. Conserver l'instant de capture permet d'envisager une correction au bon état puis une repropagation, avec une politique explicite pour les mesures trop anciennes.

**Erreurs bloquantes** : conserver implicitement un pas constant malgré des intervalles différents ; dater une image à sa réception.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Fiche complète]] ; [Solà, §5.4.2, équations 262–265, et annexe E, équations 438–440](https://arxiv.org/abs/1711.02508) ; contrat temporel et traitement des retards proposés par le projet.
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-FUSION-004 provenance::agent pole::B pole::C
END

## CV-FUSION-005

Objectif : justifier la formulation à état d'erreur. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FUSION-005
Question: Pour fusionner IMU et caméra avec une orientation représentée par un quaternion, pourquoi estimer une petite erreur autour d'un état nominal intégré, plutôt que l'état complet dans un EKF ?
Reponse: **Noyau attendu** : l'erreur d'orientation est minimale, trois paramètres pour trois degrés de liberté : on évite la redondance du quaternion et le risque de covariance singulière lié à sa contrainte de norme. L'erreur reste petite et proche de l'origine, loin des singularités de paramétrisation : la linéarisation reste valide, les produits du second ordre sont négligeables et les jacobiennes simples. Sa dynamique est lente, la dynamique rapide étant intégrée dans l'état nominal : les corrections peuvent arriver moins souvent que les prédictions IMU.

**Approfondissement** : l'état nominal intègre les mesures IMU sans bruit. Le filtre prédit la loi gaussienne de l'erreur, la corrige à l'arrivée d'une autre mesure, l'injecte dans l'état nominal puis la remet à zéro (CV-FUSION-003). L'ESKF ne supprime pas la non-linéarité du modèle de mesure : il borne la zone où l'on linéarise.

**Intuition pour le suivi** : l'état nominal porte le mouvement important, tandis que l'erreur décrit un voisinage local. La petite taille de l'erreur justifie une approximation locale seulement tant que l'estimation reste proche de la réalité. Une mauvaise initialisation ou une longue absence de mesure peut sortir de ce domaine ; conserver un quaternion normalisé n'établit pas à lui seul la cohérence du filtre.

**Erreurs bloquantes** : croire que l'ESKF supprime toute non-linéarité ; penser que le filtre estime directement l'état complet.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Fiche complète]] ; [Solà, Quaternion kinematics, §5.1 et §5.2](https://arxiv.org/abs/1711.02508).
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-FUSION-005 provenance::agent pole::B pole::C
END

## CV-FUSION-006

Objectif : stabiliser la mise à jour de covariance. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FUSION-006
Question: Après plusieurs milliers de mises à jour d'un filtre de Kalman, la factorisation de Cholesky de $P$ échoue ou une variance devient négative, alors que les modèles semblent corrects. Quelle cause d'implémentation vérifier, et quelle forme de mise à jour l’atténue ?
Reponse: **Noyau attendu** : la forme simple $P\leftarrow(I-KH)P$ n'est garantie ni symétrique ni définie positive en arithmétique finie : les arrondis s'accumulent. Préférer la forme de Joseph $P^+=(I-KH)P^-(I-KH)^T+KRK^T$. $P^-$ est la covariance avant correction, $H$ la jacobienne de mesure, $K$ le gain et $R$ la covariance du bruit de mesure. Si $P^-$ et $R$ sont symétriques semi-définies positives et les erreurs de mesure et de prédiction indépendantes, cette somme de termes quadratiques est semi-définie positive en arithmétique exacte. Elle atténue le risque numérique sans garantir la positivité stricte en précision finie. La soustraction $P^--KSK^T$, avec $S=HP^-H^T+R$, même théoriquement équivalente pour le gain optimal, reste sujette à la cancellation. Surveiller symétrie et plus petite valeur propre de $P$ au fil de l'exécution.

**Approfondissement** : Solà, qui note $V$ la covariance de mesure, donne la forme la plus simple et signale sa mauvaise stabilité numérique. Symétriser $(P+P^T)/2$ masque l'asymétrie sans corriger une valeur propre négative. Pour départager : une dérive progressive à modèles fixes désigne l'arithmétique ; un $Q$ ou un $R$ non défini positif, ou mal dimensionné, désigne la configuration.

**Erreurs bloquantes** : retoucher $Q$ ou $R$ pour masquer le problème sans regarder la forme de mise à jour ; supposer que $(I-KH)P$ reste toujours définie positive en précision finie.
Source: [[10-mathematiques-estimation/references/13-kalman-ekf-eskf|Fiche complète]] ; [Solà, Quaternion kinematics, §6.1, équations 274–276 et note 26](https://arxiv.org/abs/1711.02508) ; [Chin/JPL 2023, §III-A, équation 14](https://ipnpr.jpl.nasa.gov/progress_report/42-233/42-233A-orig.pdf) ; test discriminant proposé par le projet.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-FUSION-006 provenance::agent pole::B pole::C
END
