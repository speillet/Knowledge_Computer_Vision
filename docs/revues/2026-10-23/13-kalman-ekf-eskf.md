# Revue — Kalman, EKF, UKF et ESKF pour la fusion — 2026-10-23

## Synthèse

Quatre cartes auditées, plus leur fiche. Aucune affirmation fausse, mais
trois constats importants :

- une source UKF jamais lue depuis la première revue ;
- un noyau d'innovation normalisée sans la loi du $\chi^2$, que sa propre
  source donne pourtant ;
- une carte « diagnostic » sans symptôme.

Les corrections sont appliquées : fiche en révision 3, IDs et objectifs
inchangés. Les trois enrichissements proposés ont été acceptés et rédigés en
révision 4 : le sujet passe de 4 à 6 cartes, et CV-FUSION-004 est enrichie.

Auto-revue : Agent Claude Code (`revue-cartes`). Statut éditorial `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FUSION-001 | UKF non vérifiable jusqu'ici, puis confirmé (Julier et Uhlmann 1997, §3) ; « ESKF utilise un EKF » imprécis : Solà applique la prédiction et la jacobienne d'un EKF à l'erreur | Utile | Noyau net | Source marquée « à vérifier » depuis le 2026-10-18 | Important | Source lue ; formulation précisée ; nuance moyenne/covariance |
| CV-FUSION-002 | Confirmé, mais la loi du $\chi^2$ et le seuil étaient omis ; « sans unité lorsque cohérent » imprécis | Forte : base du gating | Noyau trop vague pour « interpréter » | Lien absent avec le gating de DeepSORT (CV-ASSOCIATION) | Important | $\chi^2_m$, quantile, gating DeepSORT, sur/sous-confiance |
| CV-FUSION-003 | Confirmé (Solà, éq. 285–288) | Forte | Recto en « pourquoi ne… pas » qui oriente ; aucun symptôme pour une carte diagnostic | Accord fiche | Important | Symptôme, test discriminant, $G\approx I$ |
| CV-FUSION-004 | Confirmé (Solà, §5.4, annexe E) | Utile | « Une caméra ralentit » vague | Accord fiche | Mineur | Enrichissement proposé plutôt que correction |

## Corrections appliquées

- `vault/10-mathematiques-estimation/references/13-kalman-ekf-eskf.md`,
  révision 3 :
  - UKF et son ordre de précision ;
  - ESKF décrit selon les équations de Solà ;
  - loi du $\chi^2$ et quantiles recalculés ;
  - seuil de DeepSORT ;
  - $G$ et pratique $G=I$ ;
  - sources précisées par équation.
- `vault/10-mathematiques-estimation/13-kalman-ekf-eskf.md` : CV-FUSION-001,
  002 et 003 corrigées ; lien arXiv PDF remplacé par la page de résumé dans
  004.
- Journal : trois lignes.

`grep` sur l'ancienne référence Julier et Uhlmann 2004 : aucune autre
occurrence active dans le vault.

## Enrichissements acceptés et appliqués

Tous acceptés le 2026-10-23 :

- **CV-FUSION-005**, pourquoi l'ESKF ;
- **CV-FUSION-006**, forme de Joseph ;
- **CV-FUSION-004**, enrichie. Raisonnement du projet : à 200 Hz, le
  pas de propagation IMU ne dépend pas de la cadence caméra. La carte vise donc
  les vrais pièges : propagation à pas figé, échantillons IMU perdus et image datée à
  réception.

Notation unifiée sur $R$ ; Solà note $V$ la covariance de mesure. Le total
passe de 240 à 242 cartes ; les compteurs d'état courant sont mis à jour.

Table des propositions telle que soumise :

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| CV-FUSION-005 : pourquoi une formulation à état d'erreur pour l'orientation IMU : erreur minimale, toujours proche de l'origine, petite, lente | Le « pourquoi » de l'ESKF n'est interrogé nulle part, alors qu'il structure tous les VIO filtrants | raisonnement | 1 carte ; noyau à 3 ou 4 points | Solà, §5.1 |
| CV-FUSION-006 : covariance qui perd symétrie ou définie positivité ; forme $(I-KH)P$ instable, forme symétrique ou de Joseph | Bug d'implémentation fréquent, aucune carte | diagnostic | 1 carte ; noyau à 3 points | Solà, §6.1, note 26 |
| CV-FUSION-004 : effet du $\Delta t$ réel sur chaque terme de covariance ; horodatage d'acquisition et non de réception ; mesures en retard | Carte juste mais générique | pratique, enrichissement de la carte | aucun nouveau rappel | Solà, §5.4.2, éq. 262–265, et annexe E, éq. 440 : exponentiel, quadratique, linéaire |
| Fiche : formes de mise à jour de $P$, dépendance au $\Delta t$, avantages de l'ESKF | Rubriques Coût et Paramètres minces | fiche | sans carte | mêmes sources |

## Sources

- [Solà, Quaternion kinematics for the error-state Kalman filter](https://arxiv.org/abs/1711.02508),
  PDF v1 lu en texte intégral :
  - §5.1, quatre avantages ;
  - §5.2 ;
  - §5.4.2, éq. 262–265 ;
  - §6.1, éq. 272–278 et note 26 sur la forme de Joseph ;
  - §6.3, éq. 284–288, et « G = I18 » dans la plupart des implémentations ;
  - annexe E, éq. 438–442.
- [Gamse, Nobakht-Ersi et Sharifi 2014, Sensors 14(10)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/) :
  §2.2.2, éq. 5–10 ; §3.4.2, $m=3$, $\alpha=0{,}05$, seuil 7,815.
- [Julier et Uhlmann 1997, SPIE 3068](https://doi.org/10.1117/12.280797),
  §3, éq. 12–14. DOI vérifié par redirection vers SPIE ; texte lu sur une
  copie de cours hébergée par Berkeley.
- [Wojke, Bewley et Paulus 2017, DeepSORT](https://arxiv.org/abs/1703.07402),
  §2.2 : seuil 9,4877.
- Quantiles du $\chi^2$ recalculés avec SciPy 1.13.1.
- Non vérifiable : Julier et Uhlmann 2004, Proceedings of the IEEE. Il n'est
  plus cité.

## Contrôles et limites

`check_vault.py` OK (240 cartes) après corrections, puis 242 cartes après
ajouts, 34 tests réussis, catalogue régénéré puis à jour. L'inventaire
comparé à l'état initial ne montre que les IDs ajoutés. Context7 n'est pas
disponible dans cette session. Non vérifiés : export Anki, rendu Obsidian et
AnkiDroid, maîtrise, validation indépendante.
