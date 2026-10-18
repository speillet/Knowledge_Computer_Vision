# VAE, GAN et diffusion pour génération/restauration — cartes

Fiche : [[120-generatif-multimodal/references/122-generation-restauration|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::120-generatif-multimodal

## CV-DIFFUSION-001

Objectif : séparer apprentissage et sampling. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-DIFFUSION-001
Question: Dans un modèle de diffusion, pourquoi entraînement et sampling ne sont-ils pas la même opération ?
Reponse: **Noyau attendu** : L’entraînement apprend une règle de débruitage sous une distribution de bruit ; le sampling utilise cette règle dans une procédure pour produire une sortie.

**Approfondissement** : Le choix du sampler, du nombre d’étapes et du conditionnement change coût et résultats sans rendre la sortie vraie par définition.

**Erreurs bloquantes** : Assimiler le processus forward d’ajout de bruit à toute la génération.
Source: [[120-generatif-multimodal/references/122-generation-restauration|Fiche complète]] ; [DDPM, processus et objectif](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html) ; [Latent Diffusion Models](https://arxiv.org/abs/2112.10752).
Tags: cv::pilote cv::d12 famille::comprehension cv_id::CV-DIFFUSION-001 provenance::agent pole::A pole::D pole::E
END

## CV-DIFFUSION-002

Objectif : situer la diffusion latente. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-DIFFUSION-002
Question: Quel compromis ajoute une diffusion dans l’espace latent d’un autoencodeur ?
Reponse: **Noyau attendu** : Réduire le coût spatial du processus au prix d’une représentation comprimée et de son erreur de reconstruction.

**Approfondissement** : Évaluer aussi ce que l’autoencodeur peut perdre, notamment les petits défauts, et pas seulement le denoiser.

**Erreurs bloquantes** : Supposer la compression sans conséquence sur la fidélité.
Source: [[120-generatif-multimodal/references/122-generation-restauration|Fiche complète]] ; [DDPM, processus et objectif](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html) ; [Latent Diffusion Models](https://arxiv.org/abs/2112.10752).
Tags: cv::pilote cv::d12 famille::comparaison cv_id::CV-DIFFUSION-002 provenance::agent pole::A pole::D pole::E
END

## CV-DIFFUSION-003

Objectif : protéger une observation industrielle. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-DIFFUSION-003
Question: Une super-résolution rend une image nette mais modifie une fissure. Pourquoi est-ce un défaut pour l’inspection ?
Reponse: **Noyau attendu** : La plausibilité visuelle n’est pas la fidélité à l’observation critique ; le modèle peut supprimer ou inventer une structure.

**Approfondissement** : Comparer aux données de référence et conserver le brut ; choisir une mesure adaptée au défaut.

**Erreurs bloquantes** : Valider une mesure dimensionnelle sur une image plus jolie seulement.
Source: [[120-generatif-multimodal/references/122-generation-restauration|Fiche complète]] ; [DDPM, processus et objectif](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html) ; [Latent Diffusion Models](https://arxiv.org/abs/2112.10752).
Tags: cv::pilote cv::d12 famille::diagnostic cv_id::CV-DIFFUSION-003 provenance::agent pole::A pole::D pole::E
END
