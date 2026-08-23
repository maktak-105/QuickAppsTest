import pytest

from quickappstest.cleanup import command_line_matches, kill_exe_by_name


def test_command_line_matches_user_data_marker() -> None:
    line = r"msedgewebview2.exe --user-data-dir=C:\Users\x\AppData\Local\Temp\QuickDiskBench_WVData2"
    assert command_line_matches(line, "QuickDiskBench_WVData2")
    assert not command_line_matches(line, "QuickFolderSize_WVData")


def test_empty_marker_rejected() -> None:
    with pytest.raises(ValueError):
        command_line_matches("anything", "")


def test_refuse_global_webview2_kill() -> None:
    with pytest.raises(ValueError, match="msedgewebview2"):
        kill_exe_by_name("msedgewebview2.exe")
