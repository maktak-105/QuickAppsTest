"""Load and validate the YAML spec. Schema is the source of truth for the runner."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .errors import SpecError

KNOWN_VIA = {"playwright", "pywinauto", "appium"}
STEP_KEYS = {
    "click",
    "eval_js",
    "sleep",
    "post_message",
    "wait_message",
    "menu_select",
    "dialog_appeared",
    "key",
}


@dataclass
class HeartbeatSpec:
    post: dict[str, Any]
    expect_type: str | None = None
    timeout_s: float = 15.0


@dataclass
class AppSpec:
    name: str
    window_class: str | None = None
    user_data_marker: str | None = None
    title_re: str | None = None
    backends: list[str] = field(default_factory=lambda: ["playwright", "pywinauto", "appium"])
    requires_elevation: bool = False
    extra_args: list[str] = field(default_factory=list)
    wire: str = "object"
    heartbeat: HeartbeatSpec | None = None
    attach_grace_s: float = 2.5
    hook_timeout_s: float = 15.0
    ready_locator: str | None = None


@dataclass
class CheckSpec:
    id: str
    category: str
    via: str
    desc: str
    locator: str | None = None
    title_re: str | None = None
    class_name: str | None = None
    accessibility_name: str | None = None
    dump_tree: bool = False
    steps: list[dict[str, Any]] = field(default_factory=list)
    expect: list[dict[str, Any]] = field(default_factory=list)
    teardown: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Spec:
    version: int
    app: AppSpec
    checks: list[CheckSpec]
    path: Path


def infer_via(raw: dict[str, Any]) -> str:
    if raw.get("via"):
        return str(raw["via"])
    if raw.get("locator") or raw.get("eval_js") or raw.get("post") or raw.get("expect_type"):
        return "playwright"
    steps = raw.get("steps") or []
    for step in steps:
        if not isinstance(step, dict):
            continue
        if "click" in step or "eval_js" in step or "post_message" in step or "wait_message" in step:
            return "playwright"
        if "menu_select" in step or "dialog_appeared" in step:
            return "pywinauto"
    if raw.get("title_re") or raw.get("class_name"):
        return "pywinauto"
    if raw.get("accessibility_name") or raw.get("automation_id") or raw.get("dump_tree"):
        return "appium"
    expect = raw.get("expect")
    if isinstance(expect, dict) and (
        "class_contains" in expect or "class_not_contains" in expect or "exists" in expect
    ):
        return "playwright"
    raise SpecError(f"cannot infer via for check {raw.get('id')!r}")


def _normalize_expect(raw: Any, locator: str | None) -> list[dict[str, Any]]:
    if raw is None:
        if locator:
            return [{"exists": True}]
        return []
    if isinstance(raw, dict):
        return [raw]
    if isinstance(raw, list):
        return [item if isinstance(item, dict) else {"value": item} for item in raw]
    raise SpecError("expect must be a map or a list")


def _normalize_steps(raw: Any) -> list[dict[str, Any]]:
    if not raw:
        return []
    if not isinstance(raw, list):
        raise SpecError("steps must be a list")
    out: list[dict[str, Any]] = []
    for step in raw:
        if not isinstance(step, dict):
            raise SpecError(f"step must be a map: {step!r}")
        keys = [k for k in step if k in STEP_KEYS]
        if len(keys) != 1:
            raise SpecError(f"step needs exactly one action key, got {list(step)}")
        out.append(step)
    return out


def load_spec(path: str | Path) -> Spec:
    spec_path = Path(path)
    if not spec_path.is_file():
        raise SpecError(f"spec not found: {spec_path}")
    data = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SpecError("spec root must be a map")
    if data.get("version") != 1:
        raise SpecError("spec version must be 1")
    app_raw = data.get("app")
    if not isinstance(app_raw, dict) or not app_raw.get("name"):
        raise SpecError("app.name is required")
    checks_raw = data.get("checks")
    if not isinstance(checks_raw, list) or not checks_raw:
        raise SpecError("checks must be a non-empty list")

    webmessage = app_raw.get("webmessage") or {}
    hb_raw = app_raw.get("heartbeat")
    heartbeat = None
    if isinstance(hb_raw, dict):
        post = hb_raw.get("post")
        if not isinstance(post, dict):
            raise SpecError("heartbeat.post must be a map")
        heartbeat = HeartbeatSpec(
            post=post,
            expect_type=hb_raw.get("expect_type"),
            timeout_s=float(hb_raw.get("timeout_s") or 15),
        )

    backends = list(app_raw.get("backends") or ["playwright", "pywinauto", "appium"])
    app = AppSpec(
        name=str(app_raw["name"]),
        window_class=app_raw.get("window_class"),
        user_data_marker=app_raw.get("user_data_marker"),
        title_re=app_raw.get("title_re"),
        backends=backends,
        requires_elevation=bool(app_raw.get("requires_elevation", False)),
        extra_args=[str(x) for x in (app_raw.get("extra_args") or [])],
        wire=str(webmessage.get("wire") or "object"),
        heartbeat=heartbeat,
        attach_grace_s=float(app_raw.get("attach_grace_s") or 2.5),
        hook_timeout_s=float(app_raw.get("hook_timeout_s") or 15),
        ready_locator=app_raw.get("ready_locator"),
    )

    checks: list[CheckSpec] = []
    seen: set[str] = set()
    for raw in checks_raw:
        if not isinstance(raw, dict) or not raw.get("id"):
            raise SpecError("each check needs an id")
        cid = str(raw["id"])
        if cid in seen:
            raise SpecError(f"duplicate check id: {cid}")
        seen.add(cid)
        locator = raw.get("locator")
        via = infer_via(raw)
        checks.append(
            CheckSpec(
                id=cid,
                category=str(raw.get("category") or "structural"),
                via=via,
                desc=str(raw.get("desc") or cid),
                locator=locator,
                title_re=raw.get("title_re"),
                class_name=raw.get("class_name"),
                accessibility_name=raw.get("accessibility_name"),
                dump_tree=bool(raw.get("dump_tree", False)),
                steps=_normalize_steps(raw.get("steps")),
                expect=_normalize_expect(raw.get("expect"), locator),
                teardown=_normalize_steps(raw.get("teardown")),
            )
        )
    return Spec(version=1, app=app, checks=checks, path=spec_path)
