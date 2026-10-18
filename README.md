# Knowledge Computer Vision

Construire un vault Obsidian de connaissances et de flashcards pour progresser
vers un niveau de Computer Vision Engineer senior.

Les cartes doivent expliquer les problèmes en profondeur : intuition, formulation,
hypothèses, méthodes, compromis, limites et cas d'usage. Le format d'export Anki
sera fixé avec le choix du plugin Obsidian et vérifié sur un petit échantillon.

## Outils de travail

- [Conventions de contribution](CONTRIBUTING.md) : branches, commits et PR.
- [Instructions pour les agents](AGENTS.md) : objectifs et règles du dépôt.
- [Audit des outils](docs/tooling-audit.md) : skills installés, versions,
  vérifications et configuration restante.

## Spécification en cours

Le [brouillon de spécification](specs/001-cv-knowledge-base/spec.md) reprend
le profil expérimenté, les objectifs et les choix pédagogiques confirmés.
Il est accompagné de :

- La [cartographie de couverture](specs/001-cv-knowledge-base/curriculum.md).
- Le [contrat des fiches et cartes](specs/001-cv-knowledge-base/learning-design.md).
- La [recherche sur l'export Obsidian–Anki](specs/001-cv-knowledge-base/research.md).
- La [revue de pertinence et ses corrections](specs/001-cv-knowledge-base/review.md).

Le plugin pressenti reste à confirmer par un pilote ; aucun export réel ni
contenu pédagogique du pilote n'a encore été produit.

GitHub Spec Kit 1.2.1 est initialisé pour Codex. Ses skills sont versionnables
dans `.agents/skills/` ; ses modèles et scripts se trouvent dans `.specify/`.
Leur [provenance et leur licence](.specify/NOTICE.md) sont conservées dans le dépôt.
La constitution générée est encore un modèle à remplir avec
`$speckit-constitution`, après clarification des principes du projet.

Les skills complémentaires de Matt Pocock, de commits et de PR sont installés
au niveau utilisateur. Ils ne sont pas inclus dans un clone du dépôt ; leurs
sources et révisions sont consignées dans l'audit.

## Poursuivre le cadrage

1. Relire le brouillon et sa cartographie ; utiliser `$grill-me` pour les
   décisions ouvertes, notamment le pilote et l'export.
2. Définir les principes avec `$speckit-constitution` et affiner le brouillon
   avec `$speckit-clarify`. Les étapes suivantes sont
   `$speckit-plan`, `$speckit-tasks` et `$speckit-analyze` selon le besoin.
3. Pour utiliser également `$to-spec`, configurer d'abord sa destination avec
   `$setup-matt-pocock-skills`. Relier les artefacts plutôt que maintenir deux
   spécifications contradictoires.

Sur la machine auditée, Context7 est configuré comme serveur MCP distant dans Codex.
Cette configuration utilisateur n'est pas embarquée dans un clone. Context7 sert à vérifier
la documentation des outils et bibliothèques utilisés. Les notions scientifiques
doivent s'appuyer sur des articles et autres sources primaires.
