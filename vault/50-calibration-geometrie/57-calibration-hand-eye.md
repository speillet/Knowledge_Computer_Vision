# Hand-eye calibration — résoudre AX = XB sans mélanger les repères — cartes

Fiche : [[50-calibration-geometrie/references/57-calibration-hand-eye|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-HANDEYE-001

Objectif : dériver les mouvements relatifs. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-HANDEYE-001
Question: En eye-in-hand, $G_i$ envoie gripper→base et $C_i$ mire→caméra. Avec $X$ caméra→gripper et une mire fixe, comment obtenir $AX=XB$ ?
Reponse: **Noyau attendu** : La chaîne fixe est $G_iXC_i=G_jXC_j$. En multipliant à gauche par $G_j^{-1}$ et à droite par $C_i^{-1}$, on obtient $A=G_j^{-1}G_i$ et $B=C_jC_i^{-1}$, puis $AX=XB$.

**Approfondissement** : Les matrices homogènes sont $4\times4$ et toutes les translations utilisent la même unité. Changer la définition de $A$ ou $B$ impose de refaire la dérivation ; mémoriser des produits sans repères favorise les inversions silencieuses.

**Lecture des repères** : en suivant un point de la mire vers la caméra, puis l'outil et la base, les indices intermédiaires se raccordent. La mire fixe impose que la transformation finale soit constante. Les deux acquisitions fournissent alors deux chemins vers le même résultat, d'où l'équation sur les mouvements relatifs.

**Contrôle construit** : vérifier d'abord cette fermeture avec des transformations synthétiques cohérentes. Introduire ensuite une seule inversion de pose pour observer l'effet sur le résidu de chaîne. Cela contrôle l'algèbre sans commander un robot ni prétendre valider des captures réelles. Une équation formellement reconnue ne dispense pas de définir montage, inconnues et synchronisation dans le dispositif utilisé.

**Erreurs bloquantes** : Permuter arbitrairement les produits ; mélanger mouvements relatifs et poses absolues.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Fiche complète]] ; [OpenCV 4.13, calibrateHandEye, repères, équations et minimum de mouvements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-HANDEYE-001 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-002

Objectif : respecter le sens des poses API. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-HANDEYE-002
Question: Quel contrat de repères faut-il vérifier pour appeler calibrateHandEye d’OpenCV 4.13 en eye-in-hand ?
Reponse: **Noyau attendu** : Fournir les poses gripper→base et mire→caméra pour les mêmes acquisitions ; la sortie est caméra→gripper. Vérifier aussi ordre des rotations, unités des translations et synchronisation.

**Approfondissement** : La pose fournie par solvePnP pour une mire est généralement objet/mire→caméra. La convention du contrôleur robot peut être l’inverse de celle attendue. Tester toute la chaîne sur un point connu avant de comparer les valeurs de la matrice finale.

**Pourquoi la sortie surprend** : la transformation caméra→gripper exprime où se situe la caméra relativement à l'outil. Pour obtenir caméra→base à une pose donnée, il faut encore composer avec la pose de l'outil dans la base ; cette transformation globale varie lorsque le robot bouge.

**Contrôle d'interface proposé** : choisir une observation, suivre un point mire→caméra→gripper→base, puis comparer avec la même mire observée depuis une autre pose. Conserver une unité unique pour toutes les translations. Un contrôleur peut stocker la pose inverse ou une autre convention de rotation ; une matrice de forme correcte n'assure pas la compatibilité. Ce test relie la fonction d'API au montage réel, au lieu d'interpréter la sortie comme une pose universelle.

**Erreurs bloquantes** : Interpréter la sortie comme base→caméra ; utiliser les poses robot à l’envers sans adapter la chaîne.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Fiche complète]] ; [OpenCV 4.13, calibrateHandEye, repères, équations et minimum de mouvements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-HANDEYE-002 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-003

Objectif : exciter les directions observables. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-HANDEYE-003
Question: Pourquoi une grande collection de poses autour d’un même axe peut-elle produire une hand-eye calibration instable ?
Reponse: **Noyau attendu** : Le nombre ne remplace pas la diversité des mouvements : certaines composantes restent peu contraintes. Acquérir des rotations autour d’axes non parallèles et des poses couvrant le volume utile, puis examiner conditionnement et validation réservée.

**Approfondissement** : OpenCV documente un minimum de deux mouvements aux axes non parallèles, soit trois poses, tout en recommandant plus de données. Le minimum théorique n’est pas un protocole industriel suffisant. Les paires tirées des mêmes poses sont corrélées.

**Exemple de répétition insuffisante** : multiplier les poses autour d'un seul axe peut rendre très nombreuses les équations issues des mêmes directions de mouvement. Le volume de données augmente alors sans supprimer toutes les ambiguïtés. Une covariance ou une dispersion calculée en supposant ces paires indépendantes peut aussi paraître trop optimiste.

**Vérification construite** : conserver un ensemble réservé avec d'autres axes et positions, puis comparer les chaînes fermées obtenues depuis plusieurs sous-ensembles d'apprentissage. Une variation importante de l'extrinsèque malgré un faible résidu d'ajustement signale un manque d'information ou une hypothèse violée. Examiner aussi qualité de pose, timing et rigidité avant de conclure qu'un solveur particulier est responsable.

**Erreurs bloquantes** : Assimiler toutes les paires de poses à autant d’observations indépendantes.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Fiche complète]] ; [OpenCV 4.13, calibrateHandEye, repères, équations et minimum de mouvements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::conception cv_id::CV-HANDEYE-003 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-004

Objectif : tester la fermeture de la chaîne. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-HANDEYE-004
Question: En eye-in-hand, la caméra est solidaire du gripper et la mire reste fixe dans la base robot. L’extrinsèque estimée paraît plausible, mais les points reconstruits se décalent quand le robot tourne. Quel test de chaîne et quelles causes vérifier ?
Reponse: **Noyau attendu** : Noter $G_i$ la transformation gripper→base, $C_i$ mire→caméra et $X$ caméra→gripper, toutes homogènes et avec des unités de translation communes. Calculer $Y_i=G_iXC_i$ sur plusieurs poses réservées : la mire fixe doit donner une transformation mire→base cohérente. Si elle varie, vérifier inversions, unités, timestamps, intrinsics et rigidité de la mire.

**Approfondissement** : Comparer rotations et translations dans leurs unités avant de les agréger. Refaire l’expérience à robot immobile puis en mouvement aide à isoler un délai. Le test est proposé par le projet ; il ne localise pas automatiquement une cause unique.

**Lecture du test** : si la mire est réellement fixe, sa pose dans la base ne doit pas suivre la rotation du gripper. Une variation de $Y_i$ révèle un désaccord dans la chaîne complète, même lorsque les nombres de $X$ semblent plausibles. Cette constance teste une propriété physique, pas une préférence numérique.

**Enquête proposée** : comparer des poses statiques, puis des mouvements de sens et vitesses différents, et inspecter séparément erreur angulaire et translation. Une erreur qui apparaît surtout en mouvement est compatible avec un délai, mais peut aussi combiner plusieurs défauts. La validation sur des poses réservées limite le risque de n'expliquer que les acquisitions d'ajustement.

**Erreurs bloquantes** : Valider sur la seule apparence de X ; corriger une erreur temporelle en ajustant arbitrairement l’extrinsèque.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Fiche complète]] ; [OpenCV 4.13, calibrateHandEye, repères, équations et minimum de mouvements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-HANDEYE-004 provenance::agent pole::B pole::C pole::E
END

## CV-HANDEYE-005

Objectif : distinguer eye-in-hand et eye-to-hand. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-HANDEYE-005
Question: Passer d’une caméra montée sur le gripper à une caméra fixe se résume-t-il à inverser la sortie du solveur ?
Reponse: **Noyau attendu** : Non : les repères fixes et les inconnues de la chaîne changent. Redéfinir les transformations mesurées et inconnues, écrire la chaîne constante, puis dériver l’équation et le contrat d’entrée adaptés.

**Approfondissement** : En eye-in-hand, caméra→gripper est fixe. En eye-to-hand, c’est caméra→base qui est fixe, tandis que la relation de la mire avec le gripper dépend du montage. Inverser une seule matrice sans reconstruire les relations peut donner un résultat numériquement valide mais physiquement faux.

**Construction du nouveau problème** : identifier ce qui est fixé à la base, ce qui suit l'outil et où se trouve la mire. Écrire ensuite deux chemins reliant les mêmes repères, avec une transformation inconnue constante seulement là où le montage le justifie. C'est cette égalité qui détermine les inverses et mouvements relatifs nécessaires.

**Exemple de piège** : une caméra devenue fixe ne possède plus une pose caméra→gripper constante lorsque l'outil se déplace. Inverser cette ancienne inconnue ne la transforme donc pas magiquement en la nouvelle constante caméra→base. Vérifier les contrats du solveur adaptés au montage et une fermeture sur plusieurs poses. Le raisonnement reste une dérivation géométrique ; aucune commande de robot ni validation d'installation n'est effectuée ici.

**Erreurs bloquantes** : Réutiliser les mêmes entrées puis inverser seulement la sortie.
Source: [[50-calibration-geometrie/references/57-calibration-hand-eye|Fiche complète]] ; [OpenCV 4.13, calibrateHandEye, repères, équations et minimum de mouvements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-HANDEYE-005 provenance::agent pole::B pole::C pole::E
END
