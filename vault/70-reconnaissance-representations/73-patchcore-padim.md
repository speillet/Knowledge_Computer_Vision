# Inspection : golden template, PatchCore et PaDiM — cartes

Fiche : [[70-reconnaissance-representations/references/73-patchcore-padim|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-ANOMALIES-001

Objectif : choisir modèle de nominal. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-ANOMALIES-001
Question: Quel compromis distingue golden template, PatchCore et PaDiM pour inspection ?
Reponse: **Noyau attendu** : Template compare à une référence alignée ; PatchCore utilise une banque de features ; PaDiM estime des distributions avec covariance par position.

**Approfondissement** : Choisir selon variabilité nominale, alignement, mémoire et évaluation métier ; aucun ne connaît tous défauts possibles.

**Lecture des hypothèses** : une comparaison directe au template exige que les écarts géométriques et photométriques légitimes soient suffisamment maîtrisés. Une banque de patches nominaux cherche des voisins représentatifs ; un modèle de distribution par position représente autrement la variabilité et les corrélations. Le mot anomalie désigne ici un écart à cette référence, pas une définition universelle du défaut métier.

**Exemple construit** : un éclairage nouveau peut déplacer toutes les features et augmenter les scores sans pièce physiquement défectueuse. Un défaut absent de l'apprentissage peut au contraire être peu visible dans la représentation. Comparer les méthodes sur lots indépendants, défauts critiques et variations nominales, avec coût complet et seuil de décision. Une bonne localisation de score doit encore être reliée à une tolérance métier. Le choix dépend de ce qui est stable dans l'acquisition et de ce qui doit être considéré comme acceptable.

**Erreurs bloquantes** : Décrire ces scores comme des probabilités universelles de défectuosité.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Fiche complète]] ; [Roth et al., PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265) ; [Defard et al., PaDiM, §III, équations 1–2](https://arxiv.org/abs/2011.08785) ; baseline template définie par le projet.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-ANOMALIES-001 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-002

Objectif : expliquer le coreset. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-ANOMALIES-002
Question: Dans PatchCore, à quoi sert un coreset de features nominales ?
Reponse: **Noyau attendu** : Réduire la banque en conservant une représentation utile de sa diversité, pour limiter mémoire et recherche.

**Approfondissement** : Le sous-échantillonnage modifie un compromis couverture/coût ; mesurer les défauts et faux rejets, pas seulement la taille de banque.

**Compromis de représentation** : une banque exhaustive peut contenir beaucoup de patches redondants. En sélectionner un sous-ensemble représentatif réduit mémoire et calcul de voisins, mais peut retirer des variations nominales rares. Une pièce conforme peu représentée peut alors devenir artificiellement éloignée de la banque.

**Ablation proposée** : conserver extracteur, données et seuil de comparaison, puis faire varier seulement la taille ou la sélection de banque. Mesurer temps, mémoire, faux rejets par condition nominale et défauts manqués. Vérifier aussi que la banque n'est pas contaminée par des pièces mal classées comme nominales. Un coreset est une approximation de la diversité de référence, pas un jeu d'exemples positifs de défauts. La mémoire réduite constitue un gain de ressource ; son utilité produit exige encore que la couverture nécessaire soit conservée au point de fonctionnement retenu.

**Erreurs bloquantes** : Prendre le coreset pour un ensemble de défauts supervisés.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Fiche complète]] ; [PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265) ; [PaDiM, §III](https://arxiv.org/abs/2011.08785).
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-ANOMALIES-002 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-003

Objectif : détecter une dérive du nominal. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-ANOMALIES-003
Question: Le score d’anomalie monte sur toutes les pièces après changement d’éclairage. Que tester ?
Reponse: **Noyau attendu** : Comparer acquisition/prétraitement, recalage et distribution des features au nominal, puis examiner des pièces réellement contrôlées.

**Approfondissement** : Réviser la référence ou le système lumineux après validation ; changer le seuil seul peut cacher de vrais défauts.

**Diagnostic par hypothèses** : la hausse peut correspondre à une vraie dérive produit, à un changement lumineux ou à une rupture du prétraitement. Le score seul ne départage pas ces explications parce qu'il mesure un écart à la référence apprise.

**Enquête construite** : repasser des pièces physiquement contrôlées sous les deux acquisitions, comparer les images et les features à prétraitement constant, puis tester le recalage. Examiner également les petites zones critiques, pas seulement la moyenne de score. Si l'éclairage est la cause, stabiliser l'acquisition ou réviser le nominal avec une validation indépendante. Augmenter le seuil peut faire disparaître les alertes tout en masquant un défaut auparavant détectable. Une correction doit donc être évaluée simultanément sur conformité et défauts connus, et son domaine de validité documenté. L'absence d'alerte après réglage n'est pas en soi une preuve de résolution.

**Erreurs bloquantes** : Étiqueter automatiquement toute hausse de score comme défaut physique.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Fiche complète]] ; [Roth et al., PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265) ; diagnostic d’acquisition déduit par le projet.
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-ANOMALIES-003 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-004

Objectif : concevoir une inspection à défauts rares. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-ANOMALIES-004
Question: Cas E — conception : très peu d’images défectueuses, ligne cadencée. Quelle baseline et quelle validation proposer ?
Reponse: **Noyau attendu** : Stabiliser acquisition, définir défauts critiques et tolérances, comparer template/anomalie nominale puis mesurer rejets et défauts manqués sur lots indépendants et variations réalistes.

**Approfondissement** : Prévoir revue des cas incertains, coût complet et suivi des dérives ; aucun taux global ne remplace les défauts rares du besoin.

**Conception proposée** : distinguer une pièce rejetée à tort, un défaut manqué et un cas soumis à vérification. Leur coût n'est pas identique. Stabiliser d'abord l'image et le recalage rend la baseline interprétable ; choisir ensuite si une référence unique ou une distribution nominale représente suffisamment la variabilité acceptable.

**Validation** : séparer pièces et lots entre réglage et test, couvrir les défauts critiques même rares et les perturbations nominales réalistes. Mesurer le point de décision retenu, le taux de vérification et la latence complète sur la ligne visée. Une AUROC résume une courbe de classement ; elle ne donne pas directement le nombre de défauts manqués au seuil exploité. Prévoir collecte et revue de nouveaux cas avant de modifier la référence, afin de ne pas intégrer silencieusement une dérive produit au nominal.

**Erreurs bloquantes** : Valider sur les seules images nominales ou l’AUROC moyenne.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Fiche complète]] ; [Roth et al., PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265) ; [Defard et al., PaDiM, §III, équations 1–2](https://arxiv.org/abs/2011.08785) ; protocole industriel proposé par le projet.
Tags: cv::pilote cv::d07 famille::conception cv_id::CV-ANOMALIES-004 provenance::agent pole::A pole::E cas_pole::E::conception
END
