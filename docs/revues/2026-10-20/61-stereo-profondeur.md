# Revue — Stéréo rectifiée, SGM et profondeur — 2026-10-20

## Synthèse

4 cartes auditées. 0 bloquant ; 2 importants (conditions et noyau) ; 1 mineur.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 1 mineure, 2 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-STEREO-001 | Confirmé par calcul : 10 m | calculer une profondeur rectifiée. | 49 mots à l’entrée ; noyau recentré sur la question | Fiche et format contrôlés | Important | Conventions et détail facultatif |
| CV-STEREO-002 | Confirmé par dérivation : sensibilité en 1/d² | interpréter l’incertitude de profondeur. | 51 mots à l’entrée ; une relation, f/B fixés | Fiche et format contrôlés | Mineur | Attribution du calcul |
| CV-STEREO-003 | Confirmé : facteur 16 et conversion flottante | décoder une disparité fixe. | 50 mots à l’entrée ; contrat de stockage | Fiche et format contrôlés | Aucune | Source versionnée |
| CV-STEREO-004 | Confirmé : rectifier ne résout pas les ambiguïtés | séparer rectification et matching. | 48 mots à l’entrée ; un rôle géométrique | Fiche et format contrôlés | Aucune | Conserver |

### Affirmations de la fiche et des cartes

Conditions du modèle simple précisées ; 1000×0,2/20=10 m, puis 20 m pour 10 px. La dérivée vaut −fB/d² ; la propagation est au premier ordre, pour f et B fixés. SGBM est explicitement une variante, avec pénalités et format documentés. La profondeur n’est pas validée par un masque de signe universel.

## Corrections appliquées

Fiche révision 2 ; carte 001 clarifiée sans changer son objectif ; références 001–003 précisées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Expliquer les pénalités SGM P1/P2 | Mécanisme nommé mais pas interrogé | Algorithme | Une carte, trois critères ; durée à mesurer | Hirschmüller, SGM ; OpenCV pour SGBM |

Familles absentes : algorithme, comprehension, conception, evaluation, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [OpenCV 4.13.0, StereoSGBM, Detailed Description et create](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html)
- [OpenCV 4.13.0, stereoRectify et reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) : conversion /16 explicitement demandée ; minDisparity peut changer avec la rectification.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
