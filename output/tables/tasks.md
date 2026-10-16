| scenario | algorithm | etm | task_id | task | wcet_ms | period_ms | deadline_ms | utilization | priority | priority_rule | released | completed | pending | deadlines_evaluated | deadlines_met | deadlines_missed | success_rate | preemptions | migrations | response_mean_ms | response_worst_ms | laxity_mean | executed_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | RM | wcet | 1 | Fumaca | 2 | 10 | 10 | 0.2 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2 | 2 | 0.8 | 120 |
| A | RM | wcet | 2 | Gas | 3 | 20 | 20 | 0.15 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 5 | 5 | 0.75 | 90 |
| A | RM | wcet | 3 | Sirene | 4 | 40 | 40 | 0.1 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 9 | 9 | 0.775 | 60 |
| A | RM | wcet | 4 | Comunic | 5 | 50 | 50 | 0.1 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 3 | 0 | 10 | 16 | 0.8 | 60 |
| A | RM | acet | 1 | Fumaca | 2 | 10 | 10 | 0.2 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 1.49446 | 1.96235 | 0.850554 | 89.6677 |
| A | RM | acet | 2 | Gas | 3 | 20 | 20 | 0.15 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 3.70383 | 4.40557 | 0.814808 | 66.0861 |
| A | RM | acet | 3 | Sirene | 4 | 40 | 40 | 0.1 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 6.58409 | 7.27576 | 0.835398 | 43.8564 |
| A | RM | acet | 4 | Comunic | 5 | 50 | 50 | 0.1 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 2 | 0 | 7.35234 | 12.1377 | 0.852953 | 45.6437 |
| A | DM | wcet | 1 | Fumaca | 2 | 10 | 10 | 0.2 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2 | 2 | 0.8 | 120 |
| A | DM | wcet | 2 | Gas | 3 | 20 | 20 | 0.15 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 5 | 5 | 0.75 | 90 |
| A | DM | wcet | 3 | Sirene | 4 | 40 | 40 | 0.1 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 9 | 9 | 0.775 | 60 |
| A | DM | wcet | 4 | Comunic | 5 | 50 | 50 | 0.1 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 3 | 0 | 10 | 16 | 0.8 | 60 |
| A | DM | acet | 1 | Fumaca | 2 | 10 | 10 | 0.2 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 1.49446 | 1.96235 | 0.850554 | 89.6677 |
| A | DM | acet | 2 | Gas | 3 | 20 | 20 | 0.15 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 3.70383 | 4.40557 | 0.814808 | 66.0861 |
| A | DM | acet | 3 | Sirene | 4 | 40 | 40 | 0.1 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 6.58409 | 7.27576 | 0.835398 | 43.8564 |
| A | DM | acet | 4 | Comunic | 5 | 50 | 50 | 0.1 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 2 | 0 | 7.35234 | 12.1377 | 0.852953 | 45.6437 |
| A | EDF | wcet | 1 | Fumaca | 2 | 10 | 10 | 0.2 | — | deadline absoluto do job | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2 | 2 | 0.8 | 120 |
| A | EDF | wcet | 2 | Gas | 3 | 20 | 20 | 0.15 | — | deadline absoluto do job | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 5 | 5 | 0.75 | 90 |
| A | EDF | wcet | 3 | Sirene | 4 | 40 | 40 | 0.1 | — | deadline absoluto do job | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 9 | 9 | 0.775 | 60 |
| A | EDF | wcet | 4 | Comunic | 5 | 50 | 50 | 0.1 | — | deadline absoluto do job | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 3 | 0 | 10 | 16 | 0.8 | 60 |
| A | EDF | acet | 1 | Fumaca | 2 | 10 | 10 | 0.2 | — | deadline absoluto do job | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 1.49446 | 1.96235 | 0.850554 | 89.6677 |
| A | EDF | acet | 2 | Gas | 3 | 20 | 20 | 0.15 | — | deadline absoluto do job | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 3.70383 | 4.40557 | 0.814808 | 66.0861 |
| A | EDF | acet | 3 | Sirene | 4 | 40 | 40 | 0.1 | — | deadline absoluto do job | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 6.58409 | 7.27576 | 0.835398 | 43.8564 |
| A | EDF | acet | 4 | Comunic | 5 | 50 | 50 | 0.1 | — | deadline absoluto do job | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 2 | 0 | 7.35234 | 12.1377 | 0.852953 | 45.6437 |
| B | RM | wcet | 1 | Fumaca | 3 | 10 | 10 | 0.3 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 3 | 3 | 0.7 | 180 |
| B | RM | wcet | 2 | Gas | 5 | 20 | 20 | 0.25 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 8 | 8 | 0.6 | 150 |
| B | RM | wcet | 3 | Sirene | 8 | 40 | 40 | 0.2 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 15 | 0 | 19 | 19 | 0.525 | 120 |
| B | RM | wcet | 4 | Comunic | 10 | 50 | 50 | 0.2 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 24 | 0 | 37.5 | 40 | 0.25 | 120 |
| B | RM | acet | 1 | Fumaca | 3 | 10 | 10 | 0.3 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2.24169 | 2.94353 | 0.775831 | 134.502 |
| B | RM | acet | 2 | Gas | 5 | 20 | 20 | 0.25 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 5.9229 | 7.04247 | 0.703855 | 110.144 |
| B | RM | acet | 3 | Sirene | 8 | 40 | 40 | 0.2 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 15 | 0 | 13.9636 | 15.7264 | 0.65091 | 87.7129 |
| B | RM | acet | 4 | Comunic | 10 | 50 | 50 | 0.2 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 10 | 0 | 18.5484 | 28.0804 | 0.629031 | 91.2875 |
| B | DM | wcet | 1 | Fumaca | 3 | 10 | 10 | 0.3 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 3 | 3 | 0.7 | 180 |
| B | DM | wcet | 2 | Gas | 5 | 20 | 20 | 0.25 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 8 | 8 | 0.6 | 150 |
| B | DM | wcet | 3 | Sirene | 8 | 40 | 40 | 0.2 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 15 | 0 | 19 | 19 | 0.525 | 120 |
| B | DM | wcet | 4 | Comunic | 10 | 50 | 50 | 0.2 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 24 | 0 | 37.5 | 40 | 0.25 | 120 |
| B | DM | acet | 1 | Fumaca | 3 | 10 | 10 | 0.3 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2.24169 | 2.94353 | 0.775831 | 134.502 |
| B | DM | acet | 2 | Gas | 5 | 20 | 20 | 0.25 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 5.9229 | 7.04247 | 0.703855 | 110.144 |
| B | DM | acet | 3 | Sirene | 8 | 40 | 40 | 0.2 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 15 | 0 | 13.9636 | 15.7264 | 0.65091 | 87.7129 |
| B | DM | acet | 4 | Comunic | 10 | 50 | 50 | 0.2 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 10 | 0 | 18.5484 | 28.0804 | 0.629031 | 91.2875 |
| B | EDF | wcet | 1 | Fumaca | 3 | 10 | 10 | 0.3 | — | deadline absoluto do job | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 3 | 3 | 0.7 | 180 |
| B | EDF | wcet | 2 | Gas | 5 | 20 | 20 | 0.25 | — | deadline absoluto do job | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 8 | 8 | 0.6 | 150 |
| B | EDF | wcet | 3 | Sirene | 8 | 40 | 40 | 0.2 | — | deadline absoluto do job | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 15 | 0 | 19.2 | 20 | 0.52 | 120 |
| B | EDF | wcet | 4 | Comunic | 10 | 50 | 50 | 0.2 | — | deadline absoluto do job | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 24 | 0 | 34.75 | 40 | 0.305 | 120 |
| B | EDF | acet | 1 | Fumaca | 3 | 10 | 10 | 0.3 | — | deadline absoluto do job | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2.24169 | 2.94353 | 0.775831 | 134.502 |
| B | EDF | acet | 2 | Gas | 5 | 20 | 20 | 0.25 | — | deadline absoluto do job | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 5.9229 | 7.04247 | 0.703855 | 110.144 |
| B | EDF | acet | 3 | Sirene | 8 | 40 | 40 | 0.2 | — | deadline absoluto do job | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 15 | 0 | 13.9636 | 15.7264 | 0.65091 | 87.7129 |
| B | EDF | acet | 4 | Comunic | 10 | 50 | 50 | 0.2 | — | deadline absoluto do job | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 10 | 0 | 18.5484 | 28.0804 | 0.629031 | 91.2875 |
| C | RM | wcet | 1 | Fumaca | 4 | 10 | 10 | 0.4 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 4 | 4 | 0.6 | 240 |
| C | RM | wcet | 2 | Gas | 5 | 20 | 20 | 0.25 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 9 | 9 | 0.55 | 150 |
| C | RM | wcet | 3 | Sirene | 8 | 40 | 40 | 0.2 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 30 | 0 | 30 | 30 | 0.25 | 120 |
| C | RM | wcet | 4 | Comunic | 10 | 50 | 50 | 0.2 | 4 | prioridade fixa (1 = maior) | 12 | 9 | 3 | 12 | 0 | 12 | 0 | 12 | 0 | 144.667 | 206 | -1.89333 | 90 |
| C | RM | acet | 1 | Fumaca | 4 | 10 | 10 | 0.4 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2.98892 | 3.92471 | 0.701108 | 179.335 |
| C | RM | acet | 2 | Gas | 5 | 20 | 20 | 0.25 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 6.67338 | 7.9429 | 0.666331 | 110.144 |
| C | RM | acet | 3 | Sirene | 8 | 40 | 40 | 0.2 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 15 | 0 | 15.4384 | 17.608 | 0.61404 | 87.7129 |
| C | RM | acet | 4 | Comunic | 10 | 50 | 50 | 0.2 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 14 | 0 | 22.8522 | 33.8358 | 0.542956 | 91.2874 |
| C | DM | wcet | 1 | Fumaca | 4 | 10 | 10 | 0.4 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 4 | 4 | 0.6 | 240 |
| C | DM | wcet | 2 | Gas | 5 | 20 | 20 | 0.25 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 9 | 9 | 0.55 | 150 |
| C | DM | wcet | 3 | Sirene | 8 | 40 | 40 | 0.2 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 30 | 0 | 30 | 30 | 0.25 | 120 |
| C | DM | wcet | 4 | Comunic | 10 | 50 | 50 | 0.2 | 4 | prioridade fixa (1 = maior) | 12 | 9 | 3 | 12 | 0 | 12 | 0 | 12 | 0 | 144.667 | 206 | -1.89333 | 90 |
| C | DM | acet | 1 | Fumaca | 4 | 10 | 10 | 0.4 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2.98892 | 3.92471 | 0.701108 | 179.335 |
| C | DM | acet | 2 | Gas | 5 | 20 | 20 | 0.25 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 6.67338 | 7.9429 | 0.666331 | 110.144 |
| C | DM | acet | 3 | Sirene | 8 | 40 | 40 | 0.2 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 15 | 0 | 15.4384 | 17.608 | 0.61404 | 87.7129 |
| C | DM | acet | 4 | Comunic | 10 | 50 | 50 | 0.2 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 14 | 0 | 22.8522 | 33.8358 | 0.542956 | 91.2874 |
| C | EDF | wcet | 1 | Fumaca | 4 | 10 | 10 | 0.4 | — | deadline absoluto do job | 60 | 58 | 2 | 60 | 29 | 31 | 0.483333 | 0 | 0 | 12.2069 | 30 | -0.22069 | 233 |
| C | EDF | wcet | 2 | Gas | 5 | 20 | 20 | 0.25 | — | deadline absoluto do job | 30 | 29 | 1 | 30 | 12 | 18 | 0.4 | 0 | 0 | 22.2759 | 39 | -0.113793 | 145 |
| C | EDF | wcet | 3 | Sirene | 8 | 40 | 40 | 0.2 | — | deadline absoluto do job | 15 | 14 | 1 | 15 | 3 | 12 | 0.2 | 4 | 0 | 48.4286 | 66 | -0.210714 | 112 |
| C | EDF | wcet | 4 | Comunic | 10 | 50 | 50 | 0.2 | — | deadline absoluto do job | 12 | 11 | 1 | 12 | 3 | 9 | 0.25 | 1 | 0 | 59.2727 | 71 | -0.185455 | 110 |
| C | EDF | acet | 1 | Fumaca | 4 | 10 | 10 | 0.4 | — | deadline absoluto do job | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2.98892 | 3.92471 | 0.701108 | 179.335 |
| C | EDF | acet | 2 | Gas | 5 | 20 | 20 | 0.25 | — | deadline absoluto do job | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 6.67338 | 7.9429 | 0.666331 | 110.144 |
| C | EDF | acet | 3 | Sirene | 8 | 40 | 40 | 0.2 | — | deadline absoluto do job | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 15 | 0 | 15.4384 | 17.608 | 0.61404 | 87.7129 |
| C | EDF | acet | 4 | Comunic | 10 | 50 | 50 | 0.2 | — | deadline absoluto do job | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 14 | 0 | 22.8522 | 33.8358 | 0.542956 | 91.2874 |
| D | RM | wcet | 1 | Fumaca | 2 | 10 | 9 | 0.2 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2 | 2 | 0.7 | 120 |
| D | RM | wcet | 2 | Gas | 3 | 20 | 18 | 0.15 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 5 | 5 | 0.65 | 90 |
| D | RM | wcet | 3 | Sirene | 4 | 40 | 8 | 0.1 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 0 | 15 | 0 | 0 | 0 | 9 | 9 | -0.025 | 60 |
| D | RM | wcet | 4 | Comunic | 5 | 50 | 45 | 0.1 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 3 | 0 | 10 | 16 | 0.7 | 60 |
| D | RM | acet | 1 | Fumaca | 2 | 10 | 9 | 0.2 | 1 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 1.49446 | 1.96235 | 0.750554 | 89.6677 |
| D | RM | acet | 2 | Gas | 3 | 20 | 18 | 0.15 | 2 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 3.70383 | 4.40557 | 0.714808 | 66.0861 |
| D | RM | acet | 3 | Sirene | 4 | 40 | 8 | 0.1 | 3 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 6.58409 | 7.27576 | 0.0353977 | 43.8564 |
| D | RM | acet | 4 | Comunic | 5 | 50 | 45 | 0.1 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 2 | 0 | 7.35234 | 12.1377 | 0.752953 | 45.6437 |
| D | DM | wcet | 1 | Fumaca | 2 | 10 | 9 | 0.2 | 2 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 3 | 6 | 0.6 | 120 |
| D | DM | wcet | 2 | Gas | 3 | 20 | 18 | 0.15 | 3 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 7 | 9 | 0.55 | 90 |
| D | DM | wcet | 3 | Sirene | 4 | 40 | 8 | 0.1 | 1 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 4 | 4 | 0.1 | 60 |
| D | DM | wcet | 4 | Comunic | 5 | 50 | 45 | 0.1 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 3 | 0 | 10 | 16 | 0.7 | 60 |
| D | DM | acet | 1 | Fumaca | 2 | 10 | 9 | 0.2 | 2 | prioridade fixa (1 = maior) | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2.2254 | 5.05098 | 0.67746 | 89.6677 |
| D | DM | acet | 2 | Gas | 3 | 20 | 18 | 0.15 | 3 | prioridade fixa (1 = maior) | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 5.16572 | 7.27576 | 0.641714 | 66.0861 |
| D | DM | acet | 3 | Sirene | 4 | 40 | 8 | 0.1 | 1 | prioridade fixa (1 = maior) | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 2.92376 | 3.56807 | 0.126906 | 43.8564 |
| D | DM | acet | 4 | Comunic | 5 | 50 | 45 | 0.1 | 4 | prioridade fixa (1 = maior) | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 2 | 0 | 7.35234 | 12.1377 | 0.752953 | 45.6437 |
| D | EDF | wcet | 1 | Fumaca | 2 | 10 | 9 | 0.2 | — | deadline absoluto do job | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 3 | 6 | 0.6 | 120 |
| D | EDF | wcet | 2 | Gas | 3 | 20 | 18 | 0.15 | — | deadline absoluto do job | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 7 | 9 | 0.55 | 90 |
| D | EDF | wcet | 3 | Sirene | 4 | 40 | 8 | 0.1 | — | deadline absoluto do job | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 4 | 4 | 0.1 | 60 |
| D | EDF | wcet | 4 | Comunic | 5 | 50 | 45 | 0.1 | — | deadline absoluto do job | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 3 | 0 | 10 | 16 | 0.7 | 60 |
| D | EDF | acet | 1 | Fumaca | 2 | 10 | 9 | 0.2 | — | deadline absoluto do job | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2.2254 | 5.05098 | 0.67746 | 89.6677 |
| D | EDF | acet | 2 | Gas | 3 | 20 | 18 | 0.15 | — | deadline absoluto do job | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 5.16572 | 7.27576 | 0.641714 | 66.0861 |
| D | EDF | acet | 3 | Sirene | 4 | 40 | 8 | 0.1 | — | deadline absoluto do job | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 2.92376 | 3.56807 | 0.126906 | 43.8564 |
| D | EDF | acet | 4 | Comunic | 5 | 50 | 45 | 0.1 | — | deadline absoluto do job | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 2 | 0 | 7.35234 | 12.1377 | 0.752953 | 45.6437 |
| E | G-EDF | wcet | 1 | Fumaca | 4 | 10 | 10 | 0.4 | — | deadline absoluto do job | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 4 | 4 | 0.6 | 240 |
| E | G-EDF | wcet | 2 | Gas | 5 | 20 | 20 | 0.25 | — | deadline absoluto do job | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 5 | 5 | 0.75 | 150 |
| E | G-EDF | wcet | 3 | Sirene | 8 | 40 | 40 | 0.2 | — | deadline absoluto do job | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 12 | 12 | 0.7 | 120 |
| E | G-EDF | wcet | 4 | Comunic | 10 | 50 | 50 | 0.2 | — | deadline absoluto do job | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 6 | 6 | 14.25 | 17 | 0.715 | 120 |
| E | G-EDF | acet | 1 | Fumaca | 4 | 10 | 10 | 0.4 | — | deadline absoluto do job | 60 | 60 | 0 | 60 | 60 | 0 | 1 | 0 | 0 | 2.98892 | 3.92471 | 0.701108 | 179.335 |
| E | G-EDF | acet | 2 | Gas | 5 | 20 | 20 | 0.25 | — | deadline absoluto do job | 30 | 30 | 0 | 30 | 30 | 0 | 1 | 0 | 0 | 3.67145 | 4.34116 | 0.816427 | 110.144 |
| E | G-EDF | acet | 3 | Sirene | 8 | 40 | 40 | 0.2 | — | deadline absoluto do job | 15 | 15 | 0 | 15 | 15 | 0 | 1 | 0 | 0 | 8.72805 | 10.102 | 0.781799 | 87.7129 |
| E | G-EDF | acet | 4 | Comunic | 10 | 50 | 50 | 0.2 | — | deadline absoluto do job | 12 | 12 | 0 | 12 | 12 | 0 | 1 | 1 | 1 | 9.3587 | 11.7334 | 0.812826 | 91.2874 |
