"""Dados dos cenários; todos os tempos são expressos em milissegundos."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskSpec:
    """Modelo periódico independente, sem jitter nem bloqueio."""

    identifier: int
    name: str
    wcet: int
    period: int
    deadline: int


@dataclass(frozen=True)
class Scenario:
    """Conjunto imutável de parâmetros de um experimento."""

    key: str
    description: str
    tasks: tuple[TaskSpec, ...]
    cpu_count: int = 1
    algorithms: tuple[str, ...] = ("RM", "DM", "EDF")


SCENARIOS = {
    "A": Scenario("A", "Carga folgada, deadlines implícitos", (
        TaskSpec(1, "Fumaca", 2, 10, 10),
        TaskSpec(2, "Gas", 3, 20, 20),
        TaskSpec(3, "Sirene", 4, 40, 40),
        TaskSpec(4, "Comunic", 5, 50, 50),
    )),
    "B": Scenario("B", "Carga alta; RM passa na RTA exata", (
        TaskSpec(1, "Fumaca", 3, 10, 10),
        TaskSpec(2, "Gas", 5, 20, 20),
        TaskSpec(3, "Sirene", 8, 40, 40),
        TaskSpec(4, "Comunic", 10, 50, 50),
    )),
    "C": Scenario("C", "Sobrecarga de uma CPU", (
        TaskSpec(1, "Fumaca", 4, 10, 10),
        TaskSpec(2, "Gas", 5, 20, 20),
        TaskSpec(3, "Sirene", 8, 40, 40),
        TaskSpec(4, "Comunic", 10, 50, 50),
    )),
    "D": Scenario("D", "Deadlines restritos; Sirene urgente", (
        TaskSpec(1, "Fumaca", 2, 10, 9),
        TaskSpec(2, "Gas", 3, 20, 18),
        TaskSpec(3, "Sirene", 4, 40, 8),
        TaskSpec(4, "Comunic", 5, 50, 45),
    )),
    "E": Scenario("E", "Tarefas de C em duas CPUs com EDF global", (
        TaskSpec(1, "Fumaca", 4, 10, 10),
        TaskSpec(2, "Gas", 5, 20, 20),
        TaskSpec(3, "Sirene", 8, 40, 40),
        TaskSpec(4, "Comunic", 10, 50, 50),
    ), cpu_count=2, algorithms=("G-EDF",)),
}

DEFAULT_HYPERPERIODS = 3
DEFAULT_SEED = 42
CYCLES_PER_MS = 1_000_000
ACET_MEAN_RATIO = 0.75
ACET_STDDEV_RATIO = 0.10
FIGURE_DPI = 180
