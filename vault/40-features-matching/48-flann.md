# FLANN — recherche approchée et contrat de distance — cartes

Fiche : [[40-features-matching/references/48-flann|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::40-features-matching

## CV-FLANN-001

Objectif : choisir recherche approchée ou exhaustive. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-FLANN-001
Question: Pourquoi un index FLANN peut-il être moins intéressant qu’une recherche exhaustive sur une petite base utilisée une seule fois ?
Reponse: **Noyau attendu** : Le coût de construction et la mémoire peuvent dépasser le gain sur les requêtes. Comparer $T_{construction}+N_qT_{requête}$ au coût exhaustif pour le nombre réel de requêtes, avec le même objectif de rappel.

**Approfondissement** : Les structures adaptées aux grands jeux ne garantissent pas un gain sur une petite base ni sur un matériel donné. Une comparaison doit inclure mises à jour de la base, transferts et traitement des lots.

**Erreurs bloquantes** : Comparer uniquement le temps de requête en excluant l’indexation.
Source: [[40-features-matching/references/48-flann|Fiche complète]] ; [Muja et Lowe 2009, §§2–3, recherche approchée et configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-FLANN-001 provenance::agent pole::B pole::E pole::F
END

## CV-FLANN-002

Objectif : préserver la métrique des descripteurs. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FLANN-002
Question: Un matcher FLANN configuré pour des vecteurs SIFT refuse les descripteurs ORB. Les convertir en float suffit-il à rendre le matching correct ?
Reponse: **Noyau attendu** : Non : le stockage ne définit pas la métrique. Les descripteurs binaires ORB usuels se comparent en Hamming ; convertir leurs octets en flottants pour L2 change le sens des distances. Choisir une recherche Hamming, par exemple BF ou une configuration LSH compatible.

**Approfondissement** : OpenCV 4.13 illustre kd-tree pour SIFT et LSH pour ORB. Pour ORB WTA_K=3 ou 4, vérifier le besoin de Hamming2 et le support réel du matcher ; LSH n’est pas une réponse universelle à toute variante.

**Erreurs bloquantes** : Traiter des octets codant plusieurs bits comme des coordonnées L2.
Source: [[40-features-matching/references/48-flann|Fiche complète]] ; [OpenCV 4.13, Feature Matching, BF et FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html).
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-FLANN-002 provenance::agent pole::B pole::E pole::F
END

## CV-FLANN-003

Objectif : évaluer une approximation de voisins. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FLANN-003
Question: Le ratio entre deux distances de matching devient plus favorable quand on réduit le budget FLANN. Est-ce une preuve de meilleurs matches ?
Reponse: **Noyau attendu** : Non : le second voisin peut avoir été manqué. Le ratio est alors artificiellement plus petit. Comparer les deux voisins à une recherche exacte sur un échantillon et mesurer la validation géométrique.

**Approfondissement** : Un bon recall@1 seul ne garantit pas un second voisin correct. Conserver la même convention de distance ou distance au carré pour appliquer un seuil de ratio. La confiance géométrique ne découle pas du seul ratio.

**Erreurs bloquantes** : Interpréter tout ratio plus petit comme un gain de précision.
Source: [[40-features-matching/references/48-flann|Fiche complète]] ; [Muja et Lowe 2009, §§2–3, recherche approchée et configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf).
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-FLANN-003 provenance::agent pole::B pole::E pole::F
END

## CV-FLANN-004

Objectif : mesurer la courbe temps rappel. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-FLANN-004
Question: Quelles mesures permettent de régler le budget d’une recherche approchée sans masquer une dégradation du pipeline ?
Reponse: **Noyau attendu** : Mesurer rappel des voisins par rapport à une baseline exacte, latence, mémoire, construction et nombre/qualité des inliers finaux. Faire varier un budget à la fois sur des données réservées.

**Approfondissement** : Le recall décrit la fidélité à la recherche exacte ; il n’est pas la précision sémantique des correspondances. Répétitions de texture et modèle géométrique erroné restent possibles même avec des voisins exacts.

**Erreurs bloquantes** : Assimiler exactitude du voisin à validité physique de la correspondance.
Source: [[40-features-matching/references/48-flann|Fiche complète]] ; [Muja et Lowe 2009, §§2–3, recherche approchée et configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf).
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-FLANN-004 provenance::agent pole::B pole::E pole::F
END
