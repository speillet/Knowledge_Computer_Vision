---
id: CV-MEANSHIFT
type: methode
domaine: d11
poles: ["C", "D", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
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

## Sources et cartes

- [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
- [Cartes associées](../115-meanshift-camshift.md) : CV-MEANSHIFT-001 à 004.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
