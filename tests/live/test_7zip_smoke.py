"""Live smoke against Quick7Zip.exe. HTML is embedded; no sidecar index.html."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from quickappstest import Session

pytestmark = pytest.mark.live

DEFAULT_EXE = Path(r"F:\project\Quick7Zip\dist\binary\Quick7Zip.exe")


def _exe() -> Path:
    raw = os.environ.get("QUICKAPPSTEST_7ZIP_EXE")
    path = Path(raw) if raw else DEFAULT_EXE
    if not path.is_file():
        pytest.skip(f"built EXE not found: {path}")
    return path


def test_language_button_and_initialize() -> None:
    exe = _exe()
    with Session.launch(
        exe,
        backends=("playwright", "pywinauto"),
        user_data_marker="Quick7Zip\\WebView2",
        window_class="Quick7ZipWindow",
        window_title_re="Quick7Zip",
        webmessage_wire="object",
        heartbeat={"type": "initialize"},
        heartbeat_expect_type="initialized",
        ready_locator="#languageButton",
    ) as session:
        assert session.playwright.locator_count("#languageButton") >= 1
        assert session.playwright.locator_count("#startButton") >= 1
        assert not session.playwright.locator_enabled("#startButton")
        cursor = session.history_len()
        session.post_message({"type": "initialize"})
        message = session.wait_message(
            lambda m: isinstance(m, dict) and m.get("type") == "initialized",
            since=cursor,
            timeout_s=10,
        )
        assert message.get("type") == "initialized"
