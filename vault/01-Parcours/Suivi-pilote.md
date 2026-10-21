# Suivi du pilote : preuves et limites

**Lot courant** : 52 fiches, 224 cartes, 14 thèmes et six pôles métiers. **Rédaction** : agent.
**Client de révision** : AnkiDroid, confirmé par l'apprenant le 2026-10-18.
Une absence de résultat signifie « non exécuté », jamais « réussi ».

## État du lot

| Dimension | État |
| --- | --- |
| Rédaction | 52 fiches et 52 ensembles de cartes présents ; 129 approfondissements ouverts |
| Revue documentaire | Auto-revue assistée par agents, consignée ci-dessous |
| Validation scientifique indépendante | Non effectuée |
| Contrôles de fichiers et calculs | Exécutés localement, voir preuves |
| Parseur officiel du plugin | Testé en simulant Obsidian/Anki |
| Export réel, historique et médias | Non testés |
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
| Création | 224 notes et 224 cartes, identités distinctes | Non exécuté |
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
| 2026-10-18 | CV-FUSION, révision 2 | CV-FUSION-001 | ESKF présenté à côté d’EKF sans expliciter leur recouvrement ; Solà §5.2 | Indiquer que la formulation ESKF emploie un EKF ; source UKF séparée, accès intégral non vérifié | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-FUSION, révision 2 | CV-FUSION-002 | Symboles non définis au recto et source NIS absente ; Gamse §2.2.2 | Définir innovation et covariance inversible ; source NIS dédiée | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-FACTEURS, révision 2 | CV-FACTEURS-001 à 003 ; fiche | Hypothèses du MAP quadratique omises et références génériques ; Kaess §2, Ceres Gauge Invariance | Facteurs gaussiens à covariances fixes ; références ciblées et scénario distingué | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
| 2026-10-18 | CV-ACQUISITION, révision 2 | CV-ACQUISITION-001 à 004 | Sources bruit/résolution utilisées aussi pour gamma, décimation et calcul de flou | Sources par affirmation ; modèle cinématique et checklist identifiés comme raisonnements du projet | Agent Codex, auto-revue (`revue-cartes`) | Voir [contrôles finaux](#validation-2026-10-21) | Non synchronisé |
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
