"""
Django ReCaptcha CSP Support

A lightweight Django app that provides Content Security Policy (CSP) nonce support
for django-recaptcha widgets.

Usage:
    from recaptcha_csp.mixins import FormCSPMixin
    from recaptcha_csp.widgets import CSPReCaptchaV2Checkbox
"""

try:
    from importlib.metadata import version

    __version__ = version("django-recaptcha-csp")
except Exception:
    # Fallback for development installations
    __version__ = "0.0.0+dev"
