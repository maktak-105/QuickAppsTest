"""Attach Playwright to a running WebView2 via CDP."""

from __future__ import annotations

import json
import socket
import time
from typing import Any, Mapping

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from ..errors import BridgeTimeout, LaunchError
from ..protocol import HISTORY_LEN_JS, INSTALL_HOOK_JS, compact_dumps


def wrap_eval_js(script: str) -> str:
    src = script.strip()
    if src.startswith("return "):
        return f"() => {{ {src} }}"
    return src


def find_free_port(start: int = 9222, max_port: int = 65535) -> int:
    for port in range(start, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError("no free CDP port")


class PlaywrightBackend:
    def __init__(
        self,
        *,
        playwright: Playwright,
        browser: Browser,
        page: Page,
        wire: str,
    ) -> None:
        self._playwright = playwright
        self.browser = browser
        self.page = page
        self.wire = wire

    @property
    def context(self) -> BrowserContext:
        return self.page.context

    def history_len(self) -> int:
        try:
            value = self.page.evaluate(HISTORY_LEN_JS)
        except Exception:
            return 0
        return int(value or 0)

    def history_from(self, since: int) -> list[Any]:
        raw = self.page.evaluate(
            "(since) => (window.__qa && window.__qa.history) ? window.__qa.history.slice(since) : []",
            since,
        )
        return list(raw or [])

    def post_message(self, payload: Mapping[str, Any]) -> None:
        compact = compact_dumps(payload)
        if self.wire == "object":
            self.page.evaluate("m => window.chrome.webview.postMessage(m)", json.loads(compact))
            return
        if self.wire == "string":
            self.page.evaluate("s => window.chrome.webview.postMessage(s)", compact)
            return
        raise ValueError(f"unknown webmessage wire: {self.wire}")

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def locator_count(self, selector: str) -> int:
        return self.page.locator(selector).count()

    def locator_enabled(self, selector: str) -> bool:
        loc = self.page.locator(selector)
        if loc.count() < 1:
            return False
        return bool(loc.first.is_enabled())

    def class_has(self, selector: str, class_name: str) -> bool:
        return bool(
            self.page.evaluate(
                """([sel, cls]) => {
                    const el = document.querySelector(sel);
                    return !!(el && el.classList.contains(cls));
                }""",
                [selector, class_name],
            )
        )

    def eval_js(self, script: str) -> Any:
        return self.page.evaluate(wrap_eval_js(script))

    def close(self) -> None:
        try:
            self.browser.close()
        except Exception:
            pass
        try:
            self._playwright.stop()
        except Exception:
            pass


def attach(
    *,
    cdp_port: int,
    wire: str,
    hook_timeout_s: float,
    ready_locator: str | None,
) -> PlaywrightBackend:
    playwright = sync_playwright().start()
    try:
        browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{cdp_port}")
    except Exception as exc:
        playwright.stop()
        raise BridgeTimeout(f"connect_over_cdp failed on port {cdp_port}: {exc}") from exc

    deadline = time.monotonic() + hook_timeout_s
    page: Page | None = None
    while time.monotonic() < deadline:
        if browser.contexts:
            pages = browser.contexts[0].pages
            if pages:
                page = pages[0]
                try:
                    hooked = page.evaluate(INSTALL_HOOK_JS)
                except Exception:
                    hooked = False
                if hooked:
                    break
        time.sleep(1.0)
    else:
        try:
            browser.close()
        except Exception:
            pass
        playwright.stop()
        raise BridgeTimeout("contexts/pages empty or hook not installed")

    assert page is not None
    backend = PlaywrightBackend(playwright=playwright, browser=browser, page=page, wire=wire)
    if ready_locator and backend.locator_count(ready_locator) < 1:
        backend.close()
        raise LaunchError(f"unbundled HTML (missing {ready_locator})")
    return backend
