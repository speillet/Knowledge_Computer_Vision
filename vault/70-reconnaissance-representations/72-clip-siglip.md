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

**Approfondissement** : La qualité dépend des prompts, du vocabulaire et du domaine ; aucun entraînement d’une nouvelle tête ne signifie aucune hypothèse.

**Erreurs bloquantes** : Présenter CLIP comme un générateur de légende autonome.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Fiche complète]] ; [CLIP, §§2.3,3 et limites §7](https://arxiv.org/abs/2103.00020) ; [SigLIP, §3 et Algorithm1](https://arxiv.org/abs/2303.15343).
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

**Erreurs bloquantes** : Interpréter tout score normalisé comme une probabilité de vérité.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Fiche complète]] ; [CLIP, §§2.3,3 et limites §7](https://arxiv.org/abs/2103.00020) ; [SigLIP, §3 et Algorithm1](https://arxiv.org/abs/2303.15343).
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

**Erreurs bloquantes** : Déduire une probabilité fiable du seul mot sigmoid.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Fiche complète]] ; [CLIP, §§2.3,3 et limites §7](https://arxiv.org/abs/2103.00020) ; [SigLIP, §3 et Algorithm1](https://arxiv.org/abs/2303.15343).
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

**Erreurs bloquantes** : Choisir les prompts d’après les résultats du test final.
Source: [[70-reconnaissance-representations/references/72-clip-siglip|Fiche complète]] ; [CLIP, §§2.3,3 et limites §7](https://arxiv.org/abs/2103.00020) ; [SigLIP, §3 et Algorithm1](https://arxiv.org/abs/2303.15343).
Tags: cv::pilote cv::d07 famille::evaluation cv_id::CV-CLIP-004 provenance::agent pole::A pole::D
END
