# QuickAppsTest — development environment

[日本語版 environment_jp.md](environment_jp.md)

## Prerequisites

- Windows 10 / 11 64-bit
- Python 3.11 or later
- Git
- For later live PRs: WebView2 Runtime (Playwright CDP), and optionally Node.js + Appium 2

`playwright install` is not required for live WebView2 tests (`connect_over_cdp` talks to the Runtime). It is only needed for the fake-HTML unit fixture in a later PR.

## Install

```powershell
cd f:\project\QuickAppsTest
python -m venv .venv
.\.venv\Scripts\pip install -e .[dev]
```

Import check (PR1 success condition):

```powershell
python -c "from quickappstest import Session, __version__; print(__version__, Session)"
```

`python -m pytest tests -m "not live"` must pass without an EXE. Live DiskBench: set `QUICKAPPSTEST_REF_EXE` to `dist/binary/QuickDiskBench.exe` with bundled `index.html` beside it.

## Layout

Python package code lives under `python/quickappstest/`. `pyproject.toml` sets `package-dir = {"" = "python"}`. Do not mark `python/**` as linguist-vendored.

## GitHub

Empty repo first, then PRs from `agent/*` into `main`. Do not push to `main` directly.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `pip` cannot find `quickappstest` | Confirm `package-dir` in `pyproject.toml` and that you used `pip install -e .` |
| `Session.launch` raises `BackendUnavailable` | Expected in PR1 |
