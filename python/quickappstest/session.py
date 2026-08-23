"""Session facade. PR2 wires Playwright; pywinauto/Appium stay None."""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from . import cleanup
from .adapters.webmessage import as_payload, type_equals
from .backends import playwright_backend, pywinauto_backend
from .errors import BackendUnavailable, LaunchError
from .protocol import wait_for_new


def _is_elevated() -> bool:
    try:
        import ctypes

        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


class Session:
    proc: subprocess.Popen[bytes] | None
    playwright: Any
    pywinauto: Any
    appium: Any
    cdp_port: int | None
    user_data_marker: str | None
    webmessage_wire: str

    def __init__(self) -> None:
        self.proc = None
        self.playwright = None
        self.pywinauto = None
        self.appium = None
        self.cdp_port = None
        self.user_data_marker = None
        self.webmessage_wire = "object"

    @classmethod
    def launch(
        cls,
        exe: str | Path,
        *,
        backends: Sequence[str] = ("playwright", "pywinauto", "appium"),
        user_data_marker: str | None = None,
        window_class: str | None = None,
        window_title_re: str | None = None,
        cdp_port: int | None = None,
        extra_args: list[str] | None = None,
        env: Mapping[str, str] | None = None,
        heartbeat: Mapping[str, Any] | None = None,
        heartbeat_expect_type: str | None = None,
        webmessage_wire: str = "object",
        requires_elevation: bool = False,
        attach_grace_s: float = 2.5,
        hook_timeout_s: float = 15.0,
        retries: int = 3,
        ready_locator: str | None = None,
    ) -> Session:
        exe_path = Path(exe)
        if not exe_path.is_file():
            raise LaunchError(f"exe not found: {exe_path}")
        if requires_elevation and not _is_elevated():
            raise LaunchError("requires_elevation: re-run the test process as Administrator")

        last_error: BaseException | None = None
        attempts = max(1, retries)
        for _ in range(attempts):
            session = cls()
            try:
                session._launch_once(
                    exe_path=exe_path,
                    backends=backends,
                    user_data_marker=user_data_marker,
                    window_class=window_class,
                    window_title_re=window_title_re,
                    cdp_port=cdp_port,
                    extra_args=list(extra_args or []),
                    env=dict(env or {}),
                    heartbeat=heartbeat,
                    heartbeat_expect_type=heartbeat_expect_type,
                    webmessage_wire=webmessage_wire,
                    attach_grace_s=attach_grace_s,
                    hook_timeout_s=hook_timeout_s,
                    ready_locator=ready_locator,
                )
                return session
            except Exception as exc:
                last_error = exc
                session.close()
        assert last_error is not None
        raise last_error

    def _launch_once(
        self,
        *,
        exe_path: Path,
        backends: Sequence[str],
        user_data_marker: str | None,
        window_class: str | None,
        window_title_re: str | None,
        cdp_port: int | None,
        extra_args: list[str],
        env: dict[str, str],
        heartbeat: Mapping[str, Any] | None,
        heartbeat_expect_type: str | None,
        webmessage_wire: str,
        attach_grace_s: float,
        hook_timeout_s: float,
        ready_locator: str | None,
    ) -> None:
        self.webmessage_wire = webmessage_wire
        self.user_data_marker = user_data_marker
        cleanup.kill_exe_by_name(exe_path.name)
        if user_data_marker:
            cleanup.kill_webview2_by_user_data_marker(user_data_marker)
        time.sleep(0.5)

        merged = dict(os.environ)
        merged.update(env)
        merged["QUICKAPPSTEST"] = "1"
        want_playwright = "playwright" in backends
        port = None
        if want_playwright:
            port = cdp_port or playwright_backend.find_free_port(9222)
            merged["WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS"] = (
                f"--remote-debugging-port={port} --remote-allow-origins=*"
            )
        self.cdp_port = port

        args = [str(exe_path), *[str(a) for a in extra_args]]
        self.proc = subprocess.Popen(args, env=merged, cwd=None)
        time.sleep(attach_grace_s)

        if want_playwright:
            assert port is not None
            self.playwright = playwright_backend.attach(
                cdp_port=port,
                wire=webmessage_wire,
                hook_timeout_s=hook_timeout_s,
                ready_locator=ready_locator,
            )
            if heartbeat is not None:
                cursor = self.history_len()
                self.post_message(as_payload(heartbeat))
                predicate = (
                    type_equals(heartbeat_expect_type)
                    if heartbeat_expect_type
                    else (lambda _m: True)
                )
                self.wait_message(predicate, since=cursor, timeout_s=max(3.0, hook_timeout_s))

        if "pywinauto" in backends:
            if self.proc is None or self.proc.pid is None:
                raise LaunchError("pywinauto attach needs a running process")
            self.pywinauto = pywinauto_backend.attach(
                pid=self.proc.pid,
                window_class=window_class or "",
            )
            if window_title_re and not self.pywinauto.title_matches(window_title_re):
                raise LaunchError(
                    f"Win32 title {self.pywinauto.window_text()!r} does not match {window_title_re!r}"
                )
        if "appium" in backends:
            self.appium = None

    def history_len(self) -> int:
        if self.playwright is None:
            return 0
        return int(self.playwright.history_len())

    def post_message(self, payload: Mapping[str, Any]) -> None:
        if self.playwright is None:
            raise BackendUnavailable("Playwright backend is not attached")
        self.playwright.post_message(payload)

    def wait_message(
        self,
        predicate: Callable[[Any], bool],
        *,
        since: int | None = None,
        timeout_s: float = 10.0,
        interval_s: float = 1.0,
    ) -> Any:
        if self.playwright is None:
            raise BackendUnavailable("Playwright backend is not attached")
        cursor = self.history_len() if since is None else since
        return wait_for_new(
            lambda: self.playwright.history_from(0),
            predicate,
            since=cursor,
            timeout_s=timeout_s,
            interval_s=interval_s,
        )

    def close(self) -> None:
        if self.playwright is not None:
            try:
                self.playwright.close()
            except Exception:
                pass
            self.playwright = None
        if self.proc is not None and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except Exception:
                self.proc.kill()
        self.proc = None
        if self.user_data_marker:
            try:
                cleanup.kill_webview2_by_user_data_marker(self.user_data_marker)
            except Exception:
                pass

    def __enter__(self) -> Session:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
