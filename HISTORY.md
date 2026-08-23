# QuickAppsTest Changelog

[日本語版 HISTORY_jp.md](HISTORY_jp.md)

This file records the major changes in each public version.

## Versioning rules

- First digit (for example, `1.0.0` to `2.0.0`): new features
- Second digit (for example, `1.0.0` to `1.1.0`): bug fixes
- Third digit (for example, `1.1.0` to `1.1.1`): other changes, such as documentation updates

## Unreleased

### Added

- Repository skeleton, MIT license, bilingual documents, and a `Session` facade that does not attach yet (`pip install -e .` imports `quickappstest.Session`).
- Playwright CDP backend, WebMessage hook (string and object), history-cursor waits, scoped WebView2 cleanup, and a QuickDiskBench example spec. `#btn-start` is never clicked.
- v1 live target is QuickDiskBench only. QuickImageView is out of scope.
- pywinauto attach for DiskBench Win32 title (`Native Storage Benchmark`), distinct from HTML `<title>`.
- Optional Appium attach by HWND. Closed port 4723 skips; Playwright/pywinauto still pass.
- YAML runner and `python -m quickappstest` CLI (`--spec` `--exe` `--report-dir`).
