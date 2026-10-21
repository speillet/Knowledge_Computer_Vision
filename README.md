# Knowledge Computer Vision

Construire un vault Obsidian de connaissances et de flashcards pour progresser
vers un niveau de Computer Vision Engineer senior.

Les fiches de référence et cartes détaillées couvrent le socle classique et
moderne, en français, avec termes techniques originaux, équations expliquées,
comparaisons et diagnostics. Les totaux actuels figurent dans le catalogue ci-dessous.

Ouvrir le dossier [`vault/`](vault/00-Accueil.md) comme vault dans Obsidian,
puis commencer par son accueil. Le [guide d'export](vault/01-Parcours/Guide-Anki.md)
prépare Obsidian_to_Anki et la révision sur **AnkiDroid** via Desktop/AnkiWeb.
Le format reste expérimental : le parseur officiel a été testé localement,
mais aucun export réel ni historique de révision n'est encore validé.

Le vault suit l'organisation par thématique de
[Knowledge_AI_Engineering](https://github.com/speillet/Knowledge_AI_Engineering) :
14 dossiers numérotés avec index, cartes à la racine de chaque thème et fiches
complètes dans `references/`. Chaque thème a son sous-deck Anki et ses états
éditoriaux ; les variantes à approfondir restent visibles dans l’inventaire.
Voir les [conventions de classement](docs/vault-layout.md).

## Couverture actuelle

<!-- cv-catalog:start -->
**52 fiches et 231 cartes**, réparties dans 14 des 14 thématiques. Rédaction par agent ; export réel, rappel et maîtrise personnelle non validés.

| Thématique | Fiches | Cartes |
| --- | ---: | ---: |
| [Mathématiques et estimation](vault/10-mathematiques-estimation/00-index.md) | 4 | 15 |
| [Formation et acquisition des images](vault/20-acquisition-images/00-index.md) | 3 | 11 |
| [Traitement d'image classique](vault/30-traitement-image/00-index.md) | 3 | 11 |
| [Features, matching et recalage](vault/40-features-matching/00-index.md) | 5 | 25 |
| [Calibration et géométrie multivue](vault/50-calibration-geometrie/00-index.md) | 5 | 26 |
| [Vision 3D](vault/60-vision-3d/00-index.md) | 4 | 19 |
| [Reconnaissance et représentations](vault/70-reconnaissance-representations/00-index.md) | 5 | 18 |
| [Détection et pose](vault/80-detection-pose/00-index.md) | 4 | 24 |
| [Segmentation](vault/90-segmentation/00-index.md) | 4 | 15 |
| [Mouvement et vidéo](vault/100-mouvement-video/00-index.md) | 2 | 8 |
| [Tracking et association](vault/110-tracking-association/00-index.md) | 3 | 14 |
| [Vision générative et multimodale](vault/120-generatif-multimodal/00-index.md) | 3 | 10 |
| [Données, évaluation et fiabilité](vault/130-evaluation-fiabilite/00-index.md) | 4 | 21 |
| [Ingénierie des systèmes de vision](vault/140-ingenierie-systemes/00-index.md) | 3 | 14 |
<!-- cv-catalog:end -->

## Vérification locale

Python 3.9+, sans dépendance supplémentaire :

```sh
python3 scripts/check_vault.py
python3 scripts/sync_catalog.py --check
python3 -m unittest discover -s tests -v
python3 examples/pilot_math.py
```

Les [preuves et essais restants](vault/01-Parcours/Suivi-pilote.md) distinguent
contrôles locaux, auto-revue, tests applicatifs et maîtrise personnelle.

## Outils de travail

- [Conventions de contribution](CONTRIBUTING.md) : branches, commits et PR.
- [Instructions pour les agents](AGENTS.md) : objectifs et règles du dépôt.
- [Audit des outils](docs/tooling-audit.md) : skills installés, versions,
  vérifications et configuration restante.
- [Skill de revue des cartes](.agents/skills/revue-cartes/SKILL.md) :
  `$revue-cartes` (Codex) ou `/revue-cartes` (Claude Code) audite, corrige
  et propose d'enrichir une fiche et ses cartes.

## Spécification en cours

Le [brouillon de spécification](specs/001-cv-knowledge-base/spec.md) reprend
le profil expérimenté, les objectifs et les choix pédagogiques confirmés.
Il est accompagné de :

- La [cartographie de couverture](specs/001-cv-knowledge-base/curriculum.md).
- Le [contrat des fiches et cartes](specs/001-cv-knowledge-base/learning-design.md).
- La [recherche sur l'export Obsidian–Anki](specs/001-cv-knowledge-base/research.md).
- La [revue de pertinence et ses corrections](specs/001-cv-knowledge-base/review.md).

Le [plan d'implémentation](specs/001-cv-knowledge-base/plan.md) et ses
[tâches](specs/001-cv-knowledge-base/tasks.md) suivent le premier lot et la
suite du pilote. Le catalogue complet, les extensions et la validation
pédagogique restent à développer ; le contenu n'est pas déclaré exhaustif.

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
