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
| Code | Inline et blocs documentés ; coloration non fournie par défaut | Exiger un code lisible sans promettre une coloration automatique |
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

Le client utilisé pour réviser (Anki Desktop, AnkiDroid ou AnkiMobile) n'est
pas encore précisé. Formules, images et blocs de code doivent être vérifiés sur
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

La syntaxe finale et les instructions d'installation seront rédigées après
ce pilote. Aucun marqueur propre à un plugin n'est imposé par cette spec.
