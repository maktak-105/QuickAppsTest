"""Live smoke against a built QuickDiskBench.exe. Skips without QUICKAPPSTEST_REF_EXE."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from quickappstest import Session

pytestmark = pytest.mark.live

DEFAULT_EXE = Path(r"F:\project\QuickDiskBench\dist\binary\QuickDiskBench.exe")


def _exe() -> Path:
    raw = os.environ.get("QUICKAPPSTEST_REF_EXE")
    path = Path(raw) if raw else DEFAULT_EXE
    if not path.is_file():
        pytest.skip(f"built EXE not found: {path}")
    sidecar = path.parent / "index.html"
    if not sidecar.is_file():
        pytest.skip(f"bundled index.html missing next to {path}")
    return path


def test_lang_button_and_second_get_drives() -> None:
    exe = _exe()
    with Session.launch(
        exe,
        backends=("playwright", "pywinauto", "appium"),
        user_data_marker="QuickDiskBench_WVData2",
        window_class="QuickDiskBenchNativeWebView2Class",
        window_title_re="Native Storage Benchmark",
        webmessage_wire="object",
        heartbeat={"action": "get_drives"},
        heartbeat_expect_type="drives",
        ready_locator="#btn-lang",
    ) as session:
        assert session.playwright.locator_count("#btn-lang") >= 1
        assert session.playwright.locator_count("#btn-start") >= 1
        cursor = session.history_len()
        session.post_message({"action": "get_drives"})
        message = session.wait_message(
            lambda m: isinstance(m, dict) and m.get("type") == "drives",
            since=cursor,
            timeout_s=10,
        )
        assert message.get("type") == "drives"
        assert session.pywinauto is not None
        assert session.pywinauto.title_matches("Native Storage Benchmark")
        html_title = session.playwright.page.title()
        assert "Native Storage Benchmark" not in html_title
        if session.appium is not None:
            assert session.appium.name_contains("QuickDiskBench")
