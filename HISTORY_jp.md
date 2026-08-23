# QuickAppsTest 変更履歴

[English HISTORY.md](HISTORY.md)

公開バージョンごとの主な変更を記録します。

## バージョン規則

- 第1桁（例: `1.0.0` → `2.0.0`）: 新機能
- 第2桁（例: `1.0.0` → `1.1.0`）: 不具合修正
- 第3桁（例: `1.1.0` → `1.1.1`）: 文書などその他の変更

## 未リリース

### 追加

- リポジトリ skeleton、MIT、日英文書、まだ接続しない `Session` facade（`pip install -e .` で `quickappstest.Session` を import できる）
- Playwright CDP バックエンド、WebMessage フック（string / object）、history cursor 待ち、user-data 付き WebView2 掃除、QuickDiskBench の example spec。`#btn-start` は押さない
- v1 ライブ対象は DiskBench のみ。QuickImageView は対象外
- DiskBench の Win32 タイトル（`Native Storage Benchmark`）を pywinauto で確認。HTML `<title>` とは別文字列
- Appium は任意。4723 が閉じているときは SKIP。Playwright / pywinauto は通る
- YAML ランナーと `python -m quickappstest` CLI（`--spec` `--exe` `--report-dir`）
