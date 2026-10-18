---
id: CV-FUSION
type: methode
domaine: d01
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-SE3"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# Kalman, EKF, UKF et ESKF pour la fusion

## Problème, données et hypothèses

Fusionner mesures et prédictions horodatées en représentant leurs incertitudes. Entrées : modèle d'état, mesures, bruit et timestamps ; sortie : état estimé et covariance. Les incertitudes supposées et les associations conditionnent la cohérence du résultat.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SE3](12-rotations-se3.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Kalman linéaire alterne prédiction et correction. EKF linéarise les modèles ; UKF propage des sigma-points ; ESKF sépare état nominal et petite erreur tangentielle. Corriger l'erreur puis l'injecter dans la pose exige aussi un reset cohérent de covariance.

## Mathématiques, conventions et unités

L'innovation est $\nu=z-h(x^-)$, de covariance $S=HP^-H^T+R$ dans l'EKF. Le score $\nu^TS^{-1}\nu$ est sans unité si modèle et covariance sont cohérents. $P^-=FP^+F^T+Q$ utilise le pas de temps réel. Dans l'ESKF, après injection, $P\leftarrow GPG^T$ selon la Jacobienne de reset G ; remettre l'erreur moyenne à zéro ne remet pas l'incertitude à zéro.

## Paramètres et propriétés

Choisir état, fréquence, Q/R, traitement des biais, délais et mesure absente. Un bruit artificiellement petit donne une confiance excessive. UKF ne garantit pas de réparer toute non-linéarité, distribution multimodale ou mauvais modèle.

## Coût et implémentation

L'état et la fréquence dominent les produits matriciels ; la cohérence temporelle prime sur une promesse de fréquence. Aucune implémentation complète de filtre n'est fournie ; l'exemple scalaire exécuté du premier lot illustre seulement une correction.

## Évaluation et variation contrôlée

Variation proposée : augmenter R en conservant mesure/prédiction ; la correction doit suivre moins fortement la mesure. Vérifier ensuite l'innovation sur séquences réservées ; une covariance faible seule n'atteste pas la précision réelle.

## Échecs et diagnostic

Deux capteurs en désaccord : comparer horodatage, extrinsèques, unités, biais et corrélations avant de diminuer R. Des innovations systématiquement biaisées suggèrent autre chose qu'un bruit blanc accru.

## Alternatives et usages

Filtrage pour faible latence ; lissage/graphes pour réestimer plusieurs états. Une mesure redondante corrélée ne doit pas être comptée deux fois comme information indépendante.

## Sources et cartes

- [Solà, ESKF : injection et reset, §§5–6](https://arxiv.org/abs/1711.02508).
- [Cartes associées](../13-kalman-ekf-eskf.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
