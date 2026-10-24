# Ajouts prioritaires — 2026-10-24

Périmètre autorisé : intégrer les PR existantes et compléter les lacunes prioritaires,
selon le choix explicite de l’apprenant. Huit nouvelles fiches et 38 cartes visent
matching classique, calibration et tracking. Les 244 IDs du lot après PR 16 sont
préservés ; le lot courant compte 60 fiches et 282 cartes.

## Choix du contenu et sources

Les méthodes sont retenues pour leur utilité de choix ou de diagnostic, et non
pour compléter artificiellement chaque famille de carte. Chaque fiche fournit
contrat des données, mécanisme, mathématiques, limites, coût, évaluation et
variation contrôlée. Les expériences proposées sont distinctes des calculs
analytiques réellement exécutés.

| Sujet | Lacune et compétences | Source effectivement consultée |
| --- | --- | --- |
| Harris et Shi–Tomasi — structure locale et points suivables | APP-017 ; APP-018 : mécanisme, choix, diagnostic et évaluation, niveau usage opérationnel | [Harris et Stephens 1988, auto-corrélation et réponse de coin](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf) |
| FAST et BRIEF — détecter un coin puis décrire son voisinage | APP-019 ; APP-020 : mécanisme, choix, diagnostic et évaluation, niveau usage opérationnel | [Rosten et Drummond 2006, §§2–3, segment test et apprentissage](https://www.edwardrosten.com/work/rosten_2006_machine.pdf) |
| FLANN — recherche approchée et contrat de distance | APP-022 : mécanisme, choix, diagnostic et évaluation, niveau usage opérationnel | [Muja et Lowe 2009, §§2–3, recherche approchée et configuration](https://www.cs.ubc.ca/research/flann/uploads/FLANN/flann_visapp09.pdf) |
| Calibration fisheye — projection angulaire et validation hors centre | APP-026 : mécanisme, choix, diagnostic et évaluation, niveau usage opérationnel | [OpenCV 4.13, fisheye, Detailed Description et estimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html) |
| Hand-eye calibration — résoudre AX = XB sans mélanger les repères | APP-027 : mécanisme, choix, diagnostic et évaluation, niveau usage opérationnel | [OpenCV 4.13, calibrateHandEye, repères, équations et minimum de mouvements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) |
| Farnebäck — flot dense par expansion polynomiale | APP-089 : mécanisme, choix, diagnostic et évaluation, niveau usage opérationnel | [Farnebäck 2003, §§2–3, expansion et déplacement, §3.5 multi-échelle](https://www.diva-portal.org/smash/get/diva2:273847/FULLTEXT01.pdf) |
| MOSSE et KCF — tracking par filtres de corrélation | APP-093 : mécanisme, choix, diagnostic et évaluation, niveau usage opérationnel | [Bolme et al. 2010, §§3.2–3.5, MOSSE, mise à jour et PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf) |
| MeanShift et CamShift — suivre une distribution d’apparence | APP-092 : mécanisme, choix, diagnostic et évaluation, niveau usage opérationnel | [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html) |

Les documentations OpenCV 4.13 ont été consultées directement et avec Context7 :
résolution `/websites/opencv_4_13_0`, puis requêtes sur conventions fisheye/hand-eye,
coins/descripteurs/matching, et flot/tracking. Les interfaces ont été vérifiées,
mais aucun appel OpenCV ou solveur complet n’a été exécuté. Les publications
FAST, BRIEF, FLANN, Farnebäck, MOSSE et KCF ont été ouvertes avec leurs passages
méthodologiques ; aucun chiffre de vitesse historique n’est promis sur le matériel
cible. Le PDF original de Shi–Tomasi hébergé par CMU n’a pas été accessible ;
le critère et le contrat OpenCV sont sourcés par sa documentation officielle.

## Inventaire et profondeur

Les dix entrées APP correspondantes restent versionnées avec leur ID, leurs
compétences et leurs dépendances, et pointent vers les fiches rédigées.
119 cibles restent ouvertes. Une comparaison de deux méthodes partage une fiche
canonique ; elle ne prétend pas traiter tous leurs dérivés ou implémentations.
Une promotion de cible exige désormais une fiche réelle : le catalogue refuse
une référence absente ou un ID APP dupliqué.

## Calculs contrôlés

Python standard, calculs exécutés hors dépôt : réponses Harris −308,04 et 336 ;
Hamming 2 ; exemple de coûts construits FLANN 2,1 contre 0,3 s puis 12 contre
30 s ; projection à 60° et focale 300 px : 314,16 contre 519,62 px ; déplacement
quadratique (2,−1) px ; flot converti (100,−50) px/s ; PSR 6 et centroïde 13 px.
Ces calculs n’exécutent ni détecteur, ni recherche de voisins, ni calibration,
ni suivi vidéo. Ils ne constituent pas un benchmark ou une mesure physique.

## Contrôles et limites

Résultats exécutés : 37 tests réussis ; contrôleur OK sur 141 documents Markdown,
60 fiches et 282 cartes ; catalogue à jour sur 18 documents ; 129 IDs APP conservés
(dix fiches associées, 119 entrées ouvertes). Les fichiers des 244 cartes déjà
présentes après PR 16 restent inchangés par ce lot.

Le `main.js` officiel Obsidian_to_Anki 3.6.0 a été retéléchargé et son SHA256
vérifié : `dcca559c8001a041ff11a5def4c6f9096969514249d1938db78ec6a7ee55bfef`.
Un harness temporaire, avec API Obsidian et identités Anki simulées, a scanné les
141 fichiers : 282 notes et IDs uniques, 14 sous-decks, puis 282 mises à jour
et zéro ajout à la seconde passe. Maths, bloc de code et SVG ont été convertis.
Aucune requête à Anki n’a été envoyée ; le harness n’est pas inclus dans le dépôt
et ne prouve pas l’historique ou le rendu applicatif.
Provenance agent et état `redige` conservés. Export réel, historique Anki,
rendu Android, rappel et validation scientifique indépendante restent ouverts.
Le travail `.apkg` présent dans le workspace initial est préservé sans publication
ou reconstruction dans ce lot.
