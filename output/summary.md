# Alarme de incêndio — resultados da simulação

Motor: SimSo 0.8.5; Python 3.11.15. Execuções: 26. Todos os tempos estão em ms.

Tarefas periódicas, independentes, preemptivas, ativadas em t=0. Sem jitter, bloqueio, dependências funcionais nem custos de sistema. Jobs atrasados continuam em execução (`abort_on_miss=False`), acumulando espera em FIFO por tarefa.

A janela conta liberações em [0, duração), conclusões e deadlines até a duração inclusive. Deadlines futuros são excluídos da taxa; uma conclusão exatamente no deadline é válida. CPU média é a utilização média dos processadores; U teórica é a soma total de Ci/Ti.

## Resultados WCET

| Cenário | Algoritmo | ETM | CPUs | U teórica (%) | CPU média (%) | Atendidos | Perdidos | Sucesso (%) | Preempções | R médio (ms) | R máximo (ms) | Pendentes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | RM | WCET | 1 | 55 | 55 | 117 | 0 | 100 | 3 | 4.48718 | 16 | 0 |
| A | DM | WCET | 1 | 55 | 55 | 117 | 0 | 100 | 3 | 4.48718 | 16 | 0 |
| A | EDF | WCET | 1 | 55 | 55 | 117 | 0 | 100 | 3 | 4.48718 | 16 | 0 |
| B | RM | WCET | 1 | 95 | 95 | 117 | 0 | 100 | 39 | 9.87179 | 40 | 0 |
| B | DM | WCET | 1 | 95 | 95 | 117 | 0 | 100 | 39 | 9.87179 | 40 | 0 |
| B | EDF | WCET | 1 | 95 | 95 | 117 | 0 | 100 | 39 | 9.61538 | 40 | 0 |
| C | RM | WCET | 1 | 105 | 100 | 105 | 12 | 89.7436 | 42 | 19.8421 | 206 | 3 |
| C | DM | WCET | 1 | 105 | 100 | 105 | 12 | 89.7436 | 42 | 19.8421 | 206 | 3 |
| C | EDF | WCET | 1 | 105 | 100 | 47 | 70 | 40.1709 | 5 | 23.9643 | 71 | 5 |
| D | RM | WCET | 1 | 55 | 55 | 102 | 15 | 87.1795 | 3 | 4.48718 | 16 | 0 |
| D | DM | WCET | 1 | 55 | 55 | 117 | 0 | 100 | 3 | 4.87179 | 16 | 0 |
| D | EDF | WCET | 1 | 55 | 55 | 117 | 0 | 100 | 3 | 4.87179 | 16 | 0 |
| E | G-EDF | WCET | 2 | 105 | 52.5 | 117 | 0 | 100 | 6 | 6.33333 | 17 | 0 |

R médio agrega todos os jobs concluídos, ponderando suas quantidades; R máximo é o maior tempo de resposta concluído entre todas as tarefas. Consulte `tables/tasks.csv` para as respostas por tarefa.

## Resultados ACET

| Cenário | Algoritmo | ETM | CPUs | U teórica (%) | CPU média (%) | Atendidos | Perdidos | Sucesso (%) | Preempções | R médio (ms) | R máximo (ms) | Pendentes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | RM | ACET | 1 | 55 | 40.8757 | 117 | 0 | 100 | 2 | 3.31429 | 12.1377 | 0 |
| A | DM | ACET | 1 | 55 | 40.8757 | 117 | 0 | 100 | 2 | 3.31429 | 12.1377 | 0 |
| A | EDF | ACET | 1 | 55 | 40.8757 | 117 | 0 | 100 | 2 | 3.31429 | 12.1377 | 0 |
| B | RM | ACET | 1 | 95 | 70.6076 | 117 | 0 | 100 | 25 | 6.36089 | 28.0804 | 0 |
| B | DM | ACET | 1 | 95 | 70.6076 | 117 | 0 | 100 | 25 | 6.36089 | 28.0804 | 0 |
| B | EDF | ACET | 1 | 95 | 70.6076 | 117 | 0 | 100 | 25 | 6.36089 | 28.0804 | 0 |
| C | RM | ACET | 1 | 105 | 78.0799 | 117 | 0 | 100 | 29 | 7.567 | 33.8358 | 0 |
| C | DM | ACET | 1 | 105 | 78.0799 | 117 | 0 | 100 | 29 | 7.567 | 33.8358 | 0 |
| C | EDF | ACET | 1 | 105 | 78.0799 | 117 | 0 | 100 | 29 | 7.567 | 33.8358 | 0 |
| D | RM | ACET | 1 | 55 | 40.8757 | 117 | 0 | 100 | 2 | 3.31429 | 12.1377 | 0 |
| D | DM | ACET | 1 | 55 | 40.8757 | 117 | 0 | 100 | 2 | 3.5947 | 12.1377 | 0 |
| D | EDF | ACET | 1 | 55 | 40.8757 | 117 | 0 | 100 | 2 | 3.5947 | 12.1377 | 0 |
| E | G-EDF | ACET | 2 | 105 | 39.0399 | 117 | 0 | 100 | 1 | 4.55303 | 11.7334 | 0 |

R médio agrega todos os jobs concluídos, ponderando suas quantidades; R máximo é o maior tempo de resposta concluído entre todas as tarefas. Consulte `tables/tasks.csv` para as respostas por tarefa.

## Teoria × simulação e divergências

**28 comparações de igualdade válidas; 0 divergências.** O pipeline falha se uma igualdade esperada não for observada, ou se ACET ultrapassar o limite WCET aplicável.

A recorrência de prioridade fixa converge até o ponto fixo. Um valor que excede D comprova a falha da tarefa no teste, mas não representa um limite exato para sucessivos jobs sobrepostos. Se a utilização das tarefas superiores for >= 1, a iteração encerra após exceder D. Por prudência, a igualdade também não é exigida após uma tarefa superior reprovar na RTA.

`rta_response_ms` contém apenas limites certificados para o prefixo de prioridades. `rta_recurrence_ms` registra o resultado numérico da recorrência; `rta_failure_witness_ms` identifica reprovações. EDF e G-EDF não usam RTA de prioridade fixa. LL e hiperbólico são testes suficientes de RM apenas para uma CPU com D=T; o teste EDF U<=1 também é restrito a esse modelo de deadlines.

| scenario | algorithm | task | deadline_ms | rta_recurrence_ms | simulated_first_ms | simulated_worst_ms | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | RM | Fumaca | 10 | 2 | 2 | 2 | match |
| A | RM | Gas | 20 | 5 | 5 | 5 | match |
| A | RM | Sirene | 40 | 9 | 9 | 9 | match |
| A | RM | Comunic | 50 | 16 | 16 | 16 | match |
| A | DM | Fumaca | 10 | 2 | 2 | 2 | match |
| A | DM | Gas | 20 | 5 | 5 | 5 | match |
| A | DM | Sirene | 40 | 9 | 9 | 9 | match |
| A | DM | Comunic | 50 | 16 | 16 | 16 | match |
| A | EDF | Fumaca | 10 | — | 2 | 2 | not_applicable_dynamic_priority |
| A | EDF | Gas | 20 | — | 5 | 5 | not_applicable_dynamic_priority |
| A | EDF | Sirene | 40 | — | 9 | 9 | not_applicable_dynamic_priority |
| A | EDF | Comunic | 50 | — | 16 | 16 | not_applicable_dynamic_priority |
| B | RM | Fumaca | 10 | 3 | 3 | 3 | match |
| B | RM | Gas | 20 | 8 | 8 | 8 | match |
| B | RM | Sirene | 40 | 19 | 19 | 19 | match |
| B | RM | Comunic | 50 | 40 | 40 | 40 | match |
| B | DM | Fumaca | 10 | 3 | 3 | 3 | match |
| B | DM | Gas | 20 | 8 | 8 | 8 | match |
| B | DM | Sirene | 40 | 19 | 19 | 19 | match |
| B | DM | Comunic | 50 | 40 | 40 | 40 | match |
| B | EDF | Fumaca | 10 | — | 3 | 3 | not_applicable_dynamic_priority |
| B | EDF | Gas | 20 | — | 8 | 8 | not_applicable_dynamic_priority |
| B | EDF | Sirene | 40 | — | 19 | 20 | not_applicable_dynamic_priority |
| B | EDF | Comunic | 50 | — | 40 | 40 | not_applicable_dynamic_priority |
| C | RM | Fumaca | 10 | 4 | 4 | 4 | match |
| C | RM | Gas | 20 | 9 | 9 | 9 | match |
| C | RM | Sirene | 40 | 30 | 30 | 30 | match |
| C | RM | Comunic | 50 | 78 | 78 | 206 | not_applicable_failed_rta |
| C | DM | Fumaca | 10 | 4 | 4 | 4 | match |
| C | DM | Gas | 20 | 9 | 9 | 9 | match |
| C | DM | Sirene | 40 | 30 | 30 | 30 | match |
| C | DM | Comunic | 50 | 78 | 78 | 206 | not_applicable_failed_rta |
| C | EDF | Fumaca | 10 | — | 4 | 30 | not_applicable_dynamic_priority |
| C | EDF | Gas | 20 | — | 9 | 39 | not_applicable_dynamic_priority |
| C | EDF | Sirene | 40 | — | 30 | 66 | not_applicable_dynamic_priority |
| C | EDF | Comunic | 50 | — | 44 | 71 | not_applicable_dynamic_priority |
| D | RM | Fumaca | 9 | 2 | 2 | 2 | match |
| D | RM | Gas | 18 | 5 | 5 | 5 | match |
| D | RM | Sirene | 8 | 9 | 9 | 9 | not_applicable_failed_rta |
| D | RM | Comunic | 45 | 16 | 16 | 16 | not_applicable_failed_rta |
| D | DM | Fumaca | 9 | 6 | 6 | 6 | match |
| D | DM | Gas | 18 | 9 | 9 | 9 | match |
| D | DM | Sirene | 8 | 4 | 4 | 4 | match |
| D | DM | Comunic | 45 | 16 | 16 | 16 | match |
| D | EDF | Fumaca | 9 | — | 6 | 6 | not_applicable_dynamic_priority |
| D | EDF | Gas | 18 | — | 9 | 9 | not_applicable_dynamic_priority |
| D | EDF | Sirene | 8 | — | 4 | 4 | not_applicable_dynamic_priority |
| D | EDF | Comunic | 45 | — | 16 | 16 | not_applicable_dynamic_priority |
| E | G-EDF | Fumaca | 10 | — | 4 | 4 | not_applicable_dynamic_priority |
| E | G-EDF | Gas | 20 | — | 5 | 5 | not_applicable_dynamic_priority |
| E | G-EDF | Sirene | 40 | — | 12 | 12 | not_applicable_dynamic_priority |
| E | G-EDF | Comunic | 50 | — | 17 | 17 | not_applicable_dynamic_priority |


Os estados `match` indicam igualdade no instante crítico; `within_wcet_bound` indica ACET dentro do limite WCET; `not_applicable_failed_rta` registra hipóteses insuficientes para exigir igualdade; `not_applicable_dynamic_priority` identifica prioridades dinâmicas.

## Interpretação

1. **A valida o pipeline:** RM teve R máximo por tarefa (2, 5, 9, 16) ms, 0 perdas e CPU ocupada 55.00%. A primeira instância de Comunic é interrompida pela segunda leitura de Fumaca; isso explica R > C.
2. **B mostra a diferença entre testes suficientes e exatos:** U=0.95 excede Liu–Layland (0.756828) e o produto hiperbólico é 2.34 > 2. Essas reprovações são inconclusivas. A RTA e o SimSo dão (3, 8, 19, 40) ms em RM, todos dentro dos deadlines; foram observadas 0 perdas.
3. **Aumentar C eleva a interferência:** de A para B, com os mesmos períodos, RM passou de 3 para 39 preempções. A pior resposta de Comunic passou de 16 para 40 ms. A utilização sozinha não informa qual tarefa absorve a espera.
4. **C satura uma CPU:** RM mediu 100.00% de ocupação para demanda WCET 105.00%. Sirene manteve R máximo 30 <= D=40 ms e 0 perdas. Comunic sofreu 12 perdas e R máximo concluído 206 ms. EDF teve 70 perdas no total e 12 em Sirene: em sobrecarga, a prioridade fixa protege as tarefas de maior prioridade; a otimalidade EDF para sistemas viáveis não implica melhor comportamento em sobrecarga.
5. **Reduzir D muda a urgência sem mudar U:** em D, Sirene tem deadline 8 ms. RM produziu resposta 9 ms e 15 perdas; DM priorizou Sirene, respondeu em 4 ms e o conjunto teve 0 perdas. RM ordena Fumaca, Gas, Sirene, Comunic; DM ordena Sirene, Fumaca, Gas, Comunic. EDF também apresentou 0 perdas nesta execução.
6. **ACET reduz a carga observada:** C/RM passou de 100.00% de CPU com WCET para 78.08% com ACET; as perdas passaram de 12 para 0. A distribuição tem média nominal 0,75 C, desvio 0,10 C e teto C. Uma amostra sem perdas não certifica o conjunto no pior caso.
7. **Duas CPUs acomodam as tarefas de C neste experimento:** E/G-EDF teve 0 perdas, ocupação média por CPU 52.50% e 6 migrações. A demanda total U não se altera com a quantidade de processadores. O teste EDF uniprocessador U <= 1 não se aplica ao escalonamento global.
8. **A comparação exige as hipóteses certas:** houve 28 igualdades RTA × pior resposta WCET verificadas e 0 divergências aplicáveis. ACET é comparado com o limite WCET, sem exigir igualdade. Tempos médios e máximos incluem apenas jobs concluídos; perdas incluem também jobs pendentes cujo deadline já venceu.

## Rastreabilidade e limites

- `tables/summary.csv`: utilização teórica/medida, testes analíticos e totais por execução.
- `tables/tasks.csv`, `jobs.csv`, `cpus.csv`: medidas por tarefa, job e processador.
- `tables/theory_comparison.csv`: recorrências completas, diferenças e estados de validação.
- `tables/execution.csv`: intervalos reais usados no Gantt e na integração da CPU.
- `figures/*_gantt.png`: primeiro hiperperíodo; `*_gantt_full.png`: janela inteira.
- `logs/*.log`: eventos nativos; `simso_api.txt`: API inspecionada; `metadata.json`: ambiente e seeds.
- `manifest.json`: arquivos desta execução e seus hashes; configurações XML em `configs/` por padrão.

Preempção efetiva é a interrupção de um job inacabado para outra tarefa executar na mesma CPU. Chamadas de sistema sem troca de tarefa e migrações instantâneas são excluídas; migrações são contadas separadamente. A contagem ocorre na interrupção, mesmo que não haja retomada antes do fim da janela. Por isso pode diferir de `preemption_inter_count` nativo, que conta retomadas na mesma CPU e não representa todas as interrupções observáveis.

ACET usa o modelo nativo com seed reiniciada por execução. A normal é limitada superiormente por C; a média amostral não precisa ser exatamente 0,75 C. A resolução é 1 ciclo = 10⁻⁶ ms. A normal nativa não possui truncamento inferior: o pipeline rejeita uma amostra não positiva. Uma seed é uma amostra, sem intervalo de confiança nem garantia probabilística. Empates EDF mantêm a decisão vigente; os demais empates seguem a ordem nativa de tarefas.

O modelo avalia cumprimento temporal de tarefas; não modela propagação física do incêndio nem latência desde a detecção física até a sirene. A cadeia analisada é tarefas → escalonamento → execução → tempo de resposta → deadline.

Referência: Chéramy, Hladik e Déplanche. *SimSo: A Simulation Tool to Evaluate Real-Time Multiprocessor Scheduling Algorithms*. WATERS 2014. [Artigo](https://hal.science/hal-01052651v1) · [API oficial](https://maximecheramy.github.io/simso/).
