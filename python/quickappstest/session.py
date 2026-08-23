"""Session facade. Backends are wired in later PRs."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from .errors import BackendUnavailable


class Session:
    proc: Any
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
        webmessage_wire: str = "object",
        requires_elevation: bool = False,
        attach_grace_s: float = 2.5,
        hook_timeout_s: float = 15.0,
        retries: int = 3,
    ) -> Session:
        """Start a target EXE and attach backends.

        Not implemented in PR1. Signature is fixed so later PRs can fill it in.
        """
        del (
            exe,
            backends,
            user_data_marker,
            window_class,
            window_title_re,
            cdp_port,
            extra_args,
            env,
            heartbeat,
            webmessage_wire,
            requires_elevation,
            attach_grace_s,
            hook_timeout_s,
            retries,
        )
        raise BackendUnavailable("Session.launch is not implemented yet; backends land in later PRs")

    def history_len(self) -> int:
        raise BackendUnavailable("Playwright backend is not implemented yet")

    def post_message(self, payload: Mapping[str, Any]) -> None:
        del payload
        raise BackendUnavailable("Playwright backend is not implemented yet")

    def wait_message(
        self,
        predicate: Callable[[Any], bool],
        *,
        since: int | None = None,
        timeout_s: float = 10.0,
        interval_s: float = 1.0,
    ) -> Any:
        del predicate, since, timeout_s, interval_s
        raise BackendUnavailable("Playwright backend is not implemented yet")

    def close(self) -> None:
        """No-op until backends exist."""
