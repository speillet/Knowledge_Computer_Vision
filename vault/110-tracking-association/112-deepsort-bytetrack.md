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

**Raisonnement d'association** : deux boîtes proches peuvent se ressembler géométriquement tout en appartenant à des personnes différentes. Une distance d'apparence ajoute une observation qui peut les distinguer ; le mouvement et le gating restreignent les candidats plausibles. La cascade organise ces décisions selon la méthode, au lieu de transformer le filtre en reconnaissance d'identité.

**Exemple de limite** : si les crops sont petits, occultés ou hors du domaine d'entraînement ReID, leurs embeddings peuvent devenir peu discriminants. Augmenter leur poids peut alors aggraver l'affectation. Contrôler distances de vraies et fausses paires dans le domaine cible, puis comparer mouvement seul, apparence seule et combinaison à détecteur fixe. La fusion de coûts doit avoir une interprétation et un protocole ; une proximité cosinus n'est pas automatiquement une probabilité calibrée d'être la même personne, ni une garantie après une disparition longue.

**Erreurs bloquantes** : Présenter toute proximité d’apparence comme identité vraie.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Fiche complète]] ; [DeepSORT, §§2.1–2.3 : Mahalanobis, apparence et cascade](https://arxiv.org/abs/1703.07402).
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

**Pourquoi garder certaines boîtes faibles** : une cible partiellement occultée peut rester visible tout en obtenant un score faible du détecteur. Supprimer systématiquement ces observations coupe une piste qui aurait pu être prolongée grâce à son historique. La seconde association cherche à récupérer cette information parmi les pistes encore candidates.

**Compromis produit** : une boîte faible peut aussi être un faux positif. La relier à une piste existante sous des règles données n'est pas la même décision que créer une nouvelle identité sans historique. Tracer les deux étapes et les seuils dans la version utilisée. Dans un test construit, faire varier le score d'une vraie boîte occultée, à localisation fixe, puis introduire de fausses boîtes. Mesurer continuité et fausses pistes ensemble. Le titre de la méthode ne signifie donc pas que toute boîte, quel que soit son score et son contexte, devient une nouvelle piste.

**Erreurs bloquantes** : Assimiler la seconde association à une création massive de pistes faibles.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Fiche complète]] ; [ByteTrack, §3 Algorithm 1 : deux associations et création depuis les scores élevés restants](https://arxiv.org/abs/2110.06864).
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

**Deux ambiguïtés possibles** : l'embedding peut mal transférer d'un domaine piéton vers des pièces, mais les pièces peuvent aussi être réellement indiscernables dans l'image. Dans le second cas, changer le réseau ne crée pas une information visuelle absente. Le mouvement, la cadence ou un marqueur distinctif peut être nécessaire pour réduire l'ambiguïté.

**Enquête construite** : conserver les détections et comparer les distributions de distances pour mêmes et différentes pièces, avec leurs crops. Vérifier résolution, normalisation et occultation, puis comparer les associations sans apparence et avec plusieurs pondérations. Examiner les séquences de croisement plutôt qu'un score moyen d'embedding. Un gain sur des images isolées ne prouve pas la continuité d'identité pendant un contact ou une occultation. Si aucune observation ne départage les hypothèses, signaler l'incertitude au lieu de présenter l'ID comme certain.

**Erreurs bloquantes** : Augmenter aveuglément le poids ReID.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Fiche complète]] ; Diagnostic de transfert construit par le projet ; [DeepSORT, §2.3 : modèle d’apparence piéton](https://arxiv.org/abs/1703.07402).
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

**Ablation causale proposée** : utiliser un fichier de détections horodatées commun aux deux trackers, avec mêmes boîtes, scores et classes. Les différences de pistes proviennent alors de leurs étapes temporelles et de leurs paramètres, dans les limites de ce contrôle. Pour comparer les systèmes complets, mesurer ensuite aussi chaque détecteur avec son tracker.

**Exemple de facteur confondant** : un détecteur qui retrouve une personne après occultation peut améliorer le score d'identité sans changement d'association. À l'inverse, une meilleure association peut être masquée par de nombreuses boîtes absentes. Reporter donc qualité de détection, erreurs d'identité, fragments, coût et règles de naissance/perte. Conserver un split par séquence et des réglages figés sur le test. Une comparaison équitable ne demande pas forcément un détecteur unique pour tous les usages, mais exige de dire précisément quelle composante a changé et ce que l'on peut lui attribuer.

**Erreurs bloquantes** : Attribuer tout gain final au tracker sans contrôler l’amont.
Source: [[110-tracking-association/references/112-deepsort-bytetrack|Fiche complète]] ; Protocole de comparaison proposé par le projet ; [SORT, §3.1 et tableau 1 : effet du détecteur](https://arxiv.org/abs/1602.00763).
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-ASSOCIATION-004 provenance::agent pole::C pole::D pole::E
END
