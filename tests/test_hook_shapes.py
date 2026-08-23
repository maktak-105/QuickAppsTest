from __future__ import annotations

from quickappstest.protocol import INSTALL_HOOK_JS, ingest_message


def test_hook_js_accepts_string_and_object() -> None:
    assert "typeof data === 'string'" in INSTALL_HOOK_JS
    assert "JSON.parse(data)" in INSTALL_HOOK_JS
    assert "window.__qa.history.push" in INSTALL_HOOK_JS


def test_ingest_object_message() -> None:
    history: list[object] = []
    ingest_message(history, {"type": "drives", "data": []})
    assert history == [{"type": "drives", "data": []}]


def test_ingest_string_json_message() -> None:
    history: list[object] = []
    ingest_message(history, '{"type":"document_state","pages":[]}')
    assert history[0]["type"] == "document_state"


def test_ingest_drops_non_json_string() -> None:
    history: list[object] = []
    ingest_message(history, "not-json")
    assert history == []
