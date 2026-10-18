# DeepSORT, ByteTrack et association multiobjet — cartes

Fiche : [[110-tracking-association/references/112-deepsort-bytetrack|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-ASSOCIATION-001

Objectif : identifier l’ajout de DeepSORT. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-ASSOCIATION-001
Question: Que rajoute DeepSORT au raisonnement d’association d’un SORT géométrique simple ?
Reponse: **Noyau attendu** : Apparence/ReID et stratégies de gating/cascade, en plus du mouvement, selon sa conception.

**Approfondissement** : Un embedding n’élimine ni mauvaise détection ni ambiguïté et doit être validé dans le domaine cible.

**Erreurs bloquantes** : Présenter toute proximité d’apparence comme identité vraie.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Fiche complète]] ; [DeepSORT, §§2.1–2.3](https://arxiv.org/abs/1703.07402) ; [ByteTrack, §3 Algorithm1](https://arxiv.org/abs/2110.06864) ; [AB3DMOT, contrat 3D](https://arxiv.org/abs/2008.08063).
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-ASSOCIATION-001 provenance::agent pole::C pole::D pole::E
END

## CV-ASSOCIATION-002

Objectif : comprendre l’usage des faibles scores ByteTrack. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-ASSOCIATION-002
Question: ByteTrack crée-t-il une piste pour toute boîte de faible score ?
Reponse: **Noyau attendu** : Non : il exploite d’abord les scores élevés, puis tente de récupérer des observations faibles pour des pistes restantes ; les faibles non associées sont rejetées selon le pipeline.

**Approfondissement** : Vérifier version et cycle de vie ; garder de faibles observations n’est pas accepter indistinctement tous faux positifs.

**Erreurs bloquantes** : Assimiler la seconde association à une création massive de pistes faibles.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Fiche complète]] ; [DeepSORT, §§2.1–2.3](https://arxiv.org/abs/1703.07402) ; [ByteTrack, §3 Algorithm1](https://arxiv.org/abs/2110.06864) ; [AB3DMOT, contrat 3D](https://arxiv.org/abs/2008.08063).
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-ASSOCIATION-002 provenance::agent pole::C pole::D pole::E
END

## CV-ASSOCIATION-003

Objectif : contrôler le transfert ReID. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-ASSOCIATION-003
Question: Un DeepSORT piéton préentraîné échange les IDs de pièces industrielles identiques. Quelle hypothèse vérifier ?
Reponse: **Noyau attendu** : La discrimination et le domaine des embeddings, ainsi que qualité des crops et ambiguïtés physiques des pièces.

**Approfondissement** : Comparer mouvement seul, apparence et combinaison sur séquences annotées ; aucune information d’apparence ne distingue deux objets visuellement identiques par principe.

**Erreurs bloquantes** : Augmenter aveuglément le poids ReID.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Fiche complète]] ; [DeepSORT, §§2.1–2.3](https://arxiv.org/abs/1703.07402) ; [ByteTrack, §3 Algorithm1](https://arxiv.org/abs/2110.06864) ; [AB3DMOT, contrat 3D](https://arxiv.org/abs/2008.08063).
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-ASSOCIATION-003 provenance::agent pole::C pole::D pole::E
END

## CV-ASSOCIATION-004

Objectif : séparer détecteur et association. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-ASSOCIATION-004
Question: Comment comparer deux trackers sans confondre leur association avec un détecteur différent ?
Reponse: **Noyau attendu** : Fixer les mêmes détections ou rapporter explicitement les deux variations ; conserver séquences, seuils et protocole temporel.

**Approfondissement** : Mesurer qualité des pistes et coût total ; AP du détecteur et score d’identité répondent à deux questions.

**Erreurs bloquantes** : Attribuer tout gain final au tracker sans contrôler l’amont.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Fiche complète]] ; [DeepSORT, §§2.1–2.3](https://arxiv.org/abs/1703.07402) ; [ByteTrack, §3 Algorithm1](https://arxiv.org/abs/2110.06864) ; [AB3DMOT, contrat 3D](https://arxiv.org/abs/2008.08063).
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-ASSOCIATION-004 provenance::agent pole::C pole::D pole::E
END
