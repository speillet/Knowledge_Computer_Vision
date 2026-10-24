---
name: paquet-anki
description: "Construit, vérifie et publie le paquet Anki CV-Pilote.apkg à partir des cartes du vault, puis guide son import dans AnkiDroid sur le téléphone. Utiliser dès que l'utilisateur veut exporter ses cartes vers Anki ou AnkiDroid, générer ou mettre à jour le paquet .apkg, récupérer ses flashcards sur son téléphone, publier une nouvelle version du deck ou savoir quelles cartes ont changé depuis la dernière version, même sans nommer ce skill. Ne pas l'utiliser pour corriger le contenu des cartes : c'est le rôle de revue-cartes."
---

# Paquet Anki pour AnkiDroid

Les cartes vivent dans le vault, au format `START/END`. Le téléphone ne lit
que des paquets Anki. Ce skill produit `CV-Pilote.apkg` avec
`scripts/build_apkg.py`, le vérifie, le publie en release GitHub si
l'utilisateur le demande, puis explique l'import dans AnkiDroid.

Le paquet remplace la chaîne Obsidian_to_Anki → AnkiConnect → Anki Desktop,
suspendue pour le pilote. Les deux chaînes ne doivent pas alimenter la même
collection : leurs identifiants de notes diffèrent et produiraient des doublons.

## Ce qui garantit les mises à jour

L'identifiant de note (GUID) est calculé à partir de l'ID pédagogique de la
carte (`CV-SIFT-003`). Réimporter un paquet plus récent met donc à jour la note
sur le téléphone sans la dupliquer si les notes du paquet sont plus récentes.
La simulation du 2026-10-24 (moteur
`anki` 26.9.3) montre aussi que l'historique de révision est conservé, y
compris après une modification du style. Quatre règles en découlent :

- ne jamais modifier l'ID d'une carte existante : ce serait une autre note,
  et l'ancienne resterait sur le téléphone ;
- ne pas changer `modelId`, le nom, les champs ou le nombre de gabarits dans
  `anki/model.json` ; tout changement de `anki/*.html` ou `style.css` passe
  d'abord par la simulation ;
- l'import n'efface jamais une note : une carte retirée du vault doit être
  supprimée à la main dans AnkiDroid ;
- le vault reste la source : une modification plus récente faite dans AnkiDroid
  peut bloquer la mise à jour conditionnelle ; résoudre le conflit dans le vault,
  puis reconstruire.

## 1. Vérifier l'état

```sh
git status --short
git branch --show-current
python3 scripts/check_vault.py
python3 -m unittest discover -s tests
```

Si le contrôle échoue, s'arrêter et le signaler : le générateur refuserait de
toute façon un vault invalide. Pour corriger des cartes, utiliser `revue-cartes`.

## 2. Construire et vérifier

```sh
uv run --no-project --with genanki==0.13.1 python scripts/build_apkg.py
```

La commande écrit `dist/CV-Pilote.apkg` et `dist/CV-Pilote-manifest.json`
(non versionnés), puis relit le paquet. Le résultat doit indiquer `OK`, autant
de notes que le contrôleur compte de cartes, 14 decks et les médias attendus.
Une erreur `ConversionError` cite l'ID de la carte et la syntaxe non prise en
charge : titre, tableau, citation ou `$` orphelin. Confronter l'erreur au
contrat `docs/export-apkg.md` : corriger le convertisseur s'il refuse une syntaxe
autorisée, et réserver `revue-cartes` aux défauts réels des cartes.

Pour savoir ce qui changera sur le téléphone, comparer avec la dernière release :

```sh
gh release download --pattern CV-Pilote-manifest.json --dir <tmp>
python3 scripts/build_apkg.py --comparer <tmp>/CV-Pilote-manifest.json
```

L'absence de release signifie une première publication. Lister les cartes
ajoutées, modifiées et **retirées** : ces dernières sont à supprimer à la main.

## 3. Simuler si nécessaire

La simulation est obligatoire si `scripts/build_apkg.py`, `anki/` ou la
version de genanki ont changé, et conseillée avant une première publication :

```sh
uv run --no-project --python 3.12 --with anki==26.9.3 --with genanki==0.13.1 \
  python scripts/simulate_anki_import.py
```

Elle construit et importe le paquet dans une collection jetable, le réimporte
sans changement, révise trois
cartes, modifie le contenu puis le style, et ré-importe. Elle échoue en cas de
doublon, de note recréée, de mise à jour non appliquée ou d'historique modifié.
Elle ne dit rien du rendu sur le téléphone.

## 4. Publier (sur demande, après confirmation)

Une release est publique, comme le dépôt. Les liens « Fiche » des cartes
pointent vers `main` : publier seulement depuis `main`, arbre propre et
synchronisé, pour que le contenu, les liens et le tag concordent.

1. Vérifier que `git branch --show-current` affiche `main`, que
   `git status --porcelain` est vide, et qu'après `git fetch`, `HEAD` est
   égal à `origin/main`. Reconstruire : le manifeste ne doit pas porter le
   suffixe `-modifie`.
2. Montrer à l'utilisateur le tag prévu, les comptes et les cartes ajoutées,
   modifiées ou retirées, et attendre sa confirmation explicite.
3. Publier :

   ```sh
   gh release create anki-AAAAMMJJ-HHMM dist/CV-Pilote.apkg dist/CV-Pilote-manifest.json \
     --target "$(git rev-parse HEAD)" --latest \
     --title "Paquet Anki AAAA-MM-JJ" --notes "<comptes ; ajoutées ; modifiées ; retirées>"
   ```

4. Vérifier le lien fixe, qui doit rediriger vers le nouveau fichier :
   `curl -sI https://github.com/speillet/Knowledge_Computer_Vision/releases/latest/download/CV-Pilote.apkg`.

## 5. Importer sur le téléphone

Donner ces étapes à l'utilisateur :

1. Si une release contenant le paquet existe, ouvrir sur Android
   <https://github.com/speillet/Knowledge_Computer_Vision/releases/latest/download/CV-Pilote.apkg>
   dans le navigateur ; le fichier se télécharge. Sans release, utiliser la
   copie locale décrite ci-dessous.
2. Ouvrir le fichier téléchargé et choisir AnkiDroid ; ou, dans AnkiDroid,
   menu **Importer**, puis le fichier. Garder les options par défaut :
   mise à jour si le paquet est plus récent.
3. Premier import : le deck `CV::Pilote` apparaît avec ses sous-decks par thème.
4. Mise à jour : même geste. Le moteur testé conserve les identités et
   l'historique ; confirmer ce comportement sur la version d'AnkiDroid utilisée.
5. Carte retirée : dans le navigateur d'AnkiDroid, chercher
   `tag:cv_id::<ID>` et supprimer la note.

Un dossier local suffit aussi : copier `dist/CV-Pilote.apkg` sur le téléphone
(câble, mail) et l'ouvrir avec AnkiDroid.

## 6. Rapporter

Indiquer :

- les commandes lancées et leurs résultats ;
- les comptes et les changements depuis la dernière release ;
- le lien de la release s'il y en a une ;
- ce qui reste à vérifier sur le téléphone : formules MathJax, image SVG,
  code, liens, puis ré-importation après révision.

Consigner dans `vault/01-Parcours/Suivi-pilote.md` une publication et chaque
essai réel sur le téléphone, avec date, version d'AnkiDroid et observation.
Ne jamais committer `dist/`.
