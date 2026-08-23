from pathlib import Path

from quickappstest.cli import main
from quickappstest.runner import CheckResult, _run_check
from quickappstest.session import Session
from quickappstest.spec import CheckSpec


def test_unknown_via_is_skip() -> None:
    session = Session()
    check = CheckSpec(id="x", category="structural", via="unknown", desc="nope")
    result = _run_check(session, check, backends=["playwright"], report_dir=None, screenshot_on_fail=False)
    assert result.status == "skip"


def test_appium_missing_is_skip() -> None:
    session = Session()
    session.appium = None
    check = CheckSpec(
        id="ax.window_name",
        category="structural",
        via="appium",
        desc="name",
        accessibility_name="QuickDiskBench",
    )
    result = _run_check(
        session,
        check,
        backends=["playwright", "pywinauto", "appium"],
        report_dir=None,
        screenshot_on_fail=False,
    )
    assert result.status == "skip"


def test_cli_missing_exe_exits_2(tmp_path: Path) -> None:
    spec = Path(__file__).resolve().parents[1] / "examples" / "QuickDiskBench" / "spec.yaml"
    code = main(
        [
            "--spec",
            str(spec),
            "--exe",
            str(tmp_path / "missing.exe"),
            "--report-dir",
            str(tmp_path / "out"),
        ]
    )
    assert code == 2
    assert (tmp_path / "out" / "results.json").is_file()


def test_check_result_fields() -> None:
    row = CheckResult("id", "playwright", "pass", "ok")
    assert row.status == "pass"
