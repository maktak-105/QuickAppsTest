# QuickAppsTest — 開発環境

[English environment.md](environment.md)

## 前提

- ライブ GUI 検査は Windows 10 / 11 64-bit
- Python 3.11 以降
- Git
- ライブ DiskBench には WebView2 Runtime（Playwright `connect_over_cdp`）
- 任意: Node.js LTS + Appium 2（`appium driver install windows`）

ライブ WebView2 に `playwright install` は **不要** です。CDP はインストール済み Runtime に繋ぎます。DiskBench 用に Chromium を入れないでください。

## 導入

```powershell
cd f:\project\QuickAppsTest
python -m venv .venv
.\.venv\Scripts\pip install -e .[dev]
python run_tests.py
```

`python run_tests.py` は `pytest tests -m "not live"` です。Quick EXE なしで通る必要があります。

## ライブ DiskBench

先にアプリ側で `python build_native.py` します。検査に必要なのは両方です。

- `dist/binary/QuickDiskBench.exe`
- 同じフォルダのバンドル済み `dist/binary/index.html`

`templates/index.html` はライブ対象ではありません（`NavigateToString` では相対 `app.js` が解決しません）。

```powershell
python -m quickappstest --spec examples/QuickDiskBench/spec.yaml --exe F:\project\QuickDiskBench\dist\binary\QuickDiskBench.exe --report-dir qa_reports
```

起動は `subprocess.Popen([exe, *args], cwd=None)` です。パスに引用符を足しません。環境変数は必ず `QUICKAPPSTEST=1`。Playwright 対象は `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=N --remote-allow-origins=*` も付けます。

`#btn-start` は押しません。`action` 値に `start` 部分文字列を含む post もしません。

`pytest tests/live -m live` には `QUICKAPPSTEST_REF_EXE` を設定します。

## Appium（任意）

オペレータが立てるのは **Appium 2 だけ**（`http://127.0.0.1:4723`、`/wd/hub` なし）。windows driver が WinAppDriver を子として `systemPort` **4724** で起動します。WinAppDriver を自分で 4723 に Listen させないでください。

クライアントは `Appium-Python-Client>=3.0` の `WindowsOptions`。`app_top_level_window` は HWND の 8 桁大文字 hex（**`0x` なし**）。Developer Mode が必要なことが多いです。4723 が閉じていれば Appium 項目は SKIP。Playwright / pywinauto は通ります。

## 昇格

QuickFolderSize の `requireAdministrator` は残します（MFT）。そのライブ検査は、すでに管理者の検査プロセスから起動します。ライブラリは **Popen 前**に `TokenElevation` / `IsUserAnAdmin` を見ます。EXE へ `ShellExecute runas` しません（PID が変わるため）。DiskBench は昇格不要です。

## 構成

パッケージ本体は `python/quickappstest/` です。`pyproject.toml` の `package-dir = {"" = "python"}` が必要です。`python/**` を linguist-vendored にしません。

## GitHub

`agent/*` から `main` へ PR します。`main` への直接 push はしません。CI は `windows-latest` で `python run_tests.py` だけ（ライブ EXE なし）。

## トラブルシューティング

| 症状 | 確認 |
| --- | --- |
| `pip` が `quickappstest` を見つけない | `package-dir` と `pip install -e .` |
| LaunchError unbundled HTML | EXE の隣にバンドル済み `index.html` が無い |
| BridgeTimeout | `QuickDiskBench_WVData2` を握った孤児 WebView2。名前一括 `taskkill /IM msedgewebview2.exe` は禁止 |
| FolderSize の attach が死んだ PID | 検査プロセスを管理者で再実行。UAC を自動クリックしない |
| Appium がいつも SKIP | 4723 が閉じていれば正常 |
| `#btn-start` / `action:start` | 禁止。ホストの `find(L"start")` が誤爆する |
