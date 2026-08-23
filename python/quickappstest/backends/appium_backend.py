"""Optional Appium 2 attach by HWND. Missing server -> None, not a launch failure."""

from __future__ import annotations

import socket
from typing import Any

from ..errors import SpecError

APPIUM_URL = "http://127.0.0.1:4723"
PROBE_TIMEOUT_S = 1.0


def port_open(host: str, port: int, timeout_s: float = PROBE_TIMEOUT_S) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            return True
    except OSError:
        return False


def hwnd_to_capability(hwnd: int) -> str:
    """8-digit uppercase hex, no 0x prefix (WinAppDriver attach)."""
    return f"{int(hwnd):08X}"


def name_contains(actual: str | None, expected: str) -> bool:
    if actual is None:
        return False
    return expected in actual


def reject_css_locator(locator: str) -> None:
    stripped = locator.strip()
    if stripped.startswith("#") or stripped.startswith(".") or stripped.startswith("//"):
        raise SpecError(f"Appium must not receive HTML/CSS locators: {locator!r}")


def find_hwnd(window_class: str | None) -> int | None:
    if not window_class:
        return None
    import ctypes

    user32 = ctypes.windll.user32
    user32.FindWindowW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
    user32.FindWindowW.restype = ctypes.c_void_p
    handle = user32.FindWindowW(window_class, None)
    return int(handle) if handle else None


class AppiumBackend:
    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def dump_tree(self) -> str:
        return str(self.driver.page_source or "")

    def window_name(self) -> str:
        try:
            return str(self.driver.title or "")
        except Exception:
            return ""

    def name_contains(self, expected: str) -> bool:
        return name_contains(self.window_name(), expected)

    def close(self) -> None:
        try:
            self.driver.quit()
        except Exception:
            pass


def attach(*, hwnd: int | None) -> AppiumBackend | None:
    """Probe 4723 for 1s. If closed, return None. If open, createSession; failure is None."""
    if hwnd is None or hwnd == 0:
        return None
    if not port_open("127.0.0.1", 4723, PROBE_TIMEOUT_S):
        return None
    try:
        from appium import webdriver
        from appium.options.windows import WindowsOptions
    except Exception:
        return None

    opts = WindowsOptions()
    opts.platform_name = "Windows"
    opts.automation_name = "Windows"
    opts.app_top_level_window = hwnd_to_capability(hwnd)
    try:
        driver = webdriver.Remote(APPIUM_URL, options=opts)
    except Exception:
        return None
    return AppiumBackend(driver)
