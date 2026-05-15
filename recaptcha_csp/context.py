"""
Context management for CSP nonce storage.

Uses contextvars to store the current request's CSP nonce in a thread-safe manner,
allowing widgets to access it without explicit passing through form constructors.
"""

from contextvars import ContextVar

# Thread-safe storage for the current request's CSP nonce
_csp_nonce: ContextVar[str | None] = ContextVar("csp_nonce", default=None)


def set_csp_nonce(nonce: str | None) -> None:
    """
    Store the CSP nonce for the current request context.

    Args:
        nonce: The CSP nonce string or None
    """
    _csp_nonce.set(nonce)


def get_csp_nonce() -> str | None:
    """
    Retrieve the CSP nonce for the current request context.

    Returns:
        The CSP nonce string or None if not set
    """
    return _csp_nonce.get()


def clear_csp_nonce() -> None:
    """Clear the CSP nonce from the current context."""
    _csp_nonce.set(None)
