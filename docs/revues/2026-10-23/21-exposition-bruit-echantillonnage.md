# Revue — Exposition, bruit, couleur et échantillonnage — 2026-10-23

## Synthèse

Quatre cartes auditées, plus leur fiche. Aucune affirmation fausse. Un
constat important de source : CV-ACQUISITION-003 attribuait l'aliasing au
tutoriel OpenCV des pyramides, qui ne le traite pas. Deux constats mineurs.
Correction appliquée : fiche en révision 3, IDs et objectifs inchangés.
Sur les enrichissements proposés, l'apprenant n'a retenu que la réécriture
chiffrée de CV-ACQUISITION-002, rédigée en révision 4 ; le nombre de cartes ne
change pas.

Auto-revue : Agent Claude Code (`revue-cartes`). Statut éditorial `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ACQUISITION-001 | Calcul refait : 800 × 0,005 = 4 px | Utile pour concevoir un test | Noyau net | Accord fiche | Aucun | — |
| CV-ACQUISITION-002 | Confirmé par EMVA 1288, §2.6, éq. 21 : hors quantification, $K$ s'annule dans le SNR | Forte | Recto en « pourquoi » qui oriente ; famille comparaison sans comparaison chiffrée | Accord fiche | Mineur | Enrichissement proposé |
| CV-ACQUISITION-003 | Non soutenu par la source citée, puis confirmé (Parmar et al. 2022, §§2, 3.2) | Forte | Noyau net | Accord fiche | Important | Source dédiée ; conventions de resize par bibliothèque |
| CV-ACQUISITION-004 | Checklist du projet, plausible | Forte | Noyau à six points vérifiables | Accord fiche | Aucun | — |

Fiche : la page Edmund Optics citée refuse les accès automatisés ; elle n'a
pas pu être revérifiée (mineur, signalé dans la fiche).

## Corrections appliquées

- Fiche `vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md`,
  révision 3 : préfiltre, repliement et conventions de resize selon Parmar
  et al. ; portée du tutoriel OpenCV précisée ; Edmund Optics signalée non
  revérifiée.
- CV-ACQUISITION-003 : source et approfondissement.
- Journal : une ligne.

## Enrichissements : décision de l'apprenant

Retenu le 2026-10-23 : CV-ACQUISITION-002, réécrite en comparaison chiffrée
sans changer d'objectif, et la partie de fiche correspondante (modèle EMVA,
régimes du SNR, saturation). Non retenus : photon transfer et
dimensionnement. Leurs sources sont vérifiées pour un ajout ultérieur.

Table des propositions telle que soumise :

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| CV-ACQUISITION-002 : comparaison chiffrée « doubler le gain ou doubler l'exposition » avec le modèle EMVA de SNR. Exemple : $\sigma_d=5$ e⁻, 100 e⁻ donne SNR 8,9 ; 200 e⁻ donne 13,3 ; doubler $K$ laisse 8,9. Effets sur flou et saturation | La carte est qualitative alors que la norme chiffre l'effet | comparaison, réécriture sans changer d'objectif | aucun nouveau rappel | EMVA 1288 Linear 4.0, §2.4, éq. 13–15, et §2.6, éq. 21–22 |
| CV-ACQUISITION-005 : estimer gain système et bruit de lecture d'une caméra par la méthode photon transfer, avec une paire d'images par niveau | Caractériser une caméra avant d'accuser un modèle ; geste d'ingénieur vision industrielle absent du vault | pratique | 1 carte ; noyau à 3 points | EMVA 1288, §2.4, éq. 15, et §2.5, éq. 16–18 |
| CV-ACQUISITION-006 : dimensionner l'acquisition d'un contrôle en ligne (rayure de 0,2 mm, champ de 150 mm, défilement à 0,5 m/s) : 15 px/mm, environ 2 500 px, exposition ≤ 133 µs, éclairage en conséquence | Famille conception absente du sujet | conception | 1 carte ; noyau à 4 points | The Imaging Source, Field of View (règle empirique de 2 à 3 px) ; EMVA 1288, §2.6 ; calculs du projet |
| Fiche : modèle de bruit EMVA, régimes du SNR, photon transfer, dimensionnement | Rubriques Mathématiques et Évaluation minces | fiche | sans carte | mêmes sources |

## Sources

- [EMVA 1288 Linear, Release 4.0, 16 juin 2021](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf),
  texte intégral :
  - §2.1, éq. 5–6 ;
  - §2.4, éq. 13–15 et méthode photon transfer ;
  - §2.5, éq. 16–19 ;
  - §2.6, éq. 20–23 ;
  - §2.7, éq. 24–25.
- [Parmar, Zhang et Zhu 2022](https://arxiv.org/abs/2104.11222), lu en HTML
  sur ar5iv : §§1, 2, 3.2–3.3, 4.1, 4.3 et 6.3.
- [The Imaging Source, Field of View in Machine Vision](https://www.theimagingsource.com/en-us/resource/glossary/field-of-view-in-machine-vision/),
  glossaire de fabricant sans date : règle empirique de 2 à 3 pixels et
  formules pixels/mm.
- Calculs du projet (Python 3.10.13) : SNR selon $K$ et $\mu_e$ ;
  dimensionnement 15 px/mm, 2 475 px avec 10 % de marge, 7 500 px/s,
  133 µs.
- Non vérifiable : Edmund Optics, Resolution, qui renvoie une page de
  vérification anti-robot.

## Contrôles et limites

`check_vault.py` OK (244 cartes) après correction. Context7 n'est pas
disponible dans cette session. Non vérifiés : export Anki, rendu Obsidian et
AnkiDroid, maîtrise, validation indépendante, toute mesure sur caméra réelle.
