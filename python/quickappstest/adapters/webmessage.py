"""Assemble heartbeat payloads. Keys stay per-app; this file does not rename them."""

from __future__ import annotations

from typing import Any, Callable, Mapping


def type_equals(expected: str) -> Callable[[Any], bool]:
    def _pred(message: Any) -> bool:
        if not isinstance(message, dict):
            return False
        return message.get("type") == expected or message.get("event") == expected

    return _pred


def as_payload(heartbeat: Mapping[str, Any]) -> dict[str, Any]:
    return dict(heartbeat)
