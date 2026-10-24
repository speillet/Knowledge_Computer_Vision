# NeRF, 3D Gaussian Splatting et reconstruction — cartes

Fiche : [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::120-generatif-multimodal

## CV-RENDU3D-001

Objectif : distinguer représentation implicite et primitives. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-RENDU3D-001
Question: Quelle différence centrale sépare NeRF et 3D Gaussian Splatting ?
Reponse: **Noyau attendu** : NeRF utilise un champ de densité/radiance avec rendu volumique ; 3DGS une représentation explicite de gaussiennes optimisées et un rendu par splatting.

**Approfondissement** : Comparer optimisation, mémoire et rendu sous même scène/matériel ; aucune vitesse universelle ne suit du nom.

**Représentation et opération** : un champ implicite est interrogé le long de rayons pour calculer une image selon son modèle volumique. Des primitives explicites portent positions, étendues et apparence, puis sont projetées par un autre mécanisme de rendu. Ces choix déplacent les coûts d'optimisation, de stockage et de synthèse.

**Comparaison construite** : utiliser les mêmes vues et poses, réserver des angles puis mesurer qualité visuelle, mémoire et temps sur le même matériel. Si la géométrie importe, ajouter une référence de surface ou de dimension indépendante. Une représentation peut expliquer des images avec des structures qui ne conviennent pas à la métrologie ; un rendu rapide ne prouve pas une surface exacte. Dans NeRF original, distinguer aussi densité dépendant de la position et radiance dépendant de la vue. Le nom d'une famille ne décrit pas toutes les variantes ni une performance universelle.

**Erreurs bloquantes** : Assimiler les deux à un maillage métrique garanti.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Fiche complète]] ; [NeRF, §§3–4](https://arxiv.org/abs/2003.08934) ; [3DGS, résumé et §§4–6](https://arxiv.org/abs/2308.04079).
Tags: cv::pilote cv::d12 famille::comparaison cv_id::CV-RENDU3D-001 provenance::agent pole::B pole::D
END

## CV-RENDU3D-002

Objectif : séparer rendu et géométrie. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-RENDU3D-002
Question: Pourquoi une excellente PSNR de nouvelles vues ne suffit-elle pas à valider une reconstruction pour métrologie ?
Reponse: **Noyau attendu** : Elle évalue une ressemblance d’image sous protocole, pas directement l’exactitude d’une surface ou d’une dimension physique.

**Approfondissement** : Utiliser une référence géométrique, unités et angles réservés ; examiner les zones jamais observées.

**Différence des espaces d'erreur** : la PSNR compare des intensités entre une vue rendue et une référence. Une erreur géométrique peut avoir peu d'effet sur des vues voisines ou être compensée par l'apparence représentée. Le score ne possède donc pas une conversion automatique en millimètres de surface.

**Protocole proposé** : fixer poses et échelle, réserver des angles réellement nouveaux, puis comparer la géométrie à des mesures indépendantes adaptées à la région utile. Examiner également les zones occultées ou jamais vues : une représentation peut y produire une hypothèse sans observation directe. Rapporter erreurs et couverture de la référence, et séparer qualité de rendu et qualité de reconstruction. Une vue magnifique peut être suffisante pour la visualisation et insuffisante pour contrôler une dimension ; ce sont deux usages différents dont les critères doivent être définis avant de choisir la méthode et l'évaluation.

**Erreurs bloquantes** : Déduire une précision en millimètres d’un score perceptuel ou pixel.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Fiche complète]] ; Distinction entre métriques image et géométrie déduite par le projet ; [NeRF, §6 : évaluation de synthèse de vues](https://arxiv.org/abs/2003.08934).
Tags: cv::pilote cv::d12 famille::evaluation cv_id::CV-RENDU3D-002 provenance::agent pole::B pole::D
END

## CV-RENDU3D-003

Objectif : vérifier une scène peu observée. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-RENDU3D-003
Question: Des vues d’entraînement sont plausibles mais une rotation de caméra révèle des artefacts. Que tester ?
Reponse: **Noyau attendu** : Couverture angulaire, poses et hypothèse de scène statique, puis régions insuffisamment contraintes.

**Approfondissement** : Comparer à des vues réservées ; augmenter les itérations sans nouvelles contraintes peut seulement surajuster.

**Origines possibles** : les vues d'apprentissage peuvent peu contraindre certaines faces, contenir des poses biaisées ou mélanger une scène qui change dans le temps. Une représentation flexible peut expliquer ces images sans reconstruire une scène cohérente depuis toutes les directions.

**Enquête construite** : cartographier couverture des rayons et erreurs selon angle, inspecter calibration et poses, puis comparer des vues réservées à distance angulaire annoncée. Faire varier séparément nombre de vues et qualité des poses, en gardant l'autre facteur contrôlé. Une amélioration sur les vues déjà utilisées peut n'être qu'un meilleur ajustement à ces données. Si une région n'a jamais été observée, davantage d'itérations n'apporte pas son apparence vraie. Le diagnostic doit donc distinguer manque d'information, modèle de scène faux et problème d'optimisation, plutôt que considérer toute synthèse plausible à l'entraînement comme une validation complète.

**Erreurs bloquantes** : Considérer les vues d’entraînement comme une validation complète.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Fiche complète]] ; Diagnostic de couverture/poses proposé par le projet ; [NeRF, §§3–4 : représentation et observations](https://arxiv.org/abs/2003.08934).
Tags: cv::pilote cv::d12 famille::diagnostic cv_id::CV-RENDU3D-003 provenance::agent pole::B pole::D
END
