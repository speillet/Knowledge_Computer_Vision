---
id: CV-DIFFUSION
type: comparaison
domaine: d12
poles: [A, D, E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 1
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d12]
---
# VAE, GAN et diffusion pour génération/restauration

## Problème, données et hypothèses

Générer ou restaurer une image selon un objectif distinct de la mesure physique. Entrées : bruit/conditionnement ou image dégradée ; sortie : image plausible sous modèle. Une texture ajoutée peut être visuellement crédible et factuellement fausse.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

VAE apprend un espace latent probabiliste ; GAN oppose génération et discrimination ; diffusion apprend un débruitage dans un processus bruité. La diffusion latente déplace ce processus dans l'espace d'un autoencodeur ; la compression devient une partie du compromis.

## Mathématiques, conventions et unités

Une étape forward peut écrire $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$, $\epsilon\sim\mathcal N(0,I)$ ; t indexe le niveau de bruit. L'entraînement et la procédure d'échantillonnage sont distincts. Les unités dépendent de la représentation normalisée, pas d'une échelle radiométrique physique implicite.

## Paramètres et propriétés

Données, conditionnement, niveaux de bruit, sampler, étapes, guidance et seed. Les variantes changent ; moins d'étapes n'a pas un effet universel sur qualité et fidélité. Une sortie conditionnée ne garantit pas la conservation de tous détails observés.

## Coût et implémentation

Autoencodeur, résolutions et itérations de génération dominent coût/mémoire. Aucun générateur exécuté, aucune image synthétique présentée comme mesure réelle.

## Évaluation et variation contrôlée

Baseline : restauration classique adaptée au bruit, puis modèle appris avec références non dégradées si disponibles. Varier niveau de dégradation et mesurer fidélité des défauts, pas seulement qualité perceptuelle globale.

## Échecs et diagnostic

Un défaut disparaît après super-résolution : vérifier que l'objectif favorise la plausibilité plutôt que sa conservation. Conserver image brute et preuve liée à la mesure utile.

## Alternatives et usages

Génératif pour synthèse/annotation assistée selon validation ; modèle de mesure explicite pour métrologie. Les données synthétiques doivent être évaluées face aux distributions réelles.

## Sources et cartes

- [DDPM, processus et objectif](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html).
- [Latent Diffusion Models](https://arxiv.org/abs/2112.10752).
- [Cartes associées](../122-generation-restauration.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
