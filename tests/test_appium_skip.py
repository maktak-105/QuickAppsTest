import socket

import pytest

from unittest.mock import patch

from quickappstest.backends.appium_backend import (
    attach,
    hwnd_to_capability,
    name_contains,
    port_open,
    reject_css_locator,
)
from quickappstest.errors import SpecError


def test_closed_port_is_not_open() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    assert port_open("127.0.0.1", port, timeout_s=0.2) is False


def test_hwnd_capability_is_8_digit_hex_without_0x() -> None:
    assert hwnd_to_capability(0x1A2B) == "00001A2B"
    assert not hwnd_to_capability(42).startswith("0x")


def test_name_contains_not_equals() -> None:
    actual = "QuickDiskBench v2.1.1 - Native Storage Benchmark (Cache Modes & Statistics)"
    assert name_contains(actual, "QuickDiskBench")
    assert not name_contains(actual, actual + " extra")
    assert not name_contains(None, "QuickDiskBench")


def test_css_locator_is_rejected() -> None:
    with pytest.raises(SpecError, match="HTML/CSS"):
        reject_css_locator("#btn-lang")
    with pytest.raises(SpecError, match="HTML/CSS"):
        reject_css_locator(".btn-start")
    reject_css_locator("QuickDiskBench")


def test_attach_skips_when_port_closed() -> None:
    with patch("quickappstest.backends.appium_backend.port_open", return_value=False):
        assert attach(hwnd=0x1234) is None


def test_attach_skips_without_hwnd() -> None:
    assert attach(hwnd=None) is None
    assert attach(hwnd=0) is None
