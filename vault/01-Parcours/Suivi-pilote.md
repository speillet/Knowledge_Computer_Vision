# Suivi du pilote : preuves et limites

**Lot courant** : 60 fiches, 282 cartes, 14 thèmes et six pôles métiers. **Rédaction** : agent.
**Client de révision** : AnkiDroid, confirmé par l'apprenant le 2026-10-18.
Une absence de résultat signifie « non exécuté », jamais « réussi ».

## État du lot

| Dimension | État |
| --- | --- |
| Rédaction | 60 fiches et 60 ensembles de cartes présents ; 119 approfondissements ouverts |
| Revue documentaire | Auto-revue assistée par agents, consignée ci-dessous |
| Validation scientifique indépendante | Non effectuée |
| Contrôles de fichiers et calculs | Exécutés localement, voir preuves |
| Parseur officiel du plugin | Testé en simulant Obsidian/Anki |
| Paquet `.apkg` et import moteur | 282 notes, 14 sous-decks, un SVG ; identités et historique conservés en collection jetable le 2026-10-24 |
| Import personnel et médias sur téléphone | Non testés |
| Rendu Obsidian et AnkiDroid | Non vérifié dans les applications |
| Rappel initial / différé et maîtrise | Non mesurés |

## Auto-revue documentaire du 2026-10-18

**Responsable** : agent Codex, avec recherches documentaires assistées par agents.
Ce travail n'est pas une revue indépendante réalisée par l'apprenant.
Les affirmations centrales suivantes ont été confrontées aux passages indiqués,
au-delà d'une simple liste bibliographique :

| Fiche et cartes affectées | Affirmation contrôlée | Passage primaire et résultat |
| --- | --- | --- |
| SIFT, CV-SIFT-001 à 007 | DoG, 128 composantes, orientation, ratio et limites | Lowe 2004 §§3–7 ; invariance recherchée distincte d'une garantie universelle |
| ORB, CV-ORB-001 à 006 | FAST/orientation/rBRIEF, norme selon WTA_K | Rublee §§3–4 ; OpenCV ORB 4.13 WTA_K ; Hamming2 n'est pas un carré |
| Homographie, CV-HOMOGRAPHIE-001 à 007 | Modèle, résidu, minimum et budget | Fischler/Bolles §II ; tutoriel/API OpenCV ; confiance nominale qualifiée |
| Zhang, CV-ZHANG-001 à 007 | Contraintes, minimum et dégénérescences | Zhang §§2–4 ; trois vues en général, deux avec skew nul imposé |
| SORT, CV-SORT-001 à 008 | État, unités, affectation, durée de vie | Bewley §3 ; code 2236dff L94/L154/L199 ; mémoire distincte de l'émission |
| NMS, CV-NMS-001 à 005 | Glouton, pénalités et coordonnées | Soft-NMS §4 ; code b8e69bd ; documentation NMS ; seuils distincts |
| IoU/AP, CV-IOU-AP-001 à 007 | AP101, ignore/crowd, catégories, maxDets | cocoeval.py 8c9bcc3 evaluateImg/accumulate/Params ; maskApi.c bbIou |

Chaque fiche et carte cite sa source. La divergence entre page COCO et code
Python sur le plafond de détections est exposée avec le contexte exact dans
la fiche. Les propositions de validation industrielle et scénarios inventés
sont des raisonnements du projet, pas des résultats de papiers.

**Limites** : aucune expérience image/vidéo ni calibration réelle exécutée.
Les petits calculs Python sont exécutés ; les appels OpenCV sont explicitement
illustratifs. Aucune performance matérielle ou mémorisation de l'apprenant
n'est démontrée par cette auto-revue.

## Preuves techniques locales du 2026-10-18

Environnement : macOS, Python 3.9.6, bibliothèque standard. Depuis le dépôt :

```sh
python3 scripts/check_vault.py
python3 -m unittest discover -s tests -v
python3 examples/pilot_math.py
```

Le contrôleur vérifie identités, parents, liens, champs, tags et rubriques.
Les tests exercent aussi doublons, orphelins, contrats invalides, frontière NMS
et résultats analytiques. Ils ne vérifient pas toute la prose.

Résultat après organisation par thématique : **25 tests réussis** ; contrôleur sans erreur sur 33 documents
Markdown, sept fiches et 47 cartes. Liens README/specs, JSON des gabarits et XML
du SVG également contrôlés. Les états applicatifs ci-dessous restent inchangés.

Résultats : IoU $2/3$ ; NMS indices `[0,2]` à 0,5 et `[0,1,2]` à 0,7 ;
RANSAC 72/9 essais ; Kalman scalaire 107,352941 px puis 102 px avec davantage
de bruit de mesure ; AP101 0,834983 pour TP/FP/TP et 0,504950 pour un seul TP
sur deux GT. Les variantes sont expliquées dans les fiches correspondantes.

Le `main.js` officiel Obsidian_to_Anki 3.6.0 a aussi été chargé dans JavaScriptCore,
avec classes Obsidian, chemins, cache de métadonnées et IDs existants simulés.
SHA256 de l'asset :
`dcca559c8001a041ff11a5def4c6f9096969514249d1938db78ec6a7ee55bfef`.

Sur les fichiers réels : **47 notes reconnues**, quatre champs ordonnés,
47 IDs uniques, deck/tags/critères conservés ; conversion de maths inline et
display, code et SVG. Après insertion simulée d'identités numériques :
**47 mises à jour et zéro ajout** à la relecture. Ce test ponctuel utilise un
harness temporaire ; ce n'est pas une CI ou une commande incluse dans le clone.
Le parseur officiel a été exécuté ; aucune requête à Anki n'a été envoyée.

Ce résultat ne prouve ni stockage du média, ni absence de doublons dans une
vraie collection, ni historique conservé, ni rendu sur Android.

## Reclassement par thématique — 2026-10-18

La demande de reprendre l'organisation de Knowledge_AI_Engineering est appliquée :
quatorze dossiers numérotés avec index ; cartes à la racine du thème, fiches
dans son sous-dossier `references/`. Les neuf sections sans fiche affichent
explicitement leur état à rédiger. Les sous-decks actifs contiennent 13 cartes
de matching, 14 de géométrie/calibration, 5 de détection, 8 de tracking et 7
d'évaluation.

Un snapshot local avant déplacement a été comparé aux fichiers après :
**47 questions, réponses, IDs pédagogiques, tags et identités de synchronisation
conservés**, après normalisation des chemins d'image. Les seules adaptations
des cartes portent sur les liens et le deck. Aucun commentaire d'identité Anki
n'était encore présent ; ce contrôle ne simule donc pas un historique réel.

Le vrai parseur 3.6.0 a été réexécuté sur les **33 fichiers Markdown du vault** :
sept fichiers de cartes reconnus, 47 notes et cinq decks cibles corrects ; aucun
bloc importé depuis un guide, un index ou une fiche complète. La seconde passe
avec IDs simulés donne encore 47 mises à jour et zéro ajout. Maths, code, SVG
et liens sont reconvertis. Les limites de simulation ci-dessus restent applicables.

## Environnement applicatif à renseigner

| Composant | Version / appareil réellement utilisé |
| --- | --- |
| Obsidian Desktop | À renseigner |
| Obsidian_to_Anki | À renseigner ; candidat documenté 3.6.0 |
| Anki Desktop / AnkiConnect | À renseigner |
| AnkiDroid / Android / appareil | À renseigner |
| Modèle / champs / gabarits | À vérifier avec le guide |

## Essais d'export à réaliser

| Essai | Attendu | Observation / date / responsable |
| --- | --- | --- |
| Installation et mapping | Modèle CV-Pilote, quatre champs, un gabarit | Non exécuté |
| Création | 282 notes et 282 cartes, identités distinctes | Non exécuté |
| Scan inchangé | Nombres et identités inchangés | Non exécuté |
| Mise à jour après révision | Même note et historique conservé | Non exécuté |
| Texte, listes, formules/matrice | Lisibles dans Obsidian, Anki, AnkiDroid | Non exécuté |
| Code ORB et SVG SORT | Lisibles, y compris hors connexion | Non exécuté |
| Tags de domaine et famille | Présents et recherchables | Non exécuté |
| Liens Obsidian / HTTPS | Comportement sur l'appareil consigné | Non exécuté |
| Copie d'une carte | Nouvel ID pédagogique et nouvelle identité Anki | Non exécuté |
| Déplacement / renommage | Identité, nombre et contenu documentés | Non exécuté |
| Suppression source / destination | Comportement observé sur note de test | Non exécuté |
| Modifications concurrentes | Résolution consignée sur note de test | Non exécuté |
| Média remplacé, cache et AnkiWeb | Nouvelle image visible après sync | Non exécuté |

## Échantillon pédagogique fixé avant résultats

Choix initial : couvrir les huit familles produites et les rendus du premier
lot. Il couvre matching, calibration, tracking et détection. L’extension ci-dessous
ajoute segmentation classique et recalage 3D avant tout résultat.
Les dates des deux sessions sont libres.

| Carte | Famille / intérêt | Session initiale : résultat, durée, date | Session différée : résultat, durée, date |
| --- | --- | --- | --- |
| CV-SIFT-001 | Compréhension | Non essayé | Non essayé |
| CV-SIFT-002 | Raisonnement / maths | Non essayé | Non essayé |
| CV-SIFT-007 | Évaluation | Non essayé | Non essayé |
| CV-ORB-003 | Pratique / code | Non essayé | Non essayé |
| CV-ORB-006 | Conception | Non essayé | Non essayé |
| CV-HOMOGRAPHIE-003 | Algorithme | Non essayé | Non essayé |
| CV-HOMOGRAPHIE-006 | Diagnostic | Non essayé | Non essayé |
| CV-ZHANG-002 | Raisonnement / matrice | Non essayé | Non essayé |
| CV-ZHANG-007 | Conception | Non essayé | Non essayé |
| CV-SORT-001 | Compréhension / image | Non essayé | Non essayé |
| CV-SORT-006 | Diagnostic / liste | Non essayé | Non essayé |
| CV-NMS-001 | Algorithme / calcul | Non essayé | Non essayé |
| CV-NMS-003 | Comparaison | Non essayé | Non essayé |
| CV-IOU-AP-004 | Raisonnement / protocole | Non essayé | Non essayé |
| CV-WATERSHED-001 | Algorithme / segmentation classique | Non essayé | Non essayé |
| CV-ICP-002 | Diagnostic / recalage 3D | Non essayé | Non essayé |
| CV-MATCH-APPRIS-001 | Comparaison / matching appris | Non essayé | Non essayé |

Pour chaque essai, noter noyau satisfait/manquant, erreur bloquante, ambiguïté,
indice révélant la réponse, surcharge et reformulation nécessaire. Garder les
échecs. Estimer ensuite la charge quotidienne avec les durées et le nombre de
révisions prévu, sans plafond imposé. Le rappel ne prouve pas le transfert.

## Suite et corrections

- Segmentation classique, matching appris et recalage global + ICP sont rédigés.
- Les [douze cas de transfert](Cas-transfert.md) disposent de corrigés et critères ;
  aucun n’a été essayé par l’apprenant.
- Les six familles disposent d’une baseline et d’une variation proposée ;
  seuls les petits calculs explicitement signalés ont été exécutés.
- Faire les essais applicatifs et les deux sessions, puis ajuster la rédaction.

Journal de correction : date, ID de fiche, cartes affectées, erreur/source,
correction, responsable, contrôles et statut d'export. Aucune correction
scientifique ne doit laisser une ancienne carte contradictoire active.

| Date | Fiche | Cartes affectées | Erreur et source | Correction | Responsable | Contrôles | Export |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-18 | CV-NMS, révision 2 | CV-NMS-004 | Seuil de score final attribué au §4 de Soft-NMS, alors que l'article le décrit au §5 ; IoU sans ses arguments dans la formule | Source §§4–5 et code b8e69bd ; formule $\operatorname{IoU}(M,b_i)$ avec $M$ défini | Agent Claude Code, auto-revue (`revue-cartes`) | Contrôleur, tests, inventaire comparé | Non synchronisé |
| 2026-10-18 | CV-NMS, révision 2 | Aucune | Divergence non consignée : article $\ge N_t$, Torchvision et code original $>$ (FR-036) | Divergence et cas d'égalité ajoutés à la fiche | Agent Claude Code, auto-revue (`revue-cartes`) | Contrôleur, tests | Non concerné |
| 2026-10-18 | CV-NMS, révision 2 | Aucune | Détection sans NMS affirmée sans source | Ajout de DETR (Carion et al. 2020, résumé) | Agent Claude Code, auto-revue (`revue-cartes`) | Contrôleur, tests | Non concerné |
| 2026-10-18 | CV-SVD, révision 2 | CV-SVD-001, 003, 004 | Eigen ne documente pas le blanchiment ni le rejet d’outliers ; Ceres, Covariance Estimation et Modeling, introductions | Sources dédiées ; diagnostic géométrique identifié comme déduction du projet | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-SVD, révision 2 | CV-SVD-003 | Inverse de covariance sans hypothèse d’inversibilité ; Ceres, Covariance Estimation, Introduction | Covariance définie positive ; distinction résidu blanchi et norme au carré | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-SE3, révision 2 | CV-SE3-001 à 004 | Référence quaternion trop large pour les poses rigides ; ambiguïté du mot orientation | Source SE(3) annexe D-A ; passages ciblés et orientation de base explicitée | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-24 | CV-SE3, révision 5 | CV-SE3-006 ; fiche | Matrice 3×3 composée avec poses homogènes 4×4 (FR-007) | Définir M pour les vecteurs 3D et M_h pour les poses homogènes ; dimensions et côtés de composition explicites | Agent Codex, auto-revue (`revue-cartes`) | Contrôleur, tests, inventaire ; rapport 2026-10-24 | Non synchronisé |
| 2026-10-18 | CV-FUSION, révision 2 | CV-FUSION-001 | ESKF présenté à côté d’EKF sans expliciter leur recouvrement ; Solà §5.2 | Indiquer que la formulation ESKF emploie un EKF ; source UKF séparée, accès intégral non vérifié | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-FUSION, révision 2 | CV-FUSION-002 | Symboles non définis au recto et source NIS absente ; Gamse §2.2.2 | Définir innovation et covariance inversible ; source NIS dédiée | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-24 | CV-FUSION, révision 5 | CV-FUSION-003, CV-FUSION-006 ; fiche | Soustraction de covariances présentée comme remède numérique et reset sans convention | Privilégier Joseph sous ses hypothèses, conserver surveillance ; reset local au premier ordre explicitement annoncé | Agent Codex, auto-revue (`revue-cartes`) | Contrôleur, tests, inventaire ; rapport 2026-10-24 | Non synchronisé |
| 2026-10-18 | CV-FACTEURS, révision 2 | CV-FACTEURS-001 à 003 ; fiche | Hypothèses du MAP quadratique omises et références génériques ; Kaess §2, Ceres Gauge Invariance | Facteurs gaussiens à covariances fixes ; références ciblées et scénario distingué | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-24 | CV-FACTEURS, révision 5 | CV-FACTEURS-003, CV-FACTEURS-005 ; fiche | Test de résidu post-ajustement assimilable à une innovation indépendante ; relinéarisation omise dans les cliques affectées | Présenter le seuil comme heuristique, contrôler corrélations et retrait de boucle ; inclure variables relinéarisées | Agent Codex, auto-revue (`revue-cartes`) | Contrôleur, tests, inventaire ; rapport 2026-10-24 | Non synchronisé |
| 2026-10-18 | CV-ACQUISITION, révision 2 | CV-ACQUISITION-001 à 004 | Sources bruit/résolution utilisées aussi pour gamma, décimation et calcul de flou | Sources par affirmation ; modèle cinématique et checklist identifiés comme raisonnements du projet | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-24 | CV-CORNERS, révision 1 | CV-CORNERS-001 à 005 | Lacune prioritaire, ajout demandé par l’apprenant | Fiche, cartes corrigibles, sources et protocole de variation | Agent Codex | Voir rapport des ajouts prioritaires | Non synchronisé |
| 2026-10-24 | CV-FAST-BRIEF, révision 1 | CV-FAST-BRIEF-001 à 005 | Lacune prioritaire, ajout demandé par l’apprenant | Fiche, cartes corrigibles, sources et protocole de variation | Agent Codex | Voir rapport des ajouts prioritaires | Non synchronisé |
| 2026-10-24 | CV-FLANN, révision 1 | CV-FLANN-001 à 004 | Lacune prioritaire, ajout demandé par l’apprenant | Fiche, cartes corrigibles, sources et protocole de variation | Agent Codex | Voir rapport des ajouts prioritaires | Non synchronisé |
| 2026-10-24 | CV-FISHEYE, révision 1 | CV-FISHEYE-001 à 005 | Lacune prioritaire, ajout demandé par l’apprenant | Fiche, cartes corrigibles, sources et protocole de variation | Agent Codex | Voir rapport des ajouts prioritaires | Non synchronisé |
| 2026-10-24 | CV-HANDEYE, révision 1 | CV-HANDEYE-001 à 005 | Lacune prioritaire, ajout demandé par l’apprenant | Fiche, cartes corrigibles, sources et protocole de variation | Agent Codex | Voir rapport des ajouts prioritaires | Non synchronisé |
| 2026-10-24 | CV-FARNEBACK, révision 1 | CV-FARNEBACK-001 à 005 | Lacune prioritaire, ajout demandé par l’apprenant | Fiche, cartes corrigibles, sources et protocole de variation | Agent Codex | Voir rapport des ajouts prioritaires | Non synchronisé |
| 2026-10-24 | CV-CORRELATION, révision 1 | CV-CORRELATION-001 à 005 | Lacune prioritaire, ajout demandé par l’apprenant | Fiche, cartes corrigibles, sources et protocole de variation | Agent Codex | Voir rapport des ajouts prioritaires | Non synchronisé |
| 2026-10-24 | CV-MEANSHIFT, révision 1 | CV-MEANSHIFT-001 à 004 | Lacune prioritaire, ajout demandé par l’apprenant | Fiche, cartes corrigibles, sources et protocole de variation | Agent Codex | Voir rapport des ajouts prioritaires | Non synchronisé |
| 2026-10-24 | CV-ACQUISITION, révision 5 | CV-ACQUISITION-002, CV-ACQUISITION-003 ; fiche | Comparaison de resize 2022 généralisée au présent ; symboles et unités SNR absents | Limiter l’observation à Parmar 2022 ; définir QE, photons, gain et variances, préciser modèle linéaire | Agent Codex, auto-revue (`revue-cartes`) | Contrôleur, tests, inventaire ; rapport 2026-10-24 | Non synchronisé |
| 2026-10-18 | CV-CAPTEURS, révision 2 | CV-CAPTEURS-002 à 004 | Forster/Basler ne soutiennent pas le Doppler radar et ne décrivent pas le cas LiDAR | Références TI/LOAM et attribution du calcul au projet | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-IMAGERIES, révision 2 | CV-IMAGERIES-001 à 003 | Source line-scan absente ; URL SpaceNet7 obsolète ; fuite géographique attribuée implicitement au dataset | Sources Basler/DICOM ciblées, lien SpaceNet actualisé et raisonnement du split distingué | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-FILTRES, révision 2 | CV-FILTRES-002, 003, 004 | Noyau 002 sans conversion explicite ; formule et pyramide insuffisamment sourcées | Sigma divisé par 255 ; source Tomasi–Manduchi et pyramides ; protocole PSNR identifié comme choix | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-CANNY-HOUGH, révision 2 | CV-CANNY-HOUGH-002 | Unité pixel exigée dans erreurs bloquantes mais absente du noyau ; OpenCV Hough | Coordonnées et unités intégrées au noyau ; sources ciblées | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-MORPHO, révision 2 | CV-MORPHO-001, 002 | Question d’effet géométrique répondue seulement par l’ordre ; connectivité absente du tutoriel cité | Effets et échelle au noyau ; source connectedComponents et masque à deux pixels explicite | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-SIFT, révision 3 | CV-SIFT-007 ; fiche | Scénario image qualifié d’analytique et références de comparaison trop larges | Baseline explicitement proposée ; passages d’évaluation Lowe/Rublee ciblés | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-ORB, révision 3 | CV-ORB-006 ; fiche | Référence d’évaluation n’incluant pas les benchmarks applicatifs §6 | Passages §§4.4, 5.3 et 6.1 précisés | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-MATCHING, révision 2 | CV-MATCHING-002 ; fiche | FAST/BRIEF/AKAZE non documentés par Harris et Shi–Tomasi | Sources dédiées OpenCV 4.13.0 | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-MATCHING, révision 2 | CV-MATCHING-003, 004 | Diagnostic et protocole attribués implicitement aux tutoriels | Passage FLANN ciblé et déductions du projet distinguées | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-MATCH-APPRIS, révision 2 | CV-MATCH-APPRIS-001 à 005 | Passages et date de documentation non précisés ; diagnostics confondus avec description de méthode | Références par carte et attribution des protocoles | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-ECC, révision 2 | Fiche ; CV-ECC-001 à 003 | Conditions de normalisation photométrique implicites ; diagnostics non attribués | Gain positif, support fixé et variance non nulle ; distinguer invariant du critère et convergence | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-HOMOGRAPHIE, révision 3 | CV-HOMOGRAPHIE-006 ; fiche | Baseline et cas de couverture insuffisamment distingués des preuves exécutées | Statut proposé et attribution du diagnostic explicités | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-ZHANG, révision 3 | CV-ZHANG-002, 003 ; fiche | La matrice intrinsèque et ses conventions sont au §2.1, les contraintes au §2.3 du rapport Zhang | Corriger les passages cités | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-EPIPOLAIRE, révision 2 | Fiche ; CV-EPIPOLAIRE-005 | API P3P confondue avec solvePnP/P3P ; solveP3P accepte trois points | Nommer les deux fonctions et leurs sorties | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-EPIPOLAIRE, révision 2 | CV-EPIPOLAIRE-004 | Sensibilité de profondeur attribuée à une simple référence API | Identifier la déduction géométrique | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-BA, révision 2 | Fiche | Symboles du coût et inversibilité des blocs Schur implicites ; Ceres équations 10–12 | Définir covariance/perte et conditions de résolution | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-BA, révision 2 | CV-BA-003, 004 | Page solveurs insuffisante pour jauge et surajustement | Source covariance/jauge et attribution du protocole | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-MULTICALIB, révision 2 | Fiche ; CV-MULTICALIB-001 | AX=XB sans repères effectivement définis ; OpenCV eye-in-hand | Définir G, C, X et les mouvements relatifs | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-MULTICALIB, révision 2 | CV-MULTICALIB-003 | calibrateHandEye ne documente pas la déformation des scans LiDAR | Source LOAM et attribution du cas | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-STEREO, révision 2 | Fiche ; CV-STEREO-001 | Z=fB/d et règle d≤0 sans préciser la convention rectifiée ; OpenCV stereoRectify/minDisparity | Définir disparité, points principaux et validité générale par Q/masque | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-STEREO, révision 2 | CV-STEREO-001 | Le noyau exigeait une seconde profondeur non demandée | Déplacer le cas 10 px en approfondissement | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-ICP, révision 2 | CV-ICP-001 à 005 | Liens release sans version observée | Consigner Open3D 0.19.0 ; calculs et diagnostics restent des déductions du projet | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-VIO, révision 2 | Fiche ; CV-VIO-001 à 005 | Symboles de préintégration partiellement définis et sources communes trop larges | Définir états/gravité/temps et passages par carte | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-BEV, révision 2 | Fiche ; CV-BEV-001 à 005 | PointNet++, LSS, BEVFusion et SDF non soutenus par la bibliographie commune ; passages trop larges | Sources propres aux méthodes et attribution des scénarios | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-REPRESENTATIONS, révision 2 | CV-REPRESENTATIONS-004 ; fiche | LoRA/adapters, MAE et HOG non soutenus par les références listées | Sources primaires dédiées ; distinguer principe et résultat de transfert | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-REPRESENTATIONS, révision 2 | CV-REPRESENTATIONS-001 | Tokens image et total avec token de classe confondus dans le recto | Préciser que le comptage exclut le token de classe | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-CLIP, révision 2 | CV-CLIP-001 à 004 ; fiche | Limites attribuées au §7 (Broader Impacts) au lieu du §6 ; formulation négative ambiguë de 001 | Section corrigée et phrase clarifiée | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-ANOMALIES, révision 2 | CV-ANOMALIES-001, 003, 004 ; fiche | Template et scénarios industriels attribués implicitement aux articles PatchCore/PaDiM | Distinguer baseline et cas construits des descriptions des méthodes | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-OCR, révision 2 | Fiche ; CV-OCR-001 à 003 | Source OCR-D décrit la formule classique mais utilise une CER normalisée différente dans ses benchmarks | Expliciter les deux conventions et N>0 ; cibler les sources | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-BIOMETRIE, révision 2 | CV-BIOMETRIE-001 ; fiche | FRTE 1:1 et ArcFace ne suffisent pas pour la tâche PAD | Source dédiée NISTIR 8491 | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-BIOMETRIE, révision 2 | CV-BIOMETRIE-002 | Table FRTE sans date ni passage | Définitions FMR/FNMR datées | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-DETECTEURS, révision 2 | CV-DETECTEURS-002 | Le seul YOLO original ne documente pas les différences entre générations. | Ajouter YOLOv3 §2.1 et YOLOX §2.1 comme contre-exemples concrets. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-DETECTEURS, révision 2 | CV-DETECTEURS-001, 003–005 | Sources identiques trop larges ; protocole propre au projet. | Cibler chaque mécanisme et attribuer les diagnostics/comparaisons au projet. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-OPENVOC, révision 2 | CV-OPENVOC-001–003 | Sources générales ne distinguant pas mécanisme et protocole métier proposé. | Cibler les sections et expliciter les raisonnements du projet. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-POSE3D, révision 2 | CV-POSE3D-001, 004 | Les sources de détection ne suffisent pas à la pose articulée ni aux symétries de pose objet. | Ajouter OpenPose et BOP, attribuer le cas cylindrique au projet. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-POSE3D, révision 2 | CV-POSE3D-002, 003 | Source de protocole non datée et références indifférenciées. | Cibler format nuScenes, distance au sol et NDS ; dater la consultation. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-SEGMENTATION, révision 2 | CV-SEGMENTATION-001 | Définition panoptique incomplète au noyau : partition sans recouvrement (§3). | Préciser cette propriété dans fiche et réponse sans changer l’objectif. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-SEGMENTATION, révision 2 | CV-SEGMENTATION-002–004 | Bibliographie d’architectures trop générale pour les limites de métriques. | Ajouter Reinke et al. ; distinguer arguments de contrat et protocole du projet. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-SAM, révision 2 | CV-SAM-001–003 | Sections de SAM 2 imprécises et provenance du protocole causal implicite. | Cibler les sections et attribuer la comparaison au projet. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-VIDEO, révision 2 | Fiche, CV-VIDEO-003 | ViViT et CoTracker3 cités sans source propre. | Ajouter les deux articles et cibler le protocole de fenêtres. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-VIDEO, révision 2 | CV-VIDEO-001, 002, 004 | Attribution imprécise de contre-exemples et diagnostics aux trois articles. | Distinguer résultats sourcés et raisonnements construits. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-SORT, révision 3 | CV-SORT-001 | Critère bloquant ambigu sur le rôle du détecteur. | Exprimer le contresens réellement interdit : attribuer la détection à SORT. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-SORT, révision 3 | CV-SORT-004 | « Liste vide » imprécise pour l’API épinglée : tableau 2D attendu. | Donner la forme (0, 5) et l’exemple officiel, dans fiche et carte. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-SORT, révision 3 | Fiche | Renvois périmés : DeepSORT/ByteTrack et métriques sont déjà rédigés. | Relier les fiches existantes, sans modifier les preuves datées. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-ASSOCIATION, révision 2 | CV-ASSOCIATION-001–004 | Sources communes trop générales, provenance des diagnostics implicite. | Cibler DeepSORT/ByteTrack ; attribuer les cas et rattacher l’effet détecteur à SORT. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-SOT, révision 2 | Fiche, CV-SOT-002 | SiamFC cité pour une dérive par mise à jour alors que son template reste fixe (§4). | Limiter l’affirmation aux variantes adaptatives, ajouter KCF et expliciter le contre-exemple SiamFC. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-SOT, révision 2 | CV-SOT-001 | La source SOT seule ne documente pas le cycle de vie MOT. | Ajouter le renvoi SORT §3. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-VLM, révision 2 | Fiche | Confusion possible entre optimisation à l’entraînement et décodage à l’inférence (LLaVA §4.2). | Séparer les deux opérations sans attribuer une maximisation universelle à toute génération. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-VLM, révision 2 | Fiche, CV-VLM-001–004 | Sources manquantes pour trois modèles nommés et sources de cartes trop larges. | Ajouter Florence-2/RT-2/π0, cibler les mécanismes, dater OpenVLA et attribuer les cas. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-DIFFUSION, révision 2 | Fiche | Le marginal q(x_t\|x_0) était appelé « une étape », sans définition de alpha-bar (DDPM eq. 4). | Nommer le marginal et définir le produit des facteurs de bruit. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-DIFFUSION, révision 2 | Fiche, CV-DIFFUSION-001–003 | VAE/GAN sans sources propres ; citations de cartes générales. | Ajouter sources originales, préciser les passages et attribuer le cas inspection au projet. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-RENDU3D, révision 2 | Fiche | La dépendance de la densité à la direction était ambiguë ; NeRF §3 la restreint à la position. | Distinguer densité et couleur directionnelle. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-RENDU3D, révision 2 | CV-RENDU3D-001–003 | Sources de pages générales ; provenance des diagnostics implicite. | Relier les sections du papier et attribuer les déductions au projet. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-IOU-AP, révision 3 | Fiche | Accord grammatical erroné, sans effet scientifique. | Corriger « une réimplémentation ». | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-METRIQUES-TEMPS, révision 2 | Fiche, CV-METRIQUES-TEMPS-004 | La formule RPE n’avait pas de source directe et T/vérité terrain n’étaient pas explicités. | Ajouter Sturm §VII et définir les deux trajectoires ; distinguer RE par sous-trajectoires. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-METRIQUES-TEMPS, révision 2 | CV-METRIQUES-TEMPS-001–005 | Sources communes trop générales pour des protocoles distincts. | Cibler HOTA, alignement et erreurs de trajectoire ; attribuer les diagnostics. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-FIABILITE, révision 2 | CV-FIABILITE-003, 005 | Sources initiales peu directes sur biais adaptatif et calibration hors distribution. | Ajouter Cawley–Talbot et Ovadia sans généraliser les performances à un nouveau capteur. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-FIABILITE, révision 2 | CV-FIABILITE-001, 002, 004 | Sources indifférenciées, calibration géométrique non référencée. | Cibler Roberts/Guo/Zhang et attribuer les cas au projet. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-METRIQUES-APPLIQUEES, révision 2 | CV-METRIQUES-APPLIQUEES-002 | Lien MVTec direct inaccessible pendant la revue. | Utiliser la même version v1 déposée sur arXiv ; conserver le protocole de référence. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-METRIQUES-APPLIQUEES, révision 2 | CV-METRIQUES-APPLIQUEES-001, 003, 004 | Sources de sommaires ou communes trop générales. | Relier les passages sur distances, vides et composantes de variation NIST. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-PIPELINE, révision 2 | Fiche, CV-PIPELINE-001–005 | Sources runtime latest non datées et distinction modèle de file/implémentation implicite. | Dater les consultations ; expliciter bilan analytique et protocoles proposés. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-QUANT, révision 2 | Fiche | Bornes du clip, arrondi et portée entière de la formule non explicités. | Définir bornes et zero-point entier, séparer FP8 et citer ONNX QuantizeLinear-21. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-QUANT, révision 2 | CV-QUANT-001–005 | Sources indifférenciées, fallback multi-runtime insuffisamment étayé. | Ajouter le mécanisme EP d’ONNX Runtime, dater et cibler les sources ; attribuer les protocoles. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-DEPLOIEMENT, révision 2 | CV-DEPLOIEMENT-001 | Sources initiales ne soutenant pas la formule d’Amdahl. | Expliciter modèle séquentiel et dérivation algébrique dans fiche/source. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-DEPLOIEMENT, révision 2 | Fiche, CV-DEPLOIEMENT-002, 004 | Matrice de support insuffisante pour sparsité, distillation et mécanisme thermique. | Ajouter passages versionnés sparsité/thermique et article de distillation. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-DEPLOIEMENT, révision 2 | CV-DEPLOIEMENT-003 | Lien résumé trop général. | Relier le PDF complet et attribuer l’adaptation de checklist au projet. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-VIDEO, révision 3 | CV-VIDEO-002 | Traçabilité externe omise lors de la précision du contre-exemple analytique. | Rétablir le contexte primaire CoTracker §3 en conservant explicitement la provenance du raisonnement. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-20 | CV-DEPLOIEMENT, révision 3 | CV-DEPLOIEMENT-001 ; fiche | La dérivation analytique ne renvoyait pas à la source du modèle d’Amdahl. | Ajouter l’article original (p. 483) ; maintenir l’attribution du calcul numérique au projet. | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 3 | CV-DETECTEURS-006 ; fiche | Enrichissement accepté : Assignation anchor-free absente ; FCOS §§3.1–3.2 | Ajouter sites admissibles, plage de distances et arbitrage par aire | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#enrichissement-des-mécanismes-de-détection--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 3 | CV-DETECTEURS-007 ; fiche | Enrichissement accepté : Encodage non exercé ; FCOS §3.1, équation 1 | Ajouter un calcul ltrb avec repère et unités | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#enrichissement-des-mécanismes-de-détection--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 3 | CV-DETECTEURS-008 ; fiche | Enrichissement accepté : Déséquilibre des négatifs non expliqué ; Focal Loss §§2–3 | Distinguer difficulté et pondération de classe | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#enrichissement-des-mécanismes-de-détection--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 3 | CV-DETECTEURS-009 ; fiche | Enrichissement accepté : Plateau sans recouvrement absent ; GIoU §3.1 | Expliquer le terme englobant et vérifier un cas numérique | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#enrichissement-des-mécanismes-de-détection--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 3 | CV-DETECTEURS-010 ; fiche | Enrichissement accepté : Features multiéchelles seulement citées ; FPN §3 | Expliquer la fusion descendante et latérale | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#enrichissement-des-mécanismes-de-détection--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 4 | CV-DETECTEURS-011 ; fiche | Enrichissement accepté : Décomposition des erreurs absente ; TIDE §2.2 | Ajouter trois cas classables et les six familles dans la fiche | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#enrichissement-du-diagnostic-de-détection--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 4 | CV-DETECTEURS-012 ; fiche | Enrichissement accepté : Qualité des annotations non interrogée ; TIDE §3.4, annexes D–E | Distinguer erreur modèle, omission et politique crowd/ignore | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#enrichissement-du-diagnostic-de-détection--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 4 | CV-DETECTEURS-004 ; fiche | Enrichissement accepté : Cas resize trop abstrait ; FPN §3 et Soft-NMS §4 | Conserver l’objectif ; chiffrer resize/padding et comparer couverture avant/après NMS | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#enrichissement-du-diagnostic-de-détection--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 4 | Fiche seulement | Enrichissement accepté : Variation de résolution insuffisamment reproductible ; protocole du projet | Définir baseline, facteur varié, prédiction, mesures, diagnostic et limites ; expérience non exécutée | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#enrichissement-du-diagnostic-de-détection--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-NMS, révision 4 | CV-NMS-003 | Complément demandé : Compromis multiclasse trop abstrait ; Torchvision 0.29 batched_nms | Comparer les sorties sur deux classes et distinguer coexistence légitime et labels exclusifs | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#cas-multiples-classes-et-tailles--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-NMS, révision 4 | CV-NMS-005 | Complément demandé : Instances de même classe non explicites ; Soft-NMS §§1 et 4 | Relier disparition à la couverture de chaque GT et distinguer suppression de doublon et perte de rappel | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#cas-multiples-classes-et-tailles--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-NMS, révision 4 | CV-NMS-006 ; fiche | Complément demandé : Inclusion et tailles différentes non exercées ; définition IoU, GIoU §3 | Ajouter le cas 100×100 / 20×20 : IoU 0,04, deux boîtes conservées | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#cas-multiples-classes-et-tailles--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 5 | CV-DETECTEURS-013 ; fiche | Complément demandé : Instances, classes et multi-étiquettes confondues dans les questions possibles ; YOLOv3 §2.2 | Ajouter un rappel distinct sur le contrat de sortie et la taxonomie | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#cas-multiples-classes-et-tailles--2026-10-21) | Non synchronisé |
| 2026-10-21 | CV-DETECTEURS, révision 5 | Fiche seulement | Complément demandé : Taille et rapport d’aspect insuffisamment illustrés ; définition IoU, GIoU §3 | Calculer l’effet d’une même translation de deux pixels sur petites, grandes et longues boîtes | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles](#cas-multiples-classes-et-tailles--2026-10-21) | Non synchronisé |
| 2026-10-23 | CV-SVD, révision 3 | CV-SVD-001 ; fiche | Famille raisonnement sans relation interrogée ; « petites valeurs singulières identifient les combinaisons » imprécis, ce sont les vecteurs singuliers droits ; Ceres, Covariance Estimation, Rank of the Jacobian | Relation $\delta\hat x=\sum_i(u_i^T\delta b/\sigma_i)v_i$ au noyau ; cas exécuté et exemple Ceres en approfondissement | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SVD, révision 3 | CV-SVD-002 ; fiche | Objectif « choisir QR ou équations normales » non entraîné : question et noyau limités à « pourquoi éviter » ; Eigen, Using normal equations ; Ceres, Linear Solvers | Question de décision ; cas où les équations normales restent défendables, dont le BA creux par Schur ; adresse Eigen redirigée remplacée | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SVD, révision 3 | CV-SVD-003 | Forme quadratique dite « cohérente avec les unités » alors qu'elle est sans dimension ; Ceres, Covariance Estimation, Introduction | Formulation corrigée | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SVD, révision 3 | CV-SVD-004 ; fiche | Famille diagnostic sans test discriminant ; recouvrement partiel avec CV-SVD-001 et CV-HOMOGRAPHIE-006 ; Chum, Werner et Matas 2005, résumé ; Hartley 1997, §4 | Contrôles qui départagent outliers résiduels et quasi-dégénérescence ; cas du plan dominant et rôle de l'avant-dernière valeur singulière | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SVD, révision 4 | CV-SVD-005 ; fiche | Enrichissement accepté : DLT absente du vault ; Zhang 1998, §3.2 et annexe A ; Hartley 1997, §§2.2–2.3 | Système $Lh=0$, contrainte de norme unité, vecteur singulier minimal, rang 2 pour $F$ | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SVD, révision 4 | CV-SVD-006 ; fiche | Enrichissement accepté : normalisation citée sans source ni mécanisme ; Hartley 1997, §§3–5 et 7.3.1 | Mécanisme, recette, dénormalisation, non-invariance ; variation contrôlée exécutée | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SVD, révision 4 | CV-SVD-007 ; fiche | Enrichissement accepté : aucun solveur non linéaire dans le vault ; Triggs et al. 2000, §§4.2–4.3 ; Ceres, Trust Region Methods | Gauss-Newton, amortissement LM, initialisation | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SVD, révision 4 | CV-SVD-008 ; fiche | Enrichissement accepté : estimation robuste annoncée par l'index sans carte ; Ceres, LossFunction ; Triggs et al. 2000, §3.3 | Quantité robustifiée, unité de l'échelle $a$, limites face aux outliers nombreux | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SVD, révision 4 | CV-SVD-009 ; fiche | Enrichissement accepté : incertitude annoncée par l'index sans carte, proposition du 2026-10-18 ; Ceres, Covariance Estimation ; Triggs et al. 2000, §3.1 | Conditions de $(J^TJ)^{-1}$, jauge, caractère asymptotique | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SVD, révision 4 | CV-SVD-003 ; CV-SVD-002 | Enrichissement accepté : exemple d'unités absent ; source scientifique absente pour QR et équations normales (FR-036) ; Triggs et al. 2000, §4.3 | Exemple chiffré m/mm ; Triggs ajouté aux sources | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SE3, révision 3 | CV-SE3-001 | Recto qui livre la réponse par substitution d'indices ; `p_a` hors math ; Solà et al., annexe D-A, équations 170–171 | Scénario de pose relative entre deux caméras SLAM ; formule de composition et variante monde→caméra | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SE3, révision 3 | CV-SE3-003 ; fiche | Question qui admet d'autres causes valides, comme une autre paramétrisation ; famille comparaison sans choix ; Solà et al., §§II-E–II-F, équation 139 | Conditions fixées au recto ; adjoint $\delta\theta_G=R\,\delta\theta_L$ et critère de choix | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SE3, révision 3 | CV-SE3-004 ; fiche | Question fermée qui suggère « non » ; aucun test discriminant ; Solà, Quaternion kinematics, §3.1 ; Eigen Quaternion ; SciPy from_quat | Scénario d'extrinsèque, test par point connu, exemples d'ordre Eigen et SciPy, double couverture | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SE3, révision 3 | Fiche seulement | Notation $\operatorname{Exp}([\delta\theta]_\times)$ qui mélange Exp et exp ; Solà et al., §II-E | $\operatorname{Exp}(\delta\theta)$ et distinction Exp/exp | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SE3, révision 4 | CV-SE3-005 ; fiche | Enrichissement accepté : aucune métrique d'erreur de rotation dans le vault ; Solà et al., annexe B ; REP 103 | Angle géodésique, pièges Euler et $q/-q$, variation contrôlée calculée | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-SE3, révision 4 | CV-SE3-006 ; fiche | Enrichissement accepté : conventions d'axes caméra absentes ; OpenCV 4.13.0 `calib3d.hpp` ; Khronos gluLookAt ; REP 103 | Axes OpenCV, OpenGL et ROS ; $\mathrm{diag}(1,-1,-1)$ et côté de composition | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-FUSION, révision 3 | CV-FUSION-001 ; fiche | Source UKF jamais lue (Julier et Uhlmann 2004) ; « ESKF utilise un EKF » plus fort que le texte de Solà ; Julier et Uhlmann 1997, §3 ; Solà, §6.1 et annexe E | Source UKF lue et citée par équation ; ESKF décrit comme appliquant prédiction et correction d'EKF à l'erreur ; nuance d'ordre de précision | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-FUSION, révision 3 | CV-FUSION-002 ; fiche | Noyau sans la loi du $\chi^2$ pourtant donnée par la source citée ; « sans unité lorsque les grandeurs sont cohérentes » imprécis ; Gamse et al. 2014, équations 7–10 | Loi du $\chi^2$ à $m$ degrés de liberté, quantile d'exemple, lien avec le gating de DeepSORT | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-FUSION, révision 3 | CV-FUSION-003 ; fiche | Famille diagnostic sans symptôme ; recto qui oriente la réponse ; Solà, §6.3, équations 285–288 | Symptôme de covariance effondrée, test discriminant, $G\approx I$ dans la plupart des implémentations | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-FUSION, révision 4 | CV-FUSION-005 ; fiche | Enrichissement accepté : le « pourquoi » de l'ESKF n'était pas interrogé ; Solà, §§5.1–5.2 | Quatre propriétés de l'état d'erreur et cycle injection/reset | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-FUSION, révision 4 | CV-FUSION-006 ; fiche | Enrichissement accepté : instabilité numérique de la mise à jour de $P$ absente ; Solà, §6.1, note 26 | Formes symétrique et de Joseph, symptômes et test discriminant | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-FUSION, révision 4 | CV-FUSION-004 ; fiche | Enrichissement accepté : contrat temporel générique ; Solà, §5.4.2, équations 262–265, annexe E, équation 440 | Dépendances en $\Delta t$, instant d'acquisition, retards ; objectif inchangé | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-FACTEURS, révision 3 | CV-FACTEURS-001 ; fiche | Question fermée dont la réponse « Non » se devine ; équivalence MAP gaussien–moindres carrés attribuée implicitement à GTSAM, qui ne la formule pas ; Kaess et al. 2012, §2 | Question ouverte sur ce que représente le graphe et ce qu'il reste à fournir ; équivalence sourcée par Kaess, QR creuse et ordre d'élimination | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-FACTEURS, révision 4 | CV-FACTEURS-002 ; fiche | Enrichissement accepté : dimension et traitement de la jauge absents ; Zhang, Gallego et Scaramuzza 2018 ; Ceres, Gauge Invariance | Jauge de dimension 6, 7 ou 4 selon les capteurs ; fixer, prior ou jauge libre | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-FACTEURS, révision 4 | CV-FACTEURS-003 ; CV-FACTEURS-004 ; fiche | Enrichissement accepté : aucun test chiffré de boucle ni back-end robuste ; Agarwal et al. 2013, §§II–IV | Test $\chi^2$ par facteur ; comparaison perte robuste, contraintes commutables, DCS et RRR | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-FACTEURS, révision 4 | CV-FACTEURS-005 ; fiche | Enrichissement accepté : « incrémental » cité sans mécanisme ; Kaess et al. 2012, §§3.3–4.2 | Partie affectée de l'arbre de Bayes, seuils $\beta$ et $\alpha$ | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-ACQUISITION, révision 3 | CV-ACQUISITION-003 ; fiche | Aliasing et convention de resize attribués au tutoriel OpenCV des pyramides, qui ne les traite pas ; Parmar et al. 2022, §§1–3.2 et 6.3 | Source dédiée ; préfiltre et différences entre bibliothèques en approfondissement | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |
| 2026-10-23 | CV-ACQUISITION, révision 4 | CV-ACQUISITION-002 ; fiche | Enrichissement accepté : comparaison gain/exposition qualitative et recto en « pourquoi » ; EMVA 1288, §2.6, équations 21–22, et §2.7 | Comparaison chiffrée du SNR, du flou et de la saturation ; objectif inchangé | Agent Claude Code, auto-revue (`revue-cartes`) | Voir [contrôles](#revue-sujet-par-sujet--2026-10-23) | Non synchronisé |

## Extension éditoriale et contrôles — 2026-10-18

À la demande de l’apprenant, 45 fiches et 177 cartes ont été ajoutées aux sept
sujets initiaux. Le total courant est de **52 fiches, 224 cartes et 14 thèmes**.
Les six pôles possèdent chacun un cas de conception et un cas de diagnostic,
avec réponse de référence et critères. Les 129 approfondissements ouverts
restent visibles dans l’inventaire ; cette couverture n’est pas une exhaustivité
des algorithmes ni une validation des compétences.

Contrôles exécutés : 34 tests unitaires réussis ; contrôleur sans erreur sur
125 documents Markdown, 52 fiches et 224 cartes ; catalogue reproductible avec
`python3 scripts/sync_catalog.py --check`. Les 47 IDs initiaux sont conservés.
Les modifications scientifiques de NMS figurent dans le journal de correction.
Les autres ajouts aux sujets initiaux portent sur les métadonnées de pôles et
les étiquettes ; aucun identifiant numérique Anki n’a été inventé.

Le parseur officiel 3.6.0, de même SHA256 que plus haut, a scanné les 125 fichiers :
224 notes et 224 IDs pédagogiques distincts, quatre champs, 14 sous-decks ;
224 mises à jour et zéro ajout à la seconde passe avec IDs numériques simulés.
La conversion a exercé 99 formules inline, deux formules display, un bloc de
code et une image SVG. Aucune requête à Anki n’a été envoyée. Le harness reste
un contrôle ponctuel externe au dépôt, pas une commande disponible au clonage.

`python3 examples/curriculum_math.py` donne : Otsu seuil 1 puis 21 après +20
sur les intensités, avec même partition ; projection (370,360) puis (165,150)
après resize/crop ; associations 1D [0,0,0] puis [0,1,2] selon l’initialisation ;
profondeur stéréo 10 puis 20 m ; huit flux à 30 Hz = 240 images/s ; gain d’Amdahl
1,05263. Ce sont des calculs contrôlés, pas une expérience sur images, un ICP
complet ni un benchmark de runtime.

La rédaction demeure `redige`, provenance `agent`. La recherche documentaire
et les limites sont détaillées dans la recherche de la spec. Export réel,
historique, rendu applicatif, rappel et revue scientifique indépendante
restent non validés.

| Date | Fiche / périmètre | Cartes affectées | Motif | Changement | Responsable | Contrôles | Export |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-18 | Sept fiches initiales, révision 2 | 47 cartes initiales | Navigation par pôles demandée | Métadonnées `poles`, tags `pole::`, prérequis explicites ; IDs conservés | Agent Codex | IDs comparés, contrôleur, tests, parseur | Non synchronisé |
| 2026-10-18 | 45 nouvelles fiches, révision 1 | 177 nouvelles cartes | Couvrir les 14 thèmes et six pôles, demande explicite | Références, réponses corrigibles, sources primaires et cas métiers | Agent Codex | Sources centrales consultées, contrôleur, tests, parseur | Non synchronisé |

## Validation 2026-10-21

Revue documentaire des 52 sujets et 224 cartes existants : 12 rapports du
18 octobre repris, puis 40 rapports du 20 octobre. Le bilan et les rapports
par sujet se trouvent dans `docs/revues/2026-10-20/00-bilan.md`. Aucun ajout,
suppression ou changement d’objectif ; IDs pédagogiques préservés. Aucun
identifiant numérique Anki présent dans ce lot. Statut `redige` conservé.

Contrôles exécutés le 20 octobre et vérifiés à la livraison du 21 octobre :
`python3 scripts/check_vault.py` sans erreur (125 Markdown, 52 fiches,
224 cartes) ; 34 tests unitaires réussis ; catalogue à jour (18 documents).
Les deux programmes `examples/pilot_math.py` et `examples/curriculum_math.py`
confirment les petits calculs documentés. `git diff --check` sans erreur.
Comparaison d'inventaire initiale sans différence, complétée à la livraison
par celle du commit de départ `e5b41f0` : aucun ID ni identité Anki modifié.
Les 52 rapports couvrent une fois chacun les 224 IDs ; liens locaux, tableaux,
objectifs et révisions contrôlés. Les preuves historiques du 18 octobre
restent inchangées.

Aucun export réel ni rendu Obsidian/AnkiDroid testé pendant cette revue.
Il s’agit d’une auto-revue documentaire, sans validation scientifique
indépendante ni mesure de maîtrise ou de charge de rappel.

## Enrichissement des mécanismes de détection — 2026-10-21

Ajout accepté de CV-DETECTEURS-006 à 010 : assignation et encodage FCOS,
Focal Loss, GIoU et FPN. Fiche en révision 3, statut `redige`. Le lot atteint
52 fiches et 229 cartes. Les cinq cartes antérieures du sujet sont intactes.
Rapport : `docs/revues/2026-10-21/82-detecteurs-apprentissage.md`.

Contrôles : `python3 scripts/check_vault.py` sans erreur (125 Markdown,
52 fiches, 229 cartes), 34 tests unitaires réussis, catalogue à jour
(`python3 scripts/sync_catalog.py --check`, 18 documents). Comparaison avec
l'inventaire des 224 cartes : seuls les cinq IDs acceptés sont ajoutés ; aucun
ID, objectif ni identité Anki existant modifié. Calculs temporaires en Python :
encodage/décodage FCOS, facteurs focaux 0,01 et 0,81, losses GIoU 6/5 puis 10/9.
Preuves datées antérieures conservées ; diff et caractères de contrôle vérifiés.

Auto-revue documentaire par Agent Codex (`revue-cartes`) ; pas d'export réel,
de rendu Obsidian/AnkiDroid, de benchmark ni de validation indépendante.
Les deux cartes de diagnostic acceptées sont traitées dans le passage suivant.

## Enrichissement du diagnostic de détection — 2026-10-21

Ajout accepté de CV-DETECTEURS-011 et 012 : décomposition des erreurs et qualité
des annotations. CV-DETECTEURS-004 conserve son objectif de diagnostic après
resize, avec un cas chiffré et des contrôles discriminants. Fiche en révision 4,
statut `redige` ; protocole de variation de résolution proposé, non exécuté.
Le lot atteint 52 fiches et 231 cartes, dont 12 sur ce sujet.
Rapport : `docs/revues/2026-10-21/82-detecteurs-diagnostic.md`.

Contrôles : `python3 scripts/check_vault.py` sans erreur (125 Markdown,
52 fiches, 231 cartes), 34 tests unitaires réussis, catalogue à jour
(`python3 scripts/sync_catalog.py --check`, 18 documents). Comparaisons des
inventaires : deux ajouts depuis le premier passage, sept depuis les 224 cartes
initiales ; aucun ID disparu, objectif ni identité Anki existant modifié.
Les autres cartes et les preuves datées des passages précédents sont conservées.

Calcul Python temporaire : resize de facteur 1/3, padding vertical de 140,
boîte (300,290,304,293), aller-retour exact. Dans le cas NMS, IoU = 5/11 entre
les candidates ; la boîte parfaite est supprimée à 0,4 par celle de score
supérieur, qui échoue au seuil d'évaluation 0,5 : rappel 1 puis 0. Diff, liens,
caractères et comptes courants vérifiés. Aucun résultat de détecteur entraîné.

Auto-revue documentaire par Agent Codex (`revue-cartes`). Export réel, rendu
Obsidian/AnkiDroid, maîtrise, charge de rappel et validation scientifique
indépendante non vérifiés. Les sept ajouts acceptés sont désormais rédigés.

## Cas multiples, classes et tailles — 2026-10-21

Complément demandé par l'apprenant : expliciter détections multiples,
multiclasse et boîtes de tailles différentes. Passage NMS : fiche en révision 4,
cartes 003 et 005 enrichies sans changement d'objectif, ajout de CV-NMS-006.
Passage détecteurs : fiche en révision 5, ajout de CV-DETECTEURS-013.
Le lot courant atteint 52 fiches et 233 cartes ; statut `redige` conservé.

Cas traités : doublons d'une instance, plusieurs instances de même classe,
objets de classes différentes qui se recouvrent, labels exclusifs ou multiples,
boîtes imbriquées, petites/grandes boîtes et rapports d'aspect allongés.
Les deux rapports sont `docs/revues/2026-10-21/81-nms-cas-multiples.md` et
`docs/revues/2026-10-21/82-detecteurs-classes-tailles.md`.

Contrôles : `python3 scripts/check_vault.py` OK (125 Markdown, 52 fiches,
233 cartes), 34 tests unitaires réussis ; catalogue à jour sur 18 documents.
L'inventaire comparé aux 231 cartes précédentes montre les deux ajouts attendus,
aucun ID disparu, objectif ou identité Anki existant modifié. Preuves datées,
liens locaux, tableaux, caractères et diff vérifiés.

Calculs Python temporaires avec fractions exactes : inclusion 20×20 dans
100×100, IoU = 1/25 = 0,04 ; translation de deux pixels sur 4×4, 40×40,
40×4 horizontalement puis verticalement : IoU = 1/3, 19/21, 19/21, 1/3.
Ces calculs et décisions NMS sur cas construits ne sont pas une mesure terrain.
Context7 indisponible : documentation officielle Torchvision 0.29 consultée
pour `batched_nms`, sans exécuter cette API.

Auto-revue par Agent Codex (`revue-cartes`), sans export réel, rendu
Obsidian/AnkiDroid, benchmark, validation indépendante ou mesure de maîtrise.

## Revue sujet par sujet — 2026-10-23

Passage `revue-cartes` demandé sur tout le vault, un sujet à la fois, avec
rapport par sujet dans `docs/revues/2026-10-23/`. Les corrections sont
appliquées ; les enrichissements sont soumis à l'accord de l'apprenant.

- CV-SVD, révision 3 : cartes 001 à 004 corrigées sans changement d'ID ni
  d'objectif. Révision 4 : ajouts acceptés CV-SVD-005 à 009 (DLT,
  normalisation de Hartley, Gauss-Newton/LM, perte robuste, covariance) et
  exemple chiffré de CV-SVD-003. Rapport :
  `docs/revues/2026-10-23/11-moindres-carres-svd.md`.
- CV-SE3, révision 3 : cartes 001, 003 et 004 corrigées sans changement
  d'ID ni d'objectif. Révision 4 : ajouts acceptés CV-SE3-005 (angle
  géodésique) et CV-SE3-006 (conventions d'axes caméra). Rapport :
  `docs/revues/2026-10-23/12-rotations-se3.md`.
- CV-FUSION, révision 3 : cartes 001 à 003 corrigées, dont la source UKF
  enfin lue et la loi du $\chi^2$ de l'innovation. Révision 4 : ajouts
  acceptés CV-FUSION-005 (pourquoi l'ESKF) et 006 (forme de Joseph),
  enrichissement de CV-FUSION-004. Rapport :
  `docs/revues/2026-10-23/13-kalman-ekf-eskf.md`.
- CV-FACTEURS, révision 3 : carte 001 corrigée (question fermée). Révision 4 :
  ajouts acceptés CV-FACTEURS-004 (fausses boucles) et 005 (iSAM2),
  enrichissement de 002 et 003. Rapport :
  `docs/revues/2026-10-23/14-graphes-facteurs.md`.
- CV-ACQUISITION, révision 3 : source de la carte 003 corrigée (aliasing de
  resize). Révision 4 : CV-ACQUISITION-002 réécrite en comparaison chiffrée
  gain/exposition. Rapport :
  `docs/revues/2026-10-23/21-exposition-bruit-echantillonnage.md`.

Passage arrêté à la demande de l'apprenant après CV-ACQUISITION : les
sujets suivants, à partir de CV-CAPTEURS, n'ont pas été revus. Les
enrichissements non retenus restent décrits dans les rapports.

Le lot courant passe de 233 à 244 cartes ; statut `redige` conservé.

Contrôles : `python3 scripts/check_vault.py` OK (125 Markdown, 52 fiches,
244 cartes), 34 tests unitaires réussis, catalogue régénéré puis à jour sur
18 documents ; inventaire comparé à l'état initial : seuls les IDs ajoutés
apparaissent, sans ID disparu ni identité Anki modifiée.

Calculs exécutés hors dépôt (Python 3.10.13, NumPy 2.2.6, SciPy 1.13.1) :

- SVD : sensibilité d'un problème à deux colonnes presque égales, exemple
  Ceres de jacobien presque singulier, DLT brute ou normalisée sur trois
  configurations de 200 tirages, blanchiment en mètres et millimètres ;
- SE(3) : centre caméra, angle géodésique et angles d'Euler près du blocage
  de cardan, double couverture, conversion OpenCV→OpenGL ;
- Kalman : quantiles du $\chi^2$ à 95 % pour $m=1$ à 4 ;
- acquisition : SNR EMVA selon le gain et le nombre d'électrons.

Cas construits, pas des mesures terrain. Context7 n'est pas disponible dans
cette session : documentations officielles consultées directement, ou fichiers
sources à un tag ou commit quand la page HTML refuse les accès automatisés
(OpenCV, REP 103). Hartley 1997 lu sur une copie hébergée par l'Université
de Crète, l'éditeur étant payant.

Auto-revue par Agent Claude Code (`revue-cartes`), sans export réel, rendu
Obsidian/AnkiDroid, validation indépendante ni mesure de maîtrise.

## Ajouts prioritaires — 2026-10-24

Les PR 13, 14, 15 et 16 ont été vérifiées, corrigées puis fusionnées dans cet
ordre. Leurs six nouvelles cartes portent le lot de 238 à 244 cartes. Les
rapports ciblés du 24 octobre conservent les limites de cette auto-revue.

À la demande de l’apprenant, huit sujets prioritaires ajoutent 38 cartes :
Harris/Shi–Tomasi, FAST/BRIEF, FLANN, fisheye, hand-eye, Farnebäck, MOSSE/KCF
et MeanShift/CamShift. Le total courant est **60 fiches et 282 cartes** dans
les 14 thèmes. Dix IDs APP sont reliés à des fiches au niveau opérationnel ;
119 entrées restent ouvertes, avec compétences/prérequis à préparer.
Ce lot ne ferme pas les variantes spécialisées ni les essais applicatifs.

Les calculs analytiques du lot ont été exécutés hors dépôt avec Python et la
bibliothèque standard : Harris −308,04 et 336 ; Hamming 2 ; coût construit
FLANN 2,1/0,3 s pour 100 requêtes puis 12/30 s pour 10 000 ; rayons à 60°
314,16 et 519,62 px ; déplacement Farnebäck idéal (2,−1) px ; vitesse image
(100,−50) px/s ; PSR 6 ; centroïde pondéré 13 px. Les coûts FLANN sont des
hypothèses numériques, sans mesure de performance réelle.

Sources et critères du lot : `docs/ajouts-prioritaires-2026-10-24.md` dans le dépôt.
Contrôles exécutés : 37 tests réussis, contrôleur OK sur 141 documents, catalogue
à jour. Le parseur officiel 3.6.0 (SHA256 identique au premier essai) a reconnu
282 notes et IDs uniques dans 14 sous-decks ; seconde passe avec IDs simulés :
282 mises à jour, zéro ajout. Maths, code et SVG convertis. Aucune requête à
Anki envoyée ; le harness reste temporaire et extérieur au dépôt. Ces résultats
ne prouvent ni export réel, ni historique, ni médias synchronisés, ni rendu AnkiDroid.


## Export direct du 2026-10-24 — collection jetable

Responsable : agent Codex. Sources du lot de départ : `84dc970` ; les scripts
et le skill d'export locaux restaient à publier. Aucun contenu pédagogique,
ID ou commentaire du plugin n'a été modifié pour cette livraison.

- Contrôleur : **141 Markdown, 60 fiches, 282 cartes**, résultat OK.
- Catalogue : 18 documents générés, aucun périmé.
- `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` :
  **48 tests réussis**, aucun ignoré avec genanki présent.
- Construction et relecture ZIP/SQLite : **282 notes, 14 sous-decks, un média**
  (`cv-sort-pipeline.svg`). La génération ne publie pas de release.
- Comparaison au paquet local sauvegardé du 2026-10-18, qui contenait 224 notes :
  **58 ajouts, 164 corrections de contenu/tags, aucun retrait**. Les 224 GUID et
  le modèle 1153189853 sont conservés. Ce paquet antérieur n'était pas une release
  GitHub ; aucune release n'était présente au moment de la vérification.
- Simulation avec Python 3.12, genanki 0.13.1 et moteur anki 26.9.3 : import puis
  réimport du même paquet, 282 notes/cartes et identités inchangées. Trois cartes
  (`CV-ACQUISITION-001` à `003`) sont révisées avec « Bien ». Une réponse est
  modifiée dans une copie du vault, réimportée, puis une autre réponse et le CSS
  sont modifiés et réimportés. Résultat **OK** : contenu et CSS appliqués, aucun
  doublon, IDs de notes conservés ; ID de carte, type, queue, échéance, intervalle,
  répétitions, échecs et nombre d'entrées du journal de révision inchangés.
- Un test de régression vérifie que la simulation refuse chacun des échecs
  de contenu, style, identité, historique ou absence de doublons. L'ancien script
  affichait certains échecs après changement de style sans retourner un échec.

Les contrôles ont utilisé uniquement des copies et une collection temporaire.
Ils ne vérifient ni le rendu Obsidian/AnkiDroid, ni le transfert sur téléphone,
ni les suppressions et conflits dans les applications. Ces essais et les sessions
de rappel restent ouverts. Les tests du plugin consignés auparavant appartiennent
à une autre chaîne d'identités ; ne pas importer les deux dans la même collection.
