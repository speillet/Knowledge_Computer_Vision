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

**Erreurs bloquantes** : promettre une latence à partir du seul article ou ignorer le taux d'échec pour choisir la méthode la plus rapide.
Source: [[40-features-matching/references/42-orb|Fiche ORB]] ; [Rublee et al., §§4–5](https://doi.org/10.1109/ICCV.2011.6126544).
Tags: cv::pilote cv::d04 famille::conception cv_id::CV-ORB-006 provenance::agent pole::B pole::E pole::F
END
