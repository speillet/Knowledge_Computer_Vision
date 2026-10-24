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

**Exemple de coût amorti** : avec 2 s de construction et 1 ms par requête, cent requêtes coûtent environ 2,1 s, tandis qu'une recherche exhaustive à 3 ms chacune coûte 0,3 s. Pour dix mille requêtes sur la même base, les coûts hypothétiques deviennent 12 s et 30 s. Les valeurs illustrent un calcul, sans constituer un benchmark FLANN.

**Interprétation** : le nombre réel de réutilisations de l'index et sa durée de validité décident de l'amortissement. Une base reconstruite à chaque image peut perdre cet avantage. Comparer également la qualité des voisins : diminuer le temps en acceptant un rappel insuffisant n'est pas un gain à objectif constant. Le choix dépend du volume, du matériel, des lots et du protocole.

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

**Contre-exemple de représentation** : deux octets qui ne diffèrent que par un bit de poids fort sont proches en Hamming mais éloignés comme nombres. Leur conversion en flottants conserve cet écart numérique ; elle ne reconstruit pas les tests binaires que la métrique doit comparer.

**Diagnostic proposé** : déterminer d'abord quelle représentation a effectivement été produite et quelle distance son constructeur attend. Tester ensuite quelques paires de descripteurs avec une référence exhaustive utilisant cette distance, puis comparer l'index envisagé. Une exception de type est un indice d'interface, pas une permission de changer le problème mathématique. Une configuration qui fonctionne pour ORB standard doit encore être réexaminée pour une variante à symboles différents ; le support annoncé par l'API et la qualité finale restent à vérifier.

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

**Exemple analytique** : si les vraies distances des deux voisins sont 10 et 11, le ratio vaut environ 0,91. Une recherche qui retrouve le premier mais manque le deuxième peut retourner 10 et 30, soit un ratio d'environ 0,33. Le meilleur candidat n'est pas devenu plus distinctif ; le concurrent pertinent a simplement disparu de la recherche.

**Contrôle proposé** : comparer les deux rangs sur le même ensemble de requêtes, puis mesurer l'effet sur les paires acceptées et les inliers. Conserver une convention cohérente si une API retourne des distances au carré : le seuil du ratio doit alors être adapté. Une approximation peut être utile, mais le budget se règle en mesurant son effet sur le raisonnement aval, pas seulement sur sa propre durée.

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

**Séparer trois mesures** : le rappel de voisins compare l'index à une recherche exacte dans un espace de descripteurs ; la précision des matches compare les paires à une vérité de correspondance ; le succès géométrique juge la transformation obtenue. Ces niveaux peuvent diverger sur des textures répétitives ou des régions mal réparties.

**Courbe de décision proposée** : pour plusieurs budgets, conserver base et requêtes puis reporter temps complet, mémoire, rappel des deux premiers voisins et erreurs du recalage final. Ajouter le coût d'entretien si la base évolue. Choisir une région de fonctionnement qui respecte les contraintes du produit, puis la vérifier sur un lot réservé. Ce résultat ne se résume pas à maximiser le rappel : une recherche exhaustive peut être inutilement chère, mais une approximation très rapide peut être insuffisante.

**Erreurs bloquantes** : Assimiler exactitude du voisin à validité physique de la correspondance.
Source: [[40-features-matching/references/48-flann|Fiche complète]] ; [Muja et Lowe 2009, §§2–3, recherche approchée et configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf).
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-FLANN-004 provenance::agent pole::B pole::E pole::F
END
