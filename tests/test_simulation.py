"""Verificações do motor real, unidades, fronteiras e métricas observadas."""

import random

import pytest

from src.metrics import extract_metrics, verify_consistency
from src.scenarios import SCENARIOS, Scenario, TaskSpec
from src.sim_runner import run_simulation


def simulate(key, algorithm, **options):
    """Executa o menor horizonte que contém um instante crítico completo."""
    metrics = extract_metrics(run_simulation(SCENARIOS[key], algorithm, hyperperiods=1, **options))
    verify_consistency(metrics)
    return metrics


def test_a_matches_theory_and_manual_gantt():
    m = simulate("A", "RM")
    assert m.summary["measured_utilization"] == pytest.approx(.55)
    assert m.summary["released"] == 39
    assert m.summary["pending"] == m.summary["deadlines_missed"] == 0
    assert m.summary["preemptions"] == 1
    assert m.summary["equality_checks"] == 4
    intervals = m.segments.query("state == 'execution' and start_ms < 20")
    assert list(intervals[["task", "start_ms", "end_ms"]].itertuples(index=False, name=None)) == [
        ("Fumaca", 0, 2), ("Gas", 2, 5), ("Sirene", 5, 9),
        ("Comunic", 9, 10), ("Fumaca", 10, 12), ("Comunic", 12, 16)]


@pytest.mark.parametrize("algorithm", ["RM", "DM", "EDF"])
def test_b_is_schedulable_in_simso(algorithm):
    m = simulate("B", algorithm)
    assert m.summary["deadlines_missed"] == 0
    assert m.summary["measured_utilization"] == pytest.approx(.95)
    if algorithm != "EDF":
        assert m.summary["equality_checks"] == 4


def test_c_pending_jobs_are_also_deadline_misses():
    m = simulate("C", "RM")
    assert m.summary["measured_utilization"] == pytest.approx(1)
    assert m.summary["deadlines_missed"] > 0
    assert m.summary["pending"] > 0
    assert m.jobs.loc[m.jobs["pending"], "deadline_missed"].all()
    siren = m.tasks.set_index("task").loc["Sirene"]
    assert siren.response_worst_ms == 30 and siren.deadlines_missed == 0
    assert m.summary["deadlines_missed"] > m.run.model.results.total_exceeded_count


def test_d_rm_and_dm_actually_differ():
    rm, dm = simulate("D", "RM"), simulate("D", "DM")
    assert rm.summary["deadlines_missed"] == 5
    assert dm.summary["deadlines_missed"] == 0
    assert rm.tasks.set_index("task").loc["Sirene", "response_worst_ms"] == 9
    assert dm.tasks.set_index("task").loc["Sirene", "response_worst_ms"] == 4


def test_job_finishing_at_window_and_deadline_is_not_a_miss():
    scenario = Scenario("Boundary", "Fronteira exata", (TaskSpec(1, "Only", 10, 10, 10),))
    m = extract_metrics(run_simulation(scenario, "RM", hyperperiods=1))
    assert m.summary["released"] == m.summary["completed"] == m.summary["deadlines_met"] == 1
    assert m.summary["deadlines_missed"] == 0
    assert m.jobs.iloc[0].end_ms == 10


@pytest.mark.parametrize("algorithm", ["RM", "DM", "EDF"])
def test_saved_xml_is_reusable(tmp_path, algorithm):
    from simso.configuration import Configuration
    from simso.core import Model
    run = run_simulation(SCENARIOS["A"], algorithm, hyperperiods=1, config_dir=tmp_path)
    reloaded = Configuration(str(tmp_path / f"{run.key}.xml"))
    reloaded.check_all()
    model = Model(reloaded)
    model.run_model()
    assert model.results.total_exceeded_count == 0
    assert next(model.results.calc_load())[1] == pytest.approx(.55)


def test_acet_is_reproducible_and_preserves_random_state():
    before = random.getstate()
    first, second = simulate("B", "RM", etm="acet"), simulate("B", "RM", etm="acet")
    assert random.getstate() == before
    assert first.jobs.equals(second.jobs)
    assert first.summary["measured_utilization"] < .95
    assert (first.jobs["executed_ms"] > 0).all()
    assert (first.jobs["executed_ms"] <= first.jobs["task"].map(
        {t.name: t.wcet for t in SCENARIOS["B"].tasks}) + 1e-6).all()


def test_two_processors_do_not_use_the_uniprocessor_edf_test():
    m = simulate("E", "G-EDF")
    assert m.summary["deadlines_missed"] == 0
    assert m.summary["measured_utilization"] == pytest.approx(.525)
    assert m.summary["edf_implicit_status"] == "not_applicable"
    assert m.summary["migrations"] > 0


def test_configuration_rejects_invalid_horizon():
    with pytest.raises(ValueError, match="hiperperíodo"):
        run_simulation(SCENARIOS["A"], "RM", hyperperiods=0)
