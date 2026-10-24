# Contribuer

## Changements

Travailler sur une branche dédiée, par exemple `docs/camera-calibration` ou
`chore/development-workflow`. Garder une intention par commit et des PR assez
petites pour être relues avec leurs sources et leurs preuves de validation.

Pour un changement structurant, rédiger les critères d'acceptation avant
l'implémentation. Spec Kit et les skills de Matt Pocock sont décrits dans
[l'audit des outils](docs/tooling-audit.md).

## Commits

Suivre [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
avec une description courte, précise et à l'impératif, en anglais :

```text
docs(calibration): explain reprojection error
fix(anki): preserve note ids during updates
chore(tooling): configure specification workflow
```

Utiliser `docs` pour le contenu pédagogique, `feat` pour une nouvelle capacité,
`fix` pour un défaut, `test` pour les tests, `ci` pour l'intégration continue et
`chore` pour l'outillage. Le scope est facultatif. Signaler les changements
incompatibles avec `!` ou un pied de message `BREAKING CHANGE:`.

Avant de committer, inspecter `git status`, le diff et les fichiers indexés.
Ajouter les fichiers par chemin et vérifier `git diff --cached --check`.
Le skill `$git-commit` aide à préparer le message et le regroupement des fichiers.

Vérifier l'identité d'auteur existante avant de committer avec
`git var GIT_AUTHOR_IDENT`. Respecter la configuration de l'utilisateur. Une
identité ponctuelle déjà vérifiée peut être fournie sans modifier ses réglages.
Pour configurer ensuite l'identité habituelle de ce dépôt :

```sh
git config --local user.name "Votre nom"
git config --local user.email "votre-adresse-de-commit"
```

## Pull requests

Le titre de PR suit la même convention que les commits :
`<type>[optional scope]: <description>`, par exemple
`docs(specs): define the computer vision learning requirements`.
Il peut ainsi servir de message lors d'une fusion par squash, après relecture.

Utiliser le modèle du dépôt : résumé du changement, preuve de validation et
impact de la fusion. Mentionner la spec ou l'issue quand elle existe.
Le skill `$pr` aide à rédiger cette description ; `$code-review` compare le
changement aux conventions et à la spec. Lui fournir une référence de départ
résolvable, par exemple `origin/main`.

Pour une carte, vérifier la justesse scientifique, les hypothèses, la cohérence
des notations, les sources et la compréhension de la question hors contexte.
Pour un changement de format, vérifier également l'export dans un deck d'essai.

Pour un changement pédagogique, lancer `python3 scripts/learning_path.py` :
chaque fiche apparaît une fois dans le parcours, après ses prérequis, et chaque
réponse atteint le seuil éditorial de développement. Relire aussi le mécanisme,
l'exemple et les limites : la longueur ne garantit pas la pertinence. Ajouter
un sujet dans `scripts/learning_path.json`, puis régénérer le catalogue avec
`python3 scripts/sync_catalog.py` ; ne pas modifier le parcours généré à la main.

Les skills `$gh-address-comments` et `$gh-fix-ci` accompagnent respectivement
les retours de revue et le diagnostic des checks GitHub Actions.
Les conventions ci-dessus ne sont pas encore imposées par des hooks ou une CI.
