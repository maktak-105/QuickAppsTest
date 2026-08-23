"""Native Win32 attach via pywinauto. DiskBench window title in v1; no ImageView."""

from __future__ import annotations

import re

from pywinauto import Application
from pywinauto.base_wrapper import BaseWrapper

from ..errors import LaunchError


def title_matches(window_text: str | None, pattern: str) -> bool:
    """True if Win32 window_text matches pattern. HTML <title> is a different string."""
    if window_text is None:
        return False
    return re.search(pattern, window_text) is not None


class PywinautoBackend:
    def __init__(self, app: Application, window: BaseWrapper) -> None:
        self.app = app
        self.window = window

    @property
    def handle(self) -> int:
        return int(self.window.handle)

    def window_text(self) -> str:
        return str(self.window.window_text() or "")

    def title_matches(self, pattern: str) -> bool:
        return title_matches(self.window_text(), pattern)

    def menu_select(self, path: str) -> None:
        """Win32 menu_select only. Do not SendMessage(WM_COMMAND)."""
        self.window.menu_select(path)


def attach(*, pid: int, window_class: str, timeout_s: float = 10.0) -> PywinautoBackend:
    if not window_class:
        raise LaunchError("pywinauto backend requires window_class")
    try:
        app = Application(backend="win32").connect(process=pid, timeout=timeout_s)
        window = app.window(class_name=window_class)
        window.wait("visible", timeout=timeout_s)
    except Exception as exc:
        raise LaunchError(f"pywinauto connect failed class={window_class!r} pid={pid}: {exc}") from exc
    return PywinautoBackend(app, window)
