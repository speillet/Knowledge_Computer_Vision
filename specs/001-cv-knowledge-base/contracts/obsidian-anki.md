# Contrat expérimental Obsidian–Anki

**Version** : pilote 1, 2026-10-18. Ne généraliser qu'après les essais réels.

Le dossier `vault/` est la racine à ouvrir dans Obsidian. Les cartes sont classées
dans les répertoires thématiques définis par `scripts/vault_sections.json`,
avec leurs fiches complètes dans `references/` et un `00-index.md` par thème.
Un scan à racine vide couvre tous ces dossiers ; un dossier thématique permet
un essai restreint. Seuls les fichiers de cartes contiennent des blocs de notes.
Les exemples de syntaxe et gabarits restent hors vault. Le contrôleur vérifie
qu'aucun bloc de note n'est ajouté dans les guides ou références.
La configuration se fait dans l'application, sans embarquer
ses fichiers privés ou le code du plugin dans Git.

Le modèle Anki s'appelle exactement `CV-Pilote`, avec les champs `ID`,
`Question`, `Reponse`, `Source` dans cet ordre. Les trois gabarits se trouvent
dans `anki/`. Le champ `ID` n'apparaît pas sur le recto. La source canonique
reste le Markdown ; les réponses ne sont pas modifiées en parallèle dans Anki.

Chaque fichier de cartes définit un seul deck cible
`CV::Pilote::<répertoire-thématique>`, par exemple
`CV::Pilote::40-features-matching`. Les quatorze sous-decks regroupent
238 notes et 238 cartes. Le statut reste rédigé et l’export expérimental ;
les totaux et pôles se vérifient dans le catalogue généré.
Un bloc commence
par `START` sur une ligne seule, suivi du nom du modèle et de ses quatre champs ;
les noms de champs ne sont pas traduits. `Tags:` précède `END`.
Après synchronisation, le plugin peut ajouter son commentaire ID avant `END` :
le préserver. Ne jamais inventer un tel commentaire avant export.

Les cartes utilisent des wikilinks depuis la racine du vault vers leurs fiches
et des sources HTTPS consultables sur Android. Le lien de fiche
dans Anki dépend de la conversion du plugin et de la présence du vault sur
l'appareil : il est à tester, pas présenté comme une navigation mobile garantie.
La réponse contient le nécessaire à la révision sans ce lien.

Maths `$…$` et `$$…$$`, blocs de code sans dépendance de coloration, image locale
SVG originale. Le gabarit ne contient aucun script distant. Le convertisseur
du plugin peut ajouter une CSS distante de coloration ; le style local doit
maintenir la lisibilité hors connexion, ce qui reste à vérifier sur le client.
Le SVG fait partie du test de transfert des médias ; son affichage sur Android
ne peut pas être certifié par un contrôle statique.

Les suppressions, renommages et conflits restent expérimentaux : les exercer
sur des copies dédiées au test selon le guide, jamais les déduire de la mise à
jour d'un simple verso. L'adoption définitive du plugin est conditionnée aux essais.
