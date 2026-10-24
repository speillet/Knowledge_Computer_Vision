# Line-scan, télédétection et volumes médicaux — cartes

Fiche : [[20-acquisition-images/references/23-imageries-specialisees|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-IMAGERIES-001

Objectif : propager les unités d’un volume. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-IMAGERIES-001
Question: Pourquoi HD95 ne doit-il pas être calculé aveuglément en indices de voxels sur une IRM anisotrope ?
Reponse: **Noyau attendu** : Les axes peuvent avoir des espacements physiques différents ; convertir les distances dans le repère et l’unité annoncés.

**Approfondissement** : Conserver orientation, rééchantillonnage et protocole des masques vides. Une différence d’un voxel n’a pas la même longueur selon l’axe.

**Exemple analytique** : avec un espacement de 0,5 mm, 0,5 mm et 3 mm, un déplacement d'un indice vaut 0,5 mm sur les deux premiers axes, mais 3 mm sur le troisième. Pour des axes orthogonaux, une différence d'indices $\Delta i$ se convertit en distance par $\sqrt{\sum_k(s_k\Delta i_k)^2}$, où $s_k$ est l'espacement de l'axe. Les conventions d'orientation et de position déterminent ensuite le repère commun.

**Conséquence pour l'évaluation** : un calcul de distance entre surfaces doit utiliser une géométrie physique cohérente pour les deux masques. Une permutation d'axes ou un rééchantillonnage oublié peut modifier le résultat sans changement de segmentation. Vérifier une distance connue et annoncer l'unité dans le rapport. Le percentile choisi et le traitement des masques vides appartiennent au protocole ; aucune valeur isolée ne constitue ici une conclusion clinique.

**Erreurs bloquantes** : Comparer des valeurs en voxels et en millimètres comme si elles étaient identiques.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Fiche complète]] ; [DICOM PS3.3, C.7.6.2.1.1, orientation/position et espacement (consulté le 2026-10-18)](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html).
Tags: cv::pilote cv::d02 famille::pratique cv_id::CV-IMAGERIES-001 provenance::agent pole::E
END

## CV-IMAGERIES-002

Objectif : contrôler une acquisition line-scan. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-IMAGERIES-002
Question: Une pièce paraît allongée sur une image line-scan quand la vitesse du convoyeur change. Que tester ?
Reponse: **Noyau attendu** : La synchronisation entre lignes et déplacement, l’encodeur et l’échelle reconstruite dans le sens de mouvement.

**Approfondissement** : Tester une dimension connue à plusieurs vitesses ; distinguer ce défaut du grandissement optique et de la détection.

**Mécanisme et unités** : une caméra line-scan empile des lignes acquises pendant le déplacement. Si la vitesse est $v$ en mm/s et la fréquence de lignes $f_l$ en lignes/s, l'avancement idéal par ligne vaut $v/f_l$ en mm/ligne. L'échelle dans ce sens dépend donc du mouvement, alors que l'autre axe est principalement lié à l'optique et au capteur.

**Exemple construit** : doubler la vitesse à fréquence de lignes constante double l'avancement entre deux lignes ; le nombre de lignes représentant une longueur donnée diminue. L'aspect affiché dépend aussi de l'échelle attribuée à l'image reconstruite. Examiner déclenchement, encodeur, pertes de lignes et métadonnées avant d'interpréter une mesure de longueur. Une mire connue observée à plusieurs vitesses aide à isoler ce défaut d'une erreur de segmentation, mais ne valide pas à elle seule toute la métrologie de la chaîne.

**Erreurs bloquantes** : Réentraîner sans vérifier le contrat spatial de l’image.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Fiche complète]] ; [Basler, GigE Line Scan Use Cases, Use Case 1 b (v136, 2026-10-01)](https://docs.baslerweb.com/line-scan-gige-use-cases).
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-IMAGERIES-002 provenance::agent pole::E
END

## CV-IMAGERIES-003

Objectif : éviter une fuite géographique. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-IMAGERIES-003
Question: Pourquoi des tuiles voisines réparties aléatoirement entre entraînement et test peuvent-elles surestimer la généralisation en télédétection ?
Reponse: **Noyau attendu** : Elles partagent scène, texture et contexte ; le test peut ressembler à l’entraînement au-delà du scénario futur visé.

**Approfondissement** : Séparer régions/dates/sites selon l’usage, contrôler les recouvrements et conserver une évaluation indépendante.

**Pourquoi le split peut tromper** : des tuiles distinctes peuvent contenir les mêmes bâtiments, le même fond ou une partie d'une image commune. Même sans recouvrement exact, un site partage acquisition, saison et matériaux. Le modèle peut donc réussir en reconnaissant un environnement déjà rencontré, alors que le produit doit fonctionner dans une autre région.

**Protocole proposé** : définir d'abord la généralisation recherchée : nouvelles positions du même site, nouvelle date ou nouveau territoire. Regrouper les données selon cette unité avant le tuilage, contrôler les empreintes géographiques et réserver un test qui représente cet usage. Comparer les résultats par site et saison plutôt que seulement la moyenne globale. Un split géographique plus difficile n'est pas automatiquement plus représentatif : il doit correspondre au besoin annoncé. Le risque décrit est un raisonnement méthodologique, pas une mesure de fuite établie sur tous les jeux de télédétection.

**Erreurs bloquantes** : Assimiler séparation de fichiers et indépendance statistique.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Fiche complète]] ; [SpaceNet7, The Problem et The Data (consulté le 2026-10-18)](https://www.spacenet.ai/sn7-challenge/) ; risque de fuite déduit par le projet.
Tags: cv::pilote cv::d02 famille::evaluation cv_id::CV-IMAGERIES-003 provenance::agent pole::E
END
