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

**Décomposition du processus** : durant l'apprentissage, on construit des exemples bruités à des niveaux choisis et on optimise une cible de prédiction selon la formulation. Au sampling, les poids sont utilisés dans une suite d'opérations pour transformer une condition et du bruit en sortie. Les données vues et les décisions prises à ces deux moments diffèrent.

**Exemple de contrôle** : conserver poids et conditionnement, puis comparer plusieurs nombres d'étapes et seeds sur un ensemble défini. Mesurer coût, diversité et fidélité à la condition plutôt que conclure depuis une seule image favorable. Le marginal forward à un niveau de bruit n'est pas toute la procédure inverse de génération. Une sortie vraisemblable peut remplir des détails non observés ; elle ne devient pas une mesure physique parce que l'entraînement a convergé. Pour une tâche de restauration, la conservation de l'information critique doit donc être évaluée séparément.

**Erreurs bloquantes** : Assimiler le processus forward d’ajout de bruit à toute la génération.
Source: [[120-generatif-multimodal/references/122-generation-restauration|Fiche complète]] ; [DDPM, équation 4 et algorithmes 1–2](https://arxiv.org/abs/2006.11239).
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

**Deux sources possibles de perte** : l'autoencodeur transforme l'image en une représentation plus compacte, puis le processus génératif agit dans cet espace. Un détail mal conservé par la première transformation peut être difficile à préserver ensuite, même si le débruitage latent fonctionne selon son objectif.

**Ablation proposée** : comparer d'abord l'image brute à sa reconstruction autoencodeur sans ajout du processus de diffusion. Examiner les petits défauts et les frontières utiles, puis introduire la génération à condition identique. Mesurer qualité perceptuelle et fidélité métier séparément, avec références réservées. Cette séparation localise l'origine d'une dégradation et évite de tout attribuer au sampler. La compression vise un compromis de calcul et de représentation ; sa pertinence dépend de ce que l'application doit conserver. Une perte peu visible pour une scène générale peut être décisive pour une rayure ou une mesure fine.

**Erreurs bloquantes** : Supposer la compression sans conséquence sur la fidélité.
Source: [[120-generatif-multimodal/references/122-generation-restauration|Fiche complète]] ; [Latent Diffusion Models, §§3.1–3.2 et fig. 1 : compression perceptuelle et diffusion latente](https://arxiv.org/abs/2112.10752).
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

**Pourquoi la netteté peut tromper** : plusieurs images détaillées peuvent être compatibles avec une observation basse résolution. Le modèle utilise ses régularités apprises pour choisir une reconstruction plausible. Cette décision peut créer une texture crédible sans correspondre à la fissure réellement présente.

**Validation proposée** : conserver le brut et, si possible, une référence acquise avec une résolution adaptée, puis mesurer conservation, largeur et localisation des défauts. Comparer à une restauration simple avec hypothèses explicites et examiner les erreurs sur cas rares. Ne pas remplacer la preuve d'acquisition par une image générée plus convaincante. Une amélioration de score perceptuel ou de reconstruction globale peut masquer la modification d'une structure petite mais critique. Le choix dépend de l'objectif : produire une illustration et mesurer une fissure n'exigent pas la même fidélité. Aucun générateur n'est exécuté dans ce cas, qui sert à raisonner sur le contrat de sortie.

**Erreurs bloquantes** : Valider une mesure dimensionnelle sur une image plus jolie seulement.
Source: [[120-generatif-multimodal/references/122-generation-restauration|Fiche complète]] ; Cas construit du projet : fidélité à une fissure versus plausibilité ; [Latent Diffusion Models, §3.1 et fig. 1](https://arxiv.org/abs/2112.10752) documente le rôle de la compression/reconstruction.
Tags: cv::pilote cv::d12 famille::diagnostic cv_id::CV-DIFFUSION-003 provenance::agent pole::A pole::D pole::E
END
