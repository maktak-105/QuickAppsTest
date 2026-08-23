# QuickDiskBench example spec

Live target is a **built** tree:

- `dist/binary/QuickDiskBench.exe`
- bundled `dist/binary/index.html` next to the EXE (`NavigateToString` cannot load `templates/index.html` + relative `app.js`)

Do **not** click `#btn-start`. That starts real disk I/O. Do not post a WebMessage whose `action` value contains the substring `start` (`find(L"start")` in the host).

YAML `checks` here are documentation until the runner (later PR). Until then, drive the EXE with `Session.launch` as in `tests/live/test_diskbench_smoke.py`.

```powershell
$env:QUICKAPPSTEST_REF_EXE = "F:\project\QuickDiskBench\dist\binary\QuickDiskBench.exe"
# from QuickAppsTest venv
python -m pytest tests/live -m live
```
