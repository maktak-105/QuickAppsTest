from __future__ import annotations

import json

import pytest

from quickappstest.protocol import compact_dumps, first_match, wait_for_new


def test_compact_dumps_has_no_spaces_after_separators() -> None:
    dumped = compact_dumps({"action": "get_drives", "n": 1})
    assert dumped == '{"action":"get_drives","n":1}'
    assert json.loads(dumped)["action"] == "get_drives"


def test_first_match_skips_entries_before_cursor() -> None:
    history = [{"type": "drives"}, {"type": "other"}, {"type": "drives"}]
    found = first_match(history, since=1, predicate=lambda m: m.get("type") == "drives")
    assert found is history[2]


def test_wait_for_new_times_out_when_only_seeded_history_exists() -> None:
    seeded = [{"type": "drives"}]
    with pytest.raises(TimeoutError):
        wait_for_new(
            lambda: seeded,
            lambda m: m.get("type") == "drives",
            since=1,
            timeout_s=0.0,
            interval_s=1.0,
            sleep=lambda _s: None,
        )


def test_wait_for_new_rejects_subsecond_interval() -> None:
    with pytest.raises(ValueError, match="interval_s"):
        wait_for_new(lambda: [], lambda _m: True, since=0, interval_s=0.5)


def test_wait_for_new_sees_appended_entry() -> None:
    history: list[dict[str, str]] = [{"type": "drives"}]
    calls = {"n": 0}

    def get_history() -> list[dict[str, str]]:
        calls["n"] += 1
        if calls["n"] >= 2:
            history.append({"type": "drives", "seq": "second"})
        return history

    found = wait_for_new(
        get_history,
        lambda m: m.get("seq") == "second",
        since=1,
        timeout_s=5.0,
        interval_s=1.0,
        sleep=lambda _s: None,
    )
    assert found["seq"] == "second"
