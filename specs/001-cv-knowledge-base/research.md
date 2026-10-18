# Recherche : interopérabilité Obsidian et Anki

**Vérification documentaire** : 2026-10-18.
**Statut** : recherche de conception ; aucune installation ni synchronisation exécutée.

## Plugin correspondant probablement au souvenir

Le candidat probable est **Obsidian_to_Anki**, également présenté comme
« Obsidian to Anki », avec l'identifiant `obsidian-to-anki-plugin`.
Le manifeste du [projet officiel](https://github.com/ObsidianToAnki/Obsidian_to_Anki)
consulté indique la version 3.6.0 et une utilisation sur ordinateur.
Cela ne permet pas d'identifier avec certitude le plugin dont l'utilisateur se souvient.

Sa [fiche dans l'annuaire Obsidian](https://community.obsidian.md/plugins/obsidian-to-anki-plugin)
était accessible. En revanche, le JSON téléchargé du
[registre officiel](https://github.com/obsidianmd/obsidian-releases/blob/master/community-plugins.json)
ne contenait pas cet identifiant. Le motif de cette divergence n'a pas été établi.
La disponibilité dans le catalogue intégré doit être vérifiée avant adoption.

L'API GitHub, consultée le 2026-10-18, indique pour ce dépôt une dernière
release 3.6.0 publiée le 2024-01-24, un dernier commit le 2024-02-01 et
277 issues ouvertes ; le dépôt n'est pas archivé. Près de trois ans sans
release rendent nécessaire de vérifier la compatibilité avec les versions
courantes d'Obsidian, d'Anki et d'AnkiConnect, et justifient une solution de repli.

## Capacités documentées

| Besoin | Constat documentaire | Conséquence pour le pilote |
| --- | --- | --- |
| Plusieurs cartes dans un document | Plusieurs blocs de notes peuvent cohabiter dans un fichier | Compatible en principe avec plusieurs cartes liées à une fiche |
| Réponses développées | Champs multilignes, paragraphes et listes documentés | Vérifier une réponse longue et sa lisibilité |
| Équations | Maths inline et en bloc documentées | Vérifier symboles, matrices et conventions utilisées |
| Images locales | Liens Markdown et embeds Obsidian documentés | Vérifier résolution et transfert des médias vers Anki |
| Code | Inline et blocs documentés ; le test de la release 3.6.0 confirme une coloration avec CSS distante | Prévoir un style local et vérifier la lecture hors connexion sur AnkiDroid |
| Mise à jour | Identifiant ajouté à la source pour retrouver la note Anki | Préserver l'identifiant et tester l'absence de doublons |
| Communication | Anki Desktop ouvert et AnkiConnect requis | Vérifier l'environnement d'essai |

Sources primaires :

- [Format des champs](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Field-formatting).
- [Mathématiques](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Math-formatting).
- [Exemples de rendu, médias et code](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/test).
- [Mise à jour de notes](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Updating-existing-notes).

La documentation d'installation du projet demande notamment d'autoriser
`app://obsidian.md` dans AnkiConnect, puis de redémarrer Anki. Aucun réglage
des applications personnelles n'a été modifié pendant ce cadrage.

## Identités et source canonique

Le plugin peut ajouter un commentaire de la forme `<!--ID: …-->`. Cette identité
de synchronisation ne doit pas être recopiée dans une nouvelle note.
L'identifiant pédagogique stable et l'identité de synchronisation ont des rôles distincts.

Le modèle de note et les noms de champs réellement présents dans Anki doivent
être vérifiés : les libellés d'un exemple ne garantissent pas ceux d'une
installation localisée. Nombres de notes et de cartes générées sont deux
mesures distinctes.

Le comportement de suppression ou de conflit ne se déduit pas du fonctionnement
des mises à jour. Les modifications pédagogiques se font dans le vault ; les
exceptions et reprises seront documentées après observation du pilote.

## Alternative identifiée

[Yanki](https://github.com/kitschpatrol/yanki-obsidian) apparaît dans le registre
consulté et documente MathJax, médias et coloration du code. Il associe un fichier
Obsidian à une note Anki. Cette contrainte change l'organisation par rapport
à plusieurs blocs dans une même fiche ; Yanki reste une alternative à évaluer,
pas une décision adoptée implicitement.

Les exigences restent formulées par capacités pour permettre ce choix sans
réécrire les objectifs pédagogiques.

## Solution de repli : paquet `.apkg` généré

Une bibliothèque comme [genanki](https://github.com/kerrickstaley/genanki)
génère un paquet `.apkg` à importer dans Anki. Selon sa documentation, une note
importée avec le même GUID qu'une note existante remplace celle-ci si les
modèles ont les mêmes champs. Dériver le GUID de l'identifiant pédagogique
stable relierait donc directement la source et la note, sans AnkiConnect ni
commentaire d'identité dans le vault.

Cette option reste à éprouver : conservation de l'historique de révision après
réimportation, options de mise à jour de l'importateur d'Anki et transfert des
médias. Elle constitue un outil sur mesure, exclu de la phase actuelle ; elle
n'est envisagée qu'en cas d'échec du pilote avec un plugin.

## Client de révision

Le client confirmé pendant l'implémentation est **AnkiDroid sur Android**.
Formules, images et blocs de code doivent être vérifiés sur
ce client : un rendu correct sur ordinateur ne garantit pas celui d'un mobile.

## Utilisation de Context7

La recherche a appelé le MCP distant Context7 : `resolve-library-id`, puis
`query-docs` sur `/obsidiantoanki/obsidian_to_anki`. Les résultats ont été
corroborés dans les sources primaires ci-dessus.

Context7 a également été interrogé sur `/websites/opencv_4_13_0` pour le
matching et la calibration. Les fiches devront vérifier les détails dans les
références officielles : une synthèse de documentation ne suffit pas à garantir
les propriétés de toutes les variantes d'une API.

## Pilote d'export à réaliser pendant la conception

| Vérification | Résultat attendu | État |
| --- | --- | --- |
| Disponibilité et prérequis | Installation reproductible du candidat retenu, versions consignées | Non exécuté |
| Modèle et champs | Mapping documenté avec les noms réels | Non exécuté |
| Première création | Nombres de notes/cartes conformes au modèle, identités distinctes | Non exécuté |
| Export répété sans modification | Aucun doublon, nombres inchangés | Non exécuté |
| Modification d'un verso | Même note mise à jour, historique conservé à modèle inchangé | Non exécuté |
| Texte développé | Paragraphes et listes lisibles, sans troncature essentielle | Non exécuté |
| Formules | Maths inline, bloc et matrice lisibles | Non exécuté |
| Médias | Image locale visible dans Anki ; déplacement documenté | Non exécuté |
| Code | Indentation, caractères et retours à la ligne préservés | Non exécuté |
| Client de révision | Formules, image et code lisibles sur le client réellement utilisé | Non exécuté |
| Étiquettes | Domaine et famille présents comme étiquettes dans Anki | Non exécuté |
| Identifiants | Copie d'une nouvelle carte et déplacement d'une carte existante distingués | Non exécuté |
| Suppressions et conflits | Comportement documenté avant usage sur un vrai deck | Non exécuté |

Le test de conservation de l'historique nécessite une carte réellement révisée
dans le deck d'essai avant modification. La seule conservation d'un identifiant
ne constitue pas une preuve de conservation de l'historique.

La syntaxe de production reste conditionnée à ce pilote. Un contrat expérimental
et un guide sont maintenant fournis pour les sept sujets initiaux ; aucune
validation réelle d'export n'est déduite de leur présence.

## Décisions de conception du premier lot — 2026-10-18

**Décision** : tester Obsidian_to_Anki 3.6.0 sur les sept fichiers de cartes
du pilote, modèle `CV-Pilote` à quatre champs et une carte par note.
Ces fichiers sont désormais répartis dans cinq répertoires thématiques,
à la demande de l'utilisateur ; les autres thèmes restent à rédiger.
**Raison** : conserver plusieurs cartes par sujet, champs explicites et ID
pédagogique stable, sans dépendre du nom localisé du modèle Basic.
**Alternatives** : Yanki reste possible mais change l'organisation ; `.apkg`
reste une solution de repli, aucun exporteur sur mesure n'est ajouté.

**Décision** : poursuivre la préparation éditoriale sans installer Anki dans
les applications personnelles. **Raison** : Anki Desktop est absent ; le parseur
officiel peut être testé isolément mais ne simule pas une collection réelle.
**Alternative** : attendre les applications ; elle n'est pas nécessaire pour
rédiger le pilote autorisé. Les essais applicatifs restent ouverts.

Context7 : résolution d'OpenCV puis interrogation `/websites/opencv_4_13_0`
sur normes et matching ; résolution et interrogation du plugin effectuées dans
la recherche de format. Résultats confrontés aux API et au code officiels.

Le [contrat](contracts/obsidian-anki.md), le
[guide du vault](../../vault/01-Parcours/Guide-Anki.md) et le
[journal des preuves](../../vault/01-Parcours/Suivi-pilote.md) précisent
versions, contrôles effectués et limites. La coloration et le comportement des
wikilinks ont été corrigés à partir de l'exécution locale du convertisseur.

## Organisation par thème — demande du 2026-10-18

**Décision** : reprendre les répertoires numérotés par dizaine et le sommaire
central du [dépôt indiqué](https://github.com/speillet/Knowledge_AI_Engineering/tree/5fdbfe259e53d01361cf6337f6c494b4663db592).
Chaque thème contient ses cartes et un sous-dossier de références ; les IDs
pédagogiques restent inchangés, le deck cible suit le thème.
**Raison** : retrouver l'organisation déjà utilisée par l'apprenant et réviser
une thématique dans Anki. Les noms et domaines sont dans `vault_sections.json`.

Le réglage de scan à racine vide et le scan récursif ont été revérifiés via
Context7, puis dans `main.ts` et `src/settings.ts` de la release 3.6.0 : le
réglage vide sélectionne les fichiers Markdown du vault. Les gabarits et les
exemples de syntaxe restent hors vault, et le contrôleur refuse les marqueurs
de note dans les guides, index et références.

## Extension aux quatorze thèmes — 2026-10-18

La demande de couverture élargie autorise la rédaction de 45 sujets
supplémentaires. Les sept sujets et 47 cartes ci-dessus désignent le lot initial ;
le catalogue courant contient 52 fiches et 224 cartes. Il garde 129 sujets
à approfondir individuellement. Les trois recherches complémentaires ont
confronté les affirmations centrales à des sources primaires ; elles ne valent
ni relecture scientifique indépendante ni validation de toutes les phrases.

Context7 a été interrogé sur les API OpenCV 4.13 (calibration, géométrie,
seuils, watershed, flot), Open3D (recalage global/ICP) et TensorRT (quantification,
mesure et limites du support). Les résultats ont été confrontés aux pages
et articles officiels, cités dans les fiches. Les tutoriels OpenCV cités en
4.12 et les paramètres dépendant d’une version gardent leur version explicite.
La documentation TensorRT courante est évolutive ; aucun support matériel
ou gain INT8/FP8 universel n’en est déduit.

Passages centraux consultés, par famille :

| Famille | Source primaire et point contrôlé |
| --- | --- |
| Estimation | [Eigen, least squares](https://eigen.tuxfamily.org/dox/group__LeastSquares.html), conditionnement des équations normales ; [Solà](https://arxiv.org/abs/1711.02508), conventions d’erreur de rotation et reset ESKF |
| Géométrie | [OpenCV solvePnP](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html), minimum API et repères ; [Open3D ICP](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html), initialisation locale ; [Zhang/Scaramuzza](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf), jauges d’alignement VO/VIO |
| Matching et segmentation | [LightGlue](https://github.com/cvg/LightGlue), matches clairsemés ; [LoFTR](https://arxiv.org/abs/2104.00680), detector-free ; [SAM](https://arxiv.org/abs/2304.02643) et [SAM 2](https://arxiv.org/abs/2408.00714), prompts, mémoire et causalité |
| Détection et tracking | [DETR](https://arxiv.org/abs/2005.12872), affectation d’entraînement et prédiction en ensemble ; [ByteTrack](https://arxiv.org/abs/2110.06864), association des détections faibles ; [HOTA](https://arxiv.org/abs/2009.07736), agrégation par seuil |
| Représentations | [CLIP](https://arxiv.org/abs/2103.00020) et [SigLIP](https://arxiv.org/abs/2303.15343), objectifs et limites des scores ; [PatchCore](https://arxiv.org/abs/2106.08265), mémoire de patches et pondération du score |
| Imagerie et métriques | [DICOM C.7.6.2](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html), repères/espacement ; [Metrics Reloaded](https://doi.org/10.1038/s41592-023-02151-z), choix des métriques selon la tâche |
| Systèmes | [TensorRT, quantification](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/work-quantized-types.html), support conditionnel ; [GStreamer queue](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), sens des politiques leaky |

Les équations analytiques et scénarios construits sont distingués des résultats
des auteurs. Seuls `examples/pilot_math.py` et `examples/curriculum_math.py`
ont été exécutés : aucun entraînement, séquence de tracking, recalage 3D,
export réel ou benchmark GPU n’a été réalisé. Le journal consigne séparément
l’exécution du parseur officiel sur 224 notes et ses limites de simulation.
