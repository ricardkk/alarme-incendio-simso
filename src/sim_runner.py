"""Configuração e execução do SimSo, sem emulação própria de eventos."""

from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
import random
import sys

from src.scenarios import (
    ACET_MEAN_RATIO, ACET_STDDEV_RATIO, CYCLES_PER_MS,
    DEFAULT_HYPERPERIODS, DEFAULT_SEED, Scenario,
)
from src.theory import hyperperiod, validate_tasks


def _require_supported_python() -> None:
    """Evita o erro obscuro de importação de imp no SimSo 0.8.5."""
    if not (3, 10) <= sys.version_info[:2] < (3, 12):
        raise RuntimeError(
            "SimSo 0.8.5 requer Python 3.10 ou 3.11 (usa o módulo imp). "
            "Crie o venv com: python3.11 -m venv .venv")


def inspect_api() -> str:
    """Registra assinaturas e arquivos da API realmente instalada."""
    _require_supported_python()
    import inspect
    import platform
    import pkgutil
    import simso
    import simso.schedulers
    from simso.configuration import Configuration
    from simso.core import Model
    from simso.core.results import Results

    lines = [f"Python: {platform.python_version()}", f"SimSo: {simso.__version__}",
             f"Configuration: {inspect.getfile(Configuration)}",
             f"Model: {inspect.getfile(Model)}", f"Results: {inspect.getfile(Results)}"]
    for name in ("add_task", "add_processor", "save", "check_all"):
        lines.append(f"Configuration.{name}{inspect.signature(getattr(Configuration, name))}")
    lines += [f"Model.run_model{inspect.signature(Model.run_model)}",
              f"Results.calc_load{inspect.signature(Results.calc_load)}",
              "Escalonadores: " + ", ".join(sorted(module.name for module in
                  pkgutil.iter_modules(simso.schedulers.__path__))),
              "DM nativo: ausente; adaptação local src.DM -> src.schedulers_custom.DM.",
              "Unidades: C/T/D e activation_date em ms; duration e JobR em ciclos.",
              "Resultados: model.results.tasks[task].jobs; model.results.calc_load().",
              "Eventos: task.monitor, processor.monitor e model.logs.",
              "Contadores nativos de preempção contam retomadas; métricas locais contam interrupções efetivas."]
    return "\n".join(lines) + "\n"


@dataclass
class SimulationRun:
    """Modelo real e metadados necessários ao pós-processamento."""

    scenario: Scenario
    algorithm: str
    etm: str
    seed: int
    duration_ms: int
    configuration: object
    model: object
    stdout: str

    @property
    def key(self) -> str:
        """Nome estável para configurações, figuras e logs."""
        return f"{self.scenario.key}_{self.algorithm}_{self.etm}"


def build_configuration(scenario: Scenario, algorithm: str,
                        hyperperiods: int = DEFAULT_HYPERPERIODS,
                        etm: str = "wcet"):
    """C, T e D entram em ms; somente a duração é convertida a ciclos."""
    _require_supported_python()
    from simso.configuration import Configuration

    validate_tasks(scenario.tasks)
    if type(hyperperiods) is not int or hyperperiods < 1:
        raise ValueError("Simule pelo menos um hiperperíodo inteiro.")
    if algorithm not in scenario.algorithms:
        raise ValueError(f"Algoritmo {algorithm} não habilitado em {scenario.key}.")
    if etm not in ("wcet", "acet"):
        raise ValueError("ETM deve ser wcet ou acet.")
    configuration = Configuration()
    configuration.cycles_per_ms = CYCLES_PER_MS
    configuration.duration = hyperperiod(scenario.tasks) * hyperperiods * CYCLES_PER_MS
    configuration.etm = etm
    # O carregador nativo exige um módulo cujo nome coincida com a classe.
    if algorithm == "DM":
        configuration.scheduler_info.clas = "src.DM"
    else:
        configuration.scheduler_info.clas = "simso.schedulers.RM" if algorithm == "RM" else "simso.schedulers.EDF"
    for task in scenario.tasks:
        configuration.add_task(
            name=task.name, identifier=task.identifier, task_type="Periodic",
            period=task.period, activation_date=0, wcet=task.wcet,
            deadline=task.deadline, abort_on_miss=False,
            acet=ACET_MEAN_RATIO * task.wcet,
            et_stddev=ACET_STDDEV_RATIO * task.wcet,
        )
    for index in range(1, scenario.cpu_count + 1):
        configuration.add_processor(f"CPU{index}", index, speed=1.0)
    configuration.check_all()
    return configuration


def run_simulation(scenario: Scenario, algorithm: str,
                   hyperperiods: int = DEFAULT_HYPERPERIODS, etm: str = "wcet",
                   seed: int = DEFAULT_SEED, config_dir: Path | None = None) -> SimulationRun:
    """Executa Model.run_model e preserva o estado aleatório do chamador."""
    configuration = build_configuration(scenario, algorithm, hyperperiods, etm)
    from simso.core import Model

    if config_dir is not None:
        config_dir.mkdir(parents=True, exist_ok=True)
        configuration.save(str(config_dir / f"{scenario.key}_{algorithm}_{etm}.xml"))
    previous_random_state = random.getstate()
    stream = StringIO()
    try:
        random.seed(seed)
        # EDF 0.8.5 imprime cada despacho; o log é salvo sem poluir a CLI.
        with redirect_stdout(stream):
            model = Model(configuration)
            model.run_model()
    finally:
        random.setstate(previous_random_state)
    if model.results is None or model.results.error:
        raise RuntimeError("O SimSo não produziu resultados válidos.")
    return SimulationRun(scenario, algorithm, etm, seed,
                         configuration.duration // CYCLES_PER_MS,
                         configuration, model, stream.getvalue())
