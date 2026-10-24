---
id: CV-MATCH-APPRIS
type: pipeline
domaine: d04
poles: [B]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-SIFT", "CV-ORB", "CV-HOMOGRAPHIE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# SuperPoint, LightGlue et LoFTR

## Problème, données et hypothèses

Construire des correspondances avec des composants appris, sans confondre détecteur, descripteur et matcher. SuperPoint produit des points/descripteurs ; LightGlue apparie des features compatibles ; LoFTR propose des correspondances detector-free coarse-to-fine. Ces sorties ne sont pas automatiquement une pose correcte.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SIFT](41-sift.md) ; [CV-ORB](42-orb.md) ; [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

SuperPoint apprend détection et description avec adaptation homographique. LightGlue exploite contexte et interactions entre features, avec adaptation de calcul. LoFTR utilise contexte et correspondances grossières puis fines sans requérir un détecteur sparse explicite.

## Mathématiques, conventions et unités

Chaque paire $(x_i,x'_i)$ est dans deux repères image explicites. Après resize ou padding, revenir à des coordonnées comparables avant le résidu géométrique. Un score de matching appris est un score du modèle ; il n'est pas automatiquement une probabilité calibrée sur l'usine.

## Paramètres et propriétés

Choisir checkpoints compatibles avec le type de features, résolution, seuil et politique de calcul. Detector-free ne signifie ni flot pour chaque pixel ni absence d'erreurs. Ne pas comparer des poids ou licences comme s'ils formaient un seul produit.

## Coût et implémentation

Résolution, nombre de features, attention et vérification aval dominent coût/mémoire. Aucun checkpoint téléchargé ou exécuté. Les résultats des auteurs restent liés à leur protocole.

## Évaluation et variation contrôlée

Baseline proposée : SIFT/ORB + même géométrie et même jeu de paires. Faire varier texture puis éclairage séparément ; mesurer succès de recalage, couverture, latence complète et échecs. Prédire un effet possible du contexte, sans annoncer de gain mesuré.

## Échecs et diagnostic

Échec sur surfaces répétitives : inspecter correspondances, répétition et modèle géométrique. Changement de checkpoint : vérifier normalisation et extraction attendues avant de régler seulement le seuil.

## Alternatives et usages

Sparse appris pour points explicites ; LoFTR pour une autre stratégie de correspondances ; ECC quand l'objectif et l'initialisation d'un recalage par intensités sont adaptés.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent compatibilité features–matcher, résolution et validation. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-MATCH-APPRIS-001

**Question de travail** : Que fournit SuperPoint et que rajoute LightGlue pour un recalage entre deux images ?

**Réponse de référence** : SuperPoint fournit des keypoints et des descripteurs ; LightGlue recherche les correspondances entre features compatibles.

**Contrats successifs** : les coordonnées indiquent où les observations se trouvent, les descripteurs représentent leurs voisinages, et le matcher utilise les deux ensembles pour décider quelles paires sont compatibles. L'information contextuelle du matcher peut aider à départager des ressemblances locales, mais elle reste une prédiction apprise sur une distribution de données.

**Exemple de pipeline construit** : extraire les features compatibles avec le checkpoint, convertir les positions dans les repères déclarés, obtenir les candidats, puis estimer une homographie si l'objet observé est plan. Contrôler erreur et couverture sur la région utile. Si la scène présente de la parallaxe, un grand nombre de matches n'autorise pas automatiquement un warp global. Comparer à une baseline SIFT ou ORB sur les mêmes paires. Le remplacement du matcher change la proposition de correspondances ; il ne fournit pas à lui seul la calibration ni la validation finale du système.

### Cas lié à CV-MATCH-APPRIS-005

**Question de travail** : Après ajout de padding, les matches semblent corrects visuellement mais l’homographie est biaisée. Que tester ?

**Réponse de référence** : La conversion des positions depuis le repère du réseau vers chaque image réelle, y compris resize et offsets.

**Exemple analytique** : si le réseau reçoit $x'=sx+p_x$ et $y'=sy+p_y$, où $s$ est le facteur de resize et $(p_x,p_y)$ le padding en pixels réseau, le retour vaut $x=(x'-p_x)/s$, $y=(y'-p_y)/s$. Chaque image peut avoir ses propres paramètres. Soustraire seulement le padding sans remettre l'échelle laisse une erreur systématique.

**Vérification proposée** : suivre trois points connus, notamment un point proche de l'origine et un point éloigné, à travers le prétraitement et son inverse. Contrôler ensuite que le seuil de reprojection est exprimé dans le même repère que les résidus. Une superposition visuelle sur l'image paddée peut sembler juste alors que l'estimateur reçoit des coordonnées de deux espaces différents. Le problème se situe alors dans le contrat des données, et changer le checkpoint ou le seuil du matcher risque de le masquer sans le résoudre.

**Repère documentaire de cette passe** : [LightGlue, dépôt officiel](https://github.com/cvg/LightGlue), README, Usage et extracteurs compatibles. Les autres développements figurent dans les [cartes associées](../44-superpoint-lightglue-loftr.md).

## Sources et cartes

- [SuperPoint, méthode et Homographic Adaptation](https://arxiv.org/abs/1712.07629).
- [LightGlue, README, Usage et Advanced configuration (consulté le 2026-10-20)](https://github.com/cvg/LightGlue).
- [LoFTR, §3](https://arxiv.org/abs/2104.00680).
- [Cartes associées](../44-superpoint-lightglue-loftr.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
