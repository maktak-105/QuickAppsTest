# QuickFolderSize example spec

The shipping EXE stays `requireAdministrator` (NTFS MFT is the product). The test process must already be elevated. The library does not `runas` the EXE.

Live target:

- `dist/binary/QuickFolderSize.exe`
- bundled `dist/binary/index.html` next to the EXE

Heartbeat is `{cmd: get_drives}` (not DiskBench `{action: get_drives}`).

Do **not** click フォルダを開く (native `IFileDialog`) or 終了. Do not scan `C:\`.

```powershell
python -m quickappstest --spec examples/QuickFolderSize/spec.yaml --exe F:\project\QuickFolderSize\dist\binary\QuickFolderSize.exe --report-dir qa_reports
```

Unelevated runs exit 2 (`requires_elevation`).
