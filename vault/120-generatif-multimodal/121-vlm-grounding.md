# VLM, grounding et frontière vision–action — cartes

Fiche : [[120-generatif-multimodal/references/121-vlm-grounding|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::120-generatif-multimodal

## CV-VLM-001

Objectif : situer encodeur VLM et VLA. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-VLM-001
Question: Que distingue CLIP, un VLM génératif et un VLA ?
Reponse: **Noyau attendu** : CLIP compare des représentations image–texte ; un VLM génère des sorties conditionnées par vision/langage ; un VLA produit une interface d’action selon sa conception.

**Approfondissement** : Les tâches, métriques et validations diffèrent. Étudier les VLA ici ne comprend pas le contrôle du robot.

**Erreurs bloquantes** : Présenter une description textuelle comme une politique de commande validée.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Fiche complète]] ; [BLIP-2, architecture](https://arxiv.org/abs/2301.12597) ; [LLaVA original](https://arxiv.org/abs/2304.08485) ; [Flamingo](https://arxiv.org/abs/2204.14198) ; [OpenVLA, interface actions](https://openvla.github.io/).
Tags: cv::pilote cv::d12 famille::comparaison cv_id::CV-VLM-001 provenance::agent pole::A pole::D
END

## CV-VLM-002

Objectif : situer un connecteur visuel. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-VLM-002
Question: Quel problème traite le Q-Former de BLIP-2 dans son architecture originale ?
Reponse: **Noyau attendu** : Relier un encodeur visuel et un modèle de langage préentraînés par une représentation apprise et un entraînement adapté.

**Approfondissement** : Ne pas généraliser ce connecteur à toutes variantes de VLM ; il ne garantit pas à lui seul le grounding exact.

**Erreurs bloquantes** : Attribuer Q-Former à tout modèle multimodal ou l’assimiler à un simple prompt.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Fiche complète]] ; [BLIP-2, architecture](https://arxiv.org/abs/2301.12597) ; [LLaVA original](https://arxiv.org/abs/2304.08485) ; [Flamingo](https://arxiv.org/abs/2204.14198) ; [OpenVLA, interface actions](https://openvla.github.io/).
Tags: cv::pilote cv::d12 famille::comprehension cv_id::CV-VLM-002 provenance::agent pole::A pole::D
END

## CV-VLM-003

Objectif : concevoir un index vidéo. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-VLM-003
Question: Cas D — conception : indexer des heures de vidéo avec événements recherchés. Comment arbitrer VLM généraliste ou détection/tracking/règles ?
Reponse: **Noyau attendu** : Définir événements, sorties temporelles, coût et latence ; construire des baselines sur clips annotés, y compris négatifs/événements courts ; comparer rappel, hallucinations et coût complet.

**Approfondissement** : Un système hybride peut être justifié ; documenter échantillonnage, accès au futur et conditions de rejet. La fluidité ne mesure pas le rappel des événements.

**Erreurs bloquantes** : Choisir sur quelques descriptions plausibles sans vérité terrain.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Fiche complète]] ; [BLIP-2, architecture](https://arxiv.org/abs/2301.12597) ; [LLaVA original](https://arxiv.org/abs/2304.08485) ; [Flamingo](https://arxiv.org/abs/2204.14198) ; [OpenVLA, interface actions](https://openvla.github.io/).
Tags: cv::pilote cv::d12 famille::conception cv_id::CV-VLM-003 provenance::agent pole::A pole::D cas_pole::D::conception
END

## CV-VLM-004

Objectif : départager hallucination et observation insuffisante. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-VLM-004
Question: Cas D — diagnostic : un VLM décrit des objets absents sur des images industrielles. Quelle enquête mène à une correction vérifiable ?
Reponse: **Noyau attendu** : Vérifier image réellement reçue, résolution/prompt, distribution, négatifs et référence ; classer hallucinations et omissions puis tester une intervention à la fois.

**Approfondissement** : Comparer à une détection structurée ou une règle de rejet mesurée. Un score textuel haut ne prouve pas l’objet ; ne pas régler le prompt sur le test final.

**Erreurs bloquantes** : Accepter la phrase fluide comme preuve visuelle ou garantir une suppression totale par prompting.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Fiche complète]] ; [BLIP-2, architecture](https://arxiv.org/abs/2301.12597) ; [LLaVA original](https://arxiv.org/abs/2304.08485) ; [Flamingo](https://arxiv.org/abs/2204.14198) ; [OpenVLA, interface actions](https://openvla.github.io/).
Tags: cv::pilote cv::d12 famille::diagnostic cv_id::CV-VLM-004 provenance::agent pole::A pole::D cas_pole::D::diagnostic
END
