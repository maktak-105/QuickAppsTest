"""Errors raised by QuickAppsTest."""


class QuickAppsTestError(Exception):
    """Base error for the library."""


class LaunchError(QuickAppsTestError):
    """The target EXE could not be started, or launch preconditions failed."""


class BridgeTimeout(QuickAppsTestError):
    """The C++/JS WebMessage bridge did not become ready in time."""


class BackendUnavailable(QuickAppsTestError):
    """A requested backend is not implemented yet, or is down at runtime."""


class SpecError(QuickAppsTestError):
    """The YAML spec is invalid."""
