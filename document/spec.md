# QuickAppsTest specification

[日本語版 spec_jp.md](spec_jp.md)

## 1. Overview

- **Name:** QuickAppsTest
- **Purpose:** Shared UI/behavior tests for Quick-series Windows apps
- **OS:** Windows 10 / 11 (64-bit)
- **Form:** Python package `quickappstest` (editable install)
- **Version:** v1.0.0

The library launches a real EXE, attaches Playwright to WebView2 over CDP, uses pywinauto for native Win32, and optionally Appium for the accessibility tree. It does not ship a GUI EXE.

## 2. v1 live targets

| App | Backend | Notes |
| --- | --- | --- |
| QuickDiskBench | Playwright | Bundled `dist/binary/index.html` required. Do not click `#btn-start`. Heartbeat `{action: get_drives}`. |
| QuickImageView | — | **Out of v1 scope** (developed elsewhere). |

QuickFolderSize stays `requireAdministrator`. Live runs of that app require an already elevated test process. Existing WebMessage keys are not renamed; specs send each app's current payload.

## 3. Layers

Do not **click** the same control with two tools. Overlapping **read** oracles are allowed.

| Surface | Tool |
| --- | --- |
| HTML / i18n / WebMessage | Playwright `connect_over_cdp` |
| Native menus, `#32770`, window class | pywinauto `backend="win32"` |
| Accessibility dump / Inspector | Appium (optional; skip if the server is down) |

## 4. App contract (existing apps)

See `quick-app-template/10_検査容易性ルール.md` and `plans/2026-08-23_初期実装_v1.0.md`.

New Quick apps use `{type: ...}` objects. Existing apps keep `action` / `cmd` / `type` / `command` / string `type`.

## 5. Implementation status

PR2 implements Playwright attach. PR3 adds pywinauto for the DiskBench Win32 title. PR4 adds optional Appium by HWND (skip if port 4723 is closed). YAML runner is later. QuickImageView is out of v1 scope.
