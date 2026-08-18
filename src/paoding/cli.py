from __future__ import annotations

import argparse
from pathlib import Path
import sys

from . import __version__
from .assemble import assemble_case
from .init_case import init_case
from .pack import package_case
from .reproduce import reproduce_case
from .reverse import reverse_case
from .trace import trace_case
from .validate import validate_case


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="paoding", description="Evidence-backed reverse distillation for finished AI artifacts")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("init", help="initialize a case from a local video")
    s.add_argument("video", type=Path)
    s.add_argument("--cases-dir", type=Path, default=Path("cases"))
    s.add_argument("--slug")

    s = sub.add_parser("trace", help="extract timestamped evidence frames")
    s.add_argument("case", type=Path)
    s.add_argument("--interval", type=float, default=2.0)
    s.add_argument("--no-audio", action="store_true")

    s = sub.add_parser("reverse", help="create or import structured production hypotheses")
    s.add_argument("case", type=Path)
    s.add_argument("--input-json", type=Path)

    s = sub.add_parser("assemble", help="assemble a provider-agnostic equivalent recipe")
    s.add_argument("case", type=Path)

    s = sub.add_parser("reproduce", help="run a reproduction adapter")
    s.add_argument("case", type=Path)
    s.add_argument("--adapter", default="mock")

    s = sub.add_parser("validate", help="validate structure, schemas, refs and verification claims")
    s.add_argument("case", type=Path)

    s = sub.add_parser("package", help="zip a case bundle")
    s.add_argument("case", type=Path)
    s.add_argument("--output", type=Path)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            case = init_case(args.video, args.cases_dir, args.slug)
            print(case)
        elif args.command == "trace":
            trace_case(args.case.resolve(), args.interval, not args.no_audio)
            print("trace complete")
        elif args.command == "reverse":
            reverse_case(args.case.resolve(), args.input_json)
            print("reverse scaffold complete")
        elif args.command == "assemble":
            assemble_case(args.case.resolve())
            print("assemble complete")
        elif args.command == "reproduce":
            reproduce_case(args.case.resolve(), args.adapter)
            print("reproduction run recorded")
        elif args.command == "validate":
            errors = validate_case(args.case.resolve())
            if errors:
                for e in errors:
                    print(f"ERROR: {e}", file=sys.stderr)
                return 1
            print("validation passed")
        elif args.command == "package":
            print(package_case(args.case.resolve(), args.output))
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
