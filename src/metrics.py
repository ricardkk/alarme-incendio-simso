"""Métricas derivadas de Results e dos monitores reais do SimSo."""

from dataclasses import dataclass
from math import isclose
from statistics import mean

import pandas as pd

from src.sim_runner import SimulationRun
from src.theory import (
    edf_implicit_test, hyperbolic_product, hyperbolic_test, hyperperiod,
    liu_layland_bound, liu_layland_test,
    response_time_analysis, utilization,
)


@dataclass
class RunMetrics:
    """Tabelas independentes do motor, prontas para CSV e figuras."""

    run: SimulationRun
    summary: dict
    tasks: pd.DataFrame
    jobs: pd.DataFrame
    cpus: pd.DataFrame
    segments: pd.DataFrame
    comparison: pd.DataFrame


def _average(values):
    """Retorna ausência de medida quando nenhum job terminou."""
    return mean(values) if values else None


def extract_cpu_segments(run: SimulationRun) -> pd.DataFrame:
    """Integra estados positivos da CPU, descartando interrupções de tempo zero."""
    from simso.core.ProcEvent import ProcEvent

    rows = []
    horizon = run.duration_ms * run.model.cycles_per_ms
    scale = run.model.cycles_per_ms
    for cpu in run.model.processors:
        for index, (start, event) in enumerate(cpu.monitor):
            end = cpu.monitor[index + 1][0] if index + 1 < len(cpu.monitor) else horizon
            start, end = max(0, start), min(horizon, end)
            if start >= end:
                continue
            job = event.args if event.event == ProcEvent.RUN else None
            state = {ProcEvent.RUN: "execution", ProcEvent.IDLE: "idle",
                     ProcEvent.OVERHEAD: "overhead"}[event.event]
            row = dict(cpu=cpu.name, state=state,
                       task_id=job.task.identifier if job else None,
                       task=job.task.name if job else None,
                       job=job.name if job else None,
                       start_ms=start / scale, end_ms=end / scale,
                       duration_ms=(end - start) / scale)
            # Uma chamada de sistema de duração zero não fragmenta execução.
            if (rows and all(rows[-1][key] == row[key] for key in ("cpu", "state", "job"))
                    and rows[-1]["end_ms"] == row["start_ms"]):
                rows[-1]["end_ms"] = row["end_ms"]
                rows[-1]["duration_ms"] += row["duration_ms"]
            else:
                rows.append(row)
    return pd.DataFrame(rows)


def _real_preemptions(segments: pd.DataFrame, jobs: pd.DataFrame) -> dict[str, int]:
    """Conta a substituição de um job inacabado por outro que de fato executou.

    Conta no instante da interrupção, mesmo sem retomada até o fim da janela.
    Assim não conta chamadas de sistema que apenas devolvem a CPU ao mesmo job.
    """
    end_dates = jobs.set_index("job")["end_ms"].to_dict()
    counts = {name: 0 for name in jobs["job"]}
    executing = segments[segments["state"] == "execution"]
    starts = executing.groupby("job")["start_ms"].apply(list).to_dict()
    for _, cpu_segments in executing.groupby("cpu", sort=False):
        entries = cpu_segments.to_dict("records")
        for previous, following in zip(entries, entries[1:]):
            end = end_dates.get(previous["job"])
            incomplete = pd.isna(end) or end > previous["end_ms"]
            immediate_migration = previous["end_ms"] in starts[previous["job"]]
            if incomplete and previous["job"] != following["job"] and not immediate_migration:
                counts[previous["job"]] += 1
    return counts


def extract_metrics(run: SimulationRun) -> RunMetrics:
    """Inclui deadlines vencidos de jobs pendentes e exclui liberações em H."""
    results = run.model.results
    scale = run.model.cycles_per_ms
    horizon = run.duration_ms
    metadata = dict(scenario=run.scenario.key, algorithm=run.algorithm, etm=run.etm)
    job_rows = []
    for task, task_result in results.tasks.items():
        for job in task_result.jobs:
            activation = job.activation_date / scale
            if activation >= horizon:
                continue
            deadline = job.absolute_deadline / scale
            end = job.end_date / scale if job.end_date is not None else None
            response = job.response_time / scale if job.response_time is not None else None
            due = deadline <= horizon
            met = due and end is not None and end <= deadline and not job.aborted
            missed = due and not met
            job_rows.append(dict(
                **metadata, task_id=task.identifier, task=task.name, job=job.name,
                activation_ms=activation, deadline_ms=deadline, end_ms=end,
                response_ms=response, completed=end is not None and not job.aborted,
                deadline_evaluated=due, deadline_met=met, deadline_missed=missed,
                pending=end is None, aborted=job.aborted,
                normalized_laxity=(task.deadline - response) / task.period if response is not None else None,
                native_preemptions=job.preemption_count,
                native_inter_task_preemptions=job.preemption_inter_count,
            ))
    jobs = pd.DataFrame(job_rows)
    segments = extract_cpu_segments(run)
    counts = _real_preemptions(segments, jobs)
    jobs["preemptions"] = jobs["job"].map(counts)
    execution = segments[segments["state"] == "execution"]
    executed = execution.groupby("job")["duration_ms"].sum()
    jobs["executed_ms"] = jobs["job"].map(executed).fillna(0)
    migrations = {}
    for name, entries in execution.sort_values("start_ms").groupby("job"):
        processors = entries["cpu"].tolist()
        migrations[name] = sum(first != second for first, second in zip(processors, processors[1:]))
    jobs["migrations"] = jobs["job"].map(migrations).fillna(0).astype(int)

    cpu_rows = []
    for cpu, load, overhead in results.calc_load():
        measured = execution.loc[execution["cpu"] == cpu.name, "duration_ms"].sum() / horizon
        if not isclose(measured, load, abs_tol=1e-10):
            raise AssertionError(f"Utilização do monitor difere de Results.calc_load: {cpu.name}.")
        cpu_rows.append(dict(**metadata, cpu=cpu.name, utilization=load,
                             overhead_utilization=overhead, busy_ms=measured * horizon))
    cpus = pd.DataFrame(cpu_rows)

    fixed = run.algorithm in ("RM", "DM") and run.scenario.cpu_count == 1
    bounds = response_time_analysis(run.scenario.tasks, run.algorithm) if fixed else {}
    task_rows, comparison_rows = [], []
    valid_prefix = True
    comparable_ids = set()
    for bound in bounds.values():
        valid_prefix = valid_prefix and bound.schedulable
        if valid_prefix:
            comparable_ids.add(bound.task_id)

    for task in run.scenario.tasks:
        selected = jobs[jobs["task_id"] == task.identifier]
        responses = selected.loc[selected["completed"], "response_ms"].dropna().tolist()
        evaluated = int(selected["deadline_evaluated"].sum())
        met, missed = int(selected["deadline_met"].sum()), int(selected["deadline_missed"].sum())
        worst = max(responses) if responses else None
        bound = bounds.get(task.identifier)
        comparison = "not_applicable_dynamic_priority" if not fixed else "not_applicable_failed_rta"
        theoretical = bound.response_ms if bound and task.identifier in comparable_ids else None
        if theoretical is not None:
            if worst is None:
                comparison = "no_completed_jobs"
            elif run.etm == "wcet":
                comparison = "match" if isclose(worst, theoretical, abs_tol=1 / scale) else "DIVERGENCE"
            else:
                comparison = "within_wcet_bound" if worst <= theoretical + 1 / scale else "DIVERGENCE"
        task_rows.append(dict(
            **metadata, task_id=task.identifier, task=task.name,
            wcet_ms=task.wcet, period_ms=task.period, deadline_ms=task.deadline,
            utilization=task.wcet / task.period,
            priority=bound.priority if bound else None,
            priority_rule="deadline absoluto do job" if not fixed else "prioridade fixa (1 = maior)",
            released=len(selected), completed=int(selected["completed"].sum()),
            pending=int(selected["pending"].sum()), deadlines_evaluated=evaluated,
            deadlines_met=met, deadlines_missed=missed,
            success_rate=met / evaluated if evaluated else None,
            preemptions=int(selected["preemptions"].sum()),
            migrations=int(selected["migrations"].sum()),
            response_mean_ms=_average(responses), response_worst_ms=worst,
            laxity_mean=_average(selected["normalized_laxity"].dropna().tolist()),
            executed_ms=float(selected["executed_ms"].sum()),
        ))
        comparison_rows.append(dict(
            **metadata, task=task.name, priority=bound.priority if bound else None,
            deadline_ms=task.deadline, rta_response_ms=theoretical,
            rta_recurrence_ms=bound.response_ms if bound else None,
            rta_failure_witness_ms=bound.response_ms if bound and not bound.schedulable else None,
            rta_trace=" -> ".join(map(str, bound.trace)) if bound else None,
            simulated_worst_ms=worst,
            simulated_first_ms=selected.iloc[0]["response_ms"],
            difference_ms=worst - theoretical if worst is not None and theoretical is not None else None,
            status=comparison,
        ))
    tasks = pd.DataFrame(task_rows)
    comparison = pd.DataFrame(comparison_rows)
    implicit = all(t.deadline == t.period for t in run.scenario.tasks)
    single_implicit = implicit and run.scenario.cpu_count == 1
    total_utilization = utilization(run.scenario.tasks)
    evaluated = int(jobs["deadline_evaluated"].sum())
    responses = jobs.loc[jobs["completed"], "response_ms"].dropna().tolist()
    summary = dict(
        **metadata, cpu_count=run.scenario.cpu_count, duration_ms=horizon,
        hyperperiod_ms=hyperperiod(run.scenario.tasks), seed=run.seed,
        theoretical_utilization=total_utilization,
        theoretical_capacity_utilization=total_utilization / run.scenario.cpu_count,
        measured_utilization=float(cpus["utilization"].mean()),
        liu_layland_bound=liu_layland_bound(len(run.scenario.tasks)),
        rm_liu_layland_status=("guaranteed" if liu_layland_test(run.scenario.tasks) else "inconclusive") if single_implicit else "not_applicable",
        hyperbolic_product=hyperbolic_product(run.scenario.tasks),
        rm_hyperbolic_status=("guaranteed" if hyperbolic_test(run.scenario.tasks) else "inconclusive") if single_implicit else "not_applicable",
        edf_implicit_status=("schedulable" if edf_implicit_test(run.scenario.tasks) else "unschedulable") if single_implicit else "not_applicable",
        fixed_priority_status=("schedulable" if all(b.schedulable for b in bounds.values()) else "unschedulable") if fixed else "not_applicable",
        released=len(jobs), completed=int(jobs["completed"].sum()),
        pending=int(jobs["pending"].sum()), deadlines_evaluated=evaluated,
        deadlines_met=int(jobs["deadline_met"].sum()),
        deadlines_missed=int(jobs["deadline_missed"].sum()),
        success_rate=int(jobs["deadline_met"].sum()) / evaluated if evaluated else None,
        preemptions=int(jobs["preemptions"].sum()),
        migrations=int(jobs["migrations"].sum()),
        native_inter_task_preemptions=int(jobs["native_inter_task_preemptions"].sum()),
        response_mean_ms=_average(responses), response_worst_ms=max(responses) if responses else None,
        equality_checks=int((comparison["status"] == "match").sum()),
        divergences=int((comparison["status"] == "DIVERGENCE").sum()),
    )
    return RunMetrics(run, summary, tasks, jobs, cpus, segments, comparison)


def verify_consistency(metrics: RunMetrics) -> None:
    """Interrompe o pipeline antes da publicação de resultados inconsistentes."""
    if metrics.summary["divergences"]:
        raise AssertionError(f"RTA diverge do SimSo em {metrics.run.key}:\n{metrics.comparison.to_string(index=False)}")
    if metrics.summary["deadlines_met"] + metrics.summary["deadlines_missed"] != metrics.summary["deadlines_evaluated"]:
        raise AssertionError("Contagem inconsistente de deadlines.")
    if ((metrics.jobs["executed_ms"] < 0).any()
            or any(metrics.cpus["utilization"] > 1 + 1e-10)):
        raise AssertionError("Tempos ou utilização fisicamente inválidos.")
    if (metrics.jobs.loc[metrics.jobs["completed"], "executed_ms"] <= 0).any():
        raise AssertionError("A normal ACET nativa sorteou execução não positiva; escolha outra seed.")
