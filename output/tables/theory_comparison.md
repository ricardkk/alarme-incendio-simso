| scenario | algorithm | etm | task | priority | deadline_ms | rta_response_ms | rta_recurrence_ms | rta_failure_witness_ms | rta_trace | simulated_worst_ms | simulated_first_ms | difference_ms | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | RM | wcet | Fumaca | 1 | 10 | 2 | 2 | — | 2 -> 2 | 2 | 2 | 0 | match |
| A | RM | wcet | Gas | 2 | 20 | 5 | 5 | — | 3 -> 5 -> 5 | 5 | 5 | 0 | match |
| A | RM | wcet | Sirene | 3 | 40 | 9 | 9 | — | 4 -> 9 -> 9 | 9 | 9 | 0 | match |
| A | RM | wcet | Comunic | 4 | 50 | 16 | 16 | — | 5 -> 14 -> 16 -> 16 | 16 | 16 | 0 | match |
| A | RM | acet | Fumaca | 1 | 10 | 2 | 2 | — | 2 -> 2 | 1.96235 | 1.54906 | -0.037646 | within_wcet_bound |
| A | RM | acet | Gas | 2 | 20 | 5 | 5 | — | 3 -> 5 -> 5 | 4.40557 | 3.65001 | -0.594433 | within_wcet_bound |
| A | RM | acet | Sirene | 3 | 40 | 9 | 9 | — | 4 -> 9 -> 9 | 7.27576 | 7.15193 | -1.72424 | within_wcet_bound |
| A | RM | acet | Comunic | 4 | 50 | 16 | 16 | — | 5 -> 14 -> 16 -> 16 | 12.1377 | 12.1377 | -3.86227 | within_wcet_bound |
| A | DM | wcet | Fumaca | 1 | 10 | 2 | 2 | — | 2 -> 2 | 2 | 2 | 0 | match |
| A | DM | wcet | Gas | 2 | 20 | 5 | 5 | — | 3 -> 5 -> 5 | 5 | 5 | 0 | match |
| A | DM | wcet | Sirene | 3 | 40 | 9 | 9 | — | 4 -> 9 -> 9 | 9 | 9 | 0 | match |
| A | DM | wcet | Comunic | 4 | 50 | 16 | 16 | — | 5 -> 14 -> 16 -> 16 | 16 | 16 | 0 | match |
| A | DM | acet | Fumaca | 1 | 10 | 2 | 2 | — | 2 -> 2 | 1.96235 | 1.54906 | -0.037646 | within_wcet_bound |
| A | DM | acet | Gas | 2 | 20 | 5 | 5 | — | 3 -> 5 -> 5 | 4.40557 | 3.65001 | -0.594433 | within_wcet_bound |
| A | DM | acet | Sirene | 3 | 40 | 9 | 9 | — | 4 -> 9 -> 9 | 7.27576 | 7.15193 | -1.72424 | within_wcet_bound |
| A | DM | acet | Comunic | 4 | 50 | 16 | 16 | — | 5 -> 14 -> 16 -> 16 | 12.1377 | 12.1377 | -3.86227 | within_wcet_bound |
| A | EDF | wcet | Fumaca | — | 10 | — | — | — | — | 2 | 2 | — | not_applicable_dynamic_priority |
| A | EDF | wcet | Gas | — | 20 | — | — | — | — | 5 | 5 | — | not_applicable_dynamic_priority |
| A | EDF | wcet | Sirene | — | 40 | — | — | — | — | 9 | 9 | — | not_applicable_dynamic_priority |
| A | EDF | wcet | Comunic | — | 50 | — | — | — | — | 16 | 16 | — | not_applicable_dynamic_priority |
| A | EDF | acet | Fumaca | — | 10 | — | — | — | — | 1.96235 | 1.54906 | — | not_applicable_dynamic_priority |
| A | EDF | acet | Gas | — | 20 | — | — | — | — | 4.40557 | 3.65001 | — | not_applicable_dynamic_priority |
| A | EDF | acet | Sirene | — | 40 | — | — | — | — | 7.27576 | 7.15193 | — | not_applicable_dynamic_priority |
| A | EDF | acet | Comunic | — | 50 | — | — | — | — | 12.1377 | 12.1377 | — | not_applicable_dynamic_priority |
| B | RM | wcet | Fumaca | 1 | 10 | 3 | 3 | — | 3 -> 3 | 3 | 3 | 0 | match |
| B | RM | wcet | Gas | 2 | 20 | 8 | 8 | — | 5 -> 8 -> 8 | 8 | 8 | 0 | match |
| B | RM | wcet | Sirene | 3 | 40 | 19 | 19 | — | 8 -> 16 -> 19 -> 19 | 19 | 19 | 0 | match |
| B | RM | wcet | Comunic | 4 | 50 | 40 | 40 | — | 10 -> 26 -> 37 -> 40 -> 40 | 40 | 40 | 0 | match |
| B | RM | acet | Fumaca | 1 | 10 | 3 | 3 | — | 3 -> 3 | 2.94353 | 2.3236 | -0.056468 | within_wcet_bound |
| B | RM | acet | Gas | 2 | 20 | 8 | 8 | — | 5 -> 8 -> 8 | 7.04247 | 5.82517 | -0.957531 | within_wcet_bound |
| B | RM | acet | Sirene | 3 | 40 | 19 | 19 | — | 8 -> 16 -> 19 -> 19 | 15.7264 | 14.7863 | -3.27361 | within_wcet_bound |
| B | RM | acet | Comunic | 4 | 50 | 40 | 40 | — | 10 -> 26 -> 37 -> 40 -> 40 | 28.0804 | 28.0804 | -11.9196 | within_wcet_bound |
| B | DM | wcet | Fumaca | 1 | 10 | 3 | 3 | — | 3 -> 3 | 3 | 3 | 0 | match |
| B | DM | wcet | Gas | 2 | 20 | 8 | 8 | — | 5 -> 8 -> 8 | 8 | 8 | 0 | match |
| B | DM | wcet | Sirene | 3 | 40 | 19 | 19 | — | 8 -> 16 -> 19 -> 19 | 19 | 19 | 0 | match |
| B | DM | wcet | Comunic | 4 | 50 | 40 | 40 | — | 10 -> 26 -> 37 -> 40 -> 40 | 40 | 40 | 0 | match |
| B | DM | acet | Fumaca | 1 | 10 | 3 | 3 | — | 3 -> 3 | 2.94353 | 2.3236 | -0.056468 | within_wcet_bound |
| B | DM | acet | Gas | 2 | 20 | 8 | 8 | — | 5 -> 8 -> 8 | 7.04247 | 5.82517 | -0.957531 | within_wcet_bound |
| B | DM | acet | Sirene | 3 | 40 | 19 | 19 | — | 8 -> 16 -> 19 -> 19 | 15.7264 | 14.7863 | -3.27361 | within_wcet_bound |
| B | DM | acet | Comunic | 4 | 50 | 40 | 40 | — | 10 -> 26 -> 37 -> 40 -> 40 | 28.0804 | 28.0804 | -11.9196 | within_wcet_bound |
| B | EDF | wcet | Fumaca | — | 10 | — | — | — | — | 3 | 3 | — | not_applicable_dynamic_priority |
| B | EDF | wcet | Gas | — | 20 | — | — | — | — | 8 | 8 | — | not_applicable_dynamic_priority |
| B | EDF | wcet | Sirene | — | 40 | — | — | — | — | 20 | 19 | — | not_applicable_dynamic_priority |
| B | EDF | wcet | Comunic | — | 50 | — | — | — | — | 40 | 40 | — | not_applicable_dynamic_priority |
| B | EDF | acet | Fumaca | — | 10 | — | — | — | — | 2.94353 | 2.3236 | — | not_applicable_dynamic_priority |
| B | EDF | acet | Gas | — | 20 | — | — | — | — | 7.04247 | 5.82517 | — | not_applicable_dynamic_priority |
| B | EDF | acet | Sirene | — | 40 | — | — | — | — | 15.7264 | 14.7863 | — | not_applicable_dynamic_priority |
| B | EDF | acet | Comunic | — | 50 | — | — | — | — | 28.0804 | 28.0804 | — | not_applicable_dynamic_priority |
| C | RM | wcet | Fumaca | 1 | 10 | 4 | 4 | — | 4 -> 4 | 4 | 4 | 0 | match |
| C | RM | wcet | Gas | 2 | 20 | 9 | 9 | — | 5 -> 9 -> 9 | 9 | 9 | 0 | match |
| C | RM | wcet | Sirene | 3 | 40 | 30 | 30 | — | 8 -> 17 -> 21 -> 30 -> 30 | 30 | 30 | 0 | match |
| C | RM | wcet | Comunic | 4 | 50 | — | 78 | 78 | 10 -> 27 -> 40 -> 44 -> 61 -> 74 -> 78 -> 78 | 206 | 78 | — | not_applicable_failed_rta |
| C | RM | acet | Fumaca | 1 | 10 | 4 | 4 | — | 4 -> 4 | 3.92471 | 3.09813 | -0.075291 | within_wcet_bound |
| C | RM | acet | Gas | 2 | 20 | 9 | 9 | — | 5 -> 9 -> 9 | 7.9429 | 6.59971 | -1.0571 | within_wcet_bound |
| C | RM | acet | Sirene | 3 | 40 | 30 | 30 | — | 8 -> 17 -> 21 -> 30 -> 30 | 17.608 | 16.2132 | -12.392 | within_wcet_bound |
| C | RM | acet | Comunic | 4 | 50 | — | 78 | 78 | 10 -> 27 -> 40 -> 44 -> 61 -> 74 -> 78 -> 78 | 33.8358 | 33.8358 | — | not_applicable_failed_rta |
| C | DM | wcet | Fumaca | 1 | 10 | 4 | 4 | — | 4 -> 4 | 4 | 4 | 0 | match |
| C | DM | wcet | Gas | 2 | 20 | 9 | 9 | — | 5 -> 9 -> 9 | 9 | 9 | 0 | match |
| C | DM | wcet | Sirene | 3 | 40 | 30 | 30 | — | 8 -> 17 -> 21 -> 30 -> 30 | 30 | 30 | 0 | match |
| C | DM | wcet | Comunic | 4 | 50 | — | 78 | 78 | 10 -> 27 -> 40 -> 44 -> 61 -> 74 -> 78 -> 78 | 206 | 78 | — | not_applicable_failed_rta |
| C | DM | acet | Fumaca | 1 | 10 | 4 | 4 | — | 4 -> 4 | 3.92471 | 3.09813 | -0.075291 | within_wcet_bound |
| C | DM | acet | Gas | 2 | 20 | 9 | 9 | — | 5 -> 9 -> 9 | 7.9429 | 6.59971 | -1.0571 | within_wcet_bound |
| C | DM | acet | Sirene | 3 | 40 | 30 | 30 | — | 8 -> 17 -> 21 -> 30 -> 30 | 17.608 | 16.2132 | -12.392 | within_wcet_bound |
| C | DM | acet | Comunic | 4 | 50 | — | 78 | 78 | 10 -> 27 -> 40 -> 44 -> 61 -> 74 -> 78 -> 78 | 33.8358 | 33.8358 | — | not_applicable_failed_rta |
| C | EDF | wcet | Fumaca | — | 10 | — | — | — | — | 30 | 4 | — | not_applicable_dynamic_priority |
| C | EDF | wcet | Gas | — | 20 | — | — | — | — | 39 | 9 | — | not_applicable_dynamic_priority |
| C | EDF | wcet | Sirene | — | 40 | — | — | — | — | 66 | 30 | — | not_applicable_dynamic_priority |
| C | EDF | wcet | Comunic | — | 50 | — | — | — | — | 71 | 44 | — | not_applicable_dynamic_priority |
| C | EDF | acet | Fumaca | — | 10 | — | — | — | — | 3.92471 | 3.09813 | — | not_applicable_dynamic_priority |
| C | EDF | acet | Gas | — | 20 | — | — | — | — | 7.9429 | 6.59971 | — | not_applicable_dynamic_priority |
| C | EDF | acet | Sirene | — | 40 | — | — | — | — | 17.608 | 16.2132 | — | not_applicable_dynamic_priority |
| C | EDF | acet | Comunic | — | 50 | — | — | — | — | 33.8358 | 33.8358 | — | not_applicable_dynamic_priority |
| D | RM | wcet | Fumaca | 1 | 9 | 2 | 2 | — | 2 -> 2 | 2 | 2 | 0 | match |
| D | RM | wcet | Gas | 2 | 18 | 5 | 5 | — | 3 -> 5 -> 5 | 5 | 5 | 0 | match |
| D | RM | wcet | Sirene | 3 | 8 | — | 9 | 9 | 4 -> 9 -> 9 | 9 | 9 | — | not_applicable_failed_rta |
| D | RM | wcet | Comunic | 4 | 45 | — | 16 | — | 5 -> 14 -> 16 -> 16 | 16 | 16 | — | not_applicable_failed_rta |
| D | RM | acet | Fumaca | 1 | 9 | 2 | 2 | — | 2 -> 2 | 1.96235 | 1.54906 | -0.037646 | within_wcet_bound |
| D | RM | acet | Gas | 2 | 18 | 5 | 5 | — | 3 -> 5 -> 5 | 4.40557 | 3.65001 | -0.594433 | within_wcet_bound |
| D | RM | acet | Sirene | 3 | 8 | — | 9 | 9 | 4 -> 9 -> 9 | 7.27576 | 7.15193 | — | not_applicable_failed_rta |
| D | RM | acet | Comunic | 4 | 45 | — | 16 | — | 5 -> 14 -> 16 -> 16 | 12.1377 | 12.1377 | — | not_applicable_failed_rta |
| D | DM | wcet | Fumaca | 2 | 9 | 6 | 6 | — | 2 -> 6 -> 6 | 6 | 6 | 0 | match |
| D | DM | wcet | Gas | 3 | 18 | 9 | 9 | — | 3 -> 9 -> 9 | 9 | 9 | 0 | match |
| D | DM | wcet | Sirene | 1 | 8 | 4 | 4 | — | 4 -> 4 | 4 | 4 | 0 | match |
| D | DM | wcet | Comunic | 4 | 45 | 16 | 16 | — | 5 -> 14 -> 16 -> 16 | 16 | 16 | 0 | match |
| D | DM | acet | Fumaca | 2 | 9 | 6 | 6 | — | 2 -> 6 -> 6 | 5.05098 | 5.05098 | -0.949021 | within_wcet_bound |
| D | DM | acet | Gas | 3 | 18 | 9 | 9 | — | 3 -> 9 -> 9 | 7.27576 | 7.15193 | -1.72424 | within_wcet_bound |
| D | DM | acet | Sirene | 1 | 8 | 4 | 4 | — | 4 -> 4 | 3.56807 | 3.50191 | -0.43193 | within_wcet_bound |
| D | DM | acet | Comunic | 4 | 45 | 16 | 16 | — | 5 -> 14 -> 16 -> 16 | 12.1377 | 12.1377 | -3.86227 | within_wcet_bound |
| D | EDF | wcet | Fumaca | — | 9 | — | — | — | — | 6 | 6 | — | not_applicable_dynamic_priority |
| D | EDF | wcet | Gas | — | 18 | — | — | — | — | 9 | 9 | — | not_applicable_dynamic_priority |
| D | EDF | wcet | Sirene | — | 8 | — | — | — | — | 4 | 4 | — | not_applicable_dynamic_priority |
| D | EDF | wcet | Comunic | — | 45 | — | — | — | — | 16 | 16 | — | not_applicable_dynamic_priority |
| D | EDF | acet | Fumaca | — | 9 | — | — | — | — | 5.05098 | 5.05098 | — | not_applicable_dynamic_priority |
| D | EDF | acet | Gas | — | 18 | — | — | — | — | 7.27576 | 7.15193 | — | not_applicable_dynamic_priority |
| D | EDF | acet | Sirene | — | 8 | — | — | — | — | 3.56807 | 3.50191 | — | not_applicable_dynamic_priority |
| D | EDF | acet | Comunic | — | 45 | — | — | — | — | 12.1377 | 12.1377 | — | not_applicable_dynamic_priority |
| E | G-EDF | wcet | Fumaca | — | 10 | — | — | — | — | 4 | 4 | — | not_applicable_dynamic_priority |
| E | G-EDF | wcet | Gas | — | 20 | — | — | — | — | 5 | 5 | — | not_applicable_dynamic_priority |
| E | G-EDF | wcet | Sirene | — | 40 | — | — | — | — | 12 | 12 | — | not_applicable_dynamic_priority |
| E | G-EDF | wcet | Comunic | — | 50 | — | — | — | — | 17 | 17 | — | not_applicable_dynamic_priority |
| E | G-EDF | acet | Fumaca | — | 10 | — | — | — | — | 3.92471 | 3.09813 | — | not_applicable_dynamic_priority |
| E | G-EDF | acet | Gas | — | 20 | — | — | — | — | 4.34116 | 3.50158 | — | not_applicable_dynamic_priority |
| E | G-EDF | acet | Sirene | — | 40 | — | — | — | — | 10.102 | 10.102 | — | not_applicable_dynamic_priority |
| E | G-EDF | acet | Comunic | — | 50 | — | — | — | — | 11.7334 | 10.9655 | — | not_applicable_dynamic_priority |
