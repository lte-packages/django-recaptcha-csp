"""
Simple CSP middleware for demonstration purposes.

In production, use a proper CSP library like django-csp:
https://github.com/mozilla/django-csp
"""

import secrets
from django.conf import settings


class SimpleCSPMiddleware:
    """
    Simple Content Security Policy middleware that generates a nonce
    for each request and sets it in the response headers.

    This is a simplified implementation for demo purposes.
    For production use, consider using django-csp or similar.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate a cryptographically secure nonce for this request
        nonce = secrets.token_urlsafe(16)

        # Store nonce on request object so it's available to templates and middleware
        request.csp_nonce = nonce

        # Process the request
        response = self.get_response(request)

        # Build CSP header
        csp_directives = [
            f"script-src 'self' 'nonce-{nonce}' https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/",
            f"frame-src https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/",
            f"style-src 'self' 'unsafe-inline'",
            "default-src 'self'",
        ]

        # Set CSP header
        response['Content-Security-Policy'] = '; '.join(csp_directives)

        return response
