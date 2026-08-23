# QuickAppsTest

[日本語版 README_jp.md](README_jp.md)

Shared UI and behavior test library for Quick-series Windows apps. It is a Python package, not a shipping GUI EXE.

v1 drives two live targets:

- QuickDiskBench (WebView2 HTML via Playwright CDP)
- QuickImageView (native Win32 via pywinauto)

Appium is optional. Existing WebMessage keys are left as-is; each spec sends that app's current payload. QuickFolderSize keeps `requireAdministrator`; live runs of that app must start from an already elevated test process.

## Status

Playwright attach is implemented. YAML runner, pywinauto, and Appium come in later PRs. Unit tests do not need a Quick EXE:

```powershell
python -m pytest tests -m "not live"
```

## Install from source

```powershell
pip install -e f:\project\QuickAppsTest
```

```python
from quickappstest import Session
```

## Specs

v1 specs live only in this repository:

- `examples/QuickDiskBench/spec.yaml` (added in a later PR)
- `examples/QuickImageView/spec.yaml` (added in a later PR)

Do not copy them into app repos during v1.

## Documentation

- [Design plan (Japanese)](plans/2026-08-23_初期実装_v1.0.md)
- [Testability rules](https://github.com/maktak-105/quick-app-template) — `10_検査容易性ルール.md`
- [spec.md](document/spec.md) / [spec_jp.md](document/spec_jp.md)
- [environment.md](document/environment.md) / [environment_jp.md](document/environment_jp.md)
- [about.md](document/about.md) / [about_jp.md](document/about_jp.md)

## License

MIT. See [LICENSE](LICENSE). Japanese reference translation: [dist/documents/LICENSE_jp.txt](dist/documents/LICENSE_jp.txt).

Copyright (c) 2026 maktak-105 (GitHub: https://github.com/maktak-105)
