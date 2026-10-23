# Revue — Moindres carrés, SVD et conditionnement — 2026-10-23

## Synthèse

Quatre cartes auditées, plus leur fiche. Aucun constat bloquant : aucune
affirmation n'est fausse. Il y a trois constats importants et un mineur sur
les cartes, et deux mineurs sur la fiche. Les corrections sont appliquées :
fiche en révision 3, IDs et objectifs inchangés. Cinq
nouvelles cartes et un complément d'approfondissement ont été proposés, puis
acceptés et rédigés en révision 4 : le sujet passe de 4 à 9 cartes.

Le défaut principal ne tient pas à l'exactitude mais à l'alignement entre
question, famille et objectif. Trois cartes posaient une question qui
n'entraînait pas l'objectif annoncé. Le sujet ignorait aussi, comme tout le
vault, la DLT, la normalisation de Hartley, Gauss-Newton/Levenberg-Marquardt
et les pertes robustes. Ce sont des outils quotidiens en géométrie.

Auto-revue : Agent Claude Code (`revue-cartes`). Le statut éditorial reste
`redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SVD-001 | Confirmé (Ceres, rang) ; « petites valeurs singulières identifient les combinaisons » imprécis : ce sont les vecteurs singuliers droits | Utile | Famille raisonnement, mais la question demandait un diagnostic sans relation | Recouvre CV-SVD-004 | Important | Relation $\delta\hat x$ au noyau ; exemple exécuté |
| CV-SVD-002 | Confirmé à rang colonne plein (Eigen) | Utile | Objectif « choisir », question « pourquoi éviter » : un seul côté de la décision | Recto en `AᵀA` Unicode ; adresse Eigen redirigée (301) | Important | Question de décision ; cas BA creux (Ceres) |
| CV-SVD-003 | Confirmé (Ceres : $S^{-1/2}f$) ; « cohérente avec les unités » imprécis | Utile | Noyau net | Accord fiche | Mineur | Formulation « sans dimension » |
| CV-SVD-004 | Diagnostic déduit, non contredit | Utile | Famille diagnostic sans test discriminant | Recouvre CV-SVD-001 et CV-HOMOGRAPHIE-006 | Important | Contrôles discriminants ; cas DEGENSAC |

### Fiche

- Mineur (FR-036) : les propriétés numériques n'étaient sourcées que par des
  documentations d'implémentation (Eigen, Ceres). Hartley 1997 et
  Chum et al. 2005 sont ajoutés. Un manuel d'analyse numérique, comme Golub et
  Van Loan, n'a pas pu être consulté.
- Mineur : la relation de sensibilité et le choix de solveur en grand
  problème creux manquaient pour soutenir les cartes corrigées.

### Longueur

Les réponses corrigées comptent 169 à 184 mots selon l'inventaire, contre
139 au plus ailleurs dans le vault. Le noyau reste à trois points notables ;
l'essentiel de l'excédent vient des formules et de l'approfondissement.
Mesurer la charge réelle en révision avant de raccourcir davantage.

## Corrections appliquées

- `vault/10-mathematiques-estimation/references/11-moindres-carres-svd.md`,
  révision 3 : relation $\delta\hat x=\sum_i(u_i^T\delta b/\sigma_i)v_i$ et
  dépendance de $\kappa_2$ aux unités ; arbitrage QR/SVD/équations normales
  selon Eigen et Ceres, dont `DENSE_QR`, `DENSE_NORMAL_CHOLESKY` et les
  solveurs de Schur ; calcul exécuté de sensibilité ; tests départageant
  outliers résiduels et quasi-dégénérescence ; théorème du plan dominant ;
  sources Eigen (nouvelle adresse), Ceres Solving, Chum 2005, Hartley 1997.
- `vault/10-mathematiques-estimation/11-moindres-carres-svd.md` :
  - CV-SVD-001 : question et noyau centrés sur la relation de sensibilité ;
  - CV-SVD-002 : question de décision à deux côtés ;
  - CV-SVD-003 : « sans dimension » ;
  - CV-SVD-004 : contrôles discriminants et cas publié.
- Journal de correction de `vault/01-Parcours/Suivi-pilote.md` : une ligne
  par carte corrigée.

Aucune carte d'un autre thème ne reprenait une affirmation corrigée (`grep`
sur équations normales, `A^TA`, `J^TJ` et conditionnement).

## Enrichissements acceptés et appliqués

L'apprenant a accepté toutes les propositions ci-dessous le 2026-10-23. Elles
sont rédigées en révision 4 de la fiche :

- CV-SVD-005 à 009 ajoutées, avec `Provenance : agent` ;
- exemple chiffré m/mm dans CV-SVD-003 ;
- Triggs et al. 2000, §4.3, ajouté comme source scientifique de CV-SVD-002 ;
- sections de la fiche : système homogène, DLT et normalisation ; moindres
  carrés non linéaires et pertes robustes ; incertitude des paramètres ;
  variation contrôlée brut/normalisé ; chaîne usuelle RANSAC → DLT → LM.

Les totaux d'état courant passent de 233 à 238 cartes : catalogue régénéré,
`docs/vault-layout.md`, `Guide-Anki.md`, contrat Obsidian–Anki et en-tête
« Lot » du suivi. Les résultats datés antérieurs ne sont pas modifiés.

Pour la vérification des nouvelles cartes, Triggs, McLauchlan, Hartley et
Fitzgibbon (2000) ont été lus en texte intégral depuis HAL :

- §3.1 : la dispersion n'approche la covariance qu'asymptotiquement, ce qui
  est moins sûr pour les petits problèmes ;
- §3.3 : robustification sur le résidu pondéré, et erreur de modèle non
  corrigible par nettoyage ;
- §4.2 : amortissement et pas de gradient ;
- §4.3 : Gauss-Newton, et QR jusqu'à deux fois plus lent que les équations
  normales mais bien moins sensible au mauvais conditionnement.

Ceres ne présente pas $(J^TJ)^{-1}$ comme une approximation ; la nuance
asymptotique vient de Triggs et al.

Longueur : les neuf réponses comptent entre 133 et 223 mots selon
l'inventaire. CV-SVD-006 est la plus longue ; son noyau compte trois points.
Mesurer en révision réelle avant de raccourcir.

Table des propositions telle que soumise :

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| CV-SVD-005 : DLT, solution de $Lh=0$ sous $\|h\|=1$ par le vecteur singulier droit de $\sigma_{\min}$, deux équations par correspondance, puis raffinement géométrique | Aucune carte du vault sur la DLT, pourtant à la base de l'homographie, de $F$, de la triangulation et de Zhang | algorithme | 1 carte ; noyau à 3 points | Zhang 1998, annexe A ; Hartley 1997, §2 |
| CV-SVD-006 : normalisation de Hartley et pourquoi elle change la solution des moindres carrés, pas seulement les arrondis | Normalisation seulement citée, sans source, dans CV-HOMOGRAPHIE-002 | raisonnement | 1 carte ; noyau à 3 points | Hartley 1997, §§3–5 et 7.3.1 ; Zhang 1998, annexe A ; calcul exécuté du projet |
| CV-SVD-007 : Gauss-Newton et Levenberg-Marquardt, initialisation linéaire puis raffinement | Aucun solveur non linéaire dans le vault, alors que calibration, PnP raffiné et BA en dépendent | comprehension | 1 carte ; noyau à 3 points | Ceres, Solving, Levenberg-Marquardt ; Zhang 1998, §3.2 |
| CV-SVD-008 : perte robuste appliquée au résidu blanchi, échelle $a$ et complémentarité avec RANSAC | « Estimation robuste » annoncée par l'index du thème, aucune carte sur Huber ou Cauchy | pratique | 1 carte ; noyau à 3 points | Ceres, Modeling, LossFunction ; Ceres, Covariance, Introduction |
| CV-SVD-009 : covariance des paramètres $(J^TJ)^{-1}$, conditions et jauge | « Incertitude » annoncée par l'index ; proposition du 2026-10-18 restée en attente | evaluation | 1 carte ; noyau à 3 points | Ceres, Covariance Estimation : Introduction, Gauge Invariance, Rank of the Jacobian |
| CV-SVD-003 : exemple chiffré m → mm | Carte juste mais abstraite | approfondissement seul | aucun nouveau rappel | calcul exécuté du projet |
| Fiche : sections DLT et normalisation, non linéaire, pertes robustes, covariance ; variation contrôlée brut/normalisé (FR-033) | Rubriques absentes | Mathématiques, Évaluation, Sources | sans carte | Hartley 1997 ; Zhang 1998 ; Ceres |

Calculs déjà exécutés pour ces propositions, hors dépôt, Python 3.10.13 et
NumPy 2.2.6, cas construits et non mesures terrain :

- DLT d'homographie, 200 tirages par configuration, bruit 0,5 px :
  - 50 points sur une image 1920×1080 : $\sigma_1/\sigma_8$ médian
    $8{,}3\cdot10^6$ brut contre 4,1 normalisé ; erreur médiane sur l'image
    entière 0,22 px contre 0,20 px ;
  - 20 points concentrés dans un carré de 200 px en coin : $1{,}4\cdot10^8$
    contre 3,5 ; erreur médiane 1013 px contre 28 px.
  La normalisation compte surtout quand les points sont loin de l'origine par
  rapport à leur étendue ; elle ne supprime pas l'erreur d'extrapolation.
- Blanchiment : $r_{px}=0{,}8$, $\sigma_{px}=0{,}5$, $r=3$ mm,
  $\sigma=2$ mm. Somme brute 0,64 en mètres, 9,64 en millimètres ; somme
  blanchie 4,81 dans les deux cas.

## Sources

- [Ceres, Covariance Estimation (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) :
  hypothèse de covariance identité et mise à l'échelle $S^{-1/2}f$,
  rang plein, pseudo-inverse, jauge, exemple de jacobien presque singulier
  sous `min_reciprocal_condition_number`.
- [Ceres, Solving Non-linear Least Squares (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_solving.html) :
  Levenberg-Marquardt comme version régularisée de Gauss-Newton,
  `DENSE_QR`, `DENSE_NORMAL_CHOLESKY`, solveurs de Schur et leurs échelles.
- [Ceres, Modeling Non-linear Least Squares (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html) :
  `LossFunction`, conditions sur $\rho$, Huber, SoftLOne, Cauchy, échelle $a$.
- [Eigen 5.0.1-dev, Solving linear least squares systems](https://libeigen.gitlab.io/eigen/docs-nightly/group__LeastSquares.html) :
  conditionnement au carré, perte d'environ deux fois plus de chiffres,
  rapidité pour $A$ haute et étroite. L'ancienne adresse
  eigen.tuxfamily.org renvoie une redirection 301 vers cette page.
- [Zhang 1998, MSR-TR-98-71](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf),
  §3.2 et annexe A : DLT par vecteur singulier, mauvais conditionnement,
  normalisation, raffinement Levenberg-Marquardt.
- [Hartley 1997, IEEE TPAMI 19(6)](https://doi.org/10.1109/34.601246), §§3–5
  et 7.3 : dénormalisation, non-invariance de la solution, rapport
  $d_1/d_8$, normalisation isotrope à distance moyenne $\sqrt2$, gain de
  conditionnement d'environ $10^8$ sur la paire « house ». Version de
  l'éditeur payante ; passages lus sur une copie hébergée par l'Université
  de Crète.
- [Triggs, McLauchlan, Hartley et Fitzgibbon 2000, HAL inria-00548290](https://inria.hal.science/inria-00548290),
  §§3.1, 3.3, 4.2 et 4.3, texte intégral.
- [Chum, Werner et Matas 2005](https://dspace.cvut.cz/bitstream/10467/9495/1/2005-Two-view-geometry-estimation-unaffected-by-dominant-plane.pdf) :
  résumé consulté via ML Anthology ; le texte intégral du dépôt CVUT n'a pas
  été lu. Le théorème cité est celui du résumé.

## Contrôles et limites

- Après corrections : `check_vault.py` OK, 125 Markdown, 52 fiches,
  233 cartes ; 34 tests réussis ; catalogue à jour.
- Après ajouts : `check_vault.py` OK, 125 Markdown, 52 fiches, 238 cartes ;
  34 tests réussis ; `sync_catalog.py` régénéré puis `--check` sans document
  périmé sur 18.
- Inventaire comparé à l'état initial : seuls CV-SVD-005 à 009 apparaissent ;
  aucun ID disparu, aucune identité Anki modifiée. Les cartes du sujet n'ont
  pas encore d'identité Anki.

Context7 n'est pas disponible dans cette session : documentations officielles
consultées directement. Non vérifiés : export Anki réel, rendu Obsidian et
AnkiDroid, maîtrise de l'apprenant, validation scientifique indépendante.
