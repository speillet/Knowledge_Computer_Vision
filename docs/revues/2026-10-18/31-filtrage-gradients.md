# Revue — Filtres, gradients et pyramides — 2026-10-18

## Synthèse

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 3 importante, 0 mineure, 1 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FILTRES-001 | Confirmé : ordre/moyenne ; effet conditionnel | choisir un filtre d’après le bruit. | Noyau fini ; 55 mots | Accord fiche et format | Aucune | Conserver |
| CV-FILTRES-002 | Confirmé par invariance du ratio ΔI/σ | régler un bilatéral dans les bonnes unités. | Noyau fini ; 57 mots | Accord fiche et format | Important | Conversion explicite |
| CV-FILTRES-003 | Protocole aval déduit ; pas résultat OpenCV | protéger un détail métier. | Noyau fini ; 44 mots | Accord fiche et format | Important (source) | Attribution corrigée |
| CV-FILTRES-004 | Confirmé : filtrage puis décimation | expliquer une pyramide. | Noyau fini ; 47 mots | Accord fiche et format | Important (source) | Source pyramide |

### Affirmations de la fiche et des cartes

Confirmés : moyenne gaussienne, statistique médiane, bilatéral non linéaire, normalisation du poids, décimation filtrée. Déduction vérifiable : diviser intensités et sigma par 255 conserve le quotient dans l’exponentielle. Choix de métrique métier, pipeline et baseline : propositions du projet. Le coût du bilatéral naïf se déduit des visites du support ; aucune mesure de temps.

## Corrections appliquées

Fiche révision 2 : cas scalaire/gaussien et conversion. Carte 002 : réponse numérique évaluable. Sources par objet pour 003–004 ; IDs préservés.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Choisir une échelle de dérivée | Relier lissage, bruit et localisation d’un contour | Raisonnement ; une carte | 3 critères ; durée à mesurer | Canny 1986 ; étude d’une marche bruitée |

## Sources

- [OpenCV 4.12.0, Smoothing Images, Gaussian/Median/Bilateral Filter](https://docs.opencv.org/4.12.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html).
- [Tomasi et Manduchi 1998, Bilateral Filtering, §§2–3](https://users.soe.ucsc.edu/~manduchi/Papers/ICCV98.pdf) : poids spatiaux et photométriques et cas gaussien.
- [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html).

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.
