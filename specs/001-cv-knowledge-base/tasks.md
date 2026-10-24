# Tâches — premier lot et suite du pilote

**Branche** : `feat/obsidian-pilot`. Les cases décrivent des résultats, pas des intentions.

- [x] T001 — Créer le vault autonome, son accueil et l'inventaire des 14 domaines.
- [x] T002 — Rédiger les fiches SIFT et ORB, leurs sources et cartes.
- [x] T003 — Rédiger RANSAC/homographie et calibration de Zhang, leurs cartes.
- [x] T004 — Rédiger SORT, NMS et IoU/AP COCO, leurs cartes et connexions.
- [x] T005 — Fournir les expériences arithmétiques exécutables et le schéma original.
- [x] T006 — Fournir le modèle Anki, le guide AnkiDroid et le journal d'essai.
- [x] T007 — Vérifier identités, liens, tags, format et cas d'erreur du contrôleur.
- [x] T008 — Auto-revoir les affirmations centrales avec les passages primaires ;
  consigner les limites et les résultats locaux.
- [ ] T009 — Installer/configurer le candidat dans les applications de l'apprenant ;
  consigner versions, champs et réglages réels.
- [ ] T010 — Exécuter tout le pilote d'export, y compris historique, médias,
  déplacements/suppressions/conflits et rendu sur AnkiDroid.
- [x] T011 — Ajouter les extensions : segmentation classique, matching appris,
  recalage global + ICP ; vérifier le format contrasté avant généralisation.
- [x] T012 — Compléter les douze cas de transfert et les six familles de variations.
- [ ] T013 — Faire les deux sessions de rappel ; mesurer ambiguïtés, durée,
  correction et charge quotidienne avant de choisir le lot suivant.

T009–T010 dépendent des applications et du compte de l'apprenant ; T011–T013
appartiennent à la suite du pilote, sans déclaration de validation anticipée.

- [x] T014 — Appliquer l'organisation demandée par thématique : 14 index,
  fiches/cartes regroupées, cinq sous-decks actifs, liens/médias adaptés et
  IDs préservés ; revérifier contrôleur, tests et parseur officiel sur tout le vault.
- [x] T015 — Reporter les pôles métiers dans `vault/01-Parcours/Inventaire.md` :
  colonne « Pôles », entrées clés et approfondissements rattachés à leur domaine
  d'accueil, scission des entrées groupées concernées (R02, X02, P03…).
- [x] T016 — Ajouter une vue par pôle dans `vault/01-Parcours/` : domaines,
  entrées, profondeur cible et avancement éditorial, sans déduire la maîtrise.
- [x] T017 — Ajouter le champ `poles` aux fiches et les étiquettes de pôle aux
  cartes ; mettre à jour `data-model.md`, `scripts/check_vault.py` et ses tests
  pour valider les lettres A à F.
- [x] T018 — Rédiger les douze cas de pôle, conception et diagnostic, avec
  réponse de référence et critères de correction.

T015–T018 découlent de la révision 5 de la spec (pôles métiers) ; ils ne
modifient pas le pilote.

- [x] T019 — Revoir les specs mises à jour : priorités V0, profondeur, cas
  corrigibles, jauges VIO, occupation, VLA, quantification et statut des preuves.
- [x] T020 — Ajouter 45 fiches et 177 cartes : chaque domaine contient des
  artefacts, sans assimiler les 129 approfondissements ouverts à des méthodes maîtrisées.
- [x] T021 — Générer index, inventaire et vues des pôles depuis le contenu ;
  vérifier étiquettes, cas métiers, liens, conservation des IDs et calculs.
- [x] T022 — Publier en commits/PR cohérents, relire, fusionner dans l'ordre
  des dépendances et vérifier le contenu final de main. Réalisé dans les PR
  [#4](https://github.com/speillet/Knowledge_Computer_Vision/pull/4),
  [#5](https://github.com/speillet/Knowledge_Computer_Vision/pull/5) et
  [#6](https://github.com/speillet/Knowledge_Computer_Vision/pull/6) ;
  [preuves après fusion](../../docs/publication-2026-10-18.md).

T011/T012 signifient contenu préparé : les résultats image/vidéo proposés ne
sont pas des expériences exécutées, et les cas de transfert n'ont pas été
essayés par l'apprenant. T009/T010/T013 restent ouverts après la publication.

- [ ] T023 — Avant la rédaction des 119 approfondissements APP encore ouverts, définir pour
  chacun les compétences observables et les dépendances obligatoires, distinctes
  de son lien thématique connexe ; compléter l’inventaire et les sources.
  SC-001/FR-030 restent partiellement satisfaits pour ce backlog. Les 60 fiches
  du lot courant ont leurs compétences et prérequis ; cette tâche n’affecte pas
  la présence effective de contenu dans les quatorze thèmes (SC-013).

- [x] T024 — Vérifier et corriger les PR 13–16, puis les fusionner dans l’ordre :
  dimensions SE(3), stabilité de covariance, contrôle postfit et contexte du resize.
- [x] T025 — Ajouter huit fiches et 38 cartes sur les lacunes classiques prioritaires ;
  relier dix cibles APP à leur contenu effectif sans supprimer leurs IDs.

Les dix entrées APP désormais rédigées conservent leurs objectifs et prérequis.
T023 reste ouverte pour les 119 autres ; T009/T010/T013 restent inchangées.

- [x] T026 — Publier l'exporteur `.apkg` local : modèle stable, conversion,
  médias embarqués, contrôle ZIP/SQLite et comparaison des manifestes.
- [x] T027 — Tester dans le moteur Anki 26.9.3 l'import, la réimportation sans
  changement, trois révisions, les corrections de contenu et du style, avec
  identités et historique conservés. Consigner les résultats dans le journal.
- [x] T028 — Documenter la construction, l'import direct et son skill ; distinguer
  cette chaîne des identités du plugin et la fusion d'une PR d'une release.

T026–T028 livrent l'export direct du 2026-10-24. Ils ne clôturent pas T009/T010 :
installation personnelle, rendu Android et cas applicatifs restent à observer.
