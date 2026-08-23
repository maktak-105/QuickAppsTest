"""JSON and HTML reports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_reports(report_dir: Path, payload: dict[str, Any]) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "artifacts").mkdir(exist_ok=True)
    (report_dir / "results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    rows = []
    for check in payload.get("checks") or []:
        status = check.get("status")
        color = {"pass": "#cfc", "fail": "#fcc", "skip": "#ffc"}.get(status, "#eee")
        rows.append(
            "<tr style='background:{color}'><td>{id}</td><td>{via}</td>"
            "<td>{status}</td><td>{detail}</td></tr>".format(
                color=color,
                id=_esc(check.get("id")),
                via=_esc(check.get("via")),
                status=_esc(status),
                detail=_esc(check.get("detail")),
            )
        )
    html = (
        "<!doctype html><meta charset='utf-8'><title>QuickAppsTest</title>"
        "<h1>QuickAppsTest</h1>"
        f"<p>{_esc(payload.get('app'))} — {_esc(payload.get('summary'))}</p>"
        "<table border='1' cellpadding='6' cellspacing='0'>"
        "<tr><th>id</th><th>via</th><th>status</th><th>detail</th></tr>"
        + "".join(rows)
        + "</table>"
    )
    (report_dir / "report.html").write_text(html, encoding="utf-8")


def _esc(value: Any) -> str:
    text = "" if value is None else str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
