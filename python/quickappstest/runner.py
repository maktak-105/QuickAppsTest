"""Run one spec against one Session."""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .adapters.webmessage import type_equals
from .backends import appium_backend
from .errors import BackendUnavailable, BridgeTimeout, LaunchError, SpecError
from .session import Session
from .spec import CheckSpec, Spec


@dataclass
class CheckResult:
    id: str
    via: str
    status: str
    detail: str


def run_spec(
    spec: Spec,
    *,
    exe: Path,
    extra_args: list[str] | None = None,
    skip_appium: bool = False,
    cdp_port: int | None = None,
    report_dir: Path | None = None,
    screenshot_on_fail: bool = False,
    trace: bool = False,
) -> tuple[int, list[CheckResult]]:
    backends = list(spec.app.backends)
    if skip_appium:
        backends = [b for b in backends if b != "appium"]

    args = list(spec.app.extra_args)
    if extra_args:
        args.extend(extra_args)

    heartbeat = spec.app.heartbeat.post if spec.app.heartbeat else None
    expect_type = spec.app.heartbeat.expect_type if spec.app.heartbeat else None
    ready = None
    if "playwright" in backends:
        ready = "#btn-lang" if spec.app.name == "QuickDiskBench" else None

    try:
        session = Session.launch(
            exe,
            backends=backends,
            user_data_marker=spec.app.user_data_marker,
            window_class=spec.app.window_class,
            window_title_re=spec.app.title_re if "pywinauto" in backends else None,
            cdp_port=cdp_port,
            extra_args=args,
            heartbeat=heartbeat,
            heartbeat_expect_type=expect_type,
            webmessage_wire=spec.app.wire,
            requires_elevation=spec.app.requires_elevation,
            attach_grace_s=spec.app.attach_grace_s,
            hook_timeout_s=spec.app.hook_timeout_s,
            ready_locator=ready,
        )
    except (LaunchError, BridgeTimeout, BackendUnavailable) as exc:
        return 2, [CheckResult("launch", "session", "fail", str(exc))]
    except Exception as exc:
        return 2, [CheckResult("launch", "session", "fail", repr(exc))]

    tracing = False
    if trace and session.playwright is not None:
        try:
            session.playwright.context.tracing.start(screenshots=True, snapshots=True)
            tracing = True
        except Exception:
            tracing = False

    results: list[CheckResult] = []
    try:
        for check in spec.checks:
            results.append(
                _run_check(
                    session,
                    check,
                    backends=backends,
                    report_dir=report_dir,
                    screenshot_on_fail=screenshot_on_fail,
                )
            )
    finally:
        if tracing and session.playwright is not None and report_dir is not None:
            try:
                report_dir.mkdir(parents=True, exist_ok=True)
                session.playwright.context.tracing.stop(path=str(report_dir / "trace.zip"))
            except Exception:
                pass
        session.close()

    if any(r.status == "fail" for r in results):
        return 1, results
    return 0, results


def _run_check(
    session: Session,
    check: CheckSpec,
    *,
    backends: list[str],
    report_dir: Path | None,
    screenshot_on_fail: bool,
) -> CheckResult:
    if check.via not in {"playwright", "pywinauto", "appium"}:
        return CheckResult(check.id, check.via, "skip", f"unknown via {check.via!r}")
    if check.via not in backends:
        return CheckResult(check.id, check.via, "skip", f"{check.via} not in backends")
    if check.via == "playwright" and session.playwright is None:
        return CheckResult(check.id, check.via, "skip", "playwright not attached")
    if check.via == "pywinauto" and session.pywinauto is None:
        return CheckResult(check.id, check.via, "skip", "pywinauto not attached")
    if check.via == "appium" and session.appium is None:
        return CheckResult(check.id, check.via, "skip", "appium server not available")

    saved: dict[str, Any] = {}
    last_cursor = 0
    try:
        last_cursor = _run_steps(session, check.steps, saved, last_cursor)
        _run_expect(session, check, saved)
        status = "pass"
        detail = check.desc
    except Exception as exc:
        status = "fail"
        detail = f"{check.desc}: {exc}"
        if screenshot_on_fail and session.playwright is not None and report_dir is not None:
            try:
                report_dir.joinpath("artifacts").mkdir(parents=True, exist_ok=True)
                session.playwright.page.screenshot(
                    path=str(report_dir / "artifacts" / f"{check.id}.png")
                )
            except Exception:
                pass
    teardown_error = None
    try:
        _run_steps(session, check.teardown, saved, last_cursor)
    except Exception as exc:
        teardown_error = exc
        status = "fail"
        detail = f"{detail}; teardown failed: {exc}"
    if teardown_error and status == "pass":
        status = "fail"
    if check.dump_tree and session.appium is not None and report_dir is not None:
        try:
            report_dir.joinpath("artifacts").mkdir(parents=True, exist_ok=True)
            (report_dir / "artifacts" / f"{check.id}.tree.xml").write_text(
                session.appium.dump_tree(), encoding="utf-8"
            )
        except Exception:
            pass
    return CheckResult(check.id, check.via, status, detail)


def _run_steps(
    session: Session,
    steps: list[dict[str, Any]],
    saved: dict[str, Any],
    last_cursor: int,
) -> int:
    cursor = last_cursor
    for step in steps:
        if "sleep" in step:
            time.sleep(float(step["sleep"]))
            continue
        if "click" in step:
            session.playwright.click(str(step["click"]))
            continue
        if "eval_js" in step:
            value = session.playwright.eval_js(str(step["eval_js"]))
            if step.get("save_as"):
                saved[str(step["save_as"])] = value
            continue
        if "post_message" in step:
            cursor = session.history_len()
            payload = step["post_message"]
            if not isinstance(payload, dict):
                raise SpecError("post_message must be a map")
            session.post_message(payload)
            continue
        if "wait_message" in step:
            wait = step["wait_message"]
            if not isinstance(wait, dict):
                raise SpecError("wait_message must be a map")
            since_raw = wait.get("since", "last")
            since = cursor if since_raw in (None, "last") else int(since_raw)
            expect_type = wait.get("type")
            predicate = type_equals(str(expect_type)) if expect_type else (lambda _m: True)
            session.wait_message(
                predicate,
                since=since,
                timeout_s=float(wait.get("timeout_s") or 10),
            )
            continue
        if "menu_select" in step:
            session.pywinauto.menu_select(str(step["menu_select"]))
            continue
        if "dialog_appeared" in step:
            raise SpecError("dialog_appeared is not used in v1 DiskBench checks")
        if "key" in step:
            raise SpecError("key step is not used in v1 DiskBench checks")
        raise SpecError(f"unknown step: {step}")
    return cursor


def _run_expect(session: Session, check: CheckSpec, saved: dict[str, Any]) -> None:
    locator = check.locator
    if check.via == "appium":
        if check.accessibility_name:
            appium_backend.reject_css_locator(check.accessibility_name)
            if not session.appium.name_contains(check.accessibility_name):
                raise AssertionError(
                    f"accessibility name does not contain {check.accessibility_name!r}"
                    f" (got {session.appium.window_name()!r})"
                )
        return
    if check.via == "pywinauto":
        pattern = check.title_re
        if pattern and not session.pywinauto.title_matches(pattern):
            raise AssertionError(
                f"Win32 title {session.pywinauto.window_text()!r} does not match {pattern!r}"
            )
        return

    pw = session.playwright
    for item in check.expect:
        if "exists" in item:
            sel = locator
            if sel is None:
                raise SpecError("exists expect needs locator")
            ok = pw.locator_count(sel) >= 1
            if bool(item["exists"]) != ok:
                raise AssertionError(f"exists={item['exists']} failed for {sel}")
        if "enabled" in item:
            sel = locator
            if sel is None:
                raise SpecError("enabled expect needs locator")
            if bool(item["enabled"]) != pw.locator_enabled(sel):
                raise AssertionError(f"enabled={item['enabled']} failed for {sel}")
        if "class_contains" in item:
            spec = item["class_contains"]
            if not pw.class_has(spec["selector"], spec["class"]):
                raise AssertionError(f"{spec['selector']} missing class {spec['class']}")
        if "class_not_contains" in item:
            spec = item["class_not_contains"]
            if pw.class_has(spec["selector"], spec["class"]):
                raise AssertionError(f"{spec['selector']} unexpectedly has class {spec['class']}")
        if "eval_js" in item:
            if not pw.eval_js(str(item["eval_js"])):
                raise AssertionError("eval_js expect was falsy")
        if "ne" in item:
            left, right = item["ne"]
            if saved.get(left) == saved.get(right):
                raise AssertionError(f"{left} == {right}: {saved.get(left)!r}")
        if "in" in item:
            name, allowed = item["in"]
            if saved.get(name) not in allowed:
                raise AssertionError(f"{name}={saved.get(name)!r} not in {allowed!r}")
