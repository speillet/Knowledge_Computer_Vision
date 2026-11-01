# Review –  Factor Graphs and Incremental Optimization –  2026-10-23

## Overview

Three flashcards audited, plus their reference note. No false claims. There is one important observation (CV-FACTEURS-001, closed question) and two flashcards fair but thin. Correction applied: reference note in revision 3, IDs and objectives unchanged. The four enrichments proposed were accepted and drafted in revision 4: the subject goes from 3 to 5 flashcards, and 002 and 003 are enriched.

Self-review: Agent Claude Code (`revue-cartes`). Editorial status `redige`.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FACTEURS-001 | Confirmed (GTSAM §§2.3 – 2.4, 4.1, 7; Kaess §2); GTSAM does not formulae MAP equivalency gaussian – less squares | Weak in yes/no form | Question closed: "No" is guessing | Agreement reference note | Important | Open question, representation and elements to be provided |
| CV-FACTEURS-002 | Confirmed (Ceres, Gauge Invariance) | Forte | Net Core | Cut CV-BA-003 without contradicting it | None | Proposed Enrichment |
| CV-FACTEURS-003 | Project diagnosis, plausible | Forte | Net core but without discriminating test | Agreement reference note | Minor | Proposed Enrichment |

## Corrections applied

- `vault/10-mathematiques-estimation/references/14-graphes-facteurs.md`, revision 3:
  - bipartite definition and role of `Values`;
  - the first pose;
  - elimination by QR sparse, fill-in and incremental order;
  - sources specified by section.
- `vault/10-mathematiques-estimation/14-graphes-facteurs.md`: CV-FACTEURS-001 rewritten without changing the objective.
- Journal: A line.

## Enrichments accepted and applied

All accepted on 2026-10-23:

- **CV-FACTEURS-002**, gauge ;
- **CV-FACTEURS-003**, $\chi^2$ test and re-optimization without the loop;
- **CV-FACTEURS-004**, robust back-ends;
- **CV-FACTEURS-005**, iSAM2.

The reference note receives the size of the gauge and its treatments, the mechanism of iSAM2 and a rubric on the false loops. The total goes from 242 to 244 flashcards.

Table of proposals as submitted:

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| CV-FACTEURS-002: gauge size according to the sensors (pose graph 6, monocular BA 7, visual-inertial 4: position and yaw) and the three treatments (fix, prior, leave free) | The flashcard does not say how many degrees are free or how to treat them | further explanation alone | No new reminders | Zhang, Gallego and Scaramuzza 2018, RA-L, summary, §I and table I; Ceres, Gauge Invariance |
| CV-FACTEURS-003: factor test, residual squared compared to a quantile of $\chi^2$ | The current diagnosis does not have an encrypted test | further explanation alone | No new reminders | Agarwal et al. 2013, §III; Gamse et al. 2014 (CV-FUSION-002) |
| CV-FACTEURS-004: robust loop closures: robust loss, switchable stresses, DCS | Perceptual aliasing makes a front-end without false positives impossible; no flashcard on robust back-end | comparison | 1 flashcard; core at 3 points | Agarwal et al. 2013, summary and §III: $s=\min(1, 2\Phi/(\Phi+\chi^2))$; Sünderhauf and Protzel 2012, to read |
| CV-FACTEURS-005: what iSAM2 recalculates at each measurement: affected part of the Bayes tree, fluid relinearization, partial updates | The word “incremental” is quoted without mechanism | algorithm | 1 flashcard; core at 3 points | Kaess et al. 2012, §§3 – 4 |

## Sources

- [Dellaert, Factor Graphs and GTSAM](https://gtsam.org/tutorials/intro.html), accessed on 2026-10-23:
  - §1, graphe biparti ;
  - §2.3, graph and `Values`;
  - §2.4, initial estimate of MAP;
  - §4.1, prior of first pose, only link to the global coordinate frame;
  - §7, iSAM and Bayes tree;
  - Fill-in and COLAMD  are not mentioned.
- [Kaess et al. 2012, iSAM2, IJRR](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf), full text:
  - §2, Gaussian case, least squares and sparse QR;
  - §3.4, incremental order and COLAMD;
  - §§4.1 – 4.2, smooth relinearization and partial updates.
- For proposals:
  - [Zhang, Gallego and Scaramuzza 2018](https://rpg.ifi.uzh.ch/docs/RAL18_Zhang.pdf), prepublication of the authors: 4 degrees of freedom not observable in visual-inertial, 7 in monocular BA, three approaches of similar precision and related covariances;
  - [Agarwal et al. 2013, DCS](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf), full text: summary and §III.
- Unread: Sünderhauf and Protzel 2012. The QUT repository provided only the record; only its rework by Agarwal et al. was read.

## Checks and limitations

`check_vault.py` OK (242 flashcards) after correction, then 244 after additions; 34 tests passed; catalog regenerated then updated; inventory without ID disappeared or identity Anki modified. Context7 is not available in this session. Not verified: export Anki, rendering Obsidian and AnkiDroid, mastering, independent validation.
