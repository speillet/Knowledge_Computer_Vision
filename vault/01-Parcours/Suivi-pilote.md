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
