---
id: CV-METRIQUES-TEMPS
type: metrique-protocole
domaine: d13
poles: [B, C, D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-VIO", "CV-SORT"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d13]
---
# Évaluer identités, trajectoires et localisation 3D

## Problème, données et hypothèses

Évaluer le livrable temporel ou métrique plutôt qu'une seule détection. Entrées : séquences/pistes ou poses horodatées et vérité terrain ; sorties : scores sous règles d'association et alignement annoncés. Les trajectoires absentes et échecs font partie du protocole.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-VIO](../../60-vision-3d/references/63-slam-vio.md) ; [CV-SORT](../../110-tracking-association/references/111-sort.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

MOTA agrège certains faux positifs, manques et échanges d'identité ; IDF1 cible une association d'identités ; HOTA équilibre détection et association selon ses seuils. ATE compare une trajectoire alignée ; RPE compare des déplacements relatifs. Ne pas substituer une métrique à une autre sans définir la tâche.

## Mathématiques, conventions et unités

À un seuil $\alpha$, $HOTA_\alpha=\sqrt{DetA_\alpha AssA_\alpha}$ puis le score moyenne les seuils ; ce n'est pas la racine du produit des moyennes. Pour des poses corps→monde, $T_i$ désignant la vérité terrain et $\hat T_i$ l’estimation, $E_{ij}=(T_i^{-1}T_j)^{-1}(\hat T_i^{-1}\hat T_j)$ définit une erreur relative. La translation est en mètres et la rotation exige angle/unité précisés.

## Paramètres et propriétés

Association, classes, ignore, timestamps, interpolation, intervalle de RPE et alignement. Monoculaire visuel : Sim(3) peut être justifié ; VIO métrique avec gravité fixée : translation/yaw selon protocole. Un alignement libre peut masquer les erreurs que l'on cherche à mesurer.

## Coût et implémentation

Les évaluateurs ont des conventions spécifiques ; versionner fichiers de sortie et paramètres. Aucun benchmark réel n'est exécuté ; aucun score calculé sur jouet n'est appelé HOTA complet.

## Évaluation et variation contrôlée

Variation analytique : conserver boîtes mais permuter IDs au croisement ; AP par frame peut rester identique alors que l'association change. Pour trajectoire, injecter une échelle fausse et comparer alignements autorisés ; une Sim(3) peut la cacher.

## Échecs et diagnostic

Score global bon mais trajectoire rare perdue : analyser longueurs, segments et sous-groupes. Écart entre outils : aligner protocole avant de conclure à un bug.

## Alternatives et usages

Choisir une batterie liée au produit : détection, identité, localisation et coût. NDS/mAP nuScenes constituent encore un autre protocole de sortie 3D.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent identité, agrégation HOTA et alignement de trajectoire. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-METRIQUES-TEMPS-001

**Question de travail** : Comment deux systèmes peuvent-ils avoir la même AP frame par frame et des qualités de tracking différentes ?

**Réponse de référence** : Les boîtes/classes peuvent être identiques tandis que les IDs sont échangés ou fragmentés ; AP ne mesure pas cette continuité.

**Exemple construit** : conserver exactement les boîtes et les classes de deux piétons, mais échanger leurs IDs au milieu de la vidéo. Les associations spatiales à la GT peuvent rester identiques à chaque frame pour l'évaluation de détection. La continuité temporelle, elle, devient fausse.

**Choix de mesures** : examiner détection, association, fragments et cas de disparition dans un protocole de séquence annoncé. Une métrique d'identité demande ses propres règles d'association et d'agrégation ; un nombre de changements d'ID ne remplace pas forcément tous les autres aspects du suivi. Comparer les mêmes séquences, périodes ignorées et détections lorsqu'on cherche l'apport de l'association. Le résultat produit peut aussi dépendre des sorties émises pendant les pertes. Cette distinction explique pourquoi le parcours introduit l'IoU avant SORT, puis revient aux métriques temporelles après avoir défini les responsabilités du tracker.

### Cas lié à CV-METRIQUES-TEMPS-005

**Question de travail** : Deux outils donnent des erreurs de trajectoire différentes pour les mêmes poses. Que contrôler ?

**Réponse de référence** : Appariement temporel, interpolation, conventions de pose, alignement, intervalles et traitement des pertes.

**Enquête reproductible** : vérifier d'abord les timestamps et combien de poses ont effectivement été appariées. Contrôler ensuite sens caméra→monde ou monde→caméra, unités des translations et convention de rotation. Rejouer une trajectoire synthétique connue avec une translation globale puis une erreur d'échelle pour observer ce que chaque outil retire.

**Comparaison équitable** : conserver fichiers et versions, groupe d'alignement, interpolation et intervalle de RPE, ainsi que traitement des absences. Deux outils peuvent afficher ATE tout en différant dans ces choix. Une différence de protocole ne constitue pas immédiatement une erreur de l'estimateur. Une fois les conventions alignées, les écarts restants justifient une inspection plus précise du calcul. La trace doit permettre à un autre ingénieur de reproduire le même ensemble de poses comparées et la même grandeur, et pas seulement une image de trajectoires superposées.

**Repère documentaire de cette passe** : [Luiten et al., HOTA](https://arxiv.org/pdf/2009.07736), définition HOTA, DetA, AssA et agrégation. Les autres développements figurent dans les [cartes associées](../132-tracking-trajectoires.md).

## Sources et cartes

- [Sturm et al., 2012, §VII-A/B, équations 1–4](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf) : RPE et ATE ; distinction avec l’erreur relative par sous-trajectoires de Zhang–Scaramuzza.

- [HOTA, §§5–6](https://arxiv.org/abs/2009.07736).
- [Zhang–Scaramuzza, §III/TableI et évaluation](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf).
- [nuScenes, métriques de détection](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md).
- [Cartes associées](../132-tracking-trajectoires.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
