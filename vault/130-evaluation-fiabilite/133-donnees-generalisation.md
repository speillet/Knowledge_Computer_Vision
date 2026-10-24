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

**Pourquoi les fichiers restent liés** : deux frames voisines contiennent souvent les mêmes objets, le même décor et presque la même acquisition. Un modèle peut retrouver ces indices dans le test sans avoir démontré sa généralisation vers une nouvelle scène. Des crops issus du même original peuvent renforcer encore cette proximité.

**Choix de protocole** : définir d'abord ce qui sera nouveau en exploitation, puis regrouper les données selon cette unité avant les dérivations et augmentations. Pour une nouvelle usine, séparer seulement les frames d'une séquence ne teste pas nécessairement le changement de site. Pour une autre tâche, une généralisation plus locale peut être pertinente. Contrôler doublons et recouvrements, conserver validation et test séparés, puis rapporter les groupes réellement évalués. Un split plus difficile n'est pas automatiquement meilleur ; il doit représenter le scénario annoncé sans lui transmettre indirectement des observations d'entraînement.

**Erreurs bloquantes** : Assimiler deux noms de fichiers différents à deux observations indépendantes.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Fiche complète]] ; [Roberts et al., résumé et recommandations de blocking](https://doi.org/10.1111/ecog.02881) ; application aux frames : raisonnement du projet.
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

**Exemples de quantités** : une focale et un point principal sont des paramètres géométriques en pixels. Un score de détection à 0,9 est une sortie numérique dont il faut étudier la relation aux événements corrects dans une population et un protocole définis. Ces objets n'utilisent ni les mêmes données de référence ni les mêmes critères d'erreur.

**Vérification proposée** : pour la caméra, tester projections et géométrie sur des observations réservées. Pour les scores, comparer décisions et références dans des groupes de score pertinents, en précisant classe, localisation et distribution. Une bonne accuracy peut coexister avec une mauvaise confiance, comme une faible erreur de reprojection peut coexister avec une mauvaise mesure physique. Employer le mot calibration sans son objet précis rend l'enquête ambiguë. Le parcours sépare donc modèle de formation d'image, score de reconnaissance et validation du produit, tout en explicitant leurs interactions.

**Erreurs bloquantes** : Utiliser RMS de reprojection pour valider une probabilité de classe.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Fiche complète]] ; [Guo et al., §2, équation 1 : calibration de confiance](https://proceedings.mlr.press/v70/guo17a.html) ; [Zhang, §2 : calibration géométrique](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf).
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

**Pourquoi la sélection biaise** : observer les échecs du test puis choisir prompts, seuils, données ou architecture pour les réduire utilise son information pour régler le système. Le meilleur score parmi ces essais peut surévaluer la généralisation, même si aucun gradient n'est calculé directement sur le test.

**Organisation proposée** : garder les cycles d'annotation et d'active learning dans un ensemble de travail avec validation dédiée. Préserver une évaluation indépendante du scénario futur, avec règles de collecte et d'annotation explicites. Si les retours terrain conduisent à un nouveau périmètre, créer et documenter un nouveau test plutôt que conserver l'étiquette final pour un ensemble devenu adaptatif. Les anciens résultats restent utiles comme historique. Le bon objectif n'est pas d'interdire l'analyse des erreurs, mais de distinguer le travail d'amélioration et la preuve finale, afin d'attribuer correctement le gain à la nouvelle version.

**Erreurs bloquantes** : Appeler performance finale le meilleur résultat d’itérations sur le même test.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Fiche complète]] ; [Cawley–Talbot, résumé/introduction : biais de sélection](https://www.jmlr.org/papers/v11/cawley10a.html) ; application au cycle d’annotation : raisonnement du projet.
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

**Décomposition proposée** : une saison peut changer lumière, végétation et distribution des classes ; elle peut aussi s'accompagner d'un autre capteur ou d'une autre politique d'annotation. Comparer des erreurs globales sans vérifier ces éléments mélange plusieurs hypothèses.

**Ablation construite** : aligner la géométrie et les bandes, examiner des zones communes contrôlées et des régions nouvelles, puis mesurer les erreurs par classe et condition. Vérifier un changement de prétraitement avant une adaptation du modèle. Si une intervention est choisie, la régler sur validation puis la tester sur des dates ou régions restées réservées. Mélanger des tuiles voisines pour augmenter artificiellement la ressemblance du test n'établit pas la généralisation saisonnière. La conclusion doit identifier ce que les observations départagent et laisser ouvertes les causes encore confondues.

**Erreurs bloquantes** : Mélanger les tuiles voisines des deux saisons pour faire disparaître l’écart du test.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Fiche complète]] ; Cas construit du projet ; [Roberts et al., séparation spatiale/temporelle](https://doi.org/10.1111/ecog.02881).
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

**Lecture de la confiance** : un score élevé peut être appris dans une distribution où certains indices étaient fiables, puis rester élevé lorsque ces indices changent de signification. La normalisation de la sortie ne détecte pas automatiquement ce décalage. Le nouveau capteur peut aussi rompre couleur, gamma, résolution ou plage d'intensité.

**Enquête proposée** : comparer une entrée identique à travers les deux chaînes et mesurer les erreurs sur un lot annoté représentatif du nouveau capteur. Examiner calibration et rejet au point d'exploitation, avec les mêmes règles de localisation. Une chute de qualité nécessite une action, mais le score seul ne dit pas s'il faut corriger le prétraitement, recollecter ou adapter le modèle. Conserver une validation indépendante pour vérifier la correction. Une surveillance des distributions peut donner une alarme utile ; elle ne démontre pas à elle seule une dérive de précision sans référence appropriée.

**Erreurs bloquantes** : Prendre le softmax pour une garantie de généralisation.
Source: [[130-evaluation-fiabilite/references/133-donnees-generalisation|Fiche complète]] ; [Ovadia et al., résumé et introduction : incertitude et calibration sous distribution shift](https://arxiv.org/abs/1906.02530).
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-FIABILITE-005 provenance::agent pole::A pole::C pole::D pole::E pole::F
END
