# Cas de transfert réservés

Douze cas construits, distincts des exemples numériques corrigés. Ne pas lire
les réponses avant la tentative de transfert. Un cas vu en révision n'est plus
un cas inédit : consigner cette exposition et préparer un autre scénario pour
mesurer le transfert. Aucun résultat de l'apprenant n'est rempli à l'avance.

Correction commune : tâche/sorties adéquates, hypothèses et conventions,
choix argumenté, vérification discriminante, limites de conclusion. Tous les
critères applicables doivent être satisfaits ; justifier une non-applicabilité.

## Matching — choix

Une pièce métallique peu texturée doit être repositionnée entre deux vues
avec reflets, budget de calcul mesuré et quelques repères possibles. Quel
pipeline comparer avant de retenir un matcher appris ?

<details><summary>Réponse de référence et critères</summary>

Stabiliser lumière/repères et définir précision/transformations. Comparer une
baseline classique, des marqueurs si possibles et un matching appris sur mêmes
paires, résolution et vérification géométrique. Mesurer couverture, erreurs et
coût complet, y compris les échecs. Un modèle ne rétablit pas une information
visuelle absente. Réussite : observations utiles, modèle compatible, comparaison
équitable et stratégie de rejet explicites.

</details>

## Matching — diagnostic

Des correspondances sont bonnes à gauche mais biaisées à droite depuis une
modification de crop dans une seule branche. Comment isoler le défaut ?

<details><summary>Réponse de référence et critères</summary>

Tracer repères/resize/padding pour chaque image et tester des points connus.
Restituer coordonnées puis examiner résidus spatiaux et modèle physique.
Comparer avant/après prétraitement à matcher inchangé. Ne pas conclure à un
défaut de descripteur depuis le seul score de matching.

</details>

Référence et sources : [matching appris](../40-features-matching/references/44-superpoint-lightglue-loftr.md).

## Calibration/géométrie — choix

Une caméra déjà calibrée doit être localisée par rapport à une pièce 3D
connue, non plane. Quelle inconnue et quel solveur choisir ?

<details><summary>Réponse de référence et critères</summary>

La pose objet→caméra est inconnue ; construire des correspondances 3D–2D puis
choisir une variante PnP et contrôle robuste appropriés, avec unités, chiralité
et validation réservée. L'homographie d'un plan ne décrit pas toute la pièce.
Comparer précision utile et ambiguïtés ; aucune précision n'est déduite du
seul nombre de points.

</details>

## Calibration/géométrie — diagnostic

Une caméra métrique fonctionne mais toutes les translations de pose changent
d'un facteur après remplacement du fichier de mire. Que vérifier ?

<details><summary>Réponse de référence et critères</summary>

Inspecter taille des carrés, unité et ordre des points 3D, sans confondre
intrinsèques pixel et translations métriques. Rejouer une pose et une dimension
de référence indépendantes ; distinguer changement d'unité et changement
physique. Un petit résidu pixel peut persister malgré une échelle fausse.

</details>

Référence et sources : [PnP/géométrie](../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md).

## Tracking — choix

Suivre des colis d'apparence identique vus par caméra mobile avec pertes
brèves de détection. Quelles hypothèses comparer avant un ReID générique ?

<details><summary>Réponse de référence et critères</summary>

Définir cadence/IDs, mesurer détecteur et ego-motion, comparer mouvement et
seconde association faible-score à une apparence évaluée dans ce domaine.
Prévoir pertes, incertitude et cycle de vie ; des colis identiques peuvent
ne pas être distinguables par apparence. Mesurer association et coût avec mêmes
détections/séquences, pas AP seulement.

</details>

## Tracking — diagnostic

Les IDs se fragmentent après changement de cadence, sans modification visible
du détecteur. Quels journaux discriminent temps, association et expiration ?

<details><summary>Réponse de référence et critères</summary>

Conserver timestamps, appels même sans détections, prédictions, gating,
associations et âges. Vérifier unité de vitesse et durées de vie exprimées en
frames ; comparer une perturbation contrôlée de cadence. Une hausse aveugle
de max_age ne démontre pas la cause ni la continuité réelle.

</details>

Référence et sources : [association](../110-tracking-association/references/112-deepsort-bytetrack.md).

## Détection — choix

Un détecteur de petits défauts doit traiter de grandes images sous budget
mémoire. Quelle comparaison entre resize global et tuilage construire ?

<details><summary>Réponse de référence et critères</summary>

Fixer taille critique et tolérance ; comparer résolution effective, tuiles
avec recouvrement et restitution des coordonnées. Mesurer défauts manqués,
doublons/raccords et coût complet à seuils figés. Séparer qualité du modèle
et défauts de posttraitement ; aucun avantage n'est universel.

</details>

## Détection — diagnostic

Les prédictions sont bonnes dans les crops, mais certaines boîtes finales sont
décalées et disparaissent près des raccords. Quelle enquête mener ?

<details><summary>Réponse de référence et critères</summary>

Tracer crop/padding/resize vers l'image globale, visualiser propositions avant
NMS et doublons de tuiles, contrôler masque de zone valide. Tester une image à
objet connu traversant un raccord. Ne pas attribuer directement l'erreur au
backbone ; mesurer ensuite le protocole complet.

</details>

Référence et sources : [détection](../80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md).

## Segmentation classique — choix

Des cellules de tailles variables se touchent sous illumination inhomogène.
Quelle baseline classique et quelle mesure tester avant un réseau ?

<details><summary>Réponse de référence et critères</summary>

Comparer correction d'éclairage/seuillage local, marqueurs et séparation,
avec annotations d'instances. Examiner variations de taille et contact ; Otsu
global ne suit pas nécessairement la sémantique. Mesurer fusions/séparations et
limites ; un réseau peut être justifié si le modèle classique reste insuffisant.

</details>

## Segmentation classique — diagnostic

Le masque foreground couvre toutes les cellules mais watershed produit trop
de fragments sur leurs surfaces texturées. Comment isoler le problème ?

<details><summary>Réponse de référence et critères</summary>

Visualiser topographie et germes, comparer sur copie avec marqueurs manuels,
contrôler maxima parasites et échelle morphologique. Départager mauvais masque
et sur-segmentation de germes ; valider par instances et tailles, sans conclure
de la seule IoU foreground.

</details>

Référence et sources : [watershed](../90-segmentation/references/91-otsu-distance-watershed.md).

## Recalage 3D — choix

Deux scans partiellement recouvrants d'un objet inconnu ont un grand décalage
initial. Quel ordre de traitement et quelle preuve de pose prévoir ?

<details><summary>Réponse de référence et critères</summary>

Vérifier unités/repères, réduire si utile, estimer features et initialisation
globale puis raffiner localement avec variante ICP adaptée. Mesurer recouvrement,
résidus et pose de référence ; tester symétries et zones indépendantes. Le faible
RMSE seul ne garantit pas le bon minimum.

</details>

## Recalage 3D — diagnostic

Une grande plaque plane donne des résidus point-to-plane très faibles tandis
que sa position tangentielle varie entre essais. Est-ce nécessairement un bug ?

<details><summary>Réponse de référence et critères</summary>

Tester les directions contraintes : un plan fournit peu d'information sur
certains glissements/rotations. Ajouter géométrie, points distinctifs ou autre
capteur selon le besoin ; examiner conditionnement et référence. Changer
seulement le nombre d'itérations ne crée pas l'information manquante.

</details>

Référence et sources : [recalage global/ICP](../60-vision-3d/references/62-recalage-global-icp.md).

[Accueil](../00-Accueil.md) · [Journal des tentatives](Suivi-pilote.md).
