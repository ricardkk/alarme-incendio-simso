"""Casos conhecidos e fronteiras dos testes analíticos."""

import pytest

from src.scenarios import SCENARIOS, TaskSpec
from src.theory import (
    edf_implicit_test, fixed_priority_test, hyperbolic_product, hyperbolic_test,
    hyperperiod, liu_layland_bound, liu_layland_test, priority_order,
    response_time_analysis, utilization,
)


@pytest.mark.parametrize("key,expected", [("A", .55), ("B", .95), ("C", 1.05)])
def test_utilization_and_hyperperiod(key, expected):
    """Reverifica os três conjuntos fornecidos pelo enunciado."""
    assert utilization(SCENARIOS[key].tasks) == pytest.approx(expected)
    assert hyperperiod(SCENARIOS[key].tasks) == 200


def test_liu_layland_values():
    assert liu_layland_bound(1) == pytest.approx(1)
    assert liu_layland_bound(4) == pytest.approx(.7568284600108841)


def test_a_passes_sufficient_and_exact_tests():
    tasks = SCENARIOS["A"].tasks
    assert liu_layland_test(tasks) and hyperbolic_test(tasks)
    assert edf_implicit_test(tasks) and fixed_priority_test(tasks)
    assert [r.response_ms for r in response_time_analysis(tasks).values()] == [2, 5, 9, 16]


def test_b_fails_sufficient_tests_but_passes_exact_analysis():
    tasks = SCENARIOS["B"].tasks
    assert not liu_layland_test(tasks)
    assert not hyperbolic_test(tasks)
    assert hyperbolic_product(tasks) == pytest.approx(2.34)
    assert fixed_priority_test(tasks) and edf_implicit_test(tasks)
    assert [r.response_ms for r in response_time_analysis(tasks).values()] == [3, 8, 19, 40]


def test_c_overload_and_failure_witness():
    tasks = SCENARIOS["C"].tasks
    assert not fixed_priority_test(tasks) and not edf_implicit_test(tasks)
    bounds = response_time_analysis(tasks)
    assert bounds[3].response_ms == 30 and bounds[3].schedulable
    assert bounds[4].response_ms == 78
    assert bounds[4].converged and not bounds[4].schedulable


def test_d_changes_priority_and_schedulability():
    tasks = SCENARIOS["D"].tasks
    assert [t.identifier for t in priority_order(tasks, "RM")] == [1, 2, 3, 4]
    assert [t.identifier for t in priority_order(tasks, "DM")] == [3, 1, 2, 4]
    assert not fixed_priority_test(tasks, "RM")
    assert fixed_priority_test(tasks, "DM")
    assert response_time_analysis(tasks, "RM")[3].response_ms == 9
    assert response_time_analysis(tasks, "DM")[3].response_ms == 4


@pytest.mark.parametrize("test", [edf_implicit_test, hyperbolic_test, liu_layland_test])
def test_implicit_tests_reject_constrained_deadlines(test):
    with pytest.raises(ValueError, match="D = T"):
        test(SCENARIOS["D"].tasks)


def test_exact_deadline_is_accepted():
    tasks = (TaskSpec(1, "One", 2, 4, 4), TaskSpec(2, "Two", 2, 4, 4))
    assert fixed_priority_test(tasks) and edf_implicit_test(tasks)
    assert response_time_analysis(tasks)[2].response_ms == 4


@pytest.mark.parametrize("tasks", [(), (TaskSpec(1, "Bad", 1, 0, 1),),
    (TaskSpec(1, "Bad", 1, 10, 11),), (TaskSpec(1, "Bad", -1, 10, 10),)])
def test_invalid_models(tasks):
    with pytest.raises(ValueError):
        response_time_analysis(tasks)


def test_nonharmonic_hyperperiod():
    assert hyperperiod((TaskSpec(1, "One", 1, 6, 6), TaskSpec(2, "Two", 1, 15, 15))) == 30
