# MeanShift et CamShift — suivre une distribution d’apparence — cartes

Fiche : [[110-tracking-association/references/115-meanshift-camshift|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-MEANSHIFT-001

Objectif : expliquer une itération MeanShift. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-MEANSHIFT-001
Question: Que calcule une itération MeanShift sur une image de backprojection, et que faire si la fenêtre ne contient aucune masse ?
Reponse: **Noyau attendu** : Calculer le centroïde des scores dans la fenêtre, puis déplacer la fenêtre vers ce centre. Si la masse totale $M_{00}$ est nulle, le centroïde est indéfini : ne pas diviser et appliquer une politique de perte/recherche explicite.

**Approfondissement** : $x_c=M_{10}/M_{00}$ et $y_c=M_{01}/M_{00}$ utilisent les moments pondérés. Le processus cherche une concentration locale et dépend de l’initialisation. La backprojection ne certifie pas l’identité de l’objet.

**Lecture des moments** : la backprojection attribue une masse à chaque position selon sa compatibilité avec l'apparence de référence. Le centroïde pondéré donne un déplacement de fenêtre vers cette concentration. Avec deux masses 1 et 3 placées à 10 et 14 pixels, le centre vaut $(10+42)/4=13$ pixels : il n'est pas la moyenne non pondérée des positions.

**Limite de décision** : si toute la masse est nulle, aucune position moyenne n'est définie par ces observations. Une sortie numérique arbitraire masquerait une absence d'information. Signaler la perte ou appliquer une recherche annoncée, puis évaluer cette politique. Même avec une masse positive, un fond de couleur semblable peut attirer la fenêtre ; la concentration trouvée ne vérifie donc pas l'identité de l'objet initialisé.

**Erreurs bloquantes** : Diviser par une masse nulle ; présenter le mode atteint comme un maximum global garanti.
Source: [[110-tracking-association/references/115-meanshift-camshift|Fiche complète]] ; [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-MEANSHIFT-001 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-002

Objectif : distinguer MeanShift et CamShift. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-MEANSHIFT-002
Question: La cible se rapproche de la caméra, mais une fenêtre de suivi reste trop petite. Qu’apporte CamShift par rapport au MeanShift usuel ?
Reponse: **Noyau attendu** : Le MeanShift usuel déplace une fenêtre de taille fixe ; CamShift adapte taille et orientation à la distribution observée, en utilisant ses moments. Cela traite une variation d’apparence projetée, pas une estimation métrique de pose.

**Approfondissement** : Une adaptation peut aussi englober du fond ou un distracteur si la backprojection est mauvaise. Comparer les deux à histogramme et initialisation identiques, en mesurant overlap et pertes, sans conclure à une robustesse universelle.

**Pourquoi l'échelle évolue** : lorsque la cible occupe une plus grande surface dans l'image, une fenêtre fixe peut n'en contenir qu'une partie ou perdre son centre d'apparence. Les moments de la distribution fournissent des indications pour adapter une fenêtre à l'étendue projetée observée.

**Exemple de limite** : si un distracteur de même couleur entre dans la région, il contribue lui aussi aux moments. La fenêtre peut s'agrandir pour un mauvais motif, sans que l'algorithme détecte cette confusion. Comparer position, overlap et taille sur des séquences avec changement d'échelle, à histogramme constant. Vérifier ensuite illumination et occultation séparément. L'adaptation résout une dimension du contrat de suivi ; elle ne fournit ni profondeur ni identité garantie, et une boîte tournée dans l'image n'est pas une pose 3D.

**Erreurs bloquantes** : Confondre boîte orientée 2D et orientation 3D ; annoncer une adaptation fiable en toute occultation.
Source: [[110-tracking-association/references/115-meanshift-camshift|Fiche complète]] ; [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-MEANSHIFT-002 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-003

Objectif : diagnostiquer un distracteur de couleur. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-MEANSHIFT-003
Question: Un suivi CamShift saute sur une autre pièce de même couleur. Pourquoi augmenter le nombre d’itérations peut-il aggraver le problème ?
Reponse: **Noyau attendu** : Le modèle d’histogramme ne distingue pas nécessairement les deux pièces. Plus d’itérations peut converger davantage vers la mauvaise concentration. Inspecter la backprojection, la ROI et la séparation cible/fond avant de régler l’arrêt.

**Approfondissement** : Conserver une politique de perte, ajouter une information de texture ou un détecteur si l’identité importe. Un pic de couleur fort peut être correct pour le modèle statistique et faux pour le besoin métier.

**Distinction entre modèle et objectif métier** : la distribution peut présenter un mode fort sur le distracteur parce qu'il correspond bien à l'histogramme. Converger vers ce mode est compatible avec le critère d'apparence, tout en étant faux pour l'identité souhaitée. Le problème vient alors de l'information qui distingue les cibles, pas seulement du nombre d'itérations.

**Enquête proposée** : afficher backprojection et fenêtre à l'instant du saut, puis comparer un masque ou une représentation plus discriminante à tracker constant. Tester le retour après occultation et les cas où le fond change. Un ajout de texture ou une détection peut apporter une observation nouvelle ; il faut encore vérifier son association. Si les pièces restent visuellement identiques, reconnaître l'ambiguïté et définir une politique de perte plutôt que transformer un score de couleur en certitude.

**Erreurs bloquantes** : Assimiler convergence de MeanShift et bonne identité.
Source: [[110-tracking-association/references/115-meanshift-camshift|Fiche complète]] ; [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-MEANSHIFT-003 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-004

Objectif : évaluer couleur et adaptation séparément. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-MEANSHIFT-004
Question: Quel essai permet de vérifier si une amélioration vient de l’adaptation CamShift plutôt que d’un nouvel histogramme ?
Reponse: **Noyau attendu** : Garder le même histogramme, les mêmes frames et la même initialisation ; comparer fenêtre fixe et fenêtre adaptative sur un changement d’échelle. Mesurer centre, overlap, taille et pertes, puis tester séparément un changement d’histogramme.

**Approfondissement** : Ajouter ensuite illumination et distracteurs un facteur à la fois. Les pixels peu saturés rendent la teinte peu informative ; documenter les masques et canaux utilisés. Ces variations sont proposées et n’ont pas été exécutées sur vidéo ici.

**Logique de l'ablation** : changer uniquement l'adaptation de fenêtre teste son effet sur le contrat de localisation. Modifier en même temps l'histogramme change les masses sur lesquelles le déplacement est calculé, ce qui empêche d'attribuer l'amélioration à un seul mécanisme.

**Expérience construite** : utiliser une séquence où la cible grossit progressivement, puis une autre où un distracteur apparaît sans changement d'échelle. Garder les mêmes critères de perte et de réinitialisation, et rapporter les erreurs sur toutes les frames. Une fenêtre adaptative peut aider le premier cas et nuire au second si la masse du distracteur la déforme. La comparaison doit rendre visible ce compromis. Les canaux, bins et masques sont des paramètres du modèle d'apparence ; leur réglage demande une autre ablation et des données réservées.

**Erreurs bloquantes** : Modifier simultanément histogramme, masque et tracker puis attribuer le résultat à CamShift seul.
Source: [[110-tracking-association/references/115-meanshift-camshift|Fiche complète]] ; [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-MEANSHIFT-004 provenance::agent pole::C pole::D pole::E
END
