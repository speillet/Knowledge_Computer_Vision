---
id: CV-STEREO
type: methode
domaine: d06
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
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

Cas rectifié idéal : $Z=fB/d$, f et d en pixels, baseline B en mètres et Z en mètres. Pour petite incertitude, $\sigma_Z\approx fB\sigma_d/d^2$. Utiliser la matrice Q pour la géométrie rectifiée générale. Une disparité entière fixe SGBM OpenCV peut être stockée multipliée par 16 : convertir selon le contrat avant reprojection.

## Paramètres et propriétés

Plage de disparités, bloc, pénalités, cohérence gauche/droite et masque invalides. Ne pas traiter d≤0 comme une profondeur numérique ordinaire. Texture répétée et surfaces brillantes peuvent produire un minimum de coût faux.

## Coût et implémentation

Résolution × plage de recherche × agrégation dominent temps/mémoire. Aucun StereoSGBM exécuté ; les paramètres et formats ont été confrontés à OpenCV 4.13.

## Évaluation et variation contrôlée

Exemple analytique : f=1000 px, B=0,2 m, d=20 px donne 10 m ; d=10 px donne 20 m. À erreur de disparité identique, la profondeur lointaine est plus sensible. Mesurer sur distances connues et régions invalides.

## Échecs et diagnostic

Profondeurs globalement ×16 : inspecter format de disparité. Erreurs aux bords d'objet : distinguer occlusion et défaut de rectification. Mauvais résultat loin ne prouve pas un manque de capacité réseau.

## Alternatives et usages

Stéréo apprise, capteur actif ou profondeur monoculaire selon précision, coût et conditions ; une prédiction monoculaire n'a pas automatiquement une échelle métrique fiable.

## Sources et cartes

- [OpenCV StereoSGBM, description et compute](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html).
- [OpenCV reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Cartes associées](../61-stereo-profondeur.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
