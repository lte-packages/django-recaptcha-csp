"""
Django settings for demo_site project.

This is a minimal configuration for testing django-recaptcha-csp locally.
"""

import os
from pathlib import Path

from csp.constants import (
    # REPORT_SAMPLE,
    NONCE,
    NONE,
    SELF,
    STRICT_DYNAMIC,
    UNSAFE_INLINE,
)

# django-csp is now used for production-ready CSP support

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-demo-key-for-local-testing-only-change-in-production"  # noqa: S105

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "captcha",  # django-recaptcha
    "recaptcha_csp",  # Our package
    # Demo app
    "demo_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # CSP middleware - django-csp
    "csp.middleware.CSPMiddleware",
    # Our middleware - MUST come after CSP middleware
    "recaptcha_csp.middleware.CSPNonceMiddleware",
]

ROOT_URLCONF = "demo_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "demo_site.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "demo_app" / "static",
]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ReCAPTCHA Settings
# For local testing, use test keys that always pass validation
# Get real keys from: https://www.google.com/recaptcha/admin
RECAPTCHA_PUBLIC_KEY = os.environ.get(
    "RECAPTCHA_PUBLIC_KEY",
    "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI",  # Google's test key
)
RECAPTCHA_PRIVATE_KEY = os.environ.get(
    "RECAPTCHA_PRIVATE_KEY",
    "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe",  # Google's test key
)

# Optional: Configure reCAPTCHA required score for v3 (0.0 - 1.0)
# RECAPTCHA_REQUIRED_SCORE = 0.85

# Silence the test key warning for demo purposes
SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

# ========================================
# Django-CSP Settings (v4.0+)
# ========================================
# https://django-csp.readthedocs.io/en/latest/configuration.html

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "frame-ancestors": [NONE],  # Prevent clickjacking
        # Default source policy
        "default-src": [SELF],
        # Script sources - use nonce-based CSP with strict-dynamic
        # Note: URL whitelists are incompatible with nonce/strict-dynamic
        # strict-dynamic allows scripts loaded by nonce-approved scripts to load other scripts
        "script-src": [
            NONCE,
            STRICT_DYNAMIC,
            "https:",  # Fallback for older browsers that don't support strict-dynamic
            UNSAFE_INLINE,  # Fallback for older browsers (ignored when nonce is supported)
        ],
        # Frame sources - required for reCAPTCHA iframe
        # This is separate from script-src, so we can whitelist the reCAPTCHA domains
        "frame-src": [
            "https://www.google.com/recaptcha/",
            "https://www.gstatic.com/recaptcha/",
        ],
        # Style sources - allow inline styles for demo (can be stricter in production)
        "style-src": [
            SELF,
            UNSAFE_INLINE,  # Required for inline styles in demo templates
        ],
        # Image sources
        "img-src": [SELF, "data:"],
        # Font sources
        "font-src": [SELF],
        # Connect sources (for AJAX, WebSocket, etc.)
        "connect-src": [SELF, 'www.google.com/recaptcha/'],  # Allow reCAPTCHA API calls
    }
}
