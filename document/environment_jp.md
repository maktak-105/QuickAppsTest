# QuickAppsTest — 開発環境

[English environment.md](environment.md)

## 前提

- Windows 10 / 11 64-bit
- Python 3.11 以降
- Git
- 後続のライブ PR: WebView2 Runtime（Playwright CDP）。任意で Node.js + Appium 2

ライブ WebView2 検査に `playwright install` は不要です（`connect_over_cdp` は Runtime に繋ぎます）。後続 PR の fake HTML 単体テストだけ任意です。

## 導入

```powershell
cd f:\project\QuickAppsTest
python -m venv .venv
.\.venv\Scripts\pip install -e .[dev]
```

import 確認（PR1 の成功条件）:

```powershell
python -c "from quickappstest import Session, __version__; print(__version__, Session)"
```

`python -m pytest tests -m "not live"` は EXE なしで通る必要があります。ライブ DiskBench は `QUICKAPPSTEST_REF_EXE` を、隣にバンドル済み `index.html` がある `dist/binary/QuickDiskBench.exe` にします。

## 構成

パッケージ本体は `python/quickappstest/` です。`pyproject.toml` の `package-dir = {"" = "python"}` が必要です。`python/**` を linguist-vendored にしません。

## GitHub

空リポジトリを先に作り、`agent/*` から `main` へ PR します。`main` への直接 push はしません。

## トラブルシューティング

| 症状 | 確認 |
| --- | --- |
| `pip` が `quickappstest` を見つけない | `pyproject.toml` の `package-dir` と `pip install -e .` |
| `Session.launch` が `BackendUnavailable` | PR1 では正常 |
