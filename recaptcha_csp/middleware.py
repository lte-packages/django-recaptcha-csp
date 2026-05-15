"""
Middleware to automatically capture and store CSP nonces.
"""

from recaptcha_csp.context import clear_csp_nonce, set_csp_nonce


class CSPNonceMiddleware:
    """
    Middleware that captures the CSP nonce from the request and makes it
    available throughout the request lifecycle via contextvars.

    This eliminates the need to explicitly pass request objects to forms.

    Add to MIDDLEWARE in settings.py:
        MIDDLEWARE = [
            # ... other middleware ...
            'csp.middleware.CSPMiddleware',  # Must come before this
            'recaptcha_csp.middleware.CSPNonceMiddleware',
            # ... other middleware ...
        ]
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract CSP nonce from request if available
        nonce = getattr(request, "csp_nonce", None)

        # Store in context for this request
        set_csp_nonce(nonce)

        try:
            response = self.get_response(request)
            return response
        finally:
            # Clean up after request completes
            clear_csp_nonce()
