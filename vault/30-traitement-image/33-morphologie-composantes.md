# Morphologie et composantes connexes — cartes

Fiche : [[30-traitement-image/references/33-morphologie-composantes|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::30-traitement-image

## CV-MORPHO-001

Objectif : distinguer ouverture et fermeture. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-MORPHO-001
Question: Quel effet géométrique distingue ouverture et fermeture binaires, et pourquoi choisir la taille du structurant avec la tâche ?
Reponse: **Noyau attendu** : L’ouverture érode puis dilate et peut retirer de petites structures de premier plan ; la fermeture dilate puis érode et peut combler des trous ou intervalles. Choisir le structurant selon les tailles et formes à conserver.

**Approfondissement** : Retirer un petit objet peut nettoyer du bruit ou effacer un défaut ; valider sur tailles et formes critiques.

**Explication géométrique** : l'érosion exige que le structurant tienne dans le premier plan ; elle retire donc des positions proches de certaines frontières. La dilatation étend ensuite les positions conservées. Dans une ouverture, une structure trop étroite pour survivre à l'érosion ne réapparaît pas simplement parce qu'une dilatation suit. Dans une fermeture, des intervalles suffisamment petits peuvent être comblés.

**Choix d'échelle** : une taille en pixels représente une taille physique seulement si résolution et géométrie sont connues. Un structurant utile sur une caméra peut effacer les défauts recherchés après un changement de résolution. Dans un exemple construit, comparer un défaut fin et une poussière de taille voisine montre que la morphologie ne possède aucune information sémantique pour les départager. Évaluer donc suppressions et fusions sur les cas critiques, avec polarité du masque, forme du structurant et traitement du bord explicités.

**Erreurs bloquantes** : Décrire ces opérations comme des filtres sémantiques garantis.
Source: [[30-traitement-image/references/33-morphologie-composantes|Fiche complète]] ; [OpenCV 4.13.0, Morphological Transformations, §§1–4](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html).
Tags: cv::pilote cv::d03 famille::comparaison cv_id::CV-MORPHO-001 provenance::agent pole::A pole::E
END

## CV-MORPHO-002

Objectif : choisir une connectivité. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-MORPHO-002
Question: Un masque ne contient que deux pixels de premier plan, qui se touchent uniquement par un coin. Combien de composantes en connectivité 4 puis 8 ?
Reponse: **Noyau attendu** : Deux en connectivité 4 ; une en connectivité 8.

**Approfondissement** : La convention doit être conservée dans l’évaluation et les mesures de trous/objets.

**Raisonnement par voisinage** : en connectivité 4, on peut avancer vers les voisins partageant un côté ; aucun chemin de premier plan ne relie ici les deux pixels. En connectivité 8, un pas diagonal est également admissible, et les pixels appartiennent au même ensemble relié. La différence vient de la définition du graphe de voisinage, pas de la classe des pixels.

**Conséquence pratique** : un même masque peut donc produire des nombres d'objets différents sans qu'un seul pixel change. Pour compter des pièces ou des cellules, décider quelle convention correspond aux contacts que l'on souhaite considérer. Conserver cette convention lors de la mesure et signaler séparément le fond lorsque l'API le compte comme un label. Les numéros de labels sont des identifiants internes à l'image : leur ordre n'indique pas une classe ni l'identité du même objet à la frame suivante. Ce dernier problème demanderait une association temporelle.

**Erreurs bloquantes** : Annoncer un nombre sans connectivité.
Source: [[30-traitement-image/references/33-morphologie-composantes|Fiche complète]] ; [OpenCV 4.13.0, connectedComponents, paramètres connectivity et labels](https://docs.opencv.org/4.13.0/d3/dc0/group__imgproc__shape.html) ; décompte déduit de la connectivité.
Tags: cv::pilote cv::d03 famille::raisonnement cv_id::CV-MORPHO-002 provenance::agent pole::A pole::E
END

## CV-MORPHO-003

Objectif : expliquer une fusion de pièces. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-MORPHO-003
Question: Après fermeture morphologique, deux pièces proches sont comptées comme une seule. Quelle hypothèse vérifier ?
Reponse: **Noyau attendu** : Le structurant peut avoir créé un pont ; inspecter le masque avant/après et la distance entre objets.

**Approfondissement** : Réduire ou adapter l’opération sous contrôle, puis envisager une séparation à marqueurs ; ne pas seulement changer le filtre d’aire.

**Mécanisme de l'erreur** : la dilatation peut joindre deux régions séparées par un intervalle plus petit que l'échelle du structurant. L'érosion suivante ne restaure pas nécessairement cet intervalle ; la fermeture peut conserver une région commune. L'étiquetage connexe compte alors correctement un seul ensemble relié, mais cet ensemble ne représente plus un seul objet du monde.

**Contrôle construit** : afficher les pixels ajoutés entre les masques avant et après, puis faire varier la taille et l'orientation du structurant à image fixe. Si le nombre d'objets change quand le pont apparaît, la cause est localisée. Un filtrage par aire après fusion ne retrouve pas les deux pièces : il agit sur la région déjà regroupée. Selon la scène, préserver l'intervalle, utiliser des marqueurs de séparation ou une segmentation d'instances. Toute correction doit aussi être évaluée sur des objets réellement jointifs, pour éviter de résoudre un cas en fragmentant les autres.

**Erreurs bloquantes** : Prendre une composante connexe pour un objet garanti.
Source: [[30-traitement-image/references/33-morphologie-composantes|Fiche complète]] ; [OpenCV 4.13.0, Morphological Transformations, §§1–4](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html) ; diagnostic de pont construit par le projet.
Tags: cv::pilote cv::d03 famille::diagnostic cv_id::CV-MORPHO-003 provenance::agent pole::A pole::E
END
