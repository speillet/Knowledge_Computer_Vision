# Farnebäck — flot dense par expansion polynomiale — cartes

Fiche : [[100-mouvement-video/references/103-farneback|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::100-mouvement-video

## CV-FARNEBACK-001

Objectif : expliquer le mécanisme polynomial. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-FARNEBACK-001
Question: Comment Farnebäck obtient-il un déplacement à partir de deux voisinages d’image, sans descripteurs de points ?
Reponse: **Noyau attendu** : Il approxime les voisinages par des polynômes quadratiques, relie leurs changements de coefficients à une translation, puis agrège les contraintes et raffine à plusieurs échelles. Pour un modèle idéal $f_2(x)=f_1(x-d)$, on a $2Ad=b_1-b_2$.

**Approfondissement** : $A$ est la matrice quadratique symétrique, $b_i$ le coefficient linéaire du voisinage $i$, et $d$ un déplacement 2D en pixels. Cette relation suppose une translation locale ; la méthode réelle traite des approximations bruitées.

**Erreurs bloquantes** : Présenter la sortie dense comme une preuve que chaque pixel est bien contraint.
Source: [[100-mouvement-video/references/103-farneback|Fiche complète]] ; [Farnebäck 2003, §§2–3, expansion et déplacement, §3.5 multi-échelle](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf).
Tags: cv::pilote cv::d10 famille::algorithme cv_id::CV-FARNEBACK-001 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-002

Objectif : résoudre une contrainte locale idéale. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FARNEBACK-002
Question: Pour un modèle quadratique idéal, $A=\mathrm{diag}(2,1)$ et $b_1-b_2=(8,-2)^T$. Si $2Ad=b_1-b_2$, quel déplacement obtient-on et quelle limite faut-il garder ?
Reponse: **Noyau attendu** : $d=(2,-1)^T$ px. La solution vient du modèle idéal à matrice inversible ; elle ne garantit pas une estimation fiable si les coefficients sont bruités ou la fenêtre ne contient pas d’information dans deux directions.

**Approfondissement** : Un $A$ singulier n’autorise pas une inversion ordinaire. Dans une image réelle, agrégation spatiale, pondération et conditionnement comptent davantage qu’une formule isolée.

**Erreurs bloquantes** : Inverser toute matrice sans vérifier son rang ; convertir directement le résultat en m/s.
Source: [[100-mouvement-video/references/103-farneback|Fiche complète]] ; [Farnebäck 2003, §§2–3, expansion et déplacement, §3.5 multi-échelle](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf).
Tags: cv::pilote cv::d10 famille::raisonnement cv_id::CV-FARNEBACK-002 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-003

Objectif : lire le repère et les unités du flot. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-FARNEBACK-003
Question: Un calcul OpenCV donne flow[y,x]=(4,-2) entre deux frames séparées de 40 ms. Où chercher la correspondance, et que peut-on conclure sur la vitesse ?
Reponse: **Noyau attendu** : À $(x+4,y-2)$ dans la seconde image. Le déplacement est en pixels ; dans cet exemple l’approximation de vitesse image est $(100,-50)$ px/s. Une vitesse en m/s exige une géométrie et une profondeur ou échelle métrique supplémentaires.

**Approfondissement** : Ne pas inverser les composantes ligne/colonne. À cadence irrégulière, prendre les timestamps d’acquisition. La présence d’un vecteur ne prouve pas que le pixel soit visible dans la seconde image.

**Erreurs bloquantes** : Lire (4,-2) comme (ligne,colonne) ; annoncer une vitesse métrique sans échelle.
Source: [[100-mouvement-video/references/103-farneback|Fiche complète]] ; [OpenCV 4.13, Optical Flow, Dense Optical Flow](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html).
Tags: cv::pilote cv::d10 famille::pratique cv_id::CV-FARNEBACK-003 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-004

Objectif : interpréter une incohérence aller-retour. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FARNEBACK-004
Question: Pour vérifier un flot avant $F(x)$, peut-on lui additionner le flot inverse $B(x)$ au même pixel ?
Reponse: **Noyau attendu** : Le point atteint est $x+F(x)$ : évaluer $B$ à cette position, généralement par interpolation, puis vérifier $F(x)+B(x+F(x))$. Le même pixel de la seconde image peut représenter une autre surface.

**Approfondissement** : Un grand écart peut venir d’une occultation, d’une sortie de champ ou d’une erreur. Un petit écart ne prouve pas la bonne association dans une texture répétitive. Le contrôle est un diagnostic du projet, pas une certification du flot.

**Erreurs bloquantes** : Comparer systématiquement les deux vecteurs à la même coordonnée sans tenir compte du déplacement.
Source: [[100-mouvement-video/references/103-farneback|Fiche complète]] ; [Farnebäck 2003, §§2–3, expansion et déplacement, §3.5 multi-échelle](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf).
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-FARNEBACK-004 provenance::agent pole::B pole::C pole::D
END

## CV-FARNEBACK-005

Objectif : régler la pyramide sans masquer les échecs. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-FARNEBACK-005
Question: Pourquoi augmenter le nombre de niveaux d’une pyramide de flot peut-il aider les grands mouvements tout en détériorant de petits objets ?
Reponse: **Noyau attendu** : Le déplacement est réduit aux niveaux grossiers, mais la réduction peut faire disparaître les petites structures et mélanger les frontières. Évaluer à la fois amplitude capturable, erreur des petits objets et limites de mouvement.

**Approfondissement** : Faire varier les niveaux à résolution, fenêtres et séquences fixes. Mesurer endpoint error sur vérité disponible, masque d’occultation et coût complet. Une carte de couleur de flot paraît souvent lisse même si la géométrie est fausse.

**Erreurs bloquantes** : Conclure que plus de niveaux améliore chaque région de l’image.
Source: [[100-mouvement-video/references/103-farneback|Fiche complète]] ; [Farnebäck 2003, §§2–3, expansion et déplacement, §3.5 multi-échelle](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf).
Tags: cv::pilote cv::d10 famille::evaluation cv_id::CV-FARNEBACK-005 provenance::agent pole::B pole::C pole::D
END
