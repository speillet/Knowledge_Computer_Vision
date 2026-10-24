# Cartes pilotes — ORB

Fiche : [[40-features-matching/references/42-orb|ORB]]. Provenance de rédaction : agent.

TARGET DECK: CV::Pilote::40-features-matching

## CV-ORB-001

Objectif : reconstruire le mécanisme d'ORB. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-ORB-001
Question: Comment ORB passe-t-il d'une image à un descripteur binaire orienté, et quel est le rôle de chaque composant ?
Reponse: **Noyau attendu** : FAST détecte les candidats dans une pyramide ; un classement, Harris dans l'article, sélectionne les points ; le centre de masse des intensités fournit une orientation ; des tests BRIEF orientés forment le descripteur binaire.

**Approfondissement** : rBRIEF choisit hors ligne des tests à variance élevée et faible corrélation. La pyramide donne des niveaux d'échelle discrets ; la rotation du motif compense une orientation locale. Le matching et la vérification géométrique sont des étapes ultérieures, pas des sorties garanties d'ORB.

**Mécanisme interprété** : détecter une position ne suffit pas pour comparer deux voisinages tournés. L'orientation établit un repère local dans lequel le motif de tests est déplacé ; les réponses binaires décrivent ensuite des relations d'intensité dans ce repère. La pyramide fournit plusieurs tailles d'observation, sans rendre identiques tous les détails aux différentes résolutions.

**Diagnostic construit** : si les keypoints sont redétectés mais les matches disparaissent sous rotation, inspecter stabilité de l'orientation et contenu des patches avant de changer le nombre de points. Si les keypoints disparaissent eux-mêmes, examiner seuils, flou et niveaux de pyramide. Cette séparation des étapes permet d'attribuer un échec à un mécanisme précis au lieu de traiter ORB comme une boîte noire.

**Erreurs bloquantes** : présenter ORB comme seulement FAST, ou dire qu'il fournit directement une transformation entre images.
Source: [[40-features-matching/references/42-orb|Fiche ORB]] ; [Rublee et al., §§3–4](https://doi.org/10.1109/ICCV.2011.6126544).
Tags: cv::pilote cv::d04 famille::algorithme cv_id::CV-ORB-001 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-002

Objectif : relier représentation et distance. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-ORB-002
Question: Pourquoi une distance L2 entre les octets d'un descripteur ORB à tests binaires n'est-elle pas équivalente à la distance de Hamming ?
Reponse: **Noyau attendu** : les octets stockent des résultats de tests bit par bit. Hamming compte les bits différents ; L2 traite les octets comme des nombres dont la valeur dépend du poids des positions binaires.

**Approfondissement** : entre `00000000` et `10000000`, Hamming vaut 1 et la différence numérique vaut 128 ; un bit de poids faible aurait une autre différence numérique malgré un seul test changé. Le type `uint8` décrit le stockage, pas la sémantique de la distance. Ce raisonnement concerne `WTA_K=2`.

**Contre-exemple analytique** : comparer `00000000` à `00000011` donne deux bits différents, mais une différence numérique de trois. Comparer le même premier octet à `10000000` donne un seul bit différent, mais une différence numérique de 128. Les deux distances peuvent donc inverser le classement des candidats.

**Conséquence pour une implémentation** : convertir les octets en flottants conserve ces valeurs numériques et ne transforme pas la comparaison en Hamming. Il faut comparer les symboles qui portent les tests, avec une variante compatible avec leur construction. Une distance correcte conserve le sens du descripteur ; elle ne démontre toujours pas que les deux patches appartiennent au même point physique. Le filtrage des ambiguïtés et la géométrie restent nécessaires.

**Erreurs bloquantes** : justifier L2 seulement par la présence d'un tableau d'octets, ou prétendre que les deux distances classent toujours les voisins de la même façon.
Source: [[40-features-matching/references/42-orb|Fiche ORB]] ; [OpenCV 4.13, matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html).
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-ORB-002 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-003

Objectif : choisir la norme après changement de variante. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-ORB-003
Question: Dans OpenCV 4.13, tu passes ORB de `WTA_K=2` à `WTA_K=4`. Que faut-il vérifier dans le matcher et pourquoi ?
Reponse: **Noyau attendu** : passer de `NORM_HAMMING` à `NORM_HAMMING2`, ou utiliser `orb.defaultNorm()`. Avec trois ou quatre candidats, chaque résultat représente un symbole sur deux bits ; Hamming2 compare les symboles.

**Approfondissement** : Hamming2 ne signifie pas Hamming au carré. Conserver les descripteurs et le matcher compatibles dans tout l'index, sans mélanger silencieusement variantes ou paramètres. Réévaluer ensuite précision des matches et succès géométrique avant d'attribuer une dégradation aux images.

Extrait illustratif non exécuté, OpenCV 4.13 :

```python
orb = cv.ORB_create(WTA_K=4)
matcher = cv.BFMatcher(orb.defaultNorm(), crossCheck=True)
```

**Exemple sur les symboles** : deux valeurs gagnantes codées `00` et `11` constituent un seul symbole différent. Compter les bits différents donnerait deux, alors qu'une comparaison des symboles doit compter un désaccord. C'est la raison sémantique du changement de norme ; le nom Hamming2 ne décrit pas une simple opération arithmétique sur le résultat précédent.

**Migration contrôlée proposée** : régénérer les descripteurs de la base avec la même configuration que les requêtes, puis vérifier matcher et index. Ne pas comparer des vecteurs provenant silencieusement de constructions différentes. Une bonne compatibilité d'API évite une erreur de mesure, mais le choix final de la variante se juge encore sur les matches et le succès du recalage.

**Erreurs bloquantes** : conserver automatiquement Hamming simple ou décrire Hamming2 comme le carré d'une distance.
Source: [[40-features-matching/references/42-orb|Fiche ORB]] ; [OpenCV ORB, WTA_K](https://docs.opencv.org/4.13.0/db/d95/classcv_1_1ORB.html).
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-ORB-003 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-004

Objectif : distinguer deux filtres de correspondances. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-ORB-004
Question: Pour des descripteurs ORB, quelle différence de logique sépare le cross-check d'un ratio test, et qu'est-ce qu'aucun des deux ne garantit ?
Reponse: **Noyau attendu** : le cross-check exige des plus proches voisins mutuels ; le ratio test exige que le meilleur voisin soit suffisamment meilleur que le deuxième. Aucun ne garantit une correspondance physique correcte ou un modèle géométrique valable.

**Approfondissement** : un match mutuel peut rester ambigu dans un motif répétitif ; un voisin distinct peut être faux. Dans BFMatcher OpenCV, le cross-check correspond à la réciprocité avec un seul voisin, pas à un remplacement transparent de `knnMatch(k=2)`. Consigner le filtrage avant la vérification géométrique.

**Exemples pour séparer les logiques** : un voisin peut être le meilleur choix dans les deux sens tout en étant presque ex æquo avec un autre motif. Le cross-check peut alors l'accepter alors qu'un ratio strict le refuse. Inversement, un voisin bien séparé pour une requête peut préférer une autre requête dans l'autre image et échouer au contrôle mutuel.

**Interprétation pratique** : ces tests filtrent des relations dans l'espace des descripteurs ; ils ne connaissent ni la profondeur ni les contraintes de projection. Garder trace des candidats rejetés et de leur couverture aide à régler le compromis entre ambiguïté et nombre de contraintes géométriques. Le protocole doit annoncer quel test est appliqué, dans quel ordre et avec quel nombre de voisins disponibles.

**Erreurs bloquantes** : présenter les tests comme identiques ou comme une validation géométrique.
Source: [[40-features-matching/references/42-orb|Fiche ORB]] ; [OpenCV BFMatcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-ORB-004 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-005

Objectif : diagnostiquer une perte de répétabilité. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-ORB-005
Question: ORB fonctionne à distance fixe mais échoue quand la caméra s'éloigne. Quelles hypothèses examiner avant de simplement augmenter le nombre de features ?
Reponse: **Noyau attendu** : vérifier la plage et l'espacement des échelles de la pyramide, la résolution effective des détails et la répétabilité des keypoints. Le nombre demandé ne rétablit pas une information disparue ou une échelle non couverte.

**Approfondissement** : visualiser les niveaux et les points détectés, garder lumière et focus contrôlés, puis comparer une variation de pyramide au protocole initial. Ajouter séparément la perspective et le flou. ORB n'a pas une invariance parfaite à l'échelle ; une autre méthode peut être nécessaire après mesure.

**Exemple physique** : un petit marquage bien résolu près de la caméra peut ne couvrir que quelques pixels après éloignement. Modifier la densité de la pyramide peut aider si une taille pertinente était mal échantillonnée, mais pas si l'acquisition a déjà détruit le contraste du marquage. Augmenter le quota ne fait alors qu'ajouter des points ailleurs.

**Enquête proposée** : suivre les mêmes structures visibles entre distances, observer leurs niveaux de détection et vérifier le nombre de pixels réellement consacrés au motif. Tester séparément résolution, mise au point et pyramide. Mesurer ensuite une erreur sur la région utile, car davantage de points sur le fond ne rétablit pas la localisation de la pièce. Ce raisonnement relie acquisition et features plutôt que de tout attribuer au matcher.

**Erreurs bloquantes** : annoncer que la pyramide résout tout changement d'échelle ou régler uniquement le matcher sans regarder la détection.
Source: [[40-features-matching/references/42-orb|Fiche ORB]] ; [Rublee et al., conclusion](https://doi.org/10.1109/ICCV.2011.6126544) ; [OpenCV ORB](https://docs.opencv.org/4.13.0/db/d95/classcv_1_1ORB.html).
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-ORB-005 provenance::agent pole::B pole::E pole::F
END

## CV-ORB-006

Objectif : articuler contrainte de calcul et réussite de tâche. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-ORB-006
Question: Tu dois localiser un marquage sur un CPU embarqué avec peu de mémoire. Comment construire une baseline avec ORB sans préjuger de son adéquation finale ?
Reponse: **Noyau attendu** : fixer les variations et la tolérance de localisation, extraire ORB avec paramètres consignés, apparier avec sa norme puis valider géométriquement. Mesurer coût complet et échecs sur des données représentatives, puis comparer une alternative si le besoin n'est pas atteint.

**Approfondissement** : les descripteurs binaires sont compacts mais le nombre de points, le matching et les cas difficiles comptent aussi. Prévoir un comportement lorsque le recalage est incertain et ne pas transformer un fort consensus en certitude. C'est une proposition de système, sans résultat terrain annoncé.

**Baseline exploitable** : prévoir explicitement trois issues : transformation acceptée, résultat incertain et absence de résultat. Définir l'acceptation à partir des résidus, de la couverture et de la plausibilité du mouvement, puis évaluer les erreurs d'acceptation sur des pièces réservées. Un refus contrôlé peut être préférable à une région d'inspection mal placée.

**Comparaison proposée** : garder les mêmes entrées et tolérances pour une alternative SIFT, en incluant les étapes qui changent réellement dans le coût. Mesurer mémoire maximale et latence en conditions représentatives, pas seulement le temps d'un appel isolé. La représentation compacte d'ORB motive l'essai ; c'est le bilan de précision, robustesse, coût et comportement en échec qui décide de son adéquation.

**Erreurs bloquantes** : promettre une latence à partir du seul article ou ignorer le taux d'échec pour choisir la méthode la plus rapide.
Source: [[40-features-matching/references/42-orb|Fiche ORB]] ; [Rublee et al., §§4–6](https://doi.org/10.1109/ICCV.2011.6126544).
Tags: cv::pilote cv::d04 famille::conception cv_id::CV-ORB-006 provenance::agent pole::B pole::E pole::F
END
