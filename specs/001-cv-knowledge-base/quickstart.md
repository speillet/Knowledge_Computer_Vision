# Valider le premier lot

Depuis la racine du dépôt :

```sh
python3 scripts/sync_catalog.py --check
python3 scripts/check_vault.py
python3 -m unittest discover -s tests -v
python3 examples/pilot_math.py
python3 examples/curriculum_math.py
```

Le contrôleur doit terminer sans erreur : liens locaux, identités, champs,
métadonnées et critères de correction. Les tests vérifient aussi des défauts
volontaires et des résultats numériques attendus ; ils ne prouvent pas la
justesse scientifique de chaque phrase ou la synchronisation.

Dans Obsidian, ouvrir `vault/`, puis `00-Accueil.md`. Lire une fiche et ouvrir
son fichier de cartes. Les formules doivent être lisibles, les liens résolus
et le schéma SORT visible. La procédure applicative et les gabarits sont
présentés dans [le guide Anki](../../vault/01-Parcours/Guide-Anki.md).

L'essai Anki se fait dans les cinq sous-decks thématiques de `CV::Pilote`,
avec le modèle `CV-Pilote`. Les directives des fichiers déterminent le sous-deck.
Vérifier nombre de notes **et** de cartes, répétition sans doublon, modification
d'une réponse après une révision réelle, identité et historique conservés.
Tester aussi déplacement/renommage, suppression et conflit sur une note d'essai.
Synchroniser via AnkiWeb, attendre les médias, puis contrôler sur AnkiDroid
les cartes de l'échantillon fixé dans [le journal](../../vault/01-Parcours/Suivi-pilote.md).

Consigner les versions réelles, les observations et les échecs. Aucune de ces
étapes applicatives n'est marquée réussie par la présence des fichiers.
