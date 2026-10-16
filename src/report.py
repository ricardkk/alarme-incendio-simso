"""Tabelas, rastros e relatório interpretativo baseados apenas nas execuções."""

from datetime import datetime
from importlib.metadata import version
import json
from pathlib import Path
import platform
from zoneinfo import ZoneInfo

import pandas as pd

from src.metrics import RunMetrics


def _combine(frames: list[pd.DataFrame]) -> pd.DataFrame:
    """Consolida registros preservando colunas numéricas com valores ausentes."""
    return pd.DataFrame.from_records([row for frame in frames for row in frame.to_dict("records")])


def markdown_table(frame: pd.DataFrame) -> str:
    """Produz markdown sem acrescentar dependência de tabulate."""
    def format_cell(value):
        if pd.isna(value):
            return "—"
        if isinstance(value, float):
            return f"{value:.6g}"
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = ["| " + " | ".join(map(str, frame.columns)) + " |",
             "| " + " | ".join("---" for _ in frame.columns) + " |"]
    lines.extend("| " + " | ".join(format_cell(value) for value in row) + " |"
                 for row in frame.itertuples(index=False, name=None))
    return "\n".join(lines) + "\n"


def summary_table(metrics_list: list[RunMetrics]) -> pd.DataFrame:
    """Resumo legível; utilização medida é a média das CPUs."""
    rows = []
    for metrics in metrics_list:
        s = metrics.summary
        rows.append({
            "Cenário": s["scenario"], "Algoritmo": s["algorithm"], "ETM": s["etm"].upper(),
            "CPUs": s["cpu_count"], "U teórica (%)": 100 * s["theoretical_utilization"],
            "CPU média (%)": 100 * s["measured_utilization"],
            "Atendidos": s["deadlines_met"], "Perdidos": s["deadlines_missed"],
            "Sucesso (%)": 100 * s["success_rate"], "Preempções": s["preemptions"],
            "R médio (ms)": s["response_mean_ms"], "R máximo (ms)": s["response_worst_ms"],
            "Pendentes": s["pending"],
        })
    return pd.DataFrame(rows)


def _observations(metrics_list: list[RunMetrics]) -> list[str]:
    """Interpreta as medidas disponíveis, sem constantes de resultados."""
    indexed = {(m.run.scenario.key, m.run.algorithm, m.run.etm): m for m in metrics_list}
    observations = []
    def get(key, algorithm="RM", etm="wcet"):
        return indexed.get((key, algorithm, etm))

    a, b, c, d = (get(key) for key in "ABCD")
    if a:
        values = ", ".join(f"{r:g}" for r in a.tasks["response_worst_ms"])
        observations.append(f"**A valida o pipeline:** RM teve R máximo por tarefa ({values}) ms, "
            f"{a.summary['deadlines_missed']} perdas e CPU ocupada {100*a.summary['measured_utilization']:.2f}%. "
            "A primeira instância de Comunic é interrompida pela segunda leitura de Fumaca; isso explica R > C.")
    if b:
        s = b.summary
        values = ", ".join(f"{r:g}" for r in b.tasks["response_worst_ms"])
        observations.append(f"**B mostra a diferença entre testes suficientes e exatos:** U={s['theoretical_utilization']:.2f} "
            f"excede Liu–Layland ({s['liu_layland_bound']:.6f}) e o produto hiperbólico "
            f"é {s['hyperbolic_product']:.2f} > 2. Essas reprovações são inconclusivas. "
            f"A RTA e o SimSo dão ({values}) ms em RM, todos dentro dos deadlines; "
            f"foram observadas {s['deadlines_missed']} perdas.")
    if a and b:
        observations.append(f"**Aumentar C eleva a interferência:** de A para B, com os mesmos períodos, "
            f"RM passou de {a.summary['preemptions']} para {b.summary['preemptions']} preempções. "
            f"A pior resposta de Comunic passou de {a.tasks.set_index('task').loc['Comunic', 'response_worst_ms']:g} "
            f"para {b.tasks.set_index('task').loc['Comunic', 'response_worst_ms']:g} ms. "
            "A utilização sozinha não informa qual tarefa absorve a espera.")
    if c:
        siren, communication = (c.tasks.set_index("task").loc[name] for name in ("Sirene", "Comunic"))
        text = (f"**C satura uma CPU:** RM mediu {100*c.summary['measured_utilization']:.2f}% de ocupação "
            f"para demanda WCET {100*c.summary['theoretical_utilization']:.2f}%. "
            f"Sirene manteve R máximo {siren.response_worst_ms:g} <= D={siren.deadline_ms:g} ms "
            f"e {int(siren.deadlines_missed)} perdas. Comunic sofreu {int(communication.deadlines_missed)} "
            f"perdas e R máximo concluído {communication.response_worst_ms:g} ms.")
        edf = get("C", "EDF")
        if edf:
            text += (f" EDF teve {edf.summary['deadlines_missed']} perdas no total e "
                f"{int(edf.tasks.set_index('task').loc['Sirene','deadlines_missed'])} em Sirene: "
                "em sobrecarga, a prioridade fixa protege as tarefas de maior prioridade; "
                "a otimalidade EDF para sistemas viáveis não implica melhor comportamento em sobrecarga.")
        observations.append(text)
    dm = get("D", "DM")
    if d and dm:
        rm_siren, dm_siren = (m.tasks.set_index("task").loc["Sirene"] for m in (d, dm))
        text = (f"**Reduzir D muda a urgência sem mudar U:** em D, Sirene tem deadline "
            f"{rm_siren.deadline_ms:g} ms. RM produziu resposta {rm_siren.response_worst_ms:g} ms "
            f"e {int(rm_siren.deadlines_missed)} perdas; DM priorizou Sirene, respondeu em "
            f"{dm_siren.response_worst_ms:g} ms e o conjunto teve {dm.summary['deadlines_missed']} perdas. "
            "RM ordena Fumaca, Gas, Sirene, Comunic; DM ordena Sirene, Fumaca, Gas, Comunic.")
        edf = get("D", "EDF")
        if edf:
            text += f" EDF também apresentou {edf.summary['deadlines_missed']} perdas nesta execução."
        observations.append(text)
    c_acet = get("C", etm="acet")
    if c and c_acet:
        observations.append(f"**ACET reduz a carga observada:** C/RM passou de "
            f"{100*c.summary['measured_utilization']:.2f}% de CPU com WCET para "
            f"{100*c_acet.summary['measured_utilization']:.2f}% com ACET; as perdas passaram de "
            f"{c.summary['deadlines_missed']} para {c_acet.summary['deadlines_missed']}. "
            "A distribuição tem média nominal 0,75 C, desvio 0,10 C e teto C. "
            "Uma amostra sem perdas não certifica o conjunto no pior caso.")
    e = get("E", "G-EDF")
    if e:
        observations.append(f"**Duas CPUs acomodam as tarefas de C neste experimento:** E/G-EDF teve "
            f"{e.summary['deadlines_missed']} perdas, ocupação média por CPU "
            f"{100*e.summary['measured_utilization']:.2f}% e {e.summary['migrations']} migrações. "
            "A demanda total U não se altera com a quantidade de processadores. "
            "O teste EDF uniprocessador U <= 1 não se aplica ao escalonamento global.")
    checks = sum(m.summary["equality_checks"] for m in metrics_list)
    divergences = sum(m.summary["divergences"] for m in metrics_list)
    observations.append(f"**A comparação exige as hipóteses certas:** houve {checks} igualdades "
        f"RTA × pior resposta WCET verificadas e {divergences} divergências aplicáveis. "
        "ACET é comparado com o limite WCET, sem exigir igualdade. Tempos médios e máximos "
        "incluem apenas jobs concluídos; perdas incluem também jobs pendentes cujo deadline já venceu.")
    return observations


def write_tables(metrics_list: list[RunMetrics], output_dir: Path) -> list[Path]:
    """Salva tabelas completas, com colunas em inglês e unidades explícitas."""
    table_dir = output_dir / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    frames = {"summary": pd.DataFrame([m.summary for m in metrics_list])}
    for name, attribute in (("tasks", "tasks"), ("jobs", "jobs"), ("cpus", "cpus"),
                             ("theory_comparison", "comparison")):
        frames[name] = _combine([getattr(m, attribute) for m in metrics_list])
    frames["execution"] = pd.concat([
        m.segments.assign(scenario=m.run.scenario.key, algorithm=m.run.algorithm, etm=m.run.etm)
        for m in metrics_list], ignore_index=True)
    paths = []
    for name, frame in frames.items():
        path = table_dir / f"{name}.csv"
        frame.to_csv(path, index=False, float_format="%.9f", encoding="utf-8")
        paths.append(path)
        if name in ("summary", "tasks", "cpus", "theory_comparison"):
            path = table_dir / f"{name}.md"
            path.write_text(markdown_table(frame), encoding="utf-8")
            paths.append(path)
    return paths


def write_logs(metrics_list: list[RunMetrics], output_dir: Path, api_snapshot: str) -> list[Path]:
    """Preserva rastros textuais nativos e o ambiente usado na execução."""
    log_dir = output_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    api_path = log_dir / "simso_api.txt"
    api_path.write_text(api_snapshot, encoding="utf-8")
    paths = [api_path]
    for m in metrics_list:
        scale = m.run.model.cycles_per_ms
        lines = [f"{m.run.key}; duração={m.run.duration_ms} ms; seed={m.run.seed}",
                 "Eventos do logger nativo SimSo (ms):"]
        lines += [f"{cycle/scale:.6f}\t{message}" for cycle, (message, _) in m.run.model.logs
                  if cycle / scale <= m.run.duration_ms]
        if m.run.stdout:
            lines += ["\nSaída nativa do escalonador (tempo em ciclos):", m.run.stdout]
        path = log_dir / f"{m.run.key}.log"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        paths.append(path)
    metadata = {
        "generated_at": datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(),
        "python": platform.python_version(),
        "packages": {name: version(name) for name in ("simso", "SimPy", "numpy", "pandas", "matplotlib", "pytest")},
        "window": "liberações em [0,H); conclusões e deadlines até H inclusive; H é a duração total",
        "abort_on_miss": False, "system_overheads_cycles": 0,
        "runs": [dict(key=m.run.key, seed=m.run.seed, duration_ms=m.run.duration_ms) for m in metrics_list],
    }
    path = log_dir / "metadata.json"
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    paths.append(path)
    return paths


def write_report(metrics_list: list[RunMetrics], output_dir: Path) -> Path:
    """Gera resumo e discussão acadêmica a partir das tabelas medidas."""
    summary = pd.DataFrame([m.summary for m in metrics_list])
    wcet = [m for m in metrics_list if m.run.etm == "wcet"]
    acet = [m for m in metrics_list if m.run.etm == "acet"]
    lines = ["# Alarme de incêndio — resultados da simulação", "",
             f"Motor: SimSo {version('simso')}; Python {platform.python_version()}. "
             f"Execuções: {len(metrics_list)}. Todos os tempos estão em ms.", "",
             "Tarefas periódicas, independentes, preemptivas, ativadas em t=0. "
             "Sem jitter, bloqueio, dependências funcionais nem custos de sistema. "
             "Jobs atrasados continuam em execução (`abort_on_miss=False`), acumulando espera em FIFO por tarefa.", "",
             "A janela conta liberações em [0, duração), conclusões e deadlines até a duração inclusive. "
             "Deadlines futuros são excluídos da taxa; uma conclusão exatamente no deadline é válida. "
             "CPU média é a utilização média dos processadores; U teórica é a soma total de Ci/Ti.", ""]
    for title, group in (("WCET", wcet), ("ACET", acet)):
        if group:
            lines += [f"## Resultados {title}", "", markdown_table(summary_table(group)),
                      "R médio agrega todos os jobs concluídos, ponderando suas quantidades; "
                      "R máximo é o maior tempo de resposta concluído entre todas as tarefas. "
                      "Consulte `tables/tasks.csv` para as respostas por tarefa.", ""]
    comparison = _combine([m.comparison for m in metrics_list])
    checks = int(summary["equality_checks"].sum())
    divergences = int(summary["divergences"].sum())
    lines += ["## Teoria × simulação e divergências", "",
              f"**{checks} comparações de igualdade válidas; {divergences} divergências.** "
              "O pipeline falha se uma igualdade esperada não for observada, ou se ACET ultrapassar o limite WCET aplicável.", "",
              "A recorrência de prioridade fixa converge até o ponto fixo. Um valor que excede D "
              "comprova a falha da tarefa no teste, mas não representa um limite exato para sucessivos jobs "
              "sobrepostos. Se a utilização das tarefas superiores for >= 1, a iteração encerra após exceder D. "
              "Por prudência, a igualdade também não é exigida após uma tarefa superior reprovar na RTA.", "",
              "`rta_response_ms` contém apenas limites certificados para o prefixo de prioridades. "
              "`rta_recurrence_ms` registra o resultado numérico da recorrência; "
              "`rta_failure_witness_ms` identifica reprovações. EDF e G-EDF não usam RTA de prioridade fixa. "
              "LL e hiperbólico são testes suficientes de RM apenas para uma CPU com D=T; "
              "o teste EDF U<=1 também é restrito a esse modelo de deadlines.", ""]
    display = comparison[comparison["etm"] == "wcet"] if wcet else comparison
    lines += [markdown_table(display[["scenario", "algorithm", "task", "deadline_ms",
              "rta_recurrence_ms", "simulated_first_ms",
              "simulated_worst_ms", "status"]]), "",
              "Os estados `match` indicam igualdade no instante crítico; `within_wcet_bound` indica "
              "ACET dentro do limite WCET; `not_applicable_failed_rta` registra hipóteses insuficientes "
              "para exigir igualdade; `not_applicable_dynamic_priority` identifica prioridades dinâmicas.", "",
              "## Interpretação", ""]
    lines += [f"{index}. {observation}" for index, observation in enumerate(_observations(metrics_list), 1)]
    lines += ["", "## Rastreabilidade e limites", "",
              "- `tables/summary.csv`: utilização teórica/medida, testes analíticos e totais por execução.",
              "- `tables/tasks.csv`, `jobs.csv`, `cpus.csv`: medidas por tarefa, job e processador.",
              "- `tables/theory_comparison.csv`: recorrências completas, diferenças e estados de validação.",
              "- `tables/execution.csv`: intervalos reais usados no Gantt e na integração da CPU.",
              "- `figures/*_gantt.png`: primeiro hiperperíodo; `*_gantt_full.png`: janela inteira.",
              "- `logs/*.log`: eventos nativos; `simso_api.txt`: API inspecionada; `metadata.json`: ambiente e seeds.",
              "- `manifest.json`: arquivos desta execução e seus hashes; configurações XML em `configs/` por padrão.", "",
              "Preempção efetiva é a interrupção de um job inacabado para outra tarefa executar na mesma CPU. "
              "Chamadas de sistema sem troca de tarefa e migrações instantâneas são excluídas; "
              "migrações são contadas separadamente. A contagem ocorre na interrupção, mesmo que não haja "
              "retomada antes do fim da janela. Por isso pode diferir de `preemption_inter_count` nativo, "
              "que conta retomadas na mesma CPU e não representa todas as interrupções observáveis.", "",
              "ACET usa o modelo nativo com seed reiniciada por execução. A normal é limitada superiormente "
              "por C; a média amostral não precisa ser exatamente 0,75 C. A resolução é 1 ciclo = 10⁻⁶ ms. "
              "A normal nativa não possui truncamento inferior: o pipeline rejeita uma amostra não positiva. "
              "Uma seed é uma amostra, sem intervalo de confiança nem garantia probabilística. "
              "Empates EDF mantêm a decisão vigente; os demais empates seguem a ordem nativa de tarefas.", "",
              "O modelo avalia cumprimento temporal de tarefas; não modela propagação física do incêndio "
              "nem latência desde a detecção física até a sirene. A cadeia analisada é tarefas → "
              "escalonamento → execução → tempo de resposta → deadline.", "",
              "Referência: Chéramy, Hladik e Déplanche. *SimSo: A Simulation Tool to Evaluate Real-Time "
              "Multiprocessor Scheduling Algorithms*. WATERS 2014. "
              "[Artigo](https://hal.science/hal-01052651v1) · "
              "[API oficial](https://maximecheramy.github.io/simso/).", ""]
    path = output_dir / "summary.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
