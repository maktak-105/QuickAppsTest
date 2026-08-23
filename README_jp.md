# QuickAppsTest

[English README.md](README.md)

Quick シリーズ向けの共有 UI / 挙動テストライブラリです。出荷用 GUI EXE ではありません。Python パッケージです。

v1 のライブ対象は次の 2 本です。

- QuickDiskBench（WebView2 HTML。Playwright の CDP）
- QuickImageView（ネイティブ Win32。pywinauto）

Appium は任意です。既存アプリの WebMessage キーは改名しません。spec が今の payload を送ります。QuickFolderSize の `requireAdministrator` は製品のまま残します。そのライブ検査は、すでに管理者の検査プロセスから起動します。

## 状態

v1.0.0 の skeleton です。`Session.launch` は未実装です。Playwright / pywinauto / Appium / YAML ランナーは後続 PR です。

## ソースからの導入

```powershell
pip install -e f:\project\QuickAppsTest
```

```python
from quickappstest import Session
```

## spec の置き場

v1 の spec はこのリポジトリだけに置きます。

- `examples/QuickDiskBench/spec.yaml`（後続 PR）
- `examples/QuickImageView/spec.yaml`（後続 PR）

v1 ではアプリ repo へコピーしません。

## 文書

- [設計計画](plans/2026-08-23_初期実装_v1.0.md)
- 検査容易性ルール: `quick-app-template` の `10_検査容易性ルール.md`
- [spec.md](document/spec.md) / [spec_jp.md](document/spec_jp.md)
- [environment.md](document/environment.md) / [environment_jp.md](document/environment_jp.md)
- [about.md](document/about.md) / [about_jp.md](document/about_jp.md)

## ライセンス

MIT。[LICENSE](LICENSE)。日本語参考訳は [dist/documents/LICENSE_jp.txt](dist/documents/LICENSE_jp.txt)。

Copyright (c) 2026 maktak-105 (GitHub: https://github.com/maktak-105)
