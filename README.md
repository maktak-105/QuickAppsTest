# QuickAppsTest

[日本語版 README_jp.md](README_jp.md)

Shared UI and behavior test library for Quick-series Windows apps. It is a Python package, not a shipping GUI EXE.

Live specs in this repo:

- QuickDiskBench (no elevation)
- QuickFolderSize (`requireAdministrator` stays; run the tester elevated)
- Quick7Zip (embedded HTML; do not start compression)

QuickImageView is out of scope while it is developed elsewhere. Appium is optional. Existing WebMessage keys are left as-is.

## Status

Run a spec (needs a built EXE + bundled `index.html`):

```powershell
python -m quickappstest --spec examples/QuickDiskBench/spec.yaml --exe F:\project\QuickDiskBench\dist\binary\QuickDiskBench.exe --report-dir qa_reports
```

Unit tests do not need a Quick EXE:

```powershell
python run_tests.py
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

- `examples/QuickDiskBench/spec.yaml`
- `examples/QuickFolderSize/spec.yaml`
- `examples/Quick7Zip/spec.yaml`

Do not add `examples/QuickImageView/`. Do not copy specs into app repos during v1.

## Documentation

- [Design plan (Japanese)](plans/2026-08-23_初期実装_v1.0.md)
- [Testability rules](https://github.com/maktak-105/quick-app-template) — `10_検査容易性ルール.md`
- [spec.md](document/spec.md) / [spec_jp.md](document/spec_jp.md)
- [environment.md](document/environment.md) / [environment_jp.md](document/environment_jp.md)
- [about.md](document/about.md) / [about_jp.md](document/about_jp.md)

## License

MIT. See [LICENSE](LICENSE). Japanese reference translation: [dist/documents/LICENSE_jp.txt](dist/documents/LICENSE_jp.txt).

Copyright (c) 2026 maktak-105 (GitHub: https://github.com/maktak-105)
