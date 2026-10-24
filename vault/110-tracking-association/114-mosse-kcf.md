# MOSSE et KCF — tracking par filtres de corrélation — cartes

Fiche : [[110-tracking-association/references/114-mosse-kcf|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-CORRELATION-001

Objectif : expliquer la boucle d’un filtre de tracking. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-CORRELATION-001
Question: Comment un filtre de corrélation initialisé par une boîte suit-il la cible à la frame suivante ?
Reponse: **Noyau attendu** : Extraire une région de recherche et ses features, corréler avec le modèle, localiser le pic, contrôler la fiabilité puis adapter le modèle seulement selon la politique retenue. La réponse vise un pic de localisation, pas une classe sémantique.

**Approfondissement** : L’initialisation fournit la cible et des réponses synthétiques autour d’elle. La recherche est locale ; une cible sortie de cette région ne réapparaît pas par la seule adaptation du filtre. Ne pas confondre tracking mono-objet et détection de tous les objets.

**Erreurs bloquantes** : Mettre à jour sans contrôle sur toute boîte prédite ; promettre une détection globale.
Source: [[110-tracking-association/references/114-mosse-kcf|Fiche complète]] ; [Bolme et al. 2010, §§3.2–3.5, MOSSE, mise à jour et PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf).
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-CORRELATION-001 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-002

Objectif : distinguer MOSSE et KCF. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-CORRELATION-002
Question: Que gagne KCF avec les décalages cycliques et les noyaux, par rapport à un filtre linéaire comme MOSSE ?
Reponse: **Noyau attendu** : KCF structure les exemples comme des décalages cycliques du patch ; la matrice circulante permet des calculs efficaces en Fourier, y compris pour des noyaux compatibles. MOSSE apprend un filtre de corrélation linéaire adapté en ligne.

**Approfondissement** : Le gain de calcul dépend de cette structure et des features. Les décalages cycliques créent des exemples artificiels aux bords : la rapidité ne supprime pas les biais. Aucun FPS de papier ne prédit celui du matériel cible.

**Erreurs bloquantes** : Présenter KCF comme un détecteur profond ; dire qu’un noyau supprime les limites de recherche locale.
Source: [[110-tracking-association/references/114-mosse-kcf|Fiche complète]] ; [Henriques et al., KCF, §§4–5, structure circulante et noyaux](https://arxiv.org/pdf/1404.7584).
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-CORRELATION-002 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-003

Objectif : interpréter un PSR. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-CORRELATION-003
Question: Une réponse a un pic à 0,8, une moyenne hors pic à 0,2 et un écart-type hors pic à 0,1. Que vaut le PSR et que signifie-t-il ?
Reponse: **Noyau attendu** : PSR=$(0,8-0,2)/0,1=6$. Le pic dépasse la moyenne du fond de six écarts-types selon la région hors pic choisie. Il mesure un contraste de réponse, sans probabilité calibrée de bonne cible.

**Approfondissement** : Définir la zone exclue et le traitement d’un écart-type nul. Le seuil dépend du tracker, du patch et du protocole. Des distracteurs peuvent produire un pic net pour le mauvais objet.

**Erreurs bloquantes** : Interpréter PSR=6 comme 60 % de confiance ; appliquer un seuil historique à toute méthode.
Source: [[110-tracking-association/references/114-mosse-kcf|Fiche complète]] ; [Bolme et al. 2010, §§3.2–3.5, MOSSE, mise à jour et PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf).
Tags: cv::pilote cv::d11 famille::raisonnement cv_id::CV-CORRELATION-003 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-004

Objectif : rechercher une contamination du modèle. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-CORRELATION-004
Question: Un tracker à filtre de corrélation reste correct avant une occultation, puis suit durablement le fond. Quelle erreur de mise à jour tester ?
Reponse: **Noyau attendu** : Il peut avoir appris le fond pendant les frames où la cible était cachée. Comparer le modèle avant/après occultation, geler les mises à jour en faible confiance et contrôler les pics concurrents et la région de recherche.

**Approfondissement** : Une adaptation rapide suit les changements d’apparence mais apprend aussi les erreurs de localisation. Un détecteur ou une réinitialisation explicite peut être requis ; geler seul ne garantit pas la récupération.

**Erreurs bloquantes** : Augmenter systématiquement le taux d’apprentissage pour corriger la dérive.
Source: [[110-tracking-association/references/114-mosse-kcf|Fiche complète]] ; [Bolme et al. 2010, §§3.2–3.5, MOSSE, mise à jour et PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf).
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-CORRELATION-004 provenance::agent pole::C pole::D pole::E pole::F
END

## CV-CORRELATION-005

Objectif : définir une comparaison honnête de trackers. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-CORRELATION-005
Question: Deux trackers donnent des scores proches, mais l’un est réinitialisé après chaque perte. Que faut-il préciser pour comparer ?
Reponse: **Noyau attendu** : Le protocole d’initialisation et de réinitialisation, les séquences, les pertes, l’overlap et l’erreur de centre, ainsi que la latence complète. Un redémarrage après erreur change la tâche évaluée.

**Approfondissement** : Conserver les mêmes frames et conditions d’occultation. Distinguer un protocole one-pass sans redémarrage d’un protocole avec resets. Une moyenne sur les seules frames réussies masque les échecs les plus coûteux.

**Erreurs bloquantes** : Comparer des scores obtenus avec des règles de reset différentes sans le signaler.
Source: [[110-tracking-association/references/114-mosse-kcf|Fiche complète]] ; [Bolme et al. 2010, §§3.2–3.5, MOSSE, mise à jour et PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf).
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-CORRELATION-005 provenance::agent pole::C pole::D pole::E pole::F
END
