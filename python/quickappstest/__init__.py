"""Shared UI and behavior tests for Quick-series Windows apps."""

from .errors import BackendUnavailable, BridgeTimeout, LaunchError, SpecError
from .session import Session

__version__ = "1.0.0"
__all__ = [
    "Session",
    "LaunchError",
    "BridgeTimeout",
    "BackendUnavailable",
    "SpecError",
    "__version__",
]
