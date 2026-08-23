# QuickAppsTest 仕様書

[English spec.md](spec.md)

## 1. 概要

- **名称:** QuickAppsTest
- **目的:** Quick シリーズ Windows アプリの共有 UI / 挙動検査
- **OS:** Windows 10 / 11 (64-bit)
- **形態:** Python パッケージ `quickappstest`（editable install）
- **バージョン:** v1.0.0

実 EXE を起動し、WebView2 には Playwright の CDP、ネイティブ Win32 には pywinauto、アクセシビリティには任意で Appium を付けます。GUI EXE は出荷しません。

## 2. v1 のライブ対象

| アプリ | バックエンド | 備考 |
| --- | --- | --- |
| QuickDiskBench | Playwright | バンドル済み `dist/binary/index.html` 必須。`#btn-start` は押さない。ハートビート `{action: get_drives}`。 |
| QuickImageView | pywinauto | CLI で画像パス。`--ui-test-hidden` は付けない。 |

QuickFolderSize の `requireAdministrator` は残します。そのライブ検査は、すでに管理者の検査プロセスから起動します。既存 WebMessage キーは改名しません。spec が今の payload を送ります。

## 3. 層

同一コントロールを二ツールで **クリック** しません。読み取り oracle の重複は可です。

| 表面 | ツール |
| --- | --- |
| HTML / i18n / WebMessage | Playwright `connect_over_cdp` |
| ネイティブメニュー、`#32770`、窓クラス | pywinauto `backend="win32"` |
| アクセシビリティ dump / Inspector | Appium（任意。サーバが無ければ SKIP） |

## 4. アプリ契約（既存）

`quick-app-template/10_検査容易性ルール.md` と `plans/2026-08-23_初期実装_v1.0.md` を正とします。

新規 Quick アプリは `{type: ...}` オブジェクトです。既存は `action` / `cmd` / `type` / `command` / 文字列 `type` のままです。

## 5. 実装状況

PR2 で Playwright の `Session.launch`（CDP、フック、heartbeat cursor、user-data 付き掃除）が入ります。pywinauto / Appium / YAML ランナーは後続です。バンドル済み DiskBench EXE に対する `backends=("playwright",)` がライブ smoke です。
