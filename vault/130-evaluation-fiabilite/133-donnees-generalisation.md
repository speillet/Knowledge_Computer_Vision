# Splits, annotations, calibration des scores et dérive — cartes

Fiche : [[130-evaluation-fiabilite/references/133-donnees-generalisation|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-FIABILITE-001

Objectif : choisir une unité de split. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-FIABILITE-001
Question: Pourquoi des frames voisines d’une même vidéo ne constituent-elles pas forcément un bon train/test indépendant ?
Reponse: **Noyau attendu** : Elles partagent scène, objets et conditions ; la séparation doit suivre le scénario de généralisation.

**Approfondissement** : Split par séquence/site/patient selon tâche, avec contrôle des crops et doublons.

**Erreurs bloquantes** : Assimiler deux noms de fichiers différents à deux observations indépendantes.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Fiche complète]] ; [Roberts et al., structured data cross-validation](https://doi.org/10.1111/ecog.02881) ; [Calibration of modern neural networks](https://proceedings.mlr.press/v70/guo17a.html) ; [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
Tags: cv::pilote cv::d13 famille::pratique cv_id::CV-FIABILITE-001 provenance::agent pole::A pole::C pole::D pole::E pole::F
END

## CV-FIABILITE-002

Objectif : distinguer deux calibrations. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-FIABILITE-002
Question: À ne pas confondre : calibration caméra et calibration des scores d’un détecteur ?
Reponse: **Noyau attendu** : La première estime géométrie/optique ; la seconde étudie l’accord entre scores et fréquences d’événements selon protocole.

**Approfondissement** : Aucune des deux n’est démontrée par une bonne accuracy seule ; préciser unité et objet du calibrage.

**Erreurs bloquantes** : Utiliser RMS de reprojection pour valider une probabilité de classe.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Fiche complète]] ; [Roberts et al., structured data cross-validation](https://doi.org/10.1111/ecog.02881) ; [Calibration of modern neural networks](https://proceedings.mlr.press/v70/guo17a.html) ; [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-FIABILITE-002 provenance::agent pole::A pole::C pole::D pole::E pole::F
END

## CV-FIABILITE-003

Objectif : garder un test non adaptatif. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-FIABILITE-003
Question: Pourquoi choisir les exemples d’active learning ne doit-il pas conduire à régler le test final au fil des échecs ?
Reponse: **Noyau attendu** : Le test doit rester une mesure indépendante du scénario choisi ; adapter sa sélection ou les seuils après résultats biaise la conclusion.

**Approfondissement** : Conserver validation pour l’itération et documenter le changement de périmètre si un nouveau test est nécessaire.

**Erreurs bloquantes** : Appeler performance finale le meilleur résultat d’itérations sur le même test.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Fiche complète]] ; [Roberts et al., structured data cross-validation](https://doi.org/10.1111/ecog.02881) ; [Calibration of modern neural networks](https://proceedings.mlr.press/v70/guo17a.html) ; [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-FIABILITE-003 provenance::agent pole::A pole::C pole::D pole::E pole::F
END

## CV-FIABILITE-004

Objectif : diagnostiquer une dérive saisonnière. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FIABILITE-004
Question: Cas E — diagnostic : un modèle de télédétection se dégrade entre saisons. Quelle analyse est discriminante ?
Reponse: **Noyau attendu** : Contrôler géoréférencement, résolution/bandes, labels et distribution ; comparer régions/dates séparées et stratifier erreurs par conditions.

**Approfondissement** : Tester une intervention ciblée sur validation puis un jeu temporel réservé. Ne pas attribuer toute saisonnalité au réseau sans vérifier acquisition et taxonomie.

**Erreurs bloquantes** : Mélanger les tuiles voisines des deux saisons pour faire disparaître l’écart du test.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Fiche complète]] ; [Roberts et al., structured data cross-validation](https://doi.org/10.1111/ecog.02881) ; [Calibration of modern neural networks](https://proceedings.mlr.press/v70/guo17a.html) ; [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-FIABILITE-004 provenance::agent pole::A pole::C pole::D pole::E pole::F cas_pole::E::diagnostic
END

## CV-FIABILITE-005

Objectif : éviter une certitude hors domaine. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FIABILITE-005
Question: Un détecteur garde des scores élevés sur un nouveau capteur mais se trompe davantage. Que conclure ?
Reponse: **Noyau attendu** : La confiance affichée n’est pas une preuve de calibration ou de fiabilité hors distribution.

**Approfondissement** : Évaluer erreurs, rejets et calibration sur acquisition représentative ; examiner le contrat d’entrée avant adaptation.

**Erreurs bloquantes** : Prendre le softmax pour une garantie de généralisation.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Fiche complète]] ; [Roberts et al., structured data cross-validation](https://doi.org/10.1111/ecog.02881) ; [Calibration of modern neural networks](https://proceedings.mlr.press/v70/guo17a.html) ; [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/).
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-FIABILITE-005 provenance::agent pole::A pole::C pole::D pole::E pole::F
END
