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
| QuickDiskBench | Playwright | バンドル済み `index.html`。`#btn-start` は押さない。ハートビート `{action: get_drives}`。 |
| QuickFolderSize | Playwright | バンドル済み `index.html`。**検査を管理者で起動。** ハートビート `{cmd: get_drives}`。ネイティブフォルダダイアログは開かない。 |
| QuickImageView | — | 対象外（別途開発中）。 |

QuickFolderSize の `requireAdministrator` は残します。そのライブ検査は、すでに管理者の検査プロセスから起動します。既存 WebMessage キーは改名しません。spec が今の payload を送ります。

## 3. 層

同一コントロールを二ツールで **クリック** しません。読み取り oracle の重複は可です。

| 表面 | ツール |
| --- | --- |
| HTML / i18n / WebMessage | Playwright `connect_over_cdp` |
| ネイティブメニュー、`#32770`、窓クラス | pywinauto `backend="win32"` |
| アクセシビリティ dump / Inspector | Appium（任意。サーバが無ければ SKIP） |

## 4. アプリ契約（既存）

正は `quick-app-template/10_検査容易性ルール.md`。検査のために既存キーは改名しません。

| アプリ | wire | ハートビート send | 応答 |
| --- | --- | --- | --- |
| QuickDiskBench | object | `{action: get_drives}` | `type: drives` |
| QuickFolderSize | object | `{cmd: get_drives}` | `type: drives` |
| Quick7Zip | object | `{type: initialize}` | `initialized` |
| QuickFileCopy | object | `{version:1, command: getState}` | `event: selection` |
| QuickMarkPDF | **string** | `{type: get_state}` | `document_state` |

MarkPDF の string `postMessage` を object ホストへコピーしない（沈黙 no-op）。新規アプリだけ `{type: ...}` オブジェクト。FolderSize の UAC は残し、検査ランナーを昇格する。ネイティブファイルダイアログは完走しない。

## 5. 実装状況

Playwright、pywinauto、任意 Appium、YAML CLI まで入りました。`python -m quickappstest --spec ... --exe ...` で DiskBench を回します。4723 が閉じなら Appium 項目は SKIP。QuickImageView は v1 対象外。
