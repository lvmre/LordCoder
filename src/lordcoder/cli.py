"""Command-line interface for LordCoder."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, List, Optional

from . import __version__
from .config import load_config, save_config
from .core.daemon import run_daemon
from .core.indexer import build_index, select_relevant_files
from .core.policy import PolicyError, PolicyManager
from .doctor import build_doctor_report
from .models import FileChange, PlanResponse


def _print_output(payload: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2))
        return
    for key, value in payload.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"{key}: {value}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lordcoder")
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a LordCoder config file")
    init_parser.add_argument("--path", default=".", help="Project root")
    init_parser.add_argument("--json", action="store_true", help="Emit JSON output")

    doctor_parser = subparsers.add_parser("doctor", help="Run environment diagnostics")
    doctor_parser.add_argument("--path", default=".", help="Project root")
    doctor_parser.add_argument("--recommend-model", action="store_true", help="Only print the recommended model")
    doctor_parser.add_argument("--json", action="store_true", help="Emit JSON output")

    daemon_parser = subparsers.add_parser("daemon", help="Run the local daemon")
    daemon_parser.add_argument("--path", default=".", help="Project root")
    daemon_parser.add_argument("--host", help="Override bind host")
    daemon_parser.add_argument("--port", type=int, help="Override bind port")

    plan_parser = subparsers.add_parser("plan", help="Inspect files and summarise a change plan")
    plan_parser.add_argument("objective", help="What you want to change")
    plan_parser.add_argument("--path", default=".", help="Project root")
    plan_parser.add_argument("--max-files", type=int, default=5, help="Maximum files to select")
    plan_parser.add_argument("--json", action="store_true", help="Emit JSON output")

    apply_parser = subparsers.add_parser("apply", help="Apply or preview explicit file changes")
    apply_parser.add_argument("--path", default=".", help="Project root")
    apply_parser.add_argument("--changes-file", help="JSON file containing a list of file changes")
    apply_parser.add_argument("--file", dest="single_file", help="Single file path to write")
    apply_parser.add_argument("--content", help="Replacement content for --file")
    apply_parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    apply_parser.add_argument("--allow-write", action="store_true", help="Allow file writes for this invocation")
    apply_parser.add_argument("--json", action="store_true", help="Emit JSON output")

    test_parser = subparsers.add_parser("test", help="Run the configured test command")
    test_parser.add_argument("--path", default=".", help="Project root")
    test_parser.add_argument("--command", dest="test_command", help="Override the configured test command")
    test_parser.add_argument("--allow-shell", action="store_true", help="Allow shell execution for this invocation")
    test_parser.add_argument("--json", action="store_true", help="Emit JSON output")

    subparsers.add_parser("version", help="Print the installed version")
    return parser


def _load_changes(args: argparse.Namespace) -> List[FileChange]:
    if args.changes_file:
        payload = json.loads(Path(args.changes_file).read_text(encoding="utf-8"))
        return [FileChange.from_dict(item) for item in payload]
    if args.single_file and args.content is not None:
        return [FileChange(path=args.single_file, content=args.content)]
    raise PolicyError("Provide --changes-file or both --file and --content.")


def _format_doctor_text(report: dict) -> None:
    print(f"Doctor status: {report['status']}")
    print(f"Recommended model: {report['recommendation']}")
    print(f"Recommended command: {report['recommended_command']}")
    for warning in report["warnings"]:
        print(f"Warning: {warning}")
    for check in report["checks"]:
        print(f"[{check['status']}] {check['name']}: {check['message']}")


def _handle_init(args: argparse.Namespace) -> int:
    project_root = Path(args.path).resolve()
    loaded = load_config(project_root)
    path = save_config(project_root, loaded.config)
    payload = {"path": str(path), "source": loaded.source, "warnings": loaded.warnings}
    _print_output(payload, args.json)
    return 0


def _handle_doctor(args: argparse.Namespace) -> int:
    project_root = Path(args.path).resolve()
    report = build_doctor_report(project_root)
    if args.recommend_model:
        if args.json:
            print(json.dumps({"recommendation": report.recommendation}))
        else:
            print(report.recommendation)
        return 0

    payload = report.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        _format_doctor_text(payload)
    return 0 if payload["status"] != "FAIL" else 1


def _handle_plan(args: argparse.Namespace) -> int:
    project_root = Path(args.path).resolve()
    loaded = load_config(project_root)
    entries = build_index(project_root, loaded.config.project.ignore)
    selected = select_relevant_files(entries, args.objective, args.max_files)
    response = PlanResponse(
        objective=args.objective,
        target_path=str(project_root),
        scanned_files=len(entries),
        selected_files=selected,
        summary=(
            f"Scanned {len(entries)} files and selected {len(selected)} files "
            f"for objective '{args.objective}'."
        ),
    )
    _print_output(response.to_dict(), args.json)
    return 0


def _handle_apply(args: argparse.Namespace) -> int:
    project_root = Path(args.path).resolve()
    loaded = load_config(project_root)
    policy = PolicyManager(
        project_root=project_root,
        allow_file_write=loaded.config.permissions.allow_file_write,
        allow_shell=loaded.config.permissions.allow_shell,
    )
    response = policy.apply_changes(
        changes=_load_changes(args),
        dry_run=args.dry_run,
        allow_write=args.allow_write,
    )
    _print_output(response.to_dict(), args.json)
    return 0


def _handle_test(args: argparse.Namespace) -> int:
    project_root = Path(args.path).resolve()
    loaded = load_config(project_root)
    policy = PolicyManager(
        project_root=project_root,
        allow_file_write=loaded.config.permissions.allow_file_write,
        allow_shell=loaded.config.permissions.allow_shell,
    )
    response = policy.run_test_command(
        command=args.test_command or loaded.config.project.test_command,
        cwd=project_root,
        allow_shell=args.allow_shell,
    )
    _print_output(response.to_dict(), args.json)
    return response.returncode


def _handle_version() -> int:
    print(__version__)
    return 0


def main(argv: Optional[Iterable[str]] = None) -> int:
    """Run the CLI."""
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        if args.command == "init":
            return _handle_init(args)
        if args.command == "doctor":
            return _handle_doctor(args)
        if args.command == "daemon":
            run_daemon(Path(args.path).resolve(), host=args.host, port=args.port)
            return 0
        if args.command == "plan":
            return _handle_plan(args)
        if args.command == "apply":
            return _handle_apply(args)
        if args.command == "test":
            return _handle_test(args)
        if args.command == "version":
            return _handle_version()
    except PolicyError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 1
