# Revue — Exposition, bruit, couleur et échantillonnage — 2026-10-18

## Synthèse

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 3 importante, 0 mineure, 1 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ACQUISITION-001 | Confirmé par calcul : 4 puis 8 px | calculer un flou simplifié. | Noyau fini ; 48 mots | Accord fiche et format | Important (attribution) | Déduction signalée |
| CV-ACQUISITION-002 | Confirmé : gain et information photonique | distinguer gain et exposition. | Noyau fini ; 46 mots | Accord fiche et format | Aucune | Conserver le noyau |
| CV-ACQUISITION-003 | Confirmé : filtrage avant décimation | reconnaître aliasing et prétraitement incohérent. | Noyau fini ; 55 mots | Accord fiche et format | Important (source) | Source pyramide |
| CV-ACQUISITION-004 | Checklist pertinente ; transfert sRGB confirmé | contrôler une entrée image. | Noyau fini ; 46 mots | Accord fiche et format | Important (source) | Source photométrique |

### Affirmations de la fiche et des cartes

Confirmés : variance photonique égale à la moyenne dans le modèle idéal ; limites du gain ; Nyquist sous hypothèse de bande ; filtrage de pyramide ; non-linéarité sRGB. Calculs exécutés : 800×0,005=4 px ; exposition doublée : 8 px. Contrôles de contrats d’entrée et protocole sur défauts : décisions du projet.

## Corrections appliquées

Fiche révision 2 et quatre champs Source corrigés ; réponses et IDs conservés.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Budget exposition–bruit–flou | Choix d’acquisition sous cadence et contraste imposés | Conception ; une carte | 3 compromis ; durée à mesurer | EMVA1288 §§2.4–2.7 ; modèle cinématique explicite |

## Sources

- [EMVA1288 Linear 4.0 (2021), §§2.1, 2.4, 2.6–2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) : variance de Poisson Eq.13, SNR Eq.20–23, saturation §2.7.
- [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html) : convolution puis décimation.
- [sRGB, §§A.7–A.8 et B.1, conversion linéaire et fonction de transfert](https://www.w3.org/Graphics/Color/srgb) : transfert non linéaire.
- [Edmund, Resolution §2.2](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/resolution/) : limite de Nyquist ; lu via navigateur documentaire, accès HTTP direct 403.

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.
