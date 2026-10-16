"""Testes analíticos para tarefas independentes, preemptivas e sem overhead."""

from dataclasses import dataclass
from math import lcm, prod
from typing import Sequence

from src.scenarios import TaskSpec


def validate_tasks(tasks: Sequence[TaskSpec]) -> None:
    """Restringe a análise a C, T e D inteiros positivos, com D <= T."""
    if not tasks:
        raise ValueError("O conjunto de tarefas não pode ser vazio.")
    if len({task.identifier for task in tasks}) != len(tasks):
        raise ValueError("Os identificadores devem ser únicos.")
    for task in tasks:
        if any(type(value) is not int or value <= 0
               for value in (task.wcet, task.period, task.deadline)):
            raise ValueError("C, T e D devem ser inteiros positivos em ms.")
        if task.deadline > task.period:
            raise ValueError("Esta RTA implementa apenas deadlines D <= T.")


def utilization(tasks: Sequence[TaskSpec]) -> float:
    """Calcula a demanda total de CPU: soma de Ci/Ti."""
    validate_tasks(tasks)
    return sum(task.wcet / task.period for task in tasks)


def hyperperiod(tasks: Sequence[TaskSpec]) -> int:
    """Calcula o MMC dos períodos inteiros, em ms."""
    validate_tasks(tasks)
    return lcm(*(task.period for task in tasks))


def liu_layland_bound(task_count: int) -> float:
    """Retorna o limite suficiente de RM para deadlines implícitos."""
    if type(task_count) is not int or task_count < 1:
        raise ValueError("O número de tarefas deve ser inteiro positivo.")
    return task_count * (2 ** (1 / task_count) - 1)


def _require_implicit_deadlines(tasks: Sequence[TaskSpec]) -> None:
    validate_tasks(tasks)
    if any(task.deadline != task.period for task in tasks):
        raise ValueError("Este teste só se aplica quando D = T em uma CPU.")


def liu_layland_test(tasks: Sequence[TaskSpec]) -> bool:
    """Aprovação garante RM; reprovação é apenas inconclusiva."""
    _require_implicit_deadlines(tasks)
    return utilization(tasks) <= liu_layland_bound(len(tasks)) + 1e-12


def hyperbolic_product(tasks: Sequence[TaskSpec]) -> float:
    """Calcula o produto (1 + Ui), sem atribuir significado fora de RM."""
    validate_tasks(tasks)
    return prod(1 + task.wcet / task.period for task in tasks)


def hyperbolic_test(tasks: Sequence[TaskSpec]) -> bool:
    """Verifica o teste suficiente hiperbólico de RM com D = T."""
    _require_implicit_deadlines(tasks)
    return hyperbolic_product(tasks) <= 2 + 1e-12


def edf_implicit_test(tasks: Sequence[TaskSpec]) -> bool:
    """Teste exato EDF uniprocessador somente para deadlines implícitos."""
    _require_implicit_deadlines(tasks)
    return utilization(tasks) <= 1 + 1e-12


def priority_order(tasks: Sequence[TaskSpec], algorithm: str) -> tuple[TaskSpec, ...]:
    """Ordena prioridades fixas; identificador desempata de forma estável."""
    validate_tasks(tasks)
    if algorithm not in ("RM", "DM"):
        raise ValueError("A ordem fixa deve ser RM ou DM.")
    return tuple(sorted(tasks, key=lambda task: (
        task.period if algorithm == "RM" else task.deadline, task.identifier)))


@dataclass(frozen=True)
class ResponseBound:
    """Um ponto fixo válido ou um testemunho de que o deadline foi excedido."""

    task_id: int
    priority: int
    response_ms: int
    schedulable: bool
    converged: bool
    trace: tuple[int, ...]


def response_time_analysis(tasks: Sequence[TaskSpec], algorithm: str = "RM") -> dict[int, ResponseBound]:
    """Itera Ri = Ci + soma(ceil(Ri/Tj) Cj), até encontrar um ponto fixo.

    Com carga de prioridades superiores >= 1, encerra ao ultrapassar Di
    para evitar uma recorrência ilimitada. Fora de Ri <= Di, o resultado
    é um testemunho de falha, não um limite para jobs sobrepostos.
    A igualdade com o pior caso simulado exige o conjunto escalonável,
    WCET constante, uma CPU e liberações simultâneas no instante crítico.
    """
    ordered = priority_order(tasks, algorithm)
    bounds = {}
    for index, task in enumerate(ordered):
        response = task.wcet
        trace = [response]
        converged = False
        higher_utilization = sum(higher.wcet / higher.period for higher in ordered[:index])
        while True:
            updated = task.wcet + sum(
                ((response + higher.period - 1) // higher.period) * higher.wcet
                for higher in ordered[:index]
            )
            trace.append(updated)
            if updated == response:
                converged = True
                break
            response = updated
            if response > task.deadline and higher_utilization >= 1:
                break
        bounds[task.identifier] = ResponseBound(
            task.identifier, index + 1, response,
            converged and response <= task.deadline, converged, tuple(trace))
    return bounds


def fixed_priority_test(tasks: Sequence[TaskSpec], algorithm: str = "RM") -> bool:
    """Decisão exata para o modelo de prioridades fixas com D <= T."""
    return all(bound.schedulable for bound in response_time_analysis(tasks, algorithm).values())
