---
id: CV-FAST-BRIEF
type: methode
domaine: d04
poles: ["B", "C", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-CORNERS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# FAST et BRIEF — détecter un coin puis décrire son voisinage

## Prérequis et compétences

**Prérequis obligatoires** : [CV-CORNERS](46-harris-shi-tomasi.md).
**Compétences visées** : expliquer le test FAST; calculer une distance binaire; séparer FAST BRIEF et ORB; isoler un échec sous rotation; mesurer le compromis calcul répétabilité.
Les notions connexes restent des alternatives, pas des dépendances implicites.

## Problème et contrat des données

Construire une chaîne de features légère en séparant détection et description. FAST prend des intensités locales et renvoie des keypoints ; BRIEF prend des patches autour de keypoints et renvoie des chaînes de bits. Un match relie ensuite deux descripteurs. Positions, motif d’échantillonnage, lissage, échelle et orientation doivent être compatibles entre images.

## Intuition et mécanisme

Le segment test FAST compare le centre à un cercle de pixels : il cherche un arc contigu uniformément plus clair ou plus sombre. L’arbre de décision de Rosten et Drummond accélère la décision ; la suppression des non-maxima évite des grappes de réponses. BRIEF lisse un patch puis compare l’intensité de paires de positions. La séquence de réponses binaires décrit le patch. BRIEF seul ne détecte pas de points ; FAST seul ne crée pas de descripteur.

## Mathématiques et conventions

Pour le centre $p$, le seuil $t>0$ est dans les mêmes unités que l’intensité $I$. Sur un cercle discret, FAST exige un arc de $n$ voisins tous au-dessus de $I(p)+t$ ou tous au-dessous de $I(p)-t$. $n$ et le cercle dépendent de la variante ; ne pas confondre FAST-9 et le test historique à 12 voisins sur 16. Un bit BRIEF est $b_j=\mathbf1[I_s(x_j)<I_s(y_j)]$, avec $I_s$ le patch lissé et $(x_j,y_j)$ une paire fixée. La distance de Hamming compte les bits différents : $d_H(a,b)=\mathrm{popcount}(a\oplus b)$, sans unité.

## Hypothèses, paramètres et coût

Seuil, variante FAST, suppression des maxima et lissage changent répétabilité et densité. L’arbre évite des tests inutiles mais n’ajoute pas une garantie géométrique. Un motif BRIEF fixe n’est pas invariant à toute rotation ou échelle : il peut comparer d’autres structures lorsque le patch tourne. Coût de description et stockage croissent avec le nombre de tests ; matching binaire reste un coût à mesurer avec le nombre de points. ORB enrichit cette famille avec orientation, pyramide et sélection de tests ; il ne se réduit pas au collage de FAST et BRIEF standards.

## Évaluation et variation contrôlée

Baseline proposée : motif et échelle fixes ; variation : rotation croissante d’une même scène, avec vérité de transformation. Séparer taux de redétection et précision des matches pour savoir quelle étape échoue. Comparer temps d’extraction, temps de matching, couverture et inliers à budget égal. Exemple analytique : 101101 XOR 100001 donne 001100, donc une distance de Hamming de 2. Un entier stockant les bits n’est pas une coordonnée euclidienne.

## Échecs, diagnostic et alternatives

Bruit fin : comparer le lissage et la stabilité des tests binaires. Flou : contrôler le contraste du cercle FAST avant d’abaisser le seuil. Rotation : garder les détections et comparer les patches orientés pour isoler le descripteur. À fortes variations d’échelle, tester SIFT ou un détecteur/descripteur appris. API OpenCV 4.13 vérifiées avec Context7 ; aucun benchmark ou appel de feature extractor exécuté.

## Sources et cartes

- [Rosten et Drummond 2006, §§2–3, segment test et apprentissage](https://www.edwardrosten.com/work/rosten_2006_machine.pdf).
- [Calonder et al. 2010, §2, tests BRIEF et lissage](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf).
- [OpenCV 4.13, FAST, Theory](https://docs.opencv.org/4.13.0/df/d0c/tutorial_py_fast.html).
- [OpenCV 4.13, BRIEF, Theory](https://docs.opencv.org/4.13.0/dc/d7d/tutorial_py_brief.html).
- [OpenCV 4.13, ORB, orientation et rBRIEF](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html).
- [Cartes associées](../47-fast-brief.md) : CV-FAST-BRIEF-001 à 005.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
