# QuickAppsTest — development environment

[日本語版 environment_jp.md](environment_jp.md)

## Prerequisites

- Windows 10 / 11 64-bit (live GUI tests)
- Python 3.11 or later
- Git
- WebView2 Runtime for live DiskBench (Playwright `connect_over_cdp`)
- Optional: Node.js LTS + Appium 2 (`appium driver install windows`) for accessibility checks

`playwright install` is **not** required for live WebView2 tests. CDP talks to the installed WebView2 Runtime. Do not download Chromium for DiskBench.

## Install

```powershell
cd f:\project\QuickAppsTest
python -m venv .venv
.\.venv\Scripts\pip install -e .[dev]
python run_tests.py
```

`python run_tests.py` is `pytest tests -m "not live"`. It must pass without a Quick EXE.

## Live DiskBench

Build the app first (`python build_native.py` in `QuickDiskBench`). The tester needs **both**:

- `dist/binary/QuickDiskBench.exe`
- bundled `dist/binary/index.html` next to the EXE

`templates/index.html` is not a live target (`NavigateToString` cannot load relative `app.js`).

```powershell
python -m quickappstest --spec examples/QuickDiskBench/spec.yaml --exe F:\project\QuickDiskBench\dist\binary\QuickDiskBench.exe --report-dir qa_reports
```

Launch uses `subprocess.Popen([exe, *args], cwd=None)` with no extra quotes around paths. Env always includes `QUICKAPPSTEST=1`. Playwright apps also get `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=N --remote-allow-origins=*`.

Do not click `#btn-start`. Do not post an `action` value containing the substring `start`.

Set `QUICKAPPSTEST_REF_EXE` for `pytest tests/live -m live`.

## Appium (optional)

Operator starts **Appium 2 only** on `http://127.0.0.1:4723` (no `/wd/hub`). The windows driver starts WinAppDriver as a child on `systemPort` **4724**. Do not listen WinAppDriver on 4723 yourself.

Client: `Appium-Python-Client>=3.0` `WindowsOptions`, `app_top_level_window` = 8-digit uppercase hex HWND **without** `0x`. Developer Mode is often required. If 4723 is closed, Appium checks are SKIP. Playwright/pywinauto still pass.

## Elevation

QuickFolderSize keeps `requireAdministrator` (MFT). Live runs of that app require an already elevated test process. The library probes `TokenElevation` / `IsUserAnAdmin` **before** `Popen`. It does not `ShellExecute runas` the EXE (that would change the PID). DiskBench does not need elevation.

## Layout

Package code is `python/quickappstest/`. `pyproject.toml` sets `package-dir = {"" = "python"}`. Do not linguist-vendor `python/**`.

## GitHub

PRs from `agent/*` into `main`. Do not push to `main` directly. CI on `windows-latest` runs `python run_tests.py` only (no live EXE).

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `pip` cannot find `quickappstest` | `package-dir` and `pip install -e .` |
| LaunchError unbundled HTML | missing bundled `index.html` beside the EXE |
| BridgeTimeout | leftover WebView2 holding `QuickDiskBench_WVData2`; library kills by marker only, never `taskkill /IM msedgewebview2.exe` |
| FolderSize attach sees a dead PID | run the test process as Administrator; do not auto-click UAC |
| Appium always skip | expected if 4723 is closed |
| `#btn-start` / `action:start` | forbidden; host `find(L"start")` can mis-fire |
