# Quick7Zip example spec

GUI HTML is embedded in the EXE. A sidecar `index.html` is not required.

Heartbeat is `{type: initialize}` → `initialized`.

Do **not** click `#startButton` (starts compression) or `#browseInput` / `#browseOutput` (native dialogs).

`AreDevToolsEnabled(FALSE)` is set for users. Live CDP is via `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS` and may still work.

```powershell
python -m quickappstest --spec examples/Quick7Zip/spec.yaml --exe F:\project\Quick7Zip\dist\binary\Quick7Zip.exe --report-dir qa_reports
```
