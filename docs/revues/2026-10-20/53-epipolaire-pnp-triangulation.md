# Revue — Épipolaire, PnP et triangulation — 2026-10-20

## Synthèse

5 cartes auditées. 0 bloquant ; 1 important dans la fiche ; 1 mineur d’attribution.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 1 mineure, 3 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-EPIPOLAIRE-001 | Confirmé : coordonnées normalisées/pixels idéaux | distinguer E et F. | 45 mots à l’entrée ; objectif unique et noyau fini | Fiche et format contrôlés | Aucune | Conserver |
| CV-EPIPOLAIRE-002 | Confirmé : translation à échelle près | interpréter l’échelle de translation. | 50 mots à l’entrée ; objectif unique et noyau fini | Fiche et format contrôlés | Aucune | Conserver |
| CV-EPIPOLAIRE-003 | Confirmé : inconnues différentes | choisir PnP ou triangulation. | 56 mots à l’entrée ; objectif unique et noyau fini | Fiche et format contrôlés | Aucune | Conserver |
| CV-EPIPOLAIRE-004 | Déduction géométrique vérifiée | détecter une faible parallaxe. | 41 mots à l’entrée ; objectif unique et noyau fini | Fiche et format contrôlés | Mineur | Attribution |
| CV-EPIPOLAIRE-005 | Carte prudente correcte ; fiche généralisait à tort | respecter la variante minimale de pose. | 44 mots à l’entrée ; objectif unique et noyau fini | Fiche et format contrôlés | Important | Distinguer solvePnP et solveP3P |

### Affirmations de la fiche et des cartes

E=[t]×R et F=K₂⁻ᵀEK₁⁻¹ concordent avec le sens caméra 1→2 ; le centre caméra se déduit par inversion. Les docs confirment l’échelle arbitraire, la chiralité et les inconnues PnP/triangulation. Correction importante du contrat P3P de la fiche. Le raisonnement faible parallaxe n’est pas une expérience exécutée.

## Corrections appliquées

Fiche révision 2 ; sources 004–005 ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Dégénérescence en rotation pure | E ne fournit alors pas une direction de translation observable | Diagnostic | Une carte, deux critères ; durée à mesurer | Géométrie épipolaire, cas dégénérés |

Familles absentes : algorithme, conception, evaluation. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [OpenCV 4.13.0, solvePnP, Pose computation methods et P3P](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html)
- [OpenCV 4.13.0, decomposeEssentialMat, recoverPose, solveP3P et triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
