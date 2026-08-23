# QuickAppsTest

[English README.md](README.md)

Quick シリーズ向けの共有 UI / 挙動テストライブラリです。出荷用 GUI EXE ではありません。Python パッケージです。

このリポジトリのライブ spec:

- QuickDiskBench（昇格不要）
- QuickFolderSize（`requireAdministrator` は残す。検査プロセスを管理者で起動）

QuickImageView は別途開発中のため対象外です。Appium は任意です。既存キーは改名しません。

## 状態

spec の実行（ビルド済み EXE と隣の `index.html` が必要）:

```powershell
python -m quickappstest --spec examples/QuickDiskBench/spec.yaml --exe F:\project\QuickDiskBench\dist\binary\QuickDiskBench.exe --report-dir qa_reports
```

単体テストに Quick EXE は不要です。

```powershell
python run_tests.py
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
- `examples/QuickFolderSize/spec.yaml`

`examples/QuickImageView/` は作りません。アプリ repo へもコピーしません。

## 文書

- [設計計画](plans/2026-08-23_初期実装_v1.0.md)
- 検査容易性ルール: `quick-app-template` の `10_検査容易性ルール.md`
- [spec.md](document/spec.md) / [spec_jp.md](document/spec_jp.md)
- [environment.md](document/environment.md) / [environment_jp.md](document/environment_jp.md)
- [about.md](document/about.md) / [about_jp.md](document/about_jp.md)

## ライセンス

MIT。[LICENSE](LICENSE)。日本語参考訳は [dist/documents/LICENSE_jp.txt](dist/documents/LICENSE_jp.txt)。

Copyright (c) 2026 maktak-105 (GitHub: https://github.com/maktak-105)
