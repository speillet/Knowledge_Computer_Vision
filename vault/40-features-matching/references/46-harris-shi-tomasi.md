---
id: CV-CORNERS
type: methode
domaine: d04
poles: ["B", "C", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-FILTRES", "CV-SVD"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# Harris et Shi–Tomasi — structure locale et points suivables

## Prérequis et compétences

**Prérequis obligatoires** : [CV-FILTRES](../../30-traitement-image/references/31-filtrage-gradients.md), [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md).
**Compétences visées** : interpréter les valeurs propres locales; distinguer scores Harris et Shi–Tomasi; régler une sélection de coins; distinguer détection et ambiguïté de matching; évaluer une sélection pour le tracking.
Les notions connexes restent des alternatives, pas des dépendances implicites.

## Problème et contrat des données

Choisir des points dont le déplacement est identifiable dans deux directions. Entrée : image en niveaux de gris, gradients et fenêtre locale ; sortie : coordonnées en pixels et score de réponse, pas un descripteur ni une correspondance. Pour suivre les points, il faut ensuite un algorithme comme Lucas–Kanade. Les unités d’intensité, l’échelle de dérivation et les bords de l’image doivent rester cohérents.

## Intuition et mécanisme

Un petit déplacement modifie peu un aplat, modifie surtout la direction normale à une arête et modifie deux directions autour d’un coin. Harris transforme cette observation en score ; Shi–Tomasi teste la direction la moins contrainte. Déroulement : dériver → agréger les produits de gradients → calculer le score → supprimer les maxima non locaux → imposer espacement et budget de points. Ce sont des détecteurs de texture locale, sans reconnaissance d’objet.

## Mathématiques et conventions

Pour un déplacement $d=(u,v)^T$ en pixels, la variation quadratique s’approxime par $E(d)\approx d^TMd$, avec $M=\sum_{p\in W}w_p\nabla I_p\nabla I_p^T$. $w_p\ge0$ pondère la fenêtre $W$, les gradients sont en intensité/pixel et $M$ est $2\times2$, semi-définie positive. Ses valeurs propres $\lambda_1,\lambda_2$ mesurent les variations dans deux directions. Harris utilise $R_H=\det M-k(\mathrm{tr}M)^2$, avec $k$ sans unité ; Shi–Tomasi utilise $R_S=\min(\lambda_1,\lambda_2)$. Leurs seuils et unités diffèrent : ne pas comparer directement les scores numériques.

## Hypothèses, paramètres et implémentation

La linéarisation suppose de petits déplacements et une apparence suffisamment stable. Une arête a une petite valeur propre : l’aperture problem subsiste le long de l’arête. Dans OpenCV 4.13, `goodFeaturesToTrack` emploie Shi–Tomasi par défaut ; `qualityLevel` est relatif au meilleur score et `minDistance` s’exprime en pixels. Fenêtre, dérivée et niveau de pyramide modifient les réponses. Ces paramètres ne garantissent ni invariance d’échelle ni suivi durable. Aucun appel OpenCV n’a été exécuté pour cette fiche.

## Coût, évaluation et variation contrôlée

Le calcul dense dépend du nombre de pixels et de la taille du voisinage ; un budget de points réduit surtout le travail du tracker suivant. Baseline : sélection des points les plus forts ; variation proposée : imposer une couverture par cellules à budget égal. Mesurer survie, erreur de tracking, couverture et erreur géométrique sur séquences réservées, pas seulement le nombre de coins. Calcul analytique du projet : $M=\mathrm{diag}(100,1)$ donne $R_H=-308{,}04$ pour $k=0{,}04$, et $R_S=1$ ; $M=\mathrm{diag}(20,20)$ donne $336$ et $20$. Une très forte dérivée dans une seule direction ne suffit pas.

## Échecs, diagnostic et alternatives

Des points concentrés sur un panneau texturé peuvent mal contraindre la géométrie globale ; vérifier leur répartition. Des motifs répétés produisent des coins forts mais des associations ambiguës. Si le score tombe après un changement de résolution ou de contraste, comparer gradients et fenêtres dans des unités cohérentes. FAST réduit le coût du test de coin ; SIFT et ORB ajoutent une description et des mécanismes d’échelle/orientation distincts.

## Sources et cartes

- [Harris et Stephens 1988, auto-corrélation et réponse de coin](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf).
- [OpenCV 4.13, Shi–Tomasi, Theory et goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html).
- [OpenCV 4.13, Harris, Theory](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html).
- [Cartes associées](../46-harris-shi-tomasi.md) : CV-CORNERS-001 à 005.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
