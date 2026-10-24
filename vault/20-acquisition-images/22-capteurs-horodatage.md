# Capteurs, rolling shutter et synchronisation — cartes

Fiche : [[20-acquisition-images/references/22-capteurs-horodatage|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-CAPTEURS-001

Objectif : séparer exposition et lecture rolling shutter. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-CAPTEURS-001
Question: Une exposition très courte suffit-elle à supprimer toute déformation rolling shutter ?
Reponse: **Noyau attendu** : Non : elle réduit le flou par ligne, mais les lignes peuvent encore représenter des instants différents.

**Approfondissement** : Mesurer durée de lecture, mouvement et type de shutter ; tester global shutter ou correction adaptée.

**Décomposition du phénomène** : l'exposition décrit la durée pendant laquelle une ligne accumule la lumière ; le temps de lecture détermine le décalage entre lignes. Une scène mobile peut donc produire des lignes individuellement nettes mais prises à des positions différentes. Dans un exemple construit, une mire verticale qui se déplace horizontalement peut apparaître inclinée, sans flou marqué sur ses bords.

**Vérification proposée** : comparer immobilité, translation et rotation, puis faire varier séparément exposition et durée de lecture lorsque le matériel le permet. Si le raccourcissement de l'exposition améliore la netteté sans supprimer l'inclinaison, les deux effets ont bien été distingués. Un global shutter modifie la simultanéité de capture ; il ne garantit pas une exposition assez courte ni une bonne synchronisation avec un autre capteur. Le modèle de projection utilisé pour la calibration doit rester compatible avec l'acquisition réelle.

**Erreurs bloquantes** : Confondre netteté de chaque ligne et simultanéité de toute l’image.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Fiche complète]] ; [Basler, Electronic Shutter Types, Rolling Shutter (v136, 2026-10-01)](https://docs.baslerweb.com/electronic-shutter-types#rolling-shutter).
Tags: cv::pilote cv::d02 famille::comparaison cv_id::CV-CAPTEURS-001 provenance::agent pole::B pole::C pole::E pole::F
END

## CV-CAPTEURS-002

Objectif : estimer un décalage temporel spatial. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-CAPTEURS-002
Question: Deux capteurs voient un objet à 2 m/s avec 50 ms de décalage. Quel ordre de grandeur d’erreur temporelle en translation uniforme ?
Reponse: **Noyau attendu** : 0,10 m, avant effets de rotation et d’estimation.

**Approfondissement** : Le calcul sert à départager timing et bruit spatial ; annoncer l’horloge et le mouvement supposés.

**Calcul et interprétation** : convertir d'abord 50 ms en 0,050 s, puis appliquer $\Delta x=v\Delta t$. Le résultat mesure la distance parcourue pendant l'écart de capture ; il ne s'agit ni d'une variance ni d'une erreur de calibration constante. Si la vitesse double, ce terme double dans le modèle annoncé. Si l'objet est immobile, le même retard peut devenir invisible dans ce contrôle.

**Usage en diagnostic** : comparer l'ordre de grandeur obtenu à l'écart observé avant de raffiner une extrinsèque. Un décalage qui varie avec la vitesse est compatible avec un problème temporel. Cela ne prouve pas que l'horloge soit l'unique cause : il faut aussi vérifier quel instant représente le timestamp et si la latence est constante. Pour exprimer le décalage en pixels, il faudrait encore la profondeur, le mouvement relatif et le modèle de projection.

**Erreurs bloquantes** : Utiliser ce modèle pour toute scène en rotation sans autre hypothèse.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Fiche complète]] ; [Basler, Electronic Shutter Types, Rolling Shutter (v136, 2026-10-01)](https://docs.baslerweb.com/electronic-shutter-types#rolling-shutter) ; calcul cinématique $v\Delta t$ du projet.
Tags: cv::pilote cv::d02 famille::raisonnement cv_id::CV-CAPTEURS-002 provenance::agent pole::B pole::C pole::E pole::F
END

## CV-CAPTEURS-003

Objectif : départager calibration et temps. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-CAPTEURS-003
Question: Cas C — diagnostic : les obstacles caméra–LiDAR se dédoublent en virage mais semblent alignés à l’arrêt. Quelle enquête mener ?
Reponse: **Noyau attendu** : Vérifier offsets/dérive des horloges, temps par point du scan, deskew puis extrinsèques dans le même repère. Comparer séquences immobiles et mouvements contrôlés.

**Approfondissement** : Le mouvement rend visible un défaut temporel ; une calibration spatiale peut aussi être fausse. Mesurer résidus selon vitesse et rotation avant de choisir une correction.

**Raisonnement discriminant** : une extrinsèque décrit une transformation spatiale fixe ; un défaut temporel associe des observations de poses différentes. Une translation compensatrice peut faire coïncider un virage donné tout en dégradant le virage opposé. Le deskew ramène les points d'un scan à un temps commun à partir d'un mouvement estimé : il ne fonctionne correctement que si ses timestamps et son modèle sont cohérents.

**Protocole construit** : enregistrer une scène statique vue par le véhicule à l'arrêt, en translation puis en rotation dans les deux sens. Tracer les résidus selon le temps dans le scan et la vitesse angulaire. Comparer une correction temporelle seule, une correction spatiale seule et leur combinaison, sur une séquence réservée. Un bon alignement à l'arrêt contraint certaines erreurs spatiales, mais ne valide pas la chaîne temporelle ni toutes les configurations géométriques.

**Erreurs bloquantes** : Corriger définitivement par une translation fixe sans examiner les timestamps.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Fiche complète]] ; [Zhang et Singh 2014, LOAM, §§II et V, correction de distorsion de mouvement](https://www.roboticsproceedings.org/rss10/p07.pdf) ; enquête caméra–LiDAR construite par le projet.
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-CAPTEURS-003 provenance::agent pole::B pole::C pole::E pole::F cas_pole::C::diagnostic
END

## CV-CAPTEURS-004

Objectif : interpréter les sorties de capteurs. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-CAPTEURS-004
Question: Pourquoi une mesure Doppler radar ne se substitue-t-elle pas directement à une vitesse cartésienne 3D ?
Reponse: **Noyau attendu** : Elle contraint la composante radiale relativement au capteur selon son modèle de mesure.

**Approfondissement** : Transformer repères et mouvement ego, puis fusionner d’autres observations pour les composantes non mesurées. Les covariances doivent suivre la transformation.

**Modèle de mesure** : si $\hat r$ est le vecteur unitaire du capteur vers la cible et $v_{rel}$ sa vitesse relative dans le même repère, la mesure idéale contraint $v_r=\hat r^Tv_{rel}$, avec une convention de signe à annoncer. C'est une projection scalaire. Toute composante orthogonale à $\hat r$ peut changer sans modifier cette mesure instantanée.

**Exemple construit** : une cible qui traverse latéralement le champ peut avoir une vitesse importante et une composante radiale faible à un instant donné. Conclure qu'elle est immobile serait donc injustifié. Pour retrouver davantage de composantes, exploiter d'autres directions, plusieurs instants ou d'autres capteurs avec un modèle dynamique explicite. Si le porteur bouge, son propre mouvement contribue à la vitesse relative. Une fusion doit traiter cette contribution et l'incertitude de la mesure, plutôt que recopier le scalaire Doppler dans trois axes.

**Erreurs bloquantes** : Prendre une vitesse radiale pour les trois composantes du mouvement.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Fiche complète]] ; [Texas Instruments, TIDUF01 (2021), §2.4.9](https://www.ti.com/lit/ug/tiduf01/tiduf01.pdf).
Tags: cv::pilote cv::d02 famille::comprehension cv_id::CV-CAPTEURS-004 provenance::agent pole::B pole::C pole::E pole::F
END
