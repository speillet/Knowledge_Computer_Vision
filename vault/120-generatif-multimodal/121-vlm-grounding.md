# VLM, grounding et frontière vision–action — cartes

Fiche : [[120-generatif-multimodal/references/121-vlm-grounding|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::120-generatif-multimodal

## CV-VLM-001

Objectif : situer encodeur VLM et VLA. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-VLM-001
Question: Que distingue CLIP utilisé pour comparer image et texte, un VLM génératif et un VLA ?
Reponse: **Noyau attendu** : CLIP compare des représentations image–texte ; un VLM génère des sorties conditionnées par vision/langage ; un VLA produit une interface d’action selon sa conception.

**Approfondissement** : Les tâches, métriques et validations diffèrent. Étudier les VLA ici ne comprend pas le contrôle du robot.

**Définir l'interface** : comparer des embeddings sert à classer ou rechercher parmi des candidats ; générer du texte produit une séquence conditionnée ; produire des actions engage une autre représentation et un autre environnement d'évaluation. Une architecture peut partager des briques sans que ces contrats deviennent interchangeables.

**Exemple construit** : « une pièce est présente » peut être une description plausible, mais ne fournit ni une boîte validée ni une commande robotique correctement référencée. Pour une application, préciser format de sortie, temps de validité et référence attendue, puis mesurer omissions et fausses assertions. Si des actions sont étudiées, distinguer connaissance de l'interface et validation d'une politique en boucle fermée. Le parcours couvre ici la perception et ses limites ; le passage à la commande ne se déduit pas d'une réponse verbale convaincante ni d'un score de génération élevé. Les preuves doivent correspondre à ce que le système promet réellement.

**Erreurs bloquantes** : Présenter une description textuelle comme une politique de commande validée.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Fiche complète]] ; [CLIP, §2.3](https://arxiv.org/abs/2103.00020) ; [LLaVA, §§4.1–4.2](https://arxiv.org/abs/2304.08485) ; [OpenVLA, architecture et actions](https://openvla.github.io/), consulté le 2026-10-20.
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

**Intuition du connecteur** : l'encodeur visuel et le modèle de langage préentraînés ne partagent pas automatiquement une interface qui transporte l'information utile. Le Q-Former apprend une représentation intermédiaire à partir de requêtes et d'objectifs adaptés pour relier ces espaces dans BLIP-2.

**Ce que cela ne démontre pas** : une connexion entraînée peut permettre des sorties conditionnées sans garantir que chaque détail affirmé soit présent dans l'image. Des informations peuvent être mal représentées, peu résolues ou dominées par les régularités linguistiques. Pour un diagnostic construit, vérifier l'image reçue, les variations de prompt et des exemples négatifs annotés, puis mesurer les sorties utiles. Comparer une version précise de l'architecture plutôt que supposer que tous les VLM utilisent le même pont. Le mécanisme explique une organisation de l'apprentissage et du transfert ; il ne remplace pas un protocole de grounding sur le domaine cible.

**Erreurs bloquantes** : Attribuer Q-Former à tout modèle multimodal ou l’assimiler à un simple prompt.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Fiche complète]] ; [BLIP-2, §§3.1–3.3 : Q-Former entre encodeur visuel et LLM gelés](https://arxiv.org/abs/2301.12597).
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

**Choix de sortie proposé** : pour une règle précise comme « objet entrant dans une zone puis en sortant », détection, tracking et logique temporelle rendent certaines hypothèses inspectables. Pour des descriptions ouvertes, un VLM peut apporter une flexibilité différente. Les deux options peuvent se compléter sans que la fluidité du texte mesure le rappel d'événements.

**Comparaison** : fixer l'échantillonnage, la durée minimale des événements, l'accès au futur et une référence d'intervalles annotés. Inclure absences d'événement, scènes proches et cas courts entièrement entre deux échantillons. Mesurer omissions, assertions fausses, localisation temporelle et coût d'encodage/décodage sur le volume réel. Une meilleure description d'un clip sélectionné ne garantit pas une bonne indexation de plusieurs heures. Le protocole doit faire apparaître le compromis entre couverture, coût et précision de la réponse attendue.

**Erreurs bloquantes** : Choisir sur quelques descriptions plausibles sans vérité terrain.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Fiche complète]] ; Cas et protocole d’indexation conçus par le projet ; exemple de modèle image/vidéo : [Flamingo, §2](https://arxiv.org/abs/2204.14198).
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

**Ablation discriminante** : garder l'image et les labels de référence, modifier uniquement la formulation sur validation, puis comparer à une chaîne visuelle structurée. Tester aussi des images sans objet cible et des variations de résolution. Cela aide à distinguer une information mal transmise d'une tendance à compléter linguistiquement une scène familière.

**Critère de correction** : chercher une baisse mesurée des assertions fausses sans augmenter silencieusement les omissions. Une consigne de prudence peut changer le style des réponses sans rendre leur contenu plus exact. Conserver une politique de refus, les entrées réellement traitées et le checkpoint pour reproduire les erreurs. Toute amélioration reste liée au protocole ; aucun prompt ne constitue ici une garantie générale de supprimer les hallucinations sur tous les nouveaux produits.

**Erreurs bloquantes** : Accepter la phrase fluide comme preuve visuelle ou garantir une suppression totale par prompting.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[120-generatif-multimodal/references/121-vlm-grounding|Fiche complète]] ; Enquête proposée par le projet ; architecture et objectif de référence : [LLaVA, §§4.1–4.2](https://arxiv.org/abs/2304.08485).
Tags: cv::pilote cv::d12 famille::diagnostic cv_id::CV-VLM-004 provenance::agent pole::A pole::D cas_pole::D::diagnostic
END
