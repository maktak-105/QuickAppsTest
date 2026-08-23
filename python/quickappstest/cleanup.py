"""Kill the target EXE and only the WebView2 processes that hold its user-data dir."""

from __future__ import annotations

import subprocess

FORBIDDEN_EXE_NAMES = {"msedgewebview2.exe", "msedgewebview2"}


def command_line_matches(command_line: str | None, marker: str) -> bool:
    if not marker:
        raise ValueError("user-data marker must not be empty")
    if not command_line:
        return False
    return marker in command_line


def kill_exe_by_name(name: str) -> None:
    """taskkill the app EXE only. Never pass msedgewebview2.exe."""
    base = name.lower().rsplit("\\", 1)[-1]
    if base in FORBIDDEN_EXE_NAMES:
        raise ValueError("refusing to kill msedgewebview2.exe by name")
    subprocess.run(
        ["taskkill", "/F", "/IM", name],
        capture_output=True,
        text=True,
        check=False,
    )


def kill_webview2_by_user_data_marker(marker: str) -> None:
    """Stop msedgewebview2.exe whose command line contains *marker*."""
    if not marker:
        raise ValueError("user-data marker must not be empty")
    # Escape regex metacharacters so PowerShell -match is literal.
    escaped = (
        marker.replace("\\", "\\\\")
        .replace(".", "\\.")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("+", "\\+")
        .replace("*", "\\*")
        .replace("?", "\\?")
        .replace("^", "\\^")
        .replace("$", "\\$")
        .replace("|", "\\|")
    )
    script = (
        "Get-CimInstance Win32_Process -Filter \"Name='msedgewebview2.exe'\" | "
        f"Where-Object {{ $_.CommandLine -match '{escaped}' }} | "
        "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        text=True,
        check=False,
    )
