#!/usr/bin/env python3
"""CLI: executa o SimSo e produz tabelas, gráficos, XMLs e relatório."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

from src.scenarios import DEFAULT_HYPERPERIODS, DEFAULT_SEED, SCENARIOS
from src.sim_runner import inspect_api, run_simulation


ROOT = Path(__file__).resolve().parent


def parse_arguments(argv=None):
    """Seleciona experimentos com padrões explícitos e reproduzíveis."""
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--all", action="store_true", help="Todos os cenários, algoritmos e ambos os ETMs.")
    selection.add_argument("--scenario", nargs="+", choices=list(SCENARIOS), help="Cenários; padrão: A.")
    parser.add_argument("--algorithm", nargs="+", choices=("RM", "DM", "EDF", "G-EDF"), help="Filtra os algoritmos disponíveis em cada cenário.")
    parser.add_argument("--etm", choices=("wcet", "acet", "both"), help="Padrão: both com --all; wcet nos demais casos.")
    parser.add_argument("--hyperperiods", type=int, default=DEFAULT_HYPERPERIODS, help="Quantidade de hiperperíodos; padrão: %(default)s.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Seed ACET; padrão: %(default)s.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "output", help="Diretório dos artefatos.")
    parser.add_argument("--config-dir", type=Path, default=ROOT / "configs", help="Diretório dos XMLs reutilizáveis.")
    parser.add_argument("--skip-plots", action="store_true", help="Executa sem renderizar PNGs.")
    parser.add_argument("--inspect-api", action="store_true", help="Exibe a API instalada e encerra.")
    parser.add_argument("--list", action="store_true", help="Lista os cenários e encerra.")
    args = parser.parse_args(argv)
    if args.hyperperiods < 1:
        parser.error("--hyperperiods deve ser >= 1.")
    return parser, args


def write_manifest(paths: list[Path], output_dir: Path) -> Path:
    """Lista somente os artefatos gerados nesta invocação, com hashes SHA-256."""
    unique_paths = sorted(set(path.resolve() for path in paths))
    payload = {"files": [dict(path=str(path), sha256=sha256(path.read_bytes()).hexdigest(),
                              bytes=path.stat().st_size) for path in unique_paths]}
    path = output_dir / "manifest.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main(argv=None) -> int:
    """Um comando executa toda a análise sem acessar rede nem abrir janelas."""
    parser, args = parse_arguments(argv)
    if args.list:
        for key, scenario in SCENARIOS.items():
            print(f"{key}: {scenario.description}; CPUs={scenario.cpu_count}; algoritmos={','.join(scenario.algorithms)}")
        return 0
    try:
        snapshot = inspect_api()
    except RuntimeError as error:
        parser.error(str(error))
    if args.inspect_api:
        print(snapshot, end="")
        return 0

    from src.metrics import extract_metrics, verify_consistency
    from src.report import summary_table, write_logs, write_report, write_tables

    keys = list(SCENARIOS) if args.all else list(dict.fromkeys(args.scenario or ["A"]))
    etm_selection = args.etm or ("both" if args.all else "wcet")
    etms = ("wcet", "acet") if etm_selection == "both" else (etm_selection,)
    plan = [(SCENARIOS[key], algorithm, etm) for key in keys
            for algorithm in SCENARIOS[key].algorithms
            if not args.algorithm or algorithm in args.algorithm for etm in etms]
    if not plan:
        parser.error("Nenhum algoritmo selecionado está disponível nos cenários informados.")
    for key in keys:
        if not any(scenario.key == key for scenario, _, _ in plan):
            print(f"Cenário {key}: ignorado pelo filtro de algoritmos.")
    print(snapshot.splitlines()[0] + " · " + snapshot.splitlines()[1], flush=True)
    metrics_list = []
    config_paths = []
    for index, (scenario, algorithm, etm) in enumerate(plan, 1):
        run = run_simulation(scenario, algorithm, hyperperiods=args.hyperperiods,
                             etm=etm, seed=args.seed, config_dir=args.config_dir)
        metrics = extract_metrics(run)
        verify_consistency(metrics)
        metrics_list.append(metrics)
        config_paths.append(args.config_dir / f"{run.key}.xml")
        summary = metrics.summary
        print(f"[{index:02d}/{len(plan):02d}] {run.key}: {run.duration_ms} ms; "
              f"CPU={summary['measured_utilization']:.2%}; perdas={summary['deadlines_missed']}; "
              f"preempções={summary['preemptions']}", flush=True)
    paths = config_paths + write_tables(metrics_list, args.output_dir)
    paths += write_logs(metrics_list, args.output_dir, snapshot)
    paths.append(write_report(metrics_list, args.output_dir))
    if not args.skip_plots:
        from src.plots import generate_figures
        print("Gerando figuras em PNG a 180 dpi...", flush=True)
        paths += generate_figures(metrics_list, args.output_dir / "figures")
    manifest = write_manifest(paths, args.output_dir)
    print("\n" + summary_table(metrics_list).to_string(index=False, float_format=lambda value: f"{value:.3f}"))
    print(f"\nRelatório: {args.output_dir / 'summary.md'}")
    print(f"Manifesto: {manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
