"""python -m quickappstest CLI."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .errors import SpecError
from .report import write_reports
from .runner import run_spec
from .spec import load_spec


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="quickappstest")
    parser.add_argument("--spec", required=True, help="YAML spec path")
    parser.add_argument("--exe", required=True, help="built EXE path")
    parser.add_argument("--extra-arg", action="append", default=[], dest="extra_args")
    parser.add_argument("--skip-appium", action="store_true")
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--report-dir", default="qa_reports")
    parser.add_argument("--cdp-port", type=int, default=None)
    parser.add_argument("--screenshot-on-fail", action="store_true")
    return parser


def _print(text: str) -> None:
    stream = sys.stdout
    try:
        stream.write(text + "\n")
    except UnicodeEncodeError:
        encoding = stream.encoding or "utf-8"
        stream.buffer.write((text + "\n").encode(encoding, errors="replace"))
        stream.buffer.flush()
        return
    stream.flush()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report_dir = Path(args.report_dir)
    try:
        spec = load_spec(args.spec)
    except SpecError as exc:
        sys.stderr.write(f"spec error: {exc}\n")
        return 2
    code, results = run_spec(
        spec,
        exe=Path(args.exe),
        extra_args=list(args.extra_args),
        skip_appium=bool(args.skip_appium),
        cdp_port=args.cdp_port,
        report_dir=report_dir,
        screenshot_on_fail=bool(args.screenshot_on_fail),
        trace=bool(args.trace),
    )
    payload = {
        "app": spec.app.name,
        "exe": str(Path(args.exe)),
        "exit_code": code,
        "summary": _summary(results, code),
        "checks": [
            {"id": r.id, "via": r.via, "status": r.status, "detail": r.detail} for r in results
        ],
    }
    write_reports(report_dir, payload)
    _print(payload["summary"])
    for row in payload["checks"]:
        _print(f"  [{row['status']}] {row['id']} ({row['via']}) {row['detail']}")
    return code


def _summary(results: list, code: int) -> str:
    counts = {"pass": 0, "fail": 0, "skip": 0}
    for row in results:
        counts[row.status] = counts.get(row.status, 0) + 1
    if code == 2:
        return f"launch failed  pass={counts['pass']} fail={counts['fail']} skip={counts['skip']}"
    return f"pass={counts['pass']} fail={counts['fail']} skip={counts['skip']}"


if __name__ == "__main__":
    raise SystemExit(main())
