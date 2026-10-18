# Revue de pertinence et de complétude des specs

**Date** : 2026-10-18
**Périmètre** : spécification, cartographie, contrat pédagogique et recherche d'export.
**Type de revue** : auto-revue assistée par l'agent auteur, confrontée à des sources
primaires ; elle ne constitue pas une expertise scientifique indépendante.
**Résultat** : révisions éditoriales 2 et 3 du brouillon, toujours à relire avec
l'utilisateur. La révision 3 provient de la revue complémentaire ci-dessous.

## Appréciation

La structure répond bien au profil confirmé : ingénieur expérimenté, bases
ML/DL acquises, besoin de spécificités de vision et d'un jugement industriel.
Le français, les réponses développées et les compléments mathématiques/code
restent adaptés à cette demande.

La première version était cependant plus précise sur la présence des documents
et l'export que sur la profondeur par famille et le transfert des connaissances.
Les grandes rubriques laissaient aussi plusieurs familles peu représentées.
La révision précise ces points sans promettre une exhaustivité universelle.

## Constats et corrections

Les niveaux d'impact ci-dessous décrivent l'effet sur le projet, pas un score
scientifique de qualité. « Corrigé dans les exigences » ne signifie pas que
les fiches existent ou que le résultat pédagogique est démontré.

| ID | Impact | Faiblesse de la première version | Correction de la révision 2 | État |
| --- | --- | --- | --- | --- |
| RV-01 | Élevé | Des domaines nommés pouvaient masquer des sous-familles absentes, notamment la segmentation classique et le matching appris | Inventaire enrichi : Otsu/watershed/GrabCut, LightGlue/LoFTR, ICP, suivi de points, anomalies et acquisition | Corrigé dans la cartographie ; contenu à produire |
| RV-02 | Élevé | Une priorité de lecture n'indiquait pas la profondeur à atteindre | Repérage, usage opérationnel et approfondissement, avec compétences et dépendances par méthode ; FR-030 | Corrigé dans les exigences |
| RV-03 | Élevé | Présence d'une fiche et de cartes assimilable à tort à une compétence applicable | Baseline, variation contrôlée et cas nouveaux de choix/diagnostic ; FR-033/034, SC-006/009 | Corrigé ; essais à réaliser |
| RV-04 | Élevé | Une réponse très détaillée n'avait pas de frontière claire entre essentiel et facultatif | Noyau attendu, approfondissement et erreurs bloquantes ; FR-015, SC-003 | Corrigé dans le contrat pédagogique |
| RV-05 | Moyen | Les six sujets du pilote étaient concentrés sur le classique 2D | Trois extensions contrastées : segmentation classique, matching appris, recalage 3D ; SC-004 | Proposition renforcée, à relire |
| RV-06 | Élevé | Les erreurs de contrat de données et de temporalité restaient peu explicites | Repères, types/plages, normalisation, crops et cibles, cadence et causalité ; FR-031/032 | Corrigé dans les exigences |
| RV-07 | Moyen | Une source primaire unique ne distinguait pas propriété générale et particularité de bibliothèque | Traçabilité scientifique/implémentation, traitement des divergences et preuve de revue ; FR-036/037 | Corrigé dans le contrat |
| RV-08 | Moyen | La revue de forme initiale ne mesurait pas l'utilité réelle des cartes | Première tentative, rappel différé, ambiguïtés et corrections ; FR-035, SC-008 | Protocole défini ; aucun résultat encore obtenu |
| RV-09 | Moyen | Les capacités d'un plugin documenté pouvaient être confondues avec une intégration validée | Recherche et essais restent séparés ; préparation éditoriale possible pendant le choix du plugin ; FR-028 | Dépendance ouverte, explicitement conservée |

## Revue complémentaire (révision 3)

**Type** : revue par un second agent (Claude Code) des documents de la
révision 2 ; ni expertise scientifique indépendante, ni essai dans Obsidian ou Anki.

| ID | Impact | Faiblesse de la révision 2 | Correction de la révision 3 | État |
| --- | --- | --- | --- | --- |
| RV-10 | Élevé | Le mode de rédaction n'était pas spécifié : une source présente n'est pas une source vérifiée, et relire un contenu généré apprend moins que le produire | Provenance de rédaction, confrontation des affirmations centrales à la source ; FR-038, SC-010 ; répartition proposée dans les hypothèses | Corrigé dans les exigences ; répartition à décider |
| RV-11 | Élevé | Le coût réel de révision des cartes développées n'était pas mesuré | Durée par carte et charge projetée du premier lot, sans plafond a priori ; FR-035, SC-008 | Protocole défini ; aucune mesure encore |
| RV-12 | Moyen | Le candidat d'export, sans release depuis 2024-01, n'avait ni solution de repli ni vérification sur le client de révision | Maintenance constatée, paquet `.apkg` en plan B, rendu sur le client utilisé ; [recherche](research.md) | Recherche complétée ; essais à réaliser |
| RV-13 | Moyen | Aucun sujet du pilote n'éprouvait le type de fiche métrique/protocole | IoU et AP (COCO) ajoutés au premier étage ; SC-004 | Proposition, à relire |
| RV-14 | Moyen | Le jugement de conception de bout en bout n'avait pas de famille de cartes | Famille « Conception de système » ; inventaire du domaine 14 ; cas tirés de l'expérience de l'apprenant, anonymisés | Corrigé dans le contrat |
| RV-15 | Faible | FR-014 listait six familles de cartes contre sept dans le contrat ; « P1 » désignait deux échelles ; « quatorze domaines » était codé en dur | FR-014 renvoie au contrat ; vagues V0–V2 ; comptes de domaines retirés | Corrigé |
| RV-16 | Faible | Aucun moyen de suivre la maîtrise, pourtant distincte des états éditoriaux | Domaine et famille exportés comme étiquettes ; FR-026 | Corrigé dans les exigences |

Points examinés sans modification : FR-007 à FR-010 reprennent la section
« Équations, code et illustrations » du contrat, mais leurs numéros sont cités
par cette revue et par la checklist de pertinence ; ils sont conservés.
Les principes candidats à la constitution sont listés dans les hypothèses de
la spec, sans être ajoutés à la constitution.

## Traçabilité des résultats attendus

| Groupe | Exigences | Critères liés |
| --- | --- | --- |
| Profil, couverture et navigation | FR-001 à FR-005, FR-025 à FR-027, FR-029/030 | SC-001 à SC-003 |
| Exactitude, contrats et preuves | FR-006 à FR-013, FR-031/032, FR-036 à FR-038 | SC-002, SC-004, SC-009/010 |
| Révision, jugement et transfert | FR-014 à FR-019, FR-033 à FR-035 | SC-002/003, SC-006, SC-008/009 |
| Export et maintenance des relations | FR-020 à FR-024, FR-028 | SC-004/005, SC-007 |

Cette correspondance relie exigences et résultats ; elle ne représente pas
une couverture par tâches d'implémentation. Le plan et les tâches ne sont pas
encore rédigés.

## Sources primaires de la revue

Les ajouts sont des choix de couverture proposés pour ce profil. Les sources
suivantes vérifient l'existence et la nature des familles concernées, sans
établir qu'il faudrait approfondir chaque variante au même niveau.

- OpenCV : [seuillage et Otsu](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html),
  [watershed](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html)
  et [GrabCut](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html)
  rendent concrète la couverture de segmentation classique.
- Les dépôts des auteurs de [LightGlue](https://github.com/cvg/LightGlue)
  et [LoFTR](https://github.com/zju3dv/LoFTR) étayent l'ajout du matching appris
  et de ses différences de composants et de représentation.
- [Open3D : recalage global](https://www.open3d.org/docs/latest/tutorial/pipelines/global_registration.html)
  présente la relation entre correspondances, initialisation globale et
  raffinement local ICP, absente de l'ancien inventaire 3D détaillé.
- [RAFT](https://github.com/princeton-vl/RAFT) et
  [CoTracker](https://github.com/facebookresearch/co-tracker) représentent
  respectivement des familles de flot optique appris et de suivi de points,
  à distinguer du suivi d'identités d'objets.
- [OpenCV calib3d](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)
  documente notamment calibration, stéréo et hand-eye ;
  [l'alignement ECC](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html)
  justifie de couvrir aussi le recalage par intensités.
- [PatchCore dans Anomalib](https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/models/image/patchcore.html)
  fournit une entrée concrète pour l'anomalie/localisation en inspection.
- [Le protocole KITTI tracking](https://www.cvlibs.net/datasets/kitti/eval_tracking.php)
  illustre l'importance des conventions de métrique et du périmètre de temps mesuré.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)
  soutient la couverture tests/données/surveillance d'un système ML ; seules
  les implications spécifiques à la vision sont approfondies ici.

Context7 a été réellement consulté pendant cette revue : résolution OpenCV
et Open3D, puis requêtes ciblées sur `/websites/opencv_4_13_0` pour la segmentation
classique et `/websites/open3d` pour le recalage. Les références officielles ont
ensuite été lues pour corroborer les synthèses.

## Limites et décisions encore ouvertes

- Le catalogue est plus représentatif, mais reste un inventaire de recherche :
  les fiches et les cartes n'ont pas encore démontré leur exactitude ou leur utilité.
- Priorités, profondeurs et pilote renforcé sont des propositions, pas de
  nouveaux choix attribués à l'utilisateur.
- Le plugin d'export et les modèles de notes restent à valider dans les applications.
- La répartition de la rédaction entre l'apprenant et un agent reste à décider (FR-038).
- Le découpage de la production en lots après le pilote reste à décider.
- La constitution n'est pas ratifiée. Aucun principe ne lui a été ajouté implicitement.
- La checklist formelle Spec Kit nécessite actuellement un `plan.md`, absent
  à cette phase. La commande a signalé ce prérequis ; la présente revue et
  [sa checklist](checklists/relevance.md) sont éditoriales et manuelles.
- L'analyse formelle croisée spec/plan/tasks aura lieu lorsque les trois
  documents existeront ; elle n'a pas été annoncée comme exécutée ici.

## Étape suivante pertinente

Relire le niveau de profondeur et les deux étages du pilote, puis produire
un petit échantillon afin de confronter les rubriques à de vrais contenus.
Le pilote doit permettre de modifier le contrat s'il génère du remplissage,
des réponses impossibles à corriger ou des comparaisons insuffisamment justifiées.
