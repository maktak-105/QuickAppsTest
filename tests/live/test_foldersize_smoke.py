"""Live smoke against QuickFolderSize.exe. Skips without EXE or elevation."""

from __future__ import annotations

import ctypes
import os
from pathlib import Path

import pytest

from quickappstest import Session

pytestmark = pytest.mark.live

DEFAULT_EXE = Path(r"F:\project\QuickFolderSize\dist\binary\QuickFolderSize.exe")


def _exe() -> Path:
    raw = os.environ.get("QUICKAPPSTEST_FOLDERSIZE_EXE") or os.environ.get("QUICKAPPSTEST_REF_EXE")
    path = Path(raw) if raw else DEFAULT_EXE
    if not path.is_file():
        pytest.skip(f"built EXE not found: {path}")
    if not (path.parent / "index.html").is_file():
        pytest.skip(f"bundled index.html missing next to {path}")
    try:
        elevated = bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        elevated = False
    if not elevated:
        pytest.skip("FolderSize live requires an elevated test process")
    return path


def test_lang_button_and_cmd_get_drives() -> None:
    exe = _exe()
    with Session.launch(
        exe,
        backends=("playwright", "pywinauto"),
        user_data_marker="QuickFolderSize_WVData",
        window_class="QuickFolderSizeNativeWebView2Class",
        window_title_re="QuickFolderSize",
        webmessage_wire="object",
        heartbeat={"cmd": "get_drives"},
        heartbeat_expect_type="drives",
        requires_elevation=True,
        ready_locator="#btn-lang",
    ) as session:
        assert session.playwright.locator_count("#btn-scan") >= 1
        cursor = session.history_len()
        session.post_message({"cmd": "get_drives"})
        message = session.wait_message(
            lambda m: isinstance(m, dict) and m.get("type") == "drives",
            since=cursor,
            timeout_s=10,
        )
        assert message.get("type") == "drives"
