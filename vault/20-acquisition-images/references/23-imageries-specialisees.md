---
id: CV-IMAGERIES
type: comparaison
domaine: d02
poles: [E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 3
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d02]
---
# Line-scan, télédétection et volumes médicaux

## Problème, données et hypothèses

Comprendre des contrats d'acquisition spécialisés avant d'appliquer un réseau 2D. Comparaison d'entrées : lignes synchronisées au mouvement, bandes multispectrales/SAR, volumes avec espacement/orientation physique. La fiche introduit ces familles ; elle ne constitue pas une maîtrise de chaque modalité.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Line-scan reconstruit une image au fil du déplacement ; une optique télécentrique vise à limiter certains changements de grandissement sur sa plage conçue. Une image géoréférencée porte une transformation vers des coordonnées terrestres. Un volume médical possède axes, espacement et orientation ; l'ordre du tableau n'est pas le repère patient.

## Mathématiques, conventions et unités

Un espacement voxel $(s_x,s_y,s_z)$ en mm transforme un déplacement d'indices en longueur physique. Des pixels ou voxels anisotropes rendent des distances en indices trompeuses. Un affine géospatial ou volumique doit conserver axe, unité et convention ; une coordonnée latitude/longitude n'est pas une distance euclidienne en mètres.

## Paramètres et propriétés

Préciser calibration line-scan/encodeur, bandes et normalisation, résolution au sol, no-data, axes et espacement. DICOM/NIfTI sont des formats avec métadonnées, pas des garanties d'annotations cohérentes ou d'utilité clinique.

## Coût et implémentation

Grandes mosaïques et volumes nécessitent tuilage avec recouvrement et restitution des coordonnées. Aucun fichier patient ou géospatial réel n'est chargé ici ; aucun résultat clinique n'est revendiqué.

## Évaluation et variation contrôlée

Variation proposée : rééchantillonner un volume anisotrope ou modifier la vitesse du convoyeur. Prédire les erreurs si la transformation n'est pas propagée ; vérifier une longueur connue et les raccords de tuiles.

## Échecs et diagnostic

Distances de contour incohérentes : vérifier espacement et orientation. Artefacts aux raccords : contrôler padding, recouvrement et fusion. Dégradation saisonnière : distinguer acquisition et distribution des labels.

## Alternatives et usages

Choisir une représentation selon la tâche et les unités ; une bonne segmentation ne prouve ni géoréférencement exact ni précision de métrologie.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent géométrie physique, line-scan et unité de généralisation. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-IMAGERIES-001

**Question de travail** : Pourquoi HD95 ne doit-il pas être calculé aveuglément en indices de voxels sur une IRM anisotrope ?

**Réponse de référence** : Les axes peuvent avoir des espacements physiques différents ; convertir les distances dans le repère et l’unité annoncés.

**Exemple analytique** : avec un espacement de 0,5 mm, 0,5 mm et 3 mm, un déplacement d'un indice vaut 0,5 mm sur les deux premiers axes, mais 3 mm sur le troisième. Pour des axes orthogonaux, une différence d'indices $\Delta i$ se convertit en distance par $\sqrt{\sum_k(s_k\Delta i_k)^2}$, où $s_k$ est l'espacement de l'axe. Les conventions d'orientation et de position déterminent ensuite le repère commun.

**Conséquence pour l'évaluation** : un calcul de distance entre surfaces doit utiliser une géométrie physique cohérente pour les deux masques. Une permutation d'axes ou un rééchantillonnage oublié peut modifier le résultat sans changement de segmentation. Vérifier une distance connue et annoncer l'unité dans le rapport. Le percentile choisi et le traitement des masques vides appartiennent au protocole ; aucune valeur isolée ne constitue ici une conclusion clinique.

### Cas lié à CV-IMAGERIES-003

**Question de travail** : Pourquoi des tuiles voisines réparties aléatoirement entre entraînement et test peuvent-elles surestimer la généralisation en télédétection ?

**Réponse de référence** : Elles partagent scène, texture et contexte ; le test peut ressembler à l’entraînement au-delà du scénario futur visé.

**Pourquoi le split peut tromper** : des tuiles distinctes peuvent contenir les mêmes bâtiments, le même fond ou une partie d'une image commune. Même sans recouvrement exact, un site partage acquisition, saison et matériaux. Le modèle peut donc réussir en reconnaissant un environnement déjà rencontré, alors que le produit doit fonctionner dans une autre région.

**Protocole proposé** : définir d'abord la généralisation recherchée : nouvelles positions du même site, nouvelle date ou nouveau territoire. Regrouper les données selon cette unité avant le tuilage, contrôler les empreintes géographiques et réserver un test qui représente cet usage. Comparer les résultats par site et saison plutôt que seulement la moyenne globale. Un split géographique plus difficile n'est pas automatiquement plus représentatif : il doit correspondre au besoin annoncé. Le risque décrit est un raisonnement méthodologique, pas une mesure de fuite établie sur tous les jeux de télédétection.

**Repère documentaire de cette passe** : [DICOM, Image Plane Module](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html), §C.7.6.2.1.1, position, orientation et pixel spacing. Les autres développements figurent dans les [cartes associées](../23-imageries-specialisees.md).

## Sources et cartes

- [Basler, GigE Line Scan Use Cases, Use Case 1 b (v136, 2026-10-01)](https://docs.baslerweb.com/line-scan-gige-use-cases).
- [Edmund Optics, The Advantages of Telecentricity](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/advantages-of-telecentricity/).

La fuite entre tuiles voisines est un risque déduit par le projet, à évaluer selon le scénario de généralisation ; la description SpaceNet contextualise les séries géographiques sans prouver à elle seule ce biais pour tout split.

- [NIfTI, standard et transformations](https://nifti.nimh.nih.gov/nifti-1/).
- [DICOM, standard courant](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html).
- [SpaceNet7, données multi-temporelles](https://www.spacenet.ai/sn7-challenge/).
- [Cartes associées](../23-imageries-specialisees.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
