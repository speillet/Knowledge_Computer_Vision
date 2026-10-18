# Instructions pour les agents

## Objectif

Ce dépôt prépare un vault Obsidian de connaissances et de flashcards de computer
vision, destiné à une progression vers un niveau d'ingénieur senior.

- Préserver la profondeur descriptive demandée : problème, intuition,
  formulation, hypothèses, compromis, limites et applications.
- Donner à chaque question un objectif de rappel explicite et une réponse
  évaluable. Une réponse développée est bienvenue lorsqu'elle sert cet objectif.
- Distinguer les faits sourcés des hypothèses et des décisions du projet.
- Ne pas annoncer une couverture exhaustive sans cartographie du programme
  et vérification des lacunes.
- Choisir et valider le plugin d'export avant de généraliser une syntaxe Anki.
  Préserver les identifiants de synchronisation lorsqu'il en génère.

## Workflow

Lire `CONTRIBUTING.md` avant de préparer un commit ou une PR.

Pour une décision structurante, clarifier le besoin avant d'implémenter.
Les skills de Matt Pocock sont installés au niveau utilisateur ; l'intégration
Spec Kit est locale au dépôt. Voir `docs/tooling-audit.md` pour leur état réel.

La constitution `.specify/memory/constitution.md` est encore le modèle fourni
par Spec Kit. Ne pas traiter ses exemples et placeholders comme des décisions
ratifiées. La remplir lors du cadrage du projet.

La configuration du tracker des skills de Matt Pocock n'est pas encore choisie.
Utiliser `$setup-matt-pocock-skills` avant le premier `$to-spec` pour fixer cette
destination. Cette préparation n'autorise aucune publication d'issue ou de PR.

## Organisation du vault

Classer les cartes par thématique, selon `scripts/vault_sections.json` :
un répertoire numéroté par domaine, un index `00-index.md`, les fichiers de
cartes directement dans le thème et leurs fiches canoniques dans `references/`.
Les conventions détaillées sont dans `docs/vault-layout.md`.
Préserver IDs pédagogiques et identités Anki lors des déplacements ; adapter
liens, médias, deck cible et preuves de validation. Un répertoire vide de contenu
reste à rédiger : sa présence ne valide pas la couverture du domaine.

Pour auditer, corriger ou enrichir des fiches et cartes existantes, utiliser le
skill du dépôt `revue-cartes` (`$revue-cartes` dans Codex, `/revue-cartes`
dans Claude Code). Il confronte les affirmations à leurs sources, préserve IDs
et identités Anki, consigne les corrections et soumet les ajouts à l'apprenant.

## Sources et documentation

Utiliser Context7 pour vérifier les API, versions, configurations et exemples de
bibliothèques : résoudre l'identifiant avec `resolve-library-id`, puis interroger
`query-docs` sur un sujet précis. Préférer les projets officiels aux forks.
Si une bibliothèque est absente de Context7, consulter sa documentation officielle
et signaler ce recours.

Pour les concepts de computer vision, consulter les articles et documentations
primaires pertinents ; Context7 ne remplace pas une bibliographie scientifique.

## Vérification

Adapter les vérifications au changement. Pour la documentation, relire les liens,
les exemples et le diff. Pour un export de cartes, tester création puis mise à
jour dans un deck d'essai, et vérifier formules, médias et absence de doublons.
Pour un script, vérifier les comportements utiles et les cas d'erreur concernés.

Ne pas présenter un skill installé comme une CI ou un contrôle automatique.
Indiquer ce qui a été vérifié et ce qui reste à valider dans Obsidian et Anki.
