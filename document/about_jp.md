# QuickAppsTest — バージョン情報

[English about.md](about.md)

## バージョン

v1.0.0

## コンセプト

Quick シリーズのデスクトップアプリを検査する再利用 Python ライブラリです。出荷する Windows GUI ではありません。v1 のライブ対象は QuickDiskBench です。

## 開発環境

- Python 3.11+
- Playwright（WebView2 は `connect_over_cdp`）
- pywinauto（DiskBench の Win32 タイトル）
- Appium 2 Windows driver（任意。4723 が閉じなら SKIP）

このリポジトリに MinGW、WebView2 SDK、`bundle_html.py` は置きません。

## 作者

GitHub: [maktak-105](https://github.com/maktak-105)

Copyright (c) 2026 maktak-105 (GitHub: https://github.com/maktak-105)
