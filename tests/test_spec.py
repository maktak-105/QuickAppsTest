from pathlib import Path

import pytest

from quickappstest.errors import SpecError
from quickappstest.spec import infer_via, load_spec

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "examples" / "QuickDiskBench" / "spec.yaml"
FOLDERSIZE_SPEC = ROOT / "examples" / "QuickFolderSize" / "spec.yaml"


def test_load_diskbench_spec() -> None:
    spec = load_spec(SPEC)
    assert spec.app.name == "QuickDiskBench"
    assert spec.app.wire == "object"
    assert spec.app.heartbeat is not None
    assert spec.app.heartbeat.post == {"action": "get_drives"}
    ids = [c.id for c in spec.checks]
    assert "structural.lang_button" in ids
    assert "native.window_title" in ids
    assert "ax.window_name" in ids
    by_id = {c.id: c for c in spec.checks}
    assert by_id["structural.lang_button"].via == "playwright"
    assert by_id["native.window_title"].via == "pywinauto"
    assert by_id["ax.window_name"].via == "appium"
    assert by_id["structural.start_button"].expect[0]["exists"] is True


def test_load_foldersize_spec() -> None:
    spec = load_spec(FOLDERSIZE_SPEC)
    assert spec.app.name == "QuickFolderSize"
    assert spec.app.requires_elevation is True
    assert spec.app.heartbeat is not None
    assert spec.app.heartbeat.post == {"cmd": "get_drives"}
    by_id = {c.id: c for c in spec.checks}
    assert by_id["structural.scan_button"].via == "playwright"
    assert by_id["protocol.get_drives"].steps[0]["post_message"] == {"cmd": "get_drives"}


def test_infer_via() -> None:
    assert infer_via({"id": "a", "locator": "#btn-lang"}) == "playwright"
    assert infer_via({"id": "b", "title_re": "Native"}) == "pywinauto"
    assert infer_via({"id": "c", "accessibility_name": "QuickDiskBench"}) == "appium"


def test_eval_js_wraps_return_statement() -> None:
    from quickappstest.backends.playwright_backend import wrap_eval_js

    src = "return document.querySelector('#btn-start [data-i18n=btn_start]').textContent"
    assert wrap_eval_js(src).startswith("() => {")
    assert wrap_eval_js("1 + 1") == "1 + 1"


def test_bad_version(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("version: 2\napp: {name: X}\nchecks: [{id: a, locator: '#x'}]\n", encoding="utf-8")
    with pytest.raises(SpecError, match="version"):
        load_spec(path)
