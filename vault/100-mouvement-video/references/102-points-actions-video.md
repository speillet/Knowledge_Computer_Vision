---
id: CV-VIDEO
type: comparaison
domaine: d10
poles: [D]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-FLOT"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d10]
---
# Suivi de points, actions et compréhension vidéo

## Problème, données et hypothèses

Distinguer trajectoires de points, classification de clips et localisation temporelle d'actions. Entrées : frames horodatées et éventuellement points/prompts ; sorties : trajectoires/visibilité, labels de clip ou intervalles. Leur protocole causal et leur supervision diffèrent.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-FLOT](101-flot-optique.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

CoTracker exploite les interactions spatiales/temporelles pour prédire points et visibilité. TimeSformer et ViViT traitent des patches vidéo avec attention selon leur architecture. VideoMAE préentraîne par reconstruction de tubes masqués ; une tâche finale doit ensuite être définie.

## Mathématiques, conventions et unités

Échantillonner une frame toutes les $\Delta t$ secondes limite les événements directement observés. Un événement plus court peut être manqué selon sa phase. Une fenêtre de L frames à fréquence f couvre environ $(L-1)/f$ secondes entre premier et dernier timestamp ; la convention de durée doit être annoncée.

## Paramètres et propriétés

Version CoTracker/CoTracker3, mode online/offline, stride, fenêtre, visibilité et accès au futur. Un mode fenêtré online peut introduire un délai. Les ratios élevés de masquage VideoMAE sont un choix de méthode, pas une règle universelle.

## Coût et implémentation

Frames, tokens spatio-temporels, fenêtre et mémoire dominent. Aucun modèle exécuté ; ne pas comparer temps de clip et latence de décision en flux.

## Évaluation et variation contrôlée

Baseline : modèle image agrégé puis modèle temporel, mêmes frames et données. Inverser l'ordre ou raréfier l'échantillonnage pour tester l'usage du temps ; mesurer événements courts, visibilité et frontières d'action.

## Échecs et diagnostic

Bon score de clip mais action mal localisée : vérifier que la sortie est un label global et non un intervalle. Points corrects mais mauvais objet : une trajectoire de point n'est pas une classe d'objet.

## Alternatives et usages

Pipeline détection/tracking/règles pour des événements définis ; modèle vidéo ou VLM selon contexte et annotations. Contrôler fuite entre clips d'une même séquence.

## Sources et cartes

- [ViViT, résumé](https://arxiv.org/abs/2103.15691) : tokens spatio-temporels et classification vidéo.
- [CoTracker3, résumé et introduction](https://arxiv.org/abs/2410.11831) : variantes offline (fenêtre unique) et online (fenêtres glissantes).

- [CoTracker, §3](https://arxiv.org/abs/2307.07635).
- [TimeSformer](https://arxiv.org/abs/2102.05095).
- [VideoMAE](https://arxiv.org/abs/2203.12602).
- [Cartes associées](../102-points-actions-video.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
