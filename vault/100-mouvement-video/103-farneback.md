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

**Interprétation du modèle local** : les coefficients quadratiques décrivent la forme des intensités dans un voisinage, plutôt qu'une signature indépendante à apparier. Une translation idéale laisse une relation particulière entre les termes des deux polynômes. L'agrégation exploite plusieurs contraintes pour limiter la fragilité d'une inversion isolée.

**Exemple de limite** : un mur uniforme n'apporte pas de courbure informative dans les deux directions ; un voisinage à cheval sur deux objets peut mélanger deux mouvements. Faire croître la fenêtre peut réduire du bruit mais lisser cette frontière. Contrôler ces régions séparément dans une évaluation. Une méthode dense offre une sortie partout selon son format ; la précision locale dépend toujours de l'information image et de l'adéquation du modèle.

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

**Calcul interprété** : les deux équations sont $4d_x=8$ et $2d_y=-2$, d'où le déplacement annoncé. Les coefficients sont supposés exprimés dans des conventions communes. L'exercice vérifie une relation de translation sur des intensités modélisées ; il ne mesure pas une vitesse physique et ne simule pas toutes les étapes du flot dense.

**Cas défavorable** : si une direction du voisinage ne présente presque aucune variation, la solution correspondante devient sensible aux petites erreurs de coefficients. Augmenter le nombre de pixels similaires ne recrée pas forcément cette information. Examiner conditionnement et mélange de mouvements, puis comparer une agrégation différente sur des translations connues. C'est le lien avec les moindres carrés : résidu faible et déplacement bien identifié ne sont pas équivalents.

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

**Lecture du repère** : l'accès au tableau utilise ligne puis colonne, mais le vecteur fournit déplacement horizontal puis vertical. Ici, une composante verticale négative signifie une position deux pixels plus haut dans le repère image usuel. Le point atteint est dans la deuxième image, et non une valeur à additionner à un indice de ligne au hasard.

**Contrôle proposé** : déplacer synthétiquement une image texturée dans une direction connue et vérifier sens, composantes et unités. Conserver les timestamps si certaines frames sont perdues. Une vitesse image moyenne peut être calculée à partir d'une paire valide, mais perspective, profondeur et mouvement de caméra empêchent de l'identifier directement à la vitesse 3D de l'objet. La conversion est donc une étape de modèle distincte.

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

**Exemple analytique** : si le point source est à 10 et que le déplacement avant vaut 4 pixels sur un axe, le point à examiner dans l'autre image est à 14. Le flot inverse correct pour ce point devrait ramener de 14 vers 10. Lire la valeur inverse à 10 testerait une autre observation.

**Politique de validité** : si la position atteinte sort de l'image ou se trouve dans une région occultée, ne pas présenter le résidu aller-retour comme une mesure ordinaire de précision. Conserver un masque et une règle explicite. Dans une répétition, deux erreurs opposées peuvent aussi être cohérentes entre elles ; une référence indépendante reste nécessaire pour établir la correspondance vraie. Ce contrôle est une alarme utile, pas une preuve complète.

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

**Compromis d'échelle** : aux niveaux grossiers, un grand déplacement de l'image initiale représente moins de pixels, ce qui facilite une recherche locale. Mais un objet de quelques pixels peut se mélanger au fond et ne plus fournir son propre mouvement. Le raffinement fin démarre alors d'une hypothèse déjà influencée par son voisinage.

**Expérience construite** : utiliser une scène avec grand mouvement de fond et petit objet indépendant, puis faire varier seulement la pyramide. Rapporter erreur sur le fond, sur l'objet et à sa frontière, ainsi que les pixels invalides. Une amélioration moyenne dominée par le fond peut masquer la perte du petit objet. Ce raisonnement relie le paramètre au signal utile, sans supposer qu'un plus grand budget améliore uniformément toutes les régions.

**Erreurs bloquantes** : Conclure que plus de niveaux améliore chaque région de l’image.
Source: [[100-mouvement-video/references/103-farneback|Fiche complète]] ; [Farnebäck 2003, §§2–3, expansion et déplacement, §3.5 multi-échelle](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf).
Tags: cv::pilote cv::d10 famille::evaluation cv_id::CV-FARNEBACK-005 provenance::agent pole::B pole::C pole::D
END
