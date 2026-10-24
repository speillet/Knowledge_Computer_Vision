---
id: CV-FARNEBACK
type: methode
domaine: d10
poles: ["B", "C", "D"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-FLOT", "CV-SVD"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d10]
---
# Farnebäck — flot dense par expansion polynomiale

## Prérequis et compétences

**Prérequis obligatoires** : [CV-FLOT](101-flot-optique.md), [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md).
**Compétences visées** : expliquer le mécanisme polynomial; résoudre une contrainte locale idéale; lire le repère et les unités du flot; interpréter une incohérence aller-retour; régler la pyramide sans masquer les échecs.
Les notions connexes restent des alternatives, pas des dépendances implicites.

## Problème et contrat des données

Estimer le déplacement apparent dense entre deux images, sans entraîner de réseau. Entrées : frames compatibles en taille, photométrie et instant ; sortie : deux composantes de déplacement par pixel. Dans OpenCV 4.13, `flow[y,x]` correspond au point $(x,y)$ de l’image précédente et donne son déplacement vers l’image suivante. Ce sont des pixels par paire de frames, pas une vitesse métrique, un identifiant d’objet ou une profondeur.

## Intuition et déroulement

Farnebäck approxime chaque voisinage par un polynôme quadratique. Un déplacement transforme ses coefficients ; on en déduit une contrainte locale, agrégée spatialement. Une pyramide et des itérations estiment un mouvement grossier puis le raffinent. Le calcul produit un vecteur même dans des régions mal informées : densité de sortie et fiabilité ne sont pas synonymes.

## Mathématiques et conventions

Écrire $f_1(x)=x^TAx+b_1^Tx+c_1$ pour des coordonnées locales $x\in\mathbb R^2$, avec $A$ symétrique $2\times2$. Pour une translation $d$ en pixels, $f_2(x)=f_1(x-d)$ donne $b_2=b_1-2Ad$, donc $2Ad=b_1-b_2$. $A$ a les unités intensité/pixel², $b$ intensité/pixel ; les deux côtés ont les mêmes unités. Les coefficients réels sont approchés et bruités : la méthode agrège des contraintes locales au lieu de supposer une inversion fiable en chaque pixel. Un voisinage plat ou essentiellement unidirectionnel rend le déplacement mal observable.

## Paramètres, hypothèses et coût

Les fenêtres d’expansion et d’agrégation régulent robustesse au bruit et lissage des frontières de mouvement. Les niveaux et rapports de pyramide étendent la plage de déplacements capturables, sans garantir tout grand mouvement ; les petites structures peuvent disparaître aux niveaux grossiers. Les itérations raffinent autour de l’initialisation. Le coût dépend pixels, échelles, voisinages et itérations ; mesurer le temps complet plutôt qu’opposer abstraitement CPU et deep learning. API OpenCV vérifiée avec Context7 ; aucune séquence vidéo n’a été traitée pour ce lot.

## Évaluation et variation contrôlée

Baseline proposée : translation connue d’une image texturée, à masques de bord explicites. Faire varier seulement l’amplitude du déplacement ; mesurer endpoint error sur pixels valides et erreurs aux frontières. Contrôler ensuite bruit, flou et occultations séparément. Exemple analytique : avec $A=\mathrm{diag}(2,1)$ et $b_1-b_2=(8,-2)^T$, la relation idéale donne $d=(2,-1)^T$ px. Ce calcul ne constitue pas une exécution du flot dense.

## Diagnostic et alternatives

Des vecteurs incohérents sur un mur uniforme demandent un contrôle de texture, pas seulement plus d’itérations. Un mouvement global peut venir de la caméra ; le soustraire exige un modèle et une validation adaptés à la scène. Le test aller-retour échantillonne le flot inverse à la position déplacée : il signale certaines incohérences mais ne prouve pas une correspondance. Comparer Lucas–Kanade si seuls des points sont nécessaires et RAFT si données, calcul et conditions de domaine le justifient.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent approximation quadratique et domaine de capture du déplacement. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-FARNEBACK-001

**Question de travail** : Comment Farnebäck obtient-il un déplacement à partir de deux voisinages d’image, sans descripteurs de points ?

**Réponse de référence** : Il approxime les voisinages par des polynômes quadratiques, relie leurs changements de coefficients à une translation, puis agrège les contraintes et raffine à plusieurs échelles. Pour un modèle idéal $f_2(x)=f_1(x-d)$, on a $2Ad=b_1-b_2$.

**Interprétation du modèle local** : les coefficients quadratiques décrivent la forme des intensités dans un voisinage, plutôt qu'une signature indépendante à apparier. Une translation idéale laisse une relation particulière entre les termes des deux polynômes. L'agrégation exploite plusieurs contraintes pour limiter la fragilité d'une inversion isolée.

**Exemple de limite** : un mur uniforme n'apporte pas de courbure informative dans les deux directions ; un voisinage à cheval sur deux objets peut mélanger deux mouvements. Faire croître la fenêtre peut réduire du bruit mais lisser cette frontière. Contrôler ces régions séparément dans une évaluation. Une méthode dense offre une sortie partout selon son format ; la précision locale dépend toujours de l'information image et de l'adéquation du modèle.

### Cas lié à CV-FARNEBACK-005

**Question de travail** : Pourquoi augmenter le nombre de niveaux d’une pyramide de flot peut-il aider les grands mouvements tout en détériorant de petits objets ?

**Réponse de référence** : Le déplacement est réduit aux niveaux grossiers, mais la réduction peut faire disparaître les petites structures et mélanger les frontières. Évaluer à la fois amplitude capturable, erreur des petits objets et limites de mouvement.

**Compromis d'échelle** : aux niveaux grossiers, un grand déplacement de l'image initiale représente moins de pixels, ce qui facilite une recherche locale. Mais un objet de quelques pixels peut se mélanger au fond et ne plus fournir son propre mouvement. Le raffinement fin démarre alors d'une hypothèse déjà influencée par son voisinage.

**Expérience construite** : utiliser une scène avec grand mouvement de fond et petit objet indépendant, puis faire varier seulement la pyramide. Rapporter erreur sur le fond, sur l'objet et à sa frontière, ainsi que les pixels invalides. Une amélioration moyenne dominée par le fond peut masquer la perte du petit objet. Ce raisonnement relie le paramètre au signal utile, sans supposer qu'un plus grand budget améliore uniformément toutes les régions.

**Repère documentaire de cette passe** : [Farnebäck 2003](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf), §§2–3, polynomial expansion et displacement estimation. Les autres développements figurent dans les [cartes associées](../103-farneback.md).

## Sources et cartes

- [Farnebäck 2003, §§2–3, expansion et déplacement, §3.5 multi-échelle](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf).
- [OpenCV 4.13, Optical Flow, Dense Optical Flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html).
- [Cartes associées](../103-farneback.md) : CV-FARNEBACK-001 à 005.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
