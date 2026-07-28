from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from . import __version__
from .catalog import Catalog
from .config import load_config, update_config
from .installer import SkillInstaller
from .progress import SpecProgress, scan_specs, specs_fingerprint, summarize_specs
from .testing import run_project_tests
from .updater import offer_startup_update


def _project_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--project", type=Path, default=Path.cwd(), help="raiz do projeto consumidor"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="specsfy")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command")

    install = commands.add_parser("install", help="instala as skills do framework")
    _project_argument(install)
    install.add_argument("--force", action="store_true")
    install.add_argument(
        "--detected",
        action="store_true",
        help="instala também os especialistas detectados",
    )
    install.add_argument(
        "--specialist",
        action="append",
        default=[],
        metavar="NOME",
        help="especialista explícito; pode ser repetido",
    )
    install.add_argument("--json", action="store_true")

    skills = commands.add_parser("skills", help="gerencia especialistas")
    skill_commands = skills.add_subparsers(dest="skills_command", required=True)
    listing = skill_commands.add_parser("list", help="lista o catálogo")
    listing.add_argument("--json", action="store_true")
    detect = skill_commands.add_parser("detect", help="detecta skills para o projeto")
    _project_argument(detect)
    detect.add_argument("--json", action="store_true")
    add = skill_commands.add_parser("add", help="instala especialistas")
    add.add_argument("names", nargs="+")
    _project_argument(add)
    add.add_argument("--force", action="store_true")
    remove = skill_commands.add_parser("remove", help="remove skills instaladas")
    remove.add_argument("names", nargs="+")
    _project_argument(remove)
    remove.add_argument("--force", action="store_true")
    update = skill_commands.add_parser(
        "update",
        help="atualiza todas as skills Specsfy instaladas",
    )
    _project_argument(update)
    update.add_argument("--force", action="store_true")

    progress = commands.add_parser("progress", help="exibe progresso das specs")
    _project_argument(progress)
    progress.add_argument("--json", action="store_true")
    progress.add_argument(
        "--watch", action="store_true", help="emite novo resumo quando uma spec muda"
    )
    progress.add_argument(
        "--interval",
        type=float,
        help="intervalo do watch em segundos; usa a configuração do projeto",
    )

    tests = commands.add_parser("test", help="executa os testes do projeto")
    _project_argument(tests)

    tui = commands.add_parser("tui", help="abre a interface terminal")
    _project_argument(tui)

    config = commands.add_parser("config", help="configura o projeto consumidor")
    config_commands = config.add_subparsers(dest="config_command", required=True)
    show = config_commands.add_parser("show", help="exibe a configuração efetiva")
    _project_argument(show)
    show.add_argument("--json", action="store_true")
    set_config = config_commands.add_parser("set", help="altera a configuração")
    _project_argument(set_config)
    set_config.add_argument("--watch-interval", type=float, required=True)
    set_config.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command in (None, "tui"):
            if offer_startup_update():
                return 0
            from .tui import SpecsfyApp

            SpecsfyApp(getattr(args, "project", Path.cwd())).run()
            return 0
        if args.command == "install":
            installer = SkillInstaller(args.project, force=args.force)
            installed = installer.install_base()
            specialist_names = list(args.specialist)
            catalog = None
            if args.detected:
                catalog = Catalog.fetch()
                specialist_names.extend(
                    entry.name for entry in catalog.detect(args.project)
                )
            if specialist_names:
                catalog = catalog or Catalog.fetch()
                specialist_names = [
                    entry.name for entry in catalog.resolve(specialist_names)
                ]
                installed.extend(installer.install_specialists(specialist_names))
            _print_installation(installed, json_output=args.json)
            return 0
        if args.command == "skills":
            return _skills(args)
        if args.command == "progress":
            return _progress(args)
        if args.command == "test":
            result = run_project_tests(args.project)
            return result.exit_code
        if args.command == "config":
            config = (
                update_config(args.project, watch_interval=args.watch_interval)
                if args.config_command == "set"
                else load_config(args.project)
            )
            if args.json:
                print(json.dumps(config.to_dict(), ensure_ascii=False))
            else:
                print(f"project\t{config.project}")
                print(f"watch_interval\t{config.watch_interval}")
            return 0
    except KeyboardInterrupt:
        return 130
    except (ValueError, FileExistsError, RuntimeError, OSError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 1
    parser.print_help()
    return 2


def _skills(args: argparse.Namespace) -> int:
    if args.skills_command == "remove":
        _print_paths(
            SkillInstaller(args.project, force=args.force).remove(args.names)
        )
        return 0
    if args.skills_command == "update":
        changed = SkillInstaller(args.project, force=args.force).update_all()
        _print_installation(changed, json_output=False)
        return 0
    catalog = Catalog.fetch()
    if args.skills_command == "list":
        entries = catalog.entries
    elif args.skills_command == "detect":
        entries = catalog.detect(args.project)
    else:
        names = [entry.name for entry in catalog.resolve(args.names)]
        installed = SkillInstaller(args.project, force=args.force).install_specialists(
            names
        )
        _print_paths(installed)
        return 0
    if args.json:
        print(
            json.dumps(
                [
                    {
                        "name": entry.name,
                        "description": entry.description,
                        "category": entry.category,
                        "tags": list(entry.tags),
                        "requires": list(entry.requires),
                    }
                    for entry in entries
                ],
                ensure_ascii=False,
            )
        )
    else:
        for entry in entries:
            print(f"{entry.name}\t{entry.description}")
    return 0


def _print_paths(paths: list[Path]) -> None:
    for path in paths:
        print(path)


def _print_installation(paths: list[Path], *, json_output: bool) -> None:
    if json_output:
        print(
            json.dumps(
                {"changed": len(paths), "paths": [str(path) for path in paths]},
                ensure_ascii=False,
            )
        )
    elif paths:
        _print_paths(paths)
    else:
        print("skills já estão atualizadas")


def _progress(args: argparse.Namespace) -> int:
    interval = (
        args.interval
        if args.interval is not None
        else load_config(args.project).watch_interval
    )
    if interval <= 0:
        raise ValueError("interval deve ser maior que zero")
    previous = ""
    while True:
        fingerprint = specs_fingerprint(args.project)
        if fingerprint != previous:
            specs = scan_specs(args.project)
            _print_progress(specs, json_output=args.json)
            previous = fingerprint
            if not args.watch:
                return 0 if specs else 2
        time.sleep(interval)


def _print_progress(specs: list[SpecProgress], *, json_output: bool) -> None:
    summary = summarize_specs(specs)
    if json_output:
        print(
            json.dumps(
                {
                    "summary": summary.to_dict(),
                    "specs": [spec.to_dict() for spec in specs],
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        return
    print(
        "Resumo\t"
        f"{summary.total_specs} specs\t"
        f"{summary.completed_tasks}/{summary.total_tasks} tarefas\t"
        f"{summary.completed_items}/{summary.total_items} itens\t"
        f"{summary.percent}%"
    )
    for spec in specs:
        print(
            f"{spec.slug}\t{spec.status}\t"
            f"{spec.completed_tasks}/{spec.total_tasks} tarefas\t"
            f"{spec.completed_items}/{spec.total_items} itens\t"
            f"{spec.percent}%"
        )
