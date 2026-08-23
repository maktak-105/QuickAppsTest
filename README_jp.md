# QuickAppsTest

[English README.md](README.md)

Quick シリーズ向けの共有 UI / 挙動テストライブラリです。出荷用 GUI EXE ではありません。Python パッケージです。

v1 のライブ対象は **QuickDiskBench のみ**です（WebView2 HTML。Playwright の CDP）。

QuickImageView は別途開発中のため、このリポジトリの対象から外します。Appium は任意です。既存アプリの WebMessage キーは改名しません。QuickFolderSize の `requireAdministrator` は製品のまま残します。そのライブ検査は、すでに管理者の検査プロセスから起動します。

## 状態

Playwright の attach は入りました。YAML ランナー、pywinauto、Appium は後続 PR です。単体テストに Quick EXE は不要です。

```powershell
python -m pytest tests -m "not live"
```

## ソースからの導入

```powershell
pip install -e f:\project\QuickAppsTest
```

```python
from quickappstest import Session
```

## spec の置き場

v1 の spec はこのリポジトリだけに置きます。

- `examples/QuickDiskBench/spec.yaml`

v1 で `examples/QuickImageView/` は作りません。アプリ repo へもコピーしません。

## 文書

- [設計計画](plans/2026-08-23_初期実装_v1.0.md)
- 検査容易性ルール: `quick-app-template` の `10_検査容易性ルール.md`
- [spec.md](document/spec.md) / [spec_jp.md](document/spec_jp.md)
- [environment.md](document/environment.md) / [environment_jp.md](document/environment_jp.md)
- [about.md](document/about.md) / [about_jp.md](document/about_jp.md)

## ライセンス

MIT。[LICENSE](LICENSE)。日本語参考訳は [dist/documents/LICENSE_jp.txt](dist/documents/LICENSE_jp.txt)。

Copyright (c) 2026 maktak-105 (GitHub: https://github.com/maktak-105)
