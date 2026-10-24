# Évaluer identités, trajectoires et localisation 3D — cartes

Fiche : [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-METRIQUES-TEMPS-001

Objectif : séparer détection et identité. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-001
Question: Comment deux systèmes peuvent-ils avoir la même AP frame par frame et des qualités de tracking différentes ?
Reponse: **Noyau attendu** : Les boîtes/classes peuvent être identiques tandis que les IDs sont échangés ou fragmentés ; AP ne mesure pas cette continuité.

**Approfondissement** : Utiliser métriques et diagnostics d’association sous protocole de séquence identique.

**Exemple construit** : conserver exactement les boîtes et les classes de deux piétons, mais échanger leurs IDs au milieu de la vidéo. Les associations spatiales à la GT peuvent rester identiques à chaque frame pour l'évaluation de détection. La continuité temporelle, elle, devient fausse.

**Choix de mesures** : examiner détection, association, fragments et cas de disparition dans un protocole de séquence annoncé. Une métrique d'identité demande ses propres règles d'association et d'agrégation ; un nombre de changements d'ID ne remplace pas forcément tous les autres aspects du suivi. Comparer les mêmes séquences, périodes ignorées et détections lorsqu'on cherche l'apport de l'association. Le résultat produit peut aussi dépendre des sorties émises pendant les pertes. Cette distinction explique pourquoi le parcours introduit l'IoU avant SORT, puis revient aux métriques temporelles après avoir défini les responsabilités du tracker.

**Erreurs bloquantes** : Déduire qualité d’identité de l’AP seule.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Fiche complète]] ; [HOTA, §§4–5 : détection et association](https://arxiv.org/abs/2009.07736) ; permutation d’IDs : cas construit du projet.
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-TEMPS-001 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-002

Objectif : respecter l’agrégation HOTA. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-002
Question: Pourquoi calculer sqrt(moyenne DetA × moyenne AssA) ne reproduit-il pas nécessairement HOTA ?
Reponse: **Noyau attendu** : La référence calcule la racine du produit à chaque seuil puis moyenne ces scores ; les opérations ne commutent pas en général.

**Approfondissement** : Conserver aussi conventions de matching, ignore et localisation ; un résumé de formule n’est pas tout l’évaluateur.

**Contre-exemple analytique** : prendre deux seuils avec couples $(DetA,AssA)=(1,0)$ et $(0,1)$. La racine du produit vaut zéro à chaque seuil, donc leur moyenne vaut zéro. Les moyennes des composantes valent chacune 0,5 ; la racine de leur produit vaut alors 0,5. L'ordre des opérations change bien le résultat. Ce cas montre une propriété algébrique, sans constituer un benchmark HOTA.

**Conséquence pratique** : conserver les valeurs au niveau où le protocole les combine, puis utiliser le code de référence et ses paramètres. Des règles différentes de matching, de classes ou d'ignore peuvent aussi modifier les composantes avant l'agrégation. Une formule résumée aide à interpréter l'équilibre entre détection et association ; elle ne remplace pas toute la définition. Comparer un chiffre reconstruit à la main à un outil officiel exige donc de reproduire les mêmes entrées et toutes les conventions pertinentes.

**Erreurs bloquantes** : Intervertir librement moyenne et racine.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Fiche complète]] ; [HOTA, §5 : HOTA par seuil puis moyenne sur les seuils](https://arxiv.org/abs/2009.07736).
Tags: cv::pilote cv::d13 famille::raisonnement cv_id::CV-METRIQUES-TEMPS-002 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-003

Objectif : choisir un alignement de trajectoire. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-003
Question: Pourquoi une Sim(3) peut-elle être un mauvais choix pour évaluer un VIO censé être métrique ?
Reponse: **Noyau attendu** : Elle ajuste l’échelle et peut donc masquer une erreur métrique que le système devait éviter.

**Approfondissement** : Le groupe d’alignement doit suivre les jauges et l’objectif ; avec gravité fixée, une rotation libre peut aussi masquer des erreurs d’inclinaison.

**Exemple d'erreur masquée** : une trajectoire deux fois trop grande peut être visuellement superposée à la référence si l'alignement ajuste librement l'échelle. Le score après ce recalage ne teste alors plus la métricité que le système devait fournir. Il peut être correct pour une autre tâche à échelle libre.

**Protocole proposé** : annoncer les jauges légitimes avant d'observer les résultats et garder une référence physique indépendante. Séparer translation globale arbitraire, lacet global et dérives relatives dans le temps. Si la gravité fournit une direction absolue sous les hypothèses du système, une rotation 3D entièrement libre peut également retirer une erreur utile à mesurer. Le choix ne consiste pas à chercher la transformation donnant le plus joli tracé : il définit quelles erreurs sont volontairement exclues du score. Rapporter cette transformation et la justifier par les informations réellement disponibles.

**Erreurs bloquantes** : Optimiser l’alignement pour obtenir le meilleur score sans justification.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Fiche complète]] ; [Zhang–Scaramuzza, §III et tableau I : groupes d’alignement](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf).
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-TEMPS-003 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-004

Objectif : distinguer ATE et RPE. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-004
Question: ATE et RPE répondent-elles exactement à la même question ?
Reponse: **Noyau attendu** : ATE évalue une trajectoire après alignement ; RPE des déplacements relatifs à des intervalles définis.

**Approfondissement** : Préciser temps/distance d’intervalle, agrégation, translation/rotation et échecs ; longueur du trajet et bouclage influencent l’interprétation.

**Lecture de deux échelles temporelles** : une trajectoire peut conserver des déplacements locaux assez précis tout en accumulant une dérive globale. À l'inverse, une correction de boucle peut améliorer la superposition globale sans rendre chaque mouvement local parfaitement exact. Les deux mesures interrogent donc des propriétés complémentaires.

**Évaluation proposée** : définir intervalle de déplacement, appariement temporel et unité, puis reporter translation et rotation séparément. Pour une RPE, des intervalles courts et longs ne représentent pas la même difficulté. Pour une ATE, le groupe d'alignement retire certaines ambiguïtés et doit être annoncé. Conserver segments perdus et durée de disponibilité : une méthode qui cesse d'émettre sur les cas difficiles ne doit pas apparaître parfaite en ne mesurant que les portions faciles. Les chiffres se lisent avec longueur, mouvement et couverture de la séquence, pas comme des constantes universelles de qualité.

**Erreurs bloquantes** : Comparer des nombres sans protocole, unité ou intervalle.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Fiche complète]] ; [Sturm et al., §VII-A/B : RPE et ATE](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf) ; [Zhang–Scaramuzza, §IV et tableau II](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf).
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-METRIQUES-TEMPS-004 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-005

Objectif : comparer des évaluateurs temporels. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-005
Question: Deux outils donnent des erreurs de trajectoire différentes pour les mêmes poses. Que contrôler ?
Reponse: **Noyau attendu** : Appariement temporel, interpolation, conventions de pose, alignement, intervalles et traitement des pertes.

**Approfondissement** : Rejouer un petit cas connu puis le même fichier/version ; ne pas attribuer l’écart immédiatement à l’estimateur.

**Enquête reproductible** : vérifier d'abord les timestamps et combien de poses ont effectivement été appariées. Contrôler ensuite sens caméra→monde ou monde→caméra, unités des translations et convention de rotation. Rejouer une trajectoire synthétique connue avec une translation globale puis une erreur d'échelle pour observer ce que chaque outil retire.

**Comparaison équitable** : conserver fichiers et versions, groupe d'alignement, interpolation et intervalle de RPE, ainsi que traitement des absences. Deux outils peuvent afficher ATE tout en différant dans ces choix. Une différence de protocole ne constitue pas immédiatement une erreur de l'estimateur. Une fois les conventions alignées, les écarts restants justifient une inspection plus précise du calcul. La trace doit permettre à un autre ingénieur de reproduire le même ensemble de poses comparées et la même grandeur, et pas seulement une image de trajectoires superposées.

**Erreurs bloquantes** : Comparer seulement le nom ATE affiché par les outils.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Fiche complète]] ; Diagnostic de protocole du projet ; [Sturm et al., §VII : synchronisation et poses](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf) ; [Zhang–Scaramuzza, §§III–IV](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf).
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-METRIQUES-TEMPS-005 provenance::agent pole::B pole::C pole::D
END
