# Export du pilote vers AnkiDroid

**Cible confirmée** : AnkiDroid sur Android. **Statut** : procédure préparée,
aucune synchronisation réelle encore exécutée. Le format est limité au pilote.

## Chaîne utilisée

Obsidian sur ordinateur → Obsidian_to_Anki → AnkiConnect dans Anki Desktop
→ AnkiWeb → AnkiDroid. Le plugin 3.6.0 est desktop uniquement ; il ne tourne
pas dans AnkiDroid. Les formules et réponses doivent rester utilisables sans
accéder à la fiche ou à Internet pendant le rappel.

Sources : [plugin officiel](https://github.com/ObsidianToAnki/Obsidian_to_Anki),
[synchronisation Anki](https://docs.ankiweb.net/manual/syncing),
[manuel AnkiDroid](https://docs.ankidroid.org/#_using_anki_desktop_with_ankidroid).

## Préparer un essai isolé

1. Ouvrir le dossier `vault/` comme vault Obsidian.
2. Préparer Anki Desktop et [AnkiConnect](https://ankiweb.net/shared/info/2055492159).
   Dans la configuration AnkiConnect, conserver les réglages nécessaires et
   autoriser `app://obsidian.md` dans `webCorsOriginList`, puis redémarrer Anki.
   Garder l'accès local : aucun port réseau n'est à ouvrir pour ce pilote.
3. Dans Anki, créer le deck parent `CV::Pilote` et un type de note **CV-Pilote**.
   Les directives des fichiers répartissent les cartes dans des sous-decks
   thématiques tels que `CV::Pilote::40-features-matching`.
   Partir d'un type simple à une seule carte. Créer/renommer et ordonner exactement
   les quatre champs **ID**, **Question**, **Reponse**, **Source**.
4. Garder un seul gabarit « Rappel ». Copier le contenu de `anki/front.html`,
   `anki/back.html` et `anki/style.css` du dépôt dans recto, verso et style.
   `anki/model.json` décrit ces correspondances ; ce fichier n'est pas un paquet
   importable dans Anki. Aucun script ne crée le modèle automatiquement.

Les comptes et la collection Anki restent ceux de l'apprenant. Pour un premier
AnkiWeb déjà rempli, suivre le manuel de synchronisation avant de choisir un
sens de transfert ; une collection locale vide ne doit pas écraser l'existante.

## Installer le candidat et limiter le scan

Le registre officiel consulté le 2026-10-18 ne liste pas ce plugin. Si cette
situation persiste dans l'application, l'installation manuelle documentée
utilise les assets `main.js`, `manifest.json`, `styles.css` de la
[release officielle 3.6.0](https://github.com/ObsidianToAnki/Obsidian_to_Anki/releases/tag/3.6.0),
dans `.obsidian/plugins/obsidian-to-anki-plugin/` du vault, puis l'activation
dans les plugins communautaires. Ces fichiers locaux ne sont pas versionnés ici.
Ne pas installer une copie de provenance inconnue pour contourner le catalogue.

Réglages du plugin, à confirmer dans la version réellement utilisée :

| Réglage | Valeur pour le pilote |
| --- | --- |
| Scan Directory | Vide pour scanner la racine du vault et ses sous-dossiers ; un seul dossier thématique pour un essai restreint |
| Scheduling Interval | `0`, lancement manuel |
| ID Comments | Activé |
| Regex personnalisée pour CV-Pilote | Vide ; blocs START/END ordinaires |
| Add Context / CurlyCloze / Add Obsidian Tags | Désactivés |
| Add File Link | Facultatif, champ **Source** si activé |

Seuls les fichiers de cartes thématiques contiennent des blocs de notes.
Les marqueurs présents dans des exemples Markdown peuvent aussi être reconnus
par le parseur : garder ces exemples et les gabarits hors du vault. Le contrôleur
refuse tout marqueur de début de bloc isolé dans un guide, index ou référence.
Sources : [format des notes](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Note-formatting),
[champs](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Field-formatting).

## Premier export et contrôle sur Android

1. Avec Anki Desktop ouvert, lancer manuellement le scan du vault pilote.
   Le nombre courant est donné par le catalogue et le contrôleur ; chaque note
   doit produire une carte. Le lot actuel comporte **244 notes et 244 cartes**,
   réparties dans les 14 sous-decks thématiques.
   Vérifier ces deux nombres dans le navigateur,
   pas le compteur quotidien du deck, qui dépend des limites de révision.
2. Vérifier que les commentaires d'identité ajoutés par le plugin sont uniques,
   puis relancer sans modification : les deux nombres doivent rester identiques.
3. Réviser une carte, noter son identité et son historique, modifier son verso
   dans le vault, puis relancer. La même note et le même historique doivent rester.
4. Synchroniser Desktop avec AnkiWeb, puis AnkiDroid avec le même compte.
   Attendre aussi la synchronisation des médias. Vérifier les cartes de
   [l'échantillon fixé](Suivi-pilote.md), puis leur lecture hors connexion.

Vérifier textes développés, listes, formules inline/en bloc et matrice,
indentation du code, image SORT, mode sombre et défilement des équations longues.
Le modèle fournit un style local de base ; le convertisseur 3.6.0 peut ajouter
une feuille CSS distante pour la coloration. La lisibilité hors connexion
doit donc être testée même si la coloration semble correcte en ligne.

Les wikilinks de fiche sont convertis en liens Obsidian. Ils n'ouvrent une fiche
sur Android que si le vault et le nom attendu y existent. Tester ce lien
séparément ; les cartes contiennent leur réponse complète et des sources HTTPS.
La mise en place d'une synchronisation du vault lui-même n'est pas comprise ici.

## Identités, médias et corrections

L'ID pédagogique `CV-…-…` est stable, présent dans un champ et un tag. Le
commentaire numérique du plugin identifie une note Anki ; ne pas le recopier
dans une nouvelle carte. Pour une copie pédagogique, changer l'ID et son tag,
puis retirer uniquement l'identité Anki de la nouvelle note.

Les médias sont exportés par **nom de fichier** : ne pas réutiliser le même
basename pour deux images différentes. Si une image modifiée sous le même nom
n'est pas transférée, vérifier le cache média du plugin avant de conclure à un
problème AnkiWeb ; consigner la manipulation dans le journal.

Une correction scientifique commence dans la fiche et toutes ses cartes,
retrouvables par ID, liens et recherche. Préserver les identités lors d'une
simple correction ; refaire les contrôles et remettre le contenu à relire.

Sources : [mises à jour](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Updating-existing-notes),
[images](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Image-formatting),
[MathJax AnkiDroid](https://docs.ankidroid.org/#_mathjax_support).

## Suppressions et conflits : test obligatoire avant extension

Sur une **note de test distincte**, essayer séparément déplacement/renommage
du fichier en conservant l'identité, suppression côté source, suppression côté
Anki et modifications concurrentes. Relever nombres, identité et contenu après
chaque opération ; ne pas supposer qu'effacer le Markdown efface la note Anki.

La règle de travail proposée est : contenu pédagogique canonique dans le vault,
résolution manuelle des conflits dans le deck d'essai. Le comportement réel
de suppression reste à observer. Arrêter l'extension du format si doublons,
historique perdu ou rendu essentiel illisible ; corriger le pilote ou réévaluer
le candidat avant de produire davantage de cartes.
