# QuickAppsTest — About

[日本語版 about_jp.md](about_jp.md)

## Version

v1.0.0

## Concept

A reusable Python library that inspects Quick-series desktop apps. It is not a shipped Windows GUI. v1 live target is QuickDiskBench.

## Development environment

- Python 3.11+
- Playwright (WebView2 via `connect_over_cdp`)
- pywinauto (DiskBench Win32 title)
- Appium 2 Windows driver (optional; skip if port 4723 is closed)

No MinGW, WebView2 SDK, or `bundle_html.py` in this repository.

## Author

GitHub: [maktak-105](https://github.com/maktak-105)

Copyright (c) 2026 maktak-105 (GitHub: https://github.com/maktak-105)
