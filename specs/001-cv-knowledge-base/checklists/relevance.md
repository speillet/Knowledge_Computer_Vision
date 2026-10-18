# Checklist de pertinence et de couverture

**Objet** : qualité des exigences pédagogiques et scientifiques du brouillon.
**Création** : 2026-10-18
**Spécification** : [spec.md](../spec.md)
**Rapport d'évaluation** : [review.md](../review.md)
**Profondeur** : revue approfondie par l'auteur et le relecteur du cadrage.

Checklist éditoriale créée manuellement après constat du prérequis `plan.md`
de la commande Spec Kit. Les cases sont laissées ouvertes pour la relecture.
Une case cochée signifiera que la qualité de l'exigence a été examinée, pas
que les fiches sont produites ni que l'apprenant a acquis la compétence.

## Complétude de la couverture

- [ ] CHK001 Le profil expérimenté et les rappels ML/DL sont-ils distingués des nouveaux apprentissages ? [Complétude, Spec FR-001]
- [ ] CHK002 Les familles classiques, géométriques et apprises sont-elles explicites au-delà des noms de domaines ? [Complétude, Spec FR-003/004, curriculum]
- [ ] CHK003 Le niveau cible et les compétences de chaque méthode sont-ils définis séparément de sa priorité et de son état éditorial ? [Clarté, Spec FR-026/030]
- [ ] CHK004 Les dépendances obligatoires et liens connexes ont-ils des rôles distincts ? [Cohérence, Spec FR-005, curriculum]
- [ ] CHK005 Acquisition, contrats de données, temporalité et pré/posttraitements sont-ils présents dans les exigences des sujets concernés ? [Couverture, Spec FR-031/032]

## Pertinence pédagogique

- [ ] CHK006 Le contrat permet-il des réponses développées tout en définissant un noyau de correction ? [Clarté, Spec FR-015/017, learning-design]
- [ ] CHK007 Le statut des approfondissements facultatifs et erreurs bloquantes est-il sans ambiguïté ? [Clarté, Spec FR-015/037]
- [ ] CHK008 Les exigences distinguent-elles rappel d'un exemple et raisonnement sur un cas nouveau ? [Couverture, Spec FR-034/035]
- [ ] CHK009 Les conditions d'un choix ou diagnostic réussi sont-elles explicitement définies ? [Mesurabilité, Spec SC-006]
- [ ] CHK010 Le protocole d'essai peut-il conduire à corriger le contrat des cartes sans imposer une durée de révision arbitraire ? [Pertinence, Spec FR-035, SC-008]
- [ ] CHK011 Une baseline et une variation contrôlée sont-elles demandées pour chaque famille du pilote ? [Complétude, Spec FR-033, SC-009]
- [ ] CHK021 La provenance de rédaction et l'appropriation des cartes par l'apprenant sont-elles exigées ? [Traçabilité, Spec FR-038, SC-010]
- [ ] CHK022 La charge de révision est-elle mesurée sans plafond arbitraire ? [Mesurabilité, Spec FR-035, SC-008]

## Exactitude et preuves

- [ ] CHK012 Les propriétés générales et les particularités d'implémentation ont-elles des exigences de provenance distinctes ? [Traçabilité, Spec FR-012/013/036]
- [ ] CHK013 Le traitement d'une contradiction centrale entre sources est-il défini ? [Cas limite, Spec FR-036]
- [ ] CHK014 Les exigences mathématiques couvrent-elles repères, unités et conditions d'application ? [Complétude, Spec FR-007/027/031]
- [ ] CHK015 Une fiche validée a-t-elle une définition indépendante de la simple présence de ses rubriques ? [Mesurabilité, Spec FR-037, Entités principales]
- [ ] CHK016 Auto-revue, revue indépendante, exemple exécuté et contenu non exécuté sont-ils distingués ? [Clarté, Spec FR-009/037]

## Cohérence et limites

- [ ] CHK017 Le pilote initial et ses extensions sont-ils cohérents entre la spec et la cartographie ? [Cohérence, Spec SC-004, curriculum]
- [ ] CHK018 Le statut de dépendance du plugin permet-il d'avancer sur le cadrage sans le déclarer validé ? [Dépendance, Spec FR-028, research]
- [ ] CHK019 La réussite éditoriale, l'export et la maîtrise personnelle restent-ils distincts ? [Cohérence, Spec FR-026, SC-005/008]
- [ ] CHK020 Les exigences bornent-elles la couverture sans promettre tous les algorithmes ou un statut professionnel par mémorisation ? [Clarté, Spec FR-029, Hypothèses]
- [ ] CHK023 Les familles de cartes n'ont-elles qu'une définition, dans le contrat ? [Cohérence, Spec FR-014, learning-design]
- [ ] CHK024 Une solution de repli d'export et le rendu sur le client de révision sont-ils prévus ? [Dépendance, Spec SC-005, research]

## Notes

Le rapport lié consigne l'évaluation effectuée et ses limites. Cette checklist
est disponible pour une relecture ultérieure ; ses marqueurs ne doivent pas
être modifiés par une future étape d'implémentation pour contourner la revue.
