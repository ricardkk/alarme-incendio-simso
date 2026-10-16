"""Figuras em português para inspeção e apresentação em slides."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator, PercentFormatter
import numpy as np
import pandas as pd

from src.metrics import RunMetrics
from src.scenarios import FIGURE_DPI
from src.theory import hyperperiod


TASK_COLORS = {"Fumaca": "#277DA1", "Gas": "#43AA8B", "Sirene": "#F9A03F", "Comunic": "#9B5DE5"}
ALGORITHM_COLORS = {"RM": "#277DA1", "DM": "#9B5DE5", "EDF": "#43AA8B", "G-EDF": "#43AA8B"}


def _style():
    """Aplica um tema legível sem exigir interface gráfica."""
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11,
        "axes.titlesize": 13, "axes.labelsize": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "figure.facecolor": "#FAFBFD", "axes.facecolor": "#FFFFFF",
        "text.color": "#25334A", "axes.labelcolor": "#25334A",
        "xtick.color": "#43516A", "ytick.color": "#43516A",
        "savefig.facecolor": "#FAFBFD",
    })


def _save(figure, path: Path) -> None:
    """Salva a figura e libera recursos para execuções em lote."""
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=FIGURE_DPI)
    plt.close(figure)


def plot_gantt(metrics: RunMetrics, path: Path, end_ms: int | None = None) -> None:
    """Mostra barras reais, liberações, deadlines e perdas em cada CPU."""
    _style()
    run = metrics.run
    limit = min(end_ms or run.duration_ms, run.duration_ms)
    tasks = list(run.scenario.tasks)
    y_positions = {task.name: index for index, task in enumerate(tasks)}
    fig, axes = plt.subplots(run.scenario.cpu_count, 1, sharex=True, squeeze=False,
                             figsize=(15, 3.2 * run.scenario.cpu_count + 1.5), layout="constrained")
    missed = metrics.jobs.set_index("job")["deadline_missed"].to_dict()
    for index, cpu in enumerate(metrics.cpus["cpu"]):
        ax = axes[index, 0]
        selected = metrics.segments.query("cpu == @cpu and state == 'execution' and start_ms < @limit")
        for segment in selected.itertuples():
            duration = min(segment.end_ms, limit) - segment.start_ms
            ax.broken_barh([(segment.start_ms, duration)], (y_positions[segment.task] - .22, .44),
                           facecolors=TASK_COLORS.get(segment.task, "#277DA1"),
                           edgecolors="#B42335" if missed[segment.job] else "white",
                           linewidth=1.1)
        for task in tasks:
            jobs = metrics.jobs.query("task == @task.name")
            activations = jobs.loc[jobs["activation_ms"] < limit, "activation_ms"]
            deadlines = jobs.loc[jobs["deadline_ms"] <= limit, "deadline_ms"]
            failures = jobs.loc[(jobs["deadline_ms"] <= limit) & jobs["deadline_missed"], "deadline_ms"]
            y = y_positions[task.name]
            ax.scatter(activations, [y + .34] * len(activations), marker="^", s=24,
                       color=TASK_COLORS[task.name], clip_on=False, zorder=4)
            ax.scatter(deadlines, [y - .34] * len(deadlines), marker="v", s=24,
                       color="#65728A", zorder=4)
            ax.scatter(failures, [y - .34] * len(failures), marker="x", s=65,
                       linewidths=2, color="#B42335", zorder=5)
        ax.set_yticks(range(len(tasks)), [task.name for task in tasks])
        ax.set_ylim(len(tasks) - .5, -.6)
        ax.set_xlim(-limit * .005, limit * 1.005)
        ax.set_title(f"{cpu} · execução das tarefas", loc="left", fontweight="bold")
        ax.xaxis.set_major_locator(MaxNLocator(nbins=12, steps=[1, 2, 5, 10], integer=True))
        ax.grid(axis="x", alpha=.18)
        ax.set_axisbelow(True)
        ax.set_ylabel("Tarefa")
    axes[-1, 0].set_xlabel("Tempo (ms)")
    subtitle = "Marcas globais repetidas por CPU" if run.scenario.cpu_count > 1 else "Faixas vazias indicam espera ou ociosidade"
    fig.suptitle(f"Alarme de incêndio · cenário {run.scenario.key} · {run.algorithm} · {run.etm.upper()}\n"
                 f"Janela: 0–{limit} ms de {run.duration_ms} ms · {subtitle}", fontweight="bold")
    fig.legend(handles=[
        Patch(facecolor=TASK_COLORS[task.name], label=task.name) for task in tasks
    ] + [
        Line2D([], [], color="#65728A", marker="^", linestyle="", label="Liberação"),
        Line2D([], [], color="#65728A", marker="v", linestyle="", label="Deadline"),
        Line2D([], [], color="#B42335", marker="x", linestyle="", label="Deadline perdido"),
    ], loc="outside lower center", ncols=7, frameon=False, fontsize=10)
    _save(fig, path)


def plot_algorithm_comparison(metrics_list: list[RunMetrics], path: Path) -> None:
    """Compara totais e respostas por tarefa no mesmo cenário e ETM."""
    _style()
    algorithms = [metrics.run.algorithm for metrics in metrics_list]
    first = metrics_list[0]
    summary = pd.DataFrame([metrics.summary for metrics in metrics_list]).set_index("algorithm")
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), layout="constrained")
    for ax, column, title in zip(axes[0], ("preemptions", "deadlines_missed"),
                                  ("Preempções efetivas", "Deadlines perdidos")):
        bars = ax.bar(algorithms, summary.loc[algorithms, column],
                      color=[ALGORITHM_COLORS[a] for a in algorithms], width=.55)
        ax.bar_label(bars, padding=4, fmt="%.0f")
        ax.set_title(title, loc="left", fontweight="bold")
        ax.set_ylabel("Quantidade na janela completa")
        ax.set_ylim(0, max(1, summary[column].max()) * 1.25)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.grid(axis="y", alpha=.16)
        ax.set_axisbelow(True)
    names = first.tasks["task"].tolist()
    positions = np.arange(len(names))
    width = .8 / len(algorithms)
    for ax, column, title in zip(axes[1], ("response_mean_ms", "response_worst_ms"),
                                  ("Resposta média por tarefa", "Pior resposta por tarefa")):
        for index, metrics in enumerate(metrics_list):
            values = metrics.tasks.set_index("task").loc[names, column]
            offset = (index - (len(algorithms) - 1) / 2) * width
            bars = ax.bar(positions + offset, values, width, label=metrics.run.algorithm,
                          color=ALGORITHM_COLORS[metrics.run.algorithm])
            ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=8)
        ax.set_xticks(positions, names)
        ax.set_title(title, loc="left", fontweight="bold")
        ax.set_ylabel("Tempo (ms), jobs concluídos")
        ax.set_ylim(0, ax.get_ylim()[1] * 1.15)
        ax.grid(axis="y", alpha=.16)
        ax.set_axisbelow(True)
        ax.legend(frameon=False)
    fig.suptitle(f"Cenário {first.run.scenario.key} · comparação dos escalonadores · {first.run.etm.upper()}\n"
                 f"{first.run.duration_ms} ms · custos de sistema nulos · seed {first.run.seed}", fontweight="bold")
    _save(fig, path)


def plot_etm_comparison(metrics_list: list[RunMetrics], path: Path) -> None:
    """Compara demanda WCET e utilização observada sob os dois ETMs."""
    _style()
    summary = pd.DataFrame([metrics.summary for metrics in metrics_list])
    pairs = summary.assign(label=summary["scenario"] + "/" + summary["algorithm"])
    labels = list(dict.fromkeys(pairs["label"]))
    positions = np.arange(len(labels))
    fig, axes = plt.subplots(2, 1, figsize=(15, 9), layout="constrained", sharex=True)
    for index, etm in enumerate(("wcet", "acet")):
        selected = pairs[pairs["etm"] == etm].set_index("label").reindex(labels)
        color = "#277DA1" if etm == "wcet" else "#43AA8B"
        axes[0].bar(positions + (index - .5) * .36, selected["measured_utilization"],
                    .36, label=etm.upper(), color=color)
        axes[1].bar(positions + (index - .5) * .36, selected["deadlines_missed"],
                    .36, label=etm.upper(), color=color)
    axes[0].set_title("Utilização média por CPU", loc="left", fontweight="bold")
    axes[0].set_ylabel("Fração da capacidade")
    axes[0].yaxis.set_major_formatter(PercentFormatter(1))
    axes[1].set_title("Deadlines perdidos na janela", loc="left", fontweight="bold")
    axes[1].set_ylabel("Quantidade")
    axes[1].set_xticks(positions, labels, rotation=30, ha="right")
    for ax in axes:
        ax.legend(frameon=False)
        ax.grid(axis="y", alpha=.16)
        ax.set_axisbelow(True)
    fig.suptitle("WCET × ACET · efeito do tempo de execução\nACET: média nominal 75% de C; desvio 10% de C; seed fixa", fontweight="bold")
    _save(fig, path)


def generate_figures(metrics_list: list[RunMetrics], figure_dir: Path) -> list[Path]:
    """Produz Gantt de um hiperperíodo, Gantt completo e comparações."""
    paths = []
    for metrics in metrics_list:
        base = figure_dir / f"{metrics.run.key}_gantt.png"
        plot_gantt(metrics, base, hyperperiod(metrics.run.scenario.tasks))
        paths.append(base)
        if metrics.run.key == "A_RM_wcet":
            initial = figure_dir / "A_RM_wcet_gantt_initial.png"
            plot_gantt(metrics, initial, 20)
            paths.append(initial)
        if metrics.run.duration_ms > hyperperiod(metrics.run.scenario.tasks):
            full = figure_dir / f"{metrics.run.key}_gantt_full.png"
            plot_gantt(metrics, full)
            paths.append(full)
    grouped = {}
    for metrics in metrics_list:
        grouped.setdefault((metrics.run.scenario.key, metrics.run.etm), []).append(metrics)
    for (scenario, etm), group in grouped.items():
        path = figure_dir / f"{scenario}_{etm}_comparison.png"
        plot_algorithm_comparison(group, path)
        paths.append(path)
    if {metrics.run.etm for metrics in metrics_list} == {"wcet", "acet"}:
        path = figure_dir / "etm_comparison.png"
        plot_etm_comparison(metrics_list, path)
        paths.append(path)
    return paths
