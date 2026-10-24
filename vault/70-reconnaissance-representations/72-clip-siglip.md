# CLIP, SigLIP et reconnaissance par texte — cartes

Fiche : [[70-reconnaissance-representations/references/72-clip-siglip|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-CLIP-001

Objectif : interpréter le zero-shot CLIP. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-CLIP-001
Question: Comment CLIP peut-il classer une image avec des classes qu’on décrit par texte ?
Reponse: **Noyau attendu** : Encoder image et descriptions, comparer dans un espace aligné puis appliquer une règle de décision sur ces candidats.

**Approfondissement** : La qualité dépend des prompts, du vocabulaire et du domaine ; l’absence d’entraînement d’une nouvelle tête n’implique pas l’absence d’hypothèses.

**Mécanisme de décision** : chaque description de classe définit un candidat textuel dans l'espace partagé. L'image est comparée à ces candidats, puis une règle choisit ou rejette une proposition. Le vocabulaire constitue donc une partie de la définition du classifieur, même sans entraînement d'une tête supplémentaire.

**Exemple construit** : proposer seulement « pièce correcte » et « pièce rayée » force une comparaison entre ces formulations, même si l'image montre une autre pièce ou un fond vide. Le meilleur candidat peut être le moins mauvais. Tester des descriptions alternatives sur validation, conserver des négatifs et définir une politique de rejet mesurée. La similarité image–texte peut servir à la recherche ou à une classification par descriptions ; elle ne fournit pas à elle seule une explication générée ni la localisation précise d'une rayure. L'interface et la métrique doivent correspondre à la sortie demandée.

**Erreurs bloquantes** : Présenter CLIP comme un générateur de légende autonome.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Fiche complète]] ; [CLIP, §§2.3,3 et limites §6](https://arxiv.org/abs/2103.00020) ; [SigLIP, §3 et Algorithm1](https://arxiv.org/abs/2303.15343).
Tags: cv::pilote cv::d07 famille::comprehension cv_id::CV-CLIP-001 provenance::agent pole::A pole::D
END

## CV-CLIP-002

Objectif : refuser une probabilité trompeuse. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-CLIP-002
Question: Pourquoi un softmax CLIP de 0,95 sur deux labels ne prouve-t-il pas que l’objet annoncé est présent ?
Reponse: **Noyau attendu** : Il normalise des scores entre ces candidats ; l’ensemble peut ne contenir aucune bonne description et le modèle peut être hors domaine.

**Approfondissement** : Tester rejets, nouveaux candidats et calibration sur données représentatives.

**Lecture du softmax** : la normalisation partage une masse entre les candidats fournis. Retirer un concurrent ou changer la température modifie les valeurs sans ajouter de preuve dans l'image. Un score très élevé peut donc seulement indiquer que les autres formulations reçoivent des scores encore plus faibles.

**Exemple de test construit** : conserver l'image et ajouter une description plausible jusque-là absente. Observer comment le classement et les valeurs changent, puis comparer à une référence annotée. Inclure aussi des images sans bonne classe et des scènes hors domaine. Une politique de rejet doit être validée sur ces cas, au point de fonctionnement du produit. La calibration concerne l'accord entre scores et fréquences d'erreurs dans un protocole donné ; elle ne découle pas de la somme égale à un. L'interprétation doit donc rester relative à l'ensemble des candidats et à la distribution observée.

**Erreurs bloquantes** : Interpréter tout score normalisé comme une probabilité de vérité.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Fiche complète]] ; [CLIP, §§2.3,3 et limites §6](https://arxiv.org/abs/2103.00020) ; [SigLIP, §3 et Algorithm1](https://arxiv.org/abs/2303.15343).
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-CLIP-002 provenance::agent pole::A pole::D
END

## CV-CLIP-003

Objectif : distinguer objectifs contrastifs. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-CLIP-003
Question: Quelle différence centrale sépare l’objectif CLIP softmax de l’objectif SigLIP ?
Reponse: **Noyau attendu** : SigLIP utilise une loss sigmoid sur des paires plutôt qu’une normalisation softmax globale du lot comme CLIP.

**Approfondissement** : Ce changement d’objectif n’accorde pas automatiquement une calibration en exploitation ; les détails de température, biais et données comptent.

**Raisonnement sur l'objectif** : une normalisation softmax de lot met les candidats en compétition dans le dénominateur. Un objectif sigmoid par paire traite les compatibilités selon une autre construction d'apprentissage, avec ses paramètres et ses positifs/négatifs. Cela modifie ce que les scores sont entraînés à représenter, sans supprimer le rôle des données.

**Conséquence d'évaluation** : comparer les modèles sur les mêmes images, textes, classes absentes et critères de rejet, en consignant checkpoint et prétraitement. Un changement d'objectif ne signifie pas qu'une valeur de sortie soit automatiquement une probabilité fiable sur une ligne industrielle. Une fonction bornée entre zéro et un peut encore être mal calibrée hors distribution. La carte demande de distinguer les mécanismes d'apprentissage ; un classement empirique des variantes réclamerait un protocole et des mesures supplémentaires, plutôt qu'une conclusion tirée du seul nom de la loss.

**Erreurs bloquantes** : Déduire une probabilité fiable du seul mot sigmoid.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Fiche complète]] ; [CLIP, §§2.3,3 et limites §6](https://arxiv.org/abs/2103.00020) ; [SigLIP, §3 et Algorithm1](https://arxiv.org/abs/2303.15343).
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-CLIP-003 provenance::agent pole::A pole::D
END

## CV-CLIP-004

Objectif : tester la sensibilité au texte. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-CLIP-004
Question: Comment tester un classifieur image–texte sans régler les prompts sur le test final ?
Reponse: **Noyau attendu** : Créer des variantes sur validation, figer prompts et vocabulaire, puis mesurer erreurs et rejets sur test séparé par scène/domaine.

**Approfondissement** : Conserver négatifs et cas sans bonne classe ; mesurer la sensibilité aux formulations sans sélectionner a posteriori le meilleur score test.

**Pourquoi les prompts sont des paramètres** : choisir une formulation en fonction de son score sur le test utilise indirectement ses labels pour régler le système. Même sans gradient, cette sélection peut suradapter la décision aux exemples censés fournir une mesure indépendante.

**Protocole proposé** : définir un ensemble de formulations et une règle de combinaison sur validation, conserver le vocabulaire et les seuils, puis ouvrir le test final une fois les choix figés. Séparer scènes ou domaines selon le futur usage et documenter les catégories absentes. Rapporter les erreurs et la sensibilité aux formulations sans ne garder que les cas favorables. Pour une nouvelle itération après analyse d'échecs, préparer une autre évaluation indépendante. Une bonne pratique de transfert conserve ainsi une distinction entre exploration du modèle et estimation de sa généralisation, même lorsque l'outil est qualifié de zero-shot.

**Erreurs bloquantes** : Choisir les prompts d’après les résultats du test final.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Fiche complète]] ; [Radford et al., CLIP, §§2.3, 3.1 et limites §6](https://arxiv.org/abs/2103.00020) ; protocole de validation proposé par le projet.
Tags: cv::pilote cv::d07 famille::evaluation cv_id::CV-CLIP-004 provenance::agent pole::A pole::D
END
