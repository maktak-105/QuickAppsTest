"""WebMessage hook, compact JSON, and history-cursor waits."""

from __future__ import annotations

import json
import time
from typing import Any, Callable, Mapping, Sequence

INSTALL_HOOK_JS = """
(() => {
  if (!window.__qa) window.__qa = { history: [], _hooked: false };
  if (!window.__qa._hooked && window.chrome && window.chrome.webview) {
    window.chrome.webview.addEventListener('message', (event) => {
      let data = event.data;
      if (typeof data === 'string') {
        try { data = JSON.parse(data); } catch (e) { return; }
      }
      if (data && typeof data === 'object') window.__qa.history.push(data);
    });
    window.__qa._hooked = true;
  }
  return !!(window.__qa && window.__qa._hooked);
})()
"""

HISTORY_LEN_JS = "return (window.__qa && window.__qa.history) ? window.__qa.history.length : 0"
HISTORY_SLICE_JS = """
(() => {
  const h = (window.__qa && window.__qa.history) ? window.__qa.history : [];
  return h.slice(arguments[0] || 0);
})()
"""


def compact_dumps(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def ingest_message(history: list[Any], event_data: Any) -> None:
    """Python twin of INSTALL_HOOK_JS. Used by unit tests."""
    data = event_data
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return
    if isinstance(data, dict):
        history.append(data)


def first_match(
    history: Sequence[Any],
    since: int,
    predicate: Callable[[Any], bool],
) -> Any | None:
    for item in history[since:]:
        if predicate(item):
            return item
    return None


def wait_for_new(
    get_history: Callable[[], Sequence[Any]],
    predicate: Callable[[Any], bool],
    *,
    since: int,
    timeout_s: float = 10.0,
    interval_s: float = 1.0,
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    if interval_s < 1.0:
        raise ValueError("interval_s must be >= 1.0 (WebMessage evaluate poll floor)")
    deadline = time.monotonic() + timeout_s
    while True:
        found = first_match(get_history(), since, predicate)
        if found is not None:
            return found
        if time.monotonic() >= deadline:
            raise TimeoutError(f"no matching WebMessage after history cursor {since}")
        sleep(interval_s)
