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
| QuickDiskBench | Playwright | Bundled `index.html`. Do not click `#btn-start`. Heartbeat `{action: get_drives}`. |
| QuickFolderSize | Playwright | Bundled `index.html`. **Elevate the tester.** Heartbeat `{cmd: get_drives}`. Do not open the native folder dialog. |
| Quick7Zip | Playwright | Embedded HTML. Heartbeat `{type: initialize}`. Do not click start or browse. |
| QuickImageView | — | Out of scope (developed elsewhere). |

QuickFolderSize stays `requireAdministrator`. Live runs of that app require an already elevated test process. Existing WebMessage keys are not renamed; specs send each app's current payload.

## 3. Layers

Do not **click** the same control with two tools. Overlapping **read** oracles are allowed.

| Surface | Tool |
| --- | --- |
| HTML / i18n / WebMessage | Playwright `connect_over_cdp` |
| Native menus, `#32770`, window class | pywinauto `backend="win32"` |
| Accessibility dump / Inspector | Appium (optional; skip if the server is down) |

## 4. App contract (existing apps)

Canonical rules: `quick-app-template/10_検査容易性ルール.md`. Do not rename existing keys for the tester.

| App | wire | Heartbeat send | Response |
| --- | --- | --- | --- |
| QuickDiskBench | object | `{action: get_drives}` | `type: drives` |
| QuickFolderSize | object | `{cmd: get_drives}` | `type: drives` |
| Quick7Zip | object | `{type: initialize}` | `initialized` |
| QuickFileCopy | object | `{version:1, command: getState}` | `event: selection` |
| QuickMarkPDF | **string** | `{type: get_state}` | `document_state` |

Do not copy MarkPDF's string `postMessage` onto object hosts (silent no-op). New apps use `{type: ...}` objects. FolderSize UAC stays; elevate the test runner. Native file dialogs are not completed by the tester.

## 5. Implementation status

Playwright, pywinauto, optional Appium, and the YAML CLI are in. `python -m quickappstest --spec ... --exe ...` runs DiskBench checks. Appium checks SKIP when 4723 is closed. QuickImageView is out of v1 scope.
