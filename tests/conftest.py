import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "live: requires a built Quick EXE")
