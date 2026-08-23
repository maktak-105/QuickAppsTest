from pathlib import Path

import pytest

from quickappstest.errors import SpecError
from quickappstest.spec import infer_via, load_spec

SPEC = Path(__file__).resolve().parents[1] / "examples" / "QuickDiskBench" / "spec.yaml"


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


def test_infer_via() -> None:
    assert infer_via({"id": "a", "locator": "#btn-lang"}) == "playwright"
    assert infer_via({"id": "b", "title_re": "Native"}) == "pywinauto"
    assert infer_via({"id": "c", "accessibility_name": "QuickDiskBench"}) == "appium"


def test_bad_version(tmp_path: Path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text("version: 2\napp: {name: X}\nchecks: [{id: a, locator: '#x'}]\n", encoding="utf-8")
    with pytest.raises(SpecError, match="version"):
        load_spec(path)
