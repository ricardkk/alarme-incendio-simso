# Alarme de incêndio com SimSo

Trabalho acadêmico de Sistemas em Tempo Real (UFERSA), baseado em *SimSo: A
Simulation Tool to Evaluate Real-Time Multiprocessor Scheduling Algorithms*
(Chéramy, Hladik e Déplanche, WATERS 2014).

O projeto analisa **tarefas → escalonamento → execução → tempo de resposta →
deadline**, usando `Configuration` e `Model` do SimSo. Compara RM, DM e EDF;
DM é uma subclasse de `simso.core.Scheduler`, sem alteração do motor.

## Instalação

Use **Python 3.10 ou 3.11**. Ambiente validado: Python 3.11.15, SimSo 0.8.5 e
SimPy 2.3.1. Python 3.12+ é incompatível com essa versão do SimSo, que usa `imp`.

Na raiz do projeto:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest
python main.py --all
```

Com Python 3.10, substitua o primeiro comando por `python3.10 -m venv .venv`.
No Windows, crie o ambiente com `py -3.11 -m venv .venv` e ative pelo script
`.venv/Scripts/Activate.ps1`. Tudo roda por terminal, sem banco de dados ou GUI.

## Execução

```bash
# Todos os cenários e algoritmos aplicáveis, com WCET e ACET:
python main.py --all

# Cenário A com RM, durante um hiperperíodo:
python main.py --scenario A --algorithm RM --hyperperiods 1

# Comparar RM, DM e EDF no cenário D:
python main.py --scenario D --etm wcet

# Comparar WCET e ACET com seed fixa:
python main.py --scenario B C --algorithm RM EDF --etm both --seed 42

# Inspecionar a API instalada e consultar outras opções:
python main.py --inspect-api
python main.py --help
```

Sem opções, executa A com RM, DM e EDF sob WCET. O padrão é **600 ms**
(3 hiperperíodos de 200 ms), com seed **42**. Use `--skip-plots` para gerar
somente tabelas e logs. `--output-dir` e `--config-dir` permitem isolar os
arquivos; execuções parciais substituem as tabelas agregadas, mas preservam
figuras antigas. O manifesto identifica os arquivos da invocação atual.

## Tarefas e cenários

O modelo é `τi = (Ci, Ti, Di)`: WCET, período e deadline relativo, em **ms**.
As tarefas são periódicas, independentes e preemptivas, ativadas em **t=0**,
sem jitter, bloqueio ou custos de sistema.

| Tarefa | Função |
| --- | --- |
| Fumaca | Leitura do sensor de fumaça/temperatura |
| Gas | Leitura do sensor de gás/CO |
| Sirene | Decisão e acionamento da sirene |
| Comunic | Comunicação e supervisão do painel |

Os valores abaixo seguem essa ordem. Todos os cenários usam períodos
**T = (10, 20, 40, 50) ms**.

| Cenário | C (ms) | D (ms) | U total | CPUs | Objetivo |
| --- | --- | --- | --- | --- | --- |
| A | (2, 3, 4, 5) | (10, 20, 40, 50) | 0,55 | 1 | Funcionamento com folga |
| B | (3, 5, 8, 10) | (10, 20, 40, 50) | 0,95 | 1 | Carga alta, escalonável por RM |
| C | (4, 5, 8, 10) | (10, 20, 40, 50) | 1,05 | 1 | Sobrecarga e perdas de deadline |
| D | (2, 3, 4, 5) | (9, 18, 8, 45) | 0,55 | 1 | Comparar RM e DM com Sirene urgente |
| E | (4, 5, 8, 10) | (10, 20, 40, 50) | 1,05 | 2 | Explorar EDF global e migrações |

A–D comparam RM, DM e EDF; E utiliza G-EDF. Em D, RM prioriza Fumaca → Gas →
Sirene → Comunic, enquanto DM prioriza Sirene → Fumaca → Gas → Comunic.

O tempo de resposta vai da liberação do job à conclusão. O modelo não inclui
precedência entre sensores e Sirene nem a latência física de detecção do incêndio.

## Teoria e métricas

A análise teórica em `src/theory.py` inclui:

- Utilização `U = Σ Ci/Ti` e hiperperíodo pelo MMC dos períodos.
- Liu–Layland: `U <= n(2^(1/n) - 1)`.
- Hiperbólico: `Π(1 + Ci/Ti) <= 2`.
- RTA: `Ri = Ci + Σ ceil(Ri/Tj) Cj`, somando tarefas de prioridade superior
  até o ponto fixo; a tarefa passa quando `Ri <= Di`.
- EDF uniprocessador com D=T: `U <= 1`.

Liu–Layland e hiperbólico são testes suficientes para RM com D=T: reprovar é
**inconclusivo**, como ocorre em B. A RTA implementada considera uma CPU e D<=T.
O teste EDF de utilização não se aplica aos deadlines restritos de D nem ao G-EDF.

As métricas incluem utilização teórica/medida, preempções, migrações, deadlines
atendidos/perdidos, taxa de sucesso, resposta média/máxima e laxidade normalizada.

- Jobs liberados exatamente no fim da janela são excluídos; concluir no deadline
  é válido. Jobs atrasados continuam executando e podem acumular espera.
- Perdas incluem pendentes com deadline vencido; respostas usam apenas jobs
  concluídos. Em E, a utilização agregada é a média das duas CPUs.
- Preempções contam interrupções efetivas por outra tarefa, excluindo chamadas
  de sistema sem troca de tarefa e migrações instantâneas.
- O pior R sob WCET é conferido com a RTA nos casos aplicáveis. Se a RTA falha,
  sua recorrência não é tratada como limite para jobs que acumulam atraso.

O SimSo recebe C, T e D em ms, mas duração e resultados `JobR` em ciclos.
As conversões usam **1.000.000 ciclos/ms**. A API inspecionada é registrada
em `output/logs/simso_api.txt`.

## WCET × ACET

WCET executa cada job com Ci. ACET usa o modelo nativo do SimSo: normal com média
nominal **75% de Ci**, desvio **10% de Ci** e teto em Ci, com seed reiniciada por
execução. Uma amostra sem perdas não substitui a análise do pior caso.

## Estrutura e resultados

| Caminho | Conteúdo |
| --- | --- |
| `main.py` | CLI dos experimentos |
| `src/scenarios.py` | Dados dos cenários |
| `src/sim_runner.py` | Configuração e execução do SimSo |
| `src/schedulers_custom.py`, `src/DM.py` | Política DM e adaptação ao carregador |
| `src/theory.py`, `src/metrics.py` | Análise teórica e métricas |
| `src/plots.py`, `src/report.py` | Gráficos, tabelas e relatório |
| `tests/` | Testes teóricos e de integração |
| `configs/` | XMLs reutilizáveis das configurações |
| `output/tables/` | CSVs e tabelas markdown |
| `output/figures/` | Gantts e comparações em PNG a 180 dpi |
| `output/logs/` | Eventos nativos, API e metadados |
| `output/manifest.json` | Arquivos gerados e hashes SHA-256 |

O [relatório completo](output/summary.md) contém resultados reais, comparação
RTA × simulação, divergências e observações interpretativas. Os Gantts mostram o
primeiro hiperperíodo e a janela completa, com liberações, deadlines e perdas.

Os testes cobrem teoria, cenários, fronteiras temporais, reutilização de XMLs,
repetibilidade ACET e duas CPUs. Os XMLs podem ser carregados com
`Configuration("configs/D_DM_wcet.xml")` e executados por `Model` a partir da
raiz do projeto. Para repetir ACET, defina `random.seed(42)` antes de criar
o modelo, pois o XML nativo não armazena a seed.

## Referências

- [Artigo — WATERS 2014](https://hal.science/hal-01052651v1).
- [Documentação oficial do SimSo](https://maximecheramy.github.io/simso/).
- [Código-fonte dos autores](https://github.com/MaximeCheramy/simso).

O artigo fundamenta a arquitetura e os ETMs. Os cenários do alarme e seus
resultados pertencem a este experimento acadêmico.
