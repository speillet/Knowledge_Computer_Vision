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
- [ ] T022 — Publier en commits/PR cohérents, relire, fusionner dans l'ordre
  des dépendances et vérifier le contenu final de main.

T011/T012 signifient contenu préparé : les résultats image/vidéo proposés ne
sont pas des expériences exécutées, et les cas de transfert n'ont pas été
essayés par l'apprenant. T009/T010/T013 restent ouverts après la publication.
