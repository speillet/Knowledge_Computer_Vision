---
id: CV-MEANSHIFT
type: methode
domaine: d11
poles: ["C", "D", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-SOT", "CV-ACQUISITION"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# MeanShift et CamShift — suivre une distribution d’apparence

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SOT](113-tracking-monoobjet.md), [CV-ACQUISITION](../../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md).
**Compétences visées** : expliquer une itération MeanShift; distinguer MeanShift et CamShift; diagnostiquer un distracteur de couleur; évaluer couleur et adaptation séparément.
Les notions connexes restent des alternatives, pas des dépendances implicites.

## Problème et contrat des données

Suivre une cible initialisée par une fenêtre et un modèle d’apparence, souvent un histogramme de couleur. Chaque frame devient une image de backprojection : les pixels reçoivent un score selon leur compatibilité avec le modèle. Une forte valeur n’est pas une probabilité calibrée d’identité. Même couleur et même objet sont deux notions différentes.

## Mécanisme et mathématiques

MeanShift déplace une fenêtre vers le centre de masse pondéré de la distribution locale, jusqu’à convergence ou arrêt. Pour des scores non négatifs $p(x,y)$, définir $M_{00}=\sum p$, $M_{10}=\sum xp$ et $M_{01}=\sum yp$ dans la fenêtre : le centroïde est $(M_{10}/M_{00},M_{01}/M_{00})$ si $M_{00}>0$. Les coordonnées sont en pixels. Il s’agit d’une recherche locale, pas d’une garantie de maximum global. Dans le tracker MeanShift usuel, la taille de fenêtre reste fixe. CamShift adapte la fenêtre et son orientation à partir des moments de la distribution, puis poursuit le suivi. Un rectangle orienté n’est pas une pose 3D.

## Hypothèses, paramètres et coût

Histogramme, canaux, bins, ROI initiale et masque de saturation/luminance changent la séparation cible/fond. La teinte est instable sur des pixels peu saturés : une simple conversion HSV ne garantit pas une invariance à l’éclairage. Budget d’itérations et déplacement minimal contrôlent l’arrêt. Une fenêtre trop petite perd la cible ; une fenêtre trop grande inclut les distracteurs. Le coût comprend conversion couleur, backprojection et itérations sur la fenêtre. API OpenCV 4.13 vérifiée ; aucun suivi vidéo exécuté.

## Évaluation et variation contrôlée

Baseline proposée : MeanShift à fenêtre fixe ; variation : CamShift sur une séquence où la cible change d’échelle, à histogramme et initialisation identiques. Mesurer overlap, erreur de centre, surface de fenêtre et pertes, en incluant un distracteur de même couleur. Exemple analytique du projet : deux masses 1 et 3 situées à $x=10$ et $x=14$ ont leur centre pondéré à 13 px, pas à 12. Si la masse est nulle, ne pas diviser : déclarer une observation invalide ou appliquer une politique de recherche annoncée.

## Diagnostic et alternatives

Une fenêtre aspirée par le fond demande d’inspecter la backprojection et le contraste d’histogramme avant d’ajouter des itérations. Pendant une occultation, un distracteur peut accumuler plus de masse que la cible. CamShift peut alors agrandir une fenêtre incorrecte ; l’adaptation d’échelle n’est pas une vérification d’identité. Comparer histogrammes mieux séparés, features de texture, filtres de corrélation ou détecteur+association selon les contraintes. Le choix de relance doit être mesuré et explicite.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent backprojection, mode local et adaptation de la fenêtre. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-MEANSHIFT-001

**Question de travail** : Que calcule une itération MeanShift sur une image de backprojection, et que faire si la fenêtre ne contient aucune masse ?

**Réponse de référence** : Calculer le centroïde des scores dans la fenêtre, puis déplacer la fenêtre vers ce centre. Si la masse totale $M_{00}$ est nulle, le centroïde est indéfini : ne pas diviser et appliquer une politique de perte/recherche explicite.

**Lecture des moments** : la backprojection attribue une masse à chaque position selon sa compatibilité avec l'apparence de référence. Le centroïde pondéré donne un déplacement de fenêtre vers cette concentration. Avec deux masses 1 et 3 placées à 10 et 14 pixels, le centre vaut $(10+42)/4=13$ pixels : il n'est pas la moyenne non pondérée des positions.

**Limite de décision** : si toute la masse est nulle, aucune position moyenne n'est définie par ces observations. Une sortie numérique arbitraire masquerait une absence d'information. Signaler la perte ou appliquer une recherche annoncée, puis évaluer cette politique. Même avec une masse positive, un fond de couleur semblable peut attirer la fenêtre ; la concentration trouvée ne vérifie donc pas l'identité de l'objet initialisé.

### Cas lié à CV-MEANSHIFT-004

**Question de travail** : Quel essai permet de vérifier si une amélioration vient de l’adaptation CamShift plutôt que d’un nouvel histogramme ?

**Réponse de référence** : Garder le même histogramme, les mêmes frames et la même initialisation ; comparer fenêtre fixe et fenêtre adaptative sur un changement d’échelle. Mesurer centre, overlap, taille et pertes, puis tester séparément un changement d’histogramme.

**Logique de l'ablation** : changer uniquement l'adaptation de fenêtre teste son effet sur le contrat de localisation. Modifier en même temps l'histogramme change les masses sur lesquelles le déplacement est calculé, ce qui empêche d'attribuer l'amélioration à un seul mécanisme.

**Expérience construite** : utiliser une séquence où la cible grossit progressivement, puis une autre où un distracteur apparaît sans changement d'échelle. Garder les mêmes critères de perte et de réinitialisation, et rapporter les erreurs sur toutes les frames. Une fenêtre adaptative peut aider le premier cas et nuire au second si la masse du distracteur la déforme. La comparaison doit rendre visible ce compromis. Les canaux, bins et masques sont des paramètres du modèle d'apparence ; leur réglage demande une autre ablation et des données réservées.

**Repère documentaire de cette passe** : [OpenCV 4.13, Meanshift and Camshift](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html), histogramme, backprojection et fenêtre CamShift. Les autres développements figurent dans les [cartes associées](../115-meanshift-camshift.md).

## Sources et cartes

- [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
- [Cartes associées](../115-meanshift-camshift.md) : CV-MEANSHIFT-001 à 004.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
