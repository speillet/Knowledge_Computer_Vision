---
id: CV-DIFFUSION
type: comparaison
domaine: d12
poles: [A, D, E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 3
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

Un échantillon du marginal forward au niveau $t$ peut s’écrire $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon$, $\epsilon\sim\mathcal N(0,I)$, avec $\bar\alpha_t=\prod_{s=1}^{t}(1-\beta_s)$ et $\beta_s$ la variance de bruit de chaque transition. Ce n’est pas une transition élémentaire depuis $x_{t-1}$ ; $t$ indexe le niveau de bruit. L'entraînement et la procédure d'échantillonnage sont distincts. Les unités dépendent de la représentation normalisée, pas d'une échelle radiométrique physique implicite.

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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent distribution conditionnelle et fidélité de la restauration. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-DIFFUSION-001

**Question de travail** : Dans un modèle de diffusion, pourquoi entraînement et sampling ne sont-ils pas la même opération ?

**Réponse de référence** : L’entraînement apprend une règle de débruitage sous une distribution de bruit ; le sampling utilise cette règle dans une procédure pour produire une sortie.

**Décomposition du processus** : durant l'apprentissage, on construit des exemples bruités à des niveaux choisis et on optimise une cible de prédiction selon la formulation. Au sampling, les poids sont utilisés dans une suite d'opérations pour transformer une condition et du bruit en sortie. Les données vues et les décisions prises à ces deux moments diffèrent.

**Exemple de contrôle** : conserver poids et conditionnement, puis comparer plusieurs nombres d'étapes et seeds sur un ensemble défini. Mesurer coût, diversité et fidélité à la condition plutôt que conclure depuis une seule image favorable. Le marginal forward à un niveau de bruit n'est pas toute la procédure inverse de génération. Une sortie vraisemblable peut remplir des détails non observés ; elle ne devient pas une mesure physique parce que l'entraînement a convergé. Pour une tâche de restauration, la conservation de l'information critique doit donc être évaluée séparément.

### Cas lié à CV-DIFFUSION-003

**Question de travail** : Une super-résolution rend une image nette mais modifie une fissure. Pourquoi est-ce un défaut pour l’inspection ?

**Réponse de référence** : La plausibilité visuelle n’est pas la fidélité à l’observation critique ; le modèle peut supprimer ou inventer une structure.

**Pourquoi la netteté peut tromper** : plusieurs images détaillées peuvent être compatibles avec une observation basse résolution. Le modèle utilise ses régularités apprises pour choisir une reconstruction plausible. Cette décision peut créer une texture crédible sans correspondre à la fissure réellement présente.

**Validation proposée** : conserver le brut et, si possible, une référence acquise avec une résolution adaptée, puis mesurer conservation, largeur et localisation des défauts. Comparer à une restauration simple avec hypothèses explicites et examiner les erreurs sur cas rares. Ne pas remplacer la preuve d'acquisition par une image générée plus convaincante. Une amélioration de score perceptuel ou de reconstruction globale peut masquer la modification d'une structure petite mais critique. Le choix dépend de l'objectif : produire une illustration et mesurer une fissure n'exigent pas la même fidélité. Aucun générateur n'est exécuté dans ce cas, qui sert à raisonner sur le contrat de sortie.

**Repère documentaire de cette passe** : [Latent Diffusion Models](https://arxiv.org/html/2112.10752v2), §3, espace latent et conditionnement. Les autres développements figurent dans les [cartes associées](../122-generation-restauration.md).

## Sources et cartes

- [VAE, résumé et §2](https://arxiv.org/abs/1312.6114) : modèle latent et inférence variationnelle.
- [GAN, résumé](https://arxiv.org/abs/1406.2661) : apprentissage adversarial générateur/discriminateur.

- [DDPM, processus et objectif](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html).
- [Latent Diffusion Models](https://arxiv.org/abs/2112.10752).
- [Cartes associées](../122-generation-restauration.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
