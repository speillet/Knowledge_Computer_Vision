# Revue — Détecteurs locaux, descripteurs et matchers — 2026-10-20

## Synthèse

4 cartes auditées. 0 bloquant ; 1 important (source absente) ; 1 constat mineur partagé (attribution des cas).
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 2 mineure, 1 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MATCHING-001 | Confirmé : deux valeurs propres et ambiguïté tangentielle | interpréter la matrice de structure. | 45 mots à l’entrée ; un mécanisme | Fiche et format contrôlés | Aucune | Conserver |
| CV-MATCHING-002 | Non soutenu par les anciennes références ; confirmé par FAST/BRIEF | séparer détecteur et descripteur. | 42 mots à l’entrée ; deux rôles distincts | Fiche et format contrôlés | Important | Sources remplacées |
| CV-MATCHING-003 | Paramètres/index confirmés ; effet aval déduit | mesurer une recherche approximative. | 54 mots à l’entrée ; quatre contrôles liés | Fiche et format contrôlés | Mineur | Attribution précisée |
| CV-MATCHING-004 | Diagnostic construit ; symétrie non résolue par réciprocité | choisir un contrôle géométrique. | 48 mots à l’entrée ; un contrôle géométrique | Fiche et format contrôlés | Mineur | Attribution précisée |

### Affirmations de la fiche et des cartes

Confirmés : matrice et score Harris, score minimum Shi–Tomasi, cercle FAST, descripteur binaire BRIEF, variantes AKAZE, compromis FLANN. Le coût exhaustif n×m est un comptage de comparaisons, pas une complexité indépendante de la dimension. Les contrôles de couverture, symétrie et succès final sont des déductions du projet. Aucun doublon de noyau détecté.

## Corrections appliquées

Fiche révision 2 et sources des cartes 002–004. Réponses et objectifs conservés.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune carte nouvelle ; relier au cas SIFT/ORB | Évaluation comparative déjà interrogée | Navigation | Aucun rappel ajouté | Lowe ; Rublee |

Familles absentes : algorithme, comprehension, conception, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Harris, Theory](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html), matrice M et score R.
- [Shi–Tomasi, Theory](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html), minimum des valeurs propres.
- [OpenCV 4.13.0, FAST, Feature Detection](https://docs.opencv.org/4.13.0/df/d0c/tutorial_py_fast.html)
- [OpenCV 4.13.0, BRIEF, Theory](https://docs.opencv.org/4.13.0/dc/d7d/tutorial_py_brief.html)
- [OpenCV 4.13.0, AKAZE, Detailed Description et DescriptorType](https://docs.opencv.org/4.13.0/d8/d30/classcv_1_1AKAZE.html)
- [OpenCV 4.13.0, Feature Matching, FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html)

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
