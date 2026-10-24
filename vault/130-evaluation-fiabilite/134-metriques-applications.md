# Métriques de segmentation, inspection et applications — cartes

Fiche : [[130-evaluation-fiabilite/references/134-metriques-applications|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-METRIQUES-APPLIQUEES-001

Objectif : distinguer recouvrement et frontière. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-001
Question: Pourquoi Dice et HD95 peuvent-ils raconter des choses différentes sur un même masque ?
Reponse: **Noyau attendu** : Dice mesure un recouvrement ; HD95 une distance de surface selon un percentile/protocole, avec unité physique si les coordonnées sont calibrées.

**Approfondissement** : Définir masques vides, directions et agrégation ; un contour éloigné ou une petite région peut peser différemment.

**Exemple de divergence** : un grand masque peut conserver presque tout son volume alors qu'une petite partie de surface est éloignée. Le recouvrement et une distance de surface pondèrent cet écart différemment. Un percentile écarte aussi une partie des distances extrêmes selon la définition retenue ; ce n'est pas nécessairement la distance maximale.

**Protocole proposé** : annoncer définition des surfaces, distances dirigées ou symétrisées, percentile, espacement et unité. Conserver le traitement des vides et le niveau d'agrégation par cas ou pixel. Examiner les exemples où les métriques divergent pour identifier l'erreur qu'elles révèlent, plutôt que choisir automatiquement le score favorable. Une distance en millimètres nécessite une géométrie physique cohérente. Ces mesures peuvent être complémentaires si l'usage dépend à la fois de couverture et de frontière ; aucune valeur isolée ne démontre toute la qualité du masque ou son utilité dans un autre processus.

**Erreurs bloquantes** : Comparer directement un nombre sans unité à une longueur.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Fiche complète]] ; [Metrics Reloaded, Semantic segmentation](https://doi.org/10.1038/s41592-023-02151-z) ; [Reinke et al., fig. 4a et 5c : recouvrement/frontières et HD95](https://www.nature.com/articles/s41592-023-02150-0).
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-METRIQUES-APPLIQUEES-001 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-002

Objectif : mesurer les petits défauts. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-002
Question: Pourquoi un score pixel global peut-il masquer de petits défauts manqués en inspection ?
Reponse: **Noyau attendu** : Les pixels de fond ou grands défauts dominent certains agrégats ; une analyse par région/pièce et taille peut révéler les manques.

**Approfondissement** : Préciser AU-PRO et sa plage FPR si utilisée, plus taux de rejets/manques au seuil utile.

**Exemple construit** : manquer un minuscule défaut peut ne modifier que quelques pixels dans une grande image parfaitement segmentée ailleurs. Une moyenne globale reste élevée alors que l'événement critique pour la pièce est perdu. Plusieurs gros défauts faciles peuvent également masquer des performances faibles sur des régions rares.

**Évaluation proposée** : mesurer rappel par défaut, faux rejets par pièce et localisation à l'échelle utile, puis stratifier taille, type et acquisition. Si une métrique par région comme PRO est utilisée, annoncer ses conventions et la plage de faux positifs intégrée, car des aires sous des domaines différents ne sont pas comparables. Conserver les négatifs et les cas manqués dans le bilan. Une bonne mesure doit permettre la décision visée ; elle ne se choisit pas parce qu'elle agrège les pixels d'une façon qui rend le résultat plus flatteur.

**Erreurs bloquantes** : Comparer des AU-PRO avec plages différentes sans le signaler.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Fiche complète]] ; [MVTec AD2 v1, protocole d’évaluation et fig. 4 : PRO et pondération des régions](https://arxiv.org/abs/2503.21622v1).
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-APPLIQUEES-002 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-003

Objectif : séparer calibration et métrologie. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-003
Question: Un faible RMS caméra suffit-il à valider répétabilité et reproductibilité d’une mesure de longueur ?
Reponse: **Noyau attendu** : Non : répéter les mesures et varier les conditions/configurations pertinentes, avec référence dimensionnelle et analyse des sources de variation.

**Approfondissement** : Distinguer biais, répétabilité, reproductibilité et stabilité ; fixer la tolérance métier.

**Différence des sources d'erreur** : le RMS de reprojection décrit un ajustement de points image au modèle. La mesure de longueur dépend aussi de l'échelle, de la pose, de l'acquisition, du montage et de la procédure de mesure. Répéter dans les mêmes conditions teste une variation différente de celle obtenue en changeant opérateur ou configuration.

**Protocole construit** : utiliser une dimension de référence indépendante, répéter les acquisitions puis varier les conditions prévues par l'étude, en conservant les unités et la géométrie. Séparer décalage moyen par rapport à la référence et dispersion des répétitions ; examiner aussi l'évolution dans le temps. La définition des facteurs de variation doit correspondre à l'exploitation réelle. Une faible dispersion autour d'une longueur biaisée n'est pas une bonne exactitude. Ce raisonnement complète la calibration caméra sans prétendre qu'un score pixel fournit directement l'incertitude dimensionnelle de toute la chaîne.

**Erreurs bloquantes** : Transformer directement une erreur pixel d’ajustement en garantie millimétrique.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Fiche complète]] ; [NIST, 2.4.4.1 répétabilité](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc441.htm), [2.4.4.2 reproductibilité](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc442.htm), [2.4.4.3 stabilité](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc443.htm), [2.4.5 biais](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc45.htm).
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-METRIQUES-APPLIQUEES-003 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-004

Objectif : traiter les masques vides. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-004
Question: Que faut-il annoncer lorsqu’une métrique de segmentation rencontre référence ou prédiction vide ?
Reponse: **Noyau attendu** : La convention choisie et son effet sur le score/agrégation ; ne pas laisser une division indéfinie devenir un résultat implicite.

**Approfondissement** : Les faux positifs sur cas négatifs et absences de détection doivent rester visibles.

**Distinguer les situations** : deux masques vides, une référence vide avec faux positif et une prédiction vide sur un objet présent n'ont pas le même sens. Une distance de surface peut être indéfinie lorsqu'une surface manque, tandis qu'un recouvrement peut nécessiter une convention particulière pour un dénominateur nul.

**Choix de protocole proposé** : définir ces cas avant les résultats et les conserver dans un tableau de comptage séparé si la métrique principale ne peut pas les résumer. Annoncer valeurs conventionnelles, exclusions éventuelles et poids dans l'agrégation. Retirer silencieusement les cas négatifs peut cacher des faux positifs ; retirer les prédictions vides peut cacher les objets entièrement manqués. Tester quelques exemples synthétiques connus dans l'outil d'évaluation et conserver sa version. La convention n'est pas une astuce numérique : elle détermine quelles erreurs le score final représente et lesquelles doivent être rapportées autrement.

**Erreurs bloquantes** : Retirer silencieusement tous les cas vides pour améliorer la moyenne.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Fiche complète]] ; [Reinke et al., P2.3–P2.4 et P3.2 : sorties/références vides et agrégation](https://www.nature.com/articles/s41592-023-02150-0).
Tags: cv::pilote cv::d13 famille::pratique cv_id::CV-METRIQUES-APPLIQUEES-004 provenance::agent pole::A pole::E
END
