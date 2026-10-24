---
id: CV-STEREO
type: methode
domaine: d06
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-EPIPOLAIRE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d06]
---
# Stéréo rectifiée, SGM et profondeur

## Problème, données et hypothèses

Estimer la profondeur à partir de deux images calibrées. Entrées : vues gauche/droite synchronisées, rectification et baseline ; sortie : disparité puis profondeur avec masque de validité. La texture, l'occultation et la précision des correspondances limitent la reconstruction.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

La rectification organise les recherches selon les lignes épipolaires. Un coût de matching compare candidats ; SGM agrège des chemins avec pénalités de variation. SGBM d'OpenCV est une variante à documenter, pas tous les détails de l'article original.

## Mathématiques, conventions et unités

Cas rectifié horizontal idéal avec points principaux de même abscisse et $d=x_g-x_d>0$ : $Z=fB/d$, f et d en pixels, baseline B en mètres et Z en mètres. Pour petite incertitude, $\sigma_Z\approx fB\sigma_d/d^2$. Utiliser la matrice Q pour la géométrie rectifiée générale. Une disparité entière fixe SGBM OpenCV peut être stockée multipliée par 16 : convertir selon le contrat avant reprojection.

## Paramètres et propriétés

Plage de disparités, bloc, pénalités, cohérence gauche/droite et masque invalides. Dans ce cas simplifié, $d\le0$ ne donne pas une profondeur avant finie valide. Dans le cas général, utiliser Q et le masque du matcher : le signe de la disparité seul ne définit pas la validité, notamment si la rectification décale les points principaux. Texture répétée et surfaces brillantes peuvent produire un minimum de coût faux.

## Coût et implémentation

Résolution × plage de recherche × agrégation dominent temps/mémoire. Aucun StereoSGBM exécuté ; les paramètres et formats ont été confrontés à OpenCV 4.13.

## Évaluation et variation contrôlée

Exemple analytique : f=1000 px, B=0,2 m, d=20 px donne 10 m ; d=10 px donne 20 m. À erreur de disparité identique, la profondeur lointaine est plus sensible. Mesurer sur distances connues et régions invalides.

## Échecs et diagnostic

Profondeurs globalement ×16 : inspecter format de disparité. Erreurs aux bords d'objet : distinguer occlusion et défaut de rectification. Mauvais résultat loin ne prouve pas un manque de capacité réseau.

## Alternatives et usages

Stéréo apprise, capteur actif ou profondeur monoculaire selon précision, coût et conditions ; une prédiction monoculaire n'a pas automatiquement une échelle métrique fiable.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent disparité, incertitude de profondeur et géométrie rectifiée. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-STEREO-001

**Question de travail** : En stéréo rectifiée horizontale avec points principaux de même abscisse, pour f=1000 px, baseline 0,2 m et disparité gauche−droite 20 px, quelle profondeur ?

**Réponse de référence** : 10 m par $Z=fB/d$.

**Dérivation d'unités** : le quotient $f/d$ est sans unité si les deux grandeurs utilisent les pixels de la même grille rectifiée ; le résultat conserve donc l'unité de la baseline. La différence de coordonnées traduit la séparation des deux rayons pour un point donné. Une faible disparité correspond ici à une grande profondeur.

**Exemple de contrôle** : vérifier une cible à distance connue, puis doubler artificiellement la valeur de la baseline dans le calcul : la profondeur calculée doublerait aussi. Cela aide à localiser une erreur d'échelle sans modifier le matcher. La formule simplifiée suppose les points principaux alignés comme annoncé et une disparité physique valide. Une région occultée ou un mauvais match peut produire un nombre positif sans profondeur correcte. En géométrie rectifiée plus générale, utiliser la transformation de reprojection et ses conventions plutôt qu'appliquer cette formule à toute sortie appelée disparité.

### Cas lié à CV-STEREO-004

**Question de travail** : La rectification garantit-elle une correspondance correcte à chaque pixel ?

**Réponse de référence** : Non : elle simplifie la géométrie de recherche ; texture, répétition et occlusion peuvent encore rendre le matching ambigu.

**Ce que la rectification change** : elle réorganise les images pour simplifier les lieux de recherche compatibles avec la géométrie. Elle ne crée pas de texture et ne rend pas visible une surface cachée dans l'une des caméras. La recherche le long d'une ligne peut donc encore contenir plusieurs candidats ou aucun correspondant réel.

**Exemple construit** : une surface uniforme offre des coûts proches pour beaucoup de disparités ; une texture périodique peut favoriser la mauvaise période ; au bord d'un objet, un point peut n'être vu que d'un côté. Une régularisation peut sélectionner une valeur dans ces régions, mais cette valeur n'est pas une nouvelle observation. Conserver une information de validité et tester les cohérences disponibles, puis évaluer sur une référence indépendante. Distinguer densité de la carte produite et quantité de profondeur réellement fiable évite d'interpréter tout pixel rempli comme une mesure.

**Repère documentaire de cette passe** : [OpenCV 4.13, Depth Map from Stereo Images](https://docs.opencv.org/4.13.0/dd/d53/tutorial_py_depthmap.html), relation profondeur–disparité et correspondance. Les autres développements figurent dans les [cartes associées](../61-stereo-profondeur.md).

## Sources et cartes

- [OpenCV StereoSGBM, description et compute](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html).
- [OpenCV reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Cartes associées](../61-stereo-profondeur.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
