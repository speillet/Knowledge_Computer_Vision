# Recalage global et ICP local — cartes

Fiche : [[60-vision-3d/references/62-recalage-global-icp|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-ICP-001

Objectif : séparer initialisation globale et raffinement. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-ICP-001
Question: Pourquoi combiner FPFH/RANSAC puis ICP plutôt que lancer ICP depuis n’importe quelle pose ?
Reponse: **Noyau attendu** : L’initialisation globale cherche une zone compatible à partir de correspondances ; ICP affine localement et peut converger sur de mauvaises associations.

**Approfondissement** : FPFH décrit la géométrie ; la pose doit être estimée puis validée. Le succès dépend aussi du recouvrement et des symétries.

**Pourquoi l'initialisation compte** : ICP construit ou actualise des associations à partir de la pose courante. Si cette pose est éloignée, les plus proches voisins peuvent représenter d'autres surfaces ; optimiser sur ces paires peut renforcer un mauvais alignement local. La recherche globale utilise d'autres indices pour proposer une région de pose avant le raffinement.

**Exemple construit** : deux pieds identiques d'une pièce peuvent offrir deux alignements locaux plausibles. Un faible résidu après ICP ne désigne pas automatiquement le bon pied. Contrôler l'orientation et la translation finales, le recouvrement et des surfaces distinctives réservées. Consigner sens source→cible et unités avant toute comparaison. Les features géométriques et RANSAC apportent des hypothèses utiles ; elles restent limitées par texture géométrique, symétries et recouvrement. Une odométrie ou une contrainte métier peut fournir une autre initialisation si elle est justifiée et évaluée.

**Erreurs bloquantes** : Présenter ICP comme un solveur global garanti.
Source: [[60-vision-3d/references/62-recalage-global-icp|Fiche complète]] ; [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::algorithme cv_id::CV-ICP-001 provenance::agent pole::B pole::C
END

## CV-ICP-002

Objectif : interpréter un résidu point-to-plane. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-ICP-002
Question: Que mesure $n^T(Rp+t-q)$ dans ICP point-to-plane ?
Reponse: **Noyau attendu** : La composante du désalignement selon la normale cible unitaire, en unité de longueur.

**Approfondissement** : Sur un plan, un déplacement tangent peut peu changer ce résidu ; contrôler observabilité et pose, pas seulement RMSE.

**Lecture géométrique** : le vecteur $Rp+t-q$ est une erreur 3D entre un point source transformé et son correspondant cible. Le produit avec la normale conserve seulement sa composante perpendiculaire au plan tangent local. Le carré de ce scalaire pénalise donc l'écart à cette surface dans une direction particulière.

**Exemple analytique** : pour une normale $(0,0,1)^T$, un déplacement de dix centimètres selon $x$ ne change pas directement ce résidu, tandis qu'un déplacement selon $z$ le change. Sur une scène composée d'un seul plan, certaines translations tangentes peuvent ainsi rester mal contraintes. Plusieurs orientations de surfaces peuvent fournir des contraintes complémentaires, si les associations et normales sont correctes. Le choix point-to-plane exploite la structure locale ; il ne transforme pas chaque correspondance en trois observations indépendantes. Vérifier la pose avec des contraintes ou une référence qui couvrent les mouvements utiles.

**Erreurs bloquantes** : Prendre ce scalaire pour une erreur complète 3D dans toutes directions.
Source: [[60-vision-3d/references/62-recalage-global-icp|Fiche complète]] ; [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-ICP-002 provenance::agent pole::B pole::C
END

## CV-ICP-003

Objectif : refuser un petit consensus trompeur. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-ICP-003
Question: ICP annonce un petit RMSE mais n’aligne qu’un coin de deux nuages. Que rapporter ?
Reponse: **Noyau attendu** : Recouvrement, seuil, distribution des correspondances et erreur de pose sur référence indépendante.

**Approfondissement** : Le RMSE conditionne son résultat aux paires retenues ; réduire le consensus peut faire baisser le nombre sans améliorer la tâche.

**Pourquoi la mesure peut s'améliorer à tort** : un RMSE calculé sur les correspondances retenues résume seulement cet ensemble. Un seuil très strict peut conserver un petit coin bien aligné et exclure presque tout le reste. Le chiffre diminue alors sans que la pose explique la partie importante de la scène.

**Comparaison proposée** : annoncer seuil, unités, nombre et répartition des paires, proportion de recouvrement selon la convention du protocole, puis erreur de transformation lorsque la référence existe. Visualiser les régions non expliquées et tester les mêmes paramètres sur des scènes réservées. Si la pièce est symétrique, examiner des repères distinctifs ou des contraintes supplémentaires. La qualité d'un ajustement local n'est pas la qualité de toute la registration : il faut définir la zone utile et ce qu'un échec coûte au système avant de classer deux poses sur un scalaire.

**Erreurs bloquantes** : Classer la pose au RMSE seul.
Source: [[60-vision-3d/references/62-recalage-global-icp|Fiche complète]] ; [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-ICP-003 provenance::agent pole::B pole::C
END

## CV-ICP-004

Objectif : garder les unités du recalage. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-ICP-004
Question: Pourquoi réutiliser un seuil ICP de 0,02 après passage des nuages de mètres à millimètres change-t-il le problème ?
Reponse: **Noyau attendu** : Le seuil est une longueur dans l’unité des coordonnées ; il faut propager l’échelle aux paramètres pertinents.

**Approfondissement** : Vérifier voxel et voisinages aussi, puis le modèle de bruit.

**Calcul d'échelle** : 0,02 m correspond à 20 mm. Si les coordonnées sont multipliées par mille mais le seuil reste numériquement 0,02, le rayon admissible devient mille fois plus petit dans la scène physique. Le nombre de correspondances et le comportement de l'optimisation peuvent changer brutalement.

**Contrôle complet** : convertir ensemble les coordonnées, translations, tailles de voxel et rayons de voisinage exprimés en longueur. Les rotations restent sans unité, tandis que les coûts quadratiques suivent le carré de l'échelle. Dans un exemple construit, appliquer le même recalage avant et après conversion cohérente doit décrire la même transformation physique, à effets numériques près. Vérifier ce cas simple avant de modifier les critères d'arrêt ou l'initialisation. Une normalisation des données doit donc être une transformation de contrat tracée, et non une modification isolée des points d'entrée.

**Erreurs bloquantes** : Traiter le seuil comme un nombre sans unité.
Source: [[60-vision-3d/references/62-recalage-global-icp|Fiche complète]] ; [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::pratique cv_id::CV-ICP-004 provenance::agent pole::B pole::C
END

## CV-ICP-005

Objectif : choisir une variante ICP. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-ICP-005
Question: Point-to-plane remplace-t-il toujours avantageusement point-to-point ?
Reponse: **Noyau attendu** : Il exploite des normales fiables et une géométrie qui contraint les mouvements utiles ; il peut être mal posé sur certaines surfaces ou normales bruitées.

**Approfondissement** : Comparer initialisation, estimation des normales et précision de pose dans le protocole cible.

**Comparaison des informations utilisées** : point-to-point pénalise une différence de positions selon trois composantes ; point-to-plane utilise une approximation locale de surface. Lorsque les normales et l'initialisation sont adaptées, cette approximation peut être efficace. Si les normales sont instables ou la géométrie pauvre, le critère peut perdre son intérêt ou laisser certaines directions peu contraintes.

**Ablation construite** : conserver nuages, correspondances initiales, seuil et référence, puis comparer les variantes en faisant varier séparément le bruit des normales et le recouvrement. Mesurer erreur de pose, convergence, échecs et coût. Une baisse du résidu propre à une variante n'est pas directement comparable au résidu d'une autre formulation. Le bon choix dépend de la surface observée et de la précision demandée. Ne pas utiliser un seul cas plan favorable pour annoncer une supériorité sur toutes les pièces et toutes les initialisations.

**Erreurs bloquantes** : Annoncer une domination universelle d’une variante.
Source: [[60-vision-3d/references/62-recalage-global-icp|Fiche complète]] ; [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-ICP-005 provenance::agent pole::B pole::C
END
