# Django ReCaptcha CSP - Demo Site

This is a demonstration Django website for testing and developing the `django-recaptcha-csp` package locally.

## Features

The demo site showcases:

- ✅ **CSP-aware reCAPTCHA v2 Checkbox** - Traditional visible checkbox
- ✅ **CSP-aware reCAPTCHA v2 Invisible** - Seamless background validation  
- ✅ **Simple CSP middleware** - Example implementation for testing
- ✅ **Multiple form examples** - Various use cases
- ✅ **CSP information page** - Educational content about Content Security Policy

## Quick Start

### 1. Install Dependencies

From the demo_site directory:

```bash
# If you don't have a virtual environment yet
cd /path/to/recaptcha-csp
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in development mode
pip install -e .

# Install demo site dependencies
cd demo_site
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

Or from the project root, use the Makefile:

```bash
make demo-run
```

### 5. Open in Browser

Visit: http://localhost:8000/

## Using Your Own reCAPTCHA Keys

By default, the demo uses Google's test keys which always pass validation. To use real reCAPTCHA:

1. Get keys from: https://www.google.com/recaptcha/admin
2. Choose reCAPTCHA v2
3. Set environment variables:

```bash
export RECAPTCHA_PUBLIC_KEY='your-site-key'
export RECAPTCHA_PRIVATE_KEY='your-secret-key'
python manage.py runserver
```

Or edit `demo_site/settings.py` directly (not recommended for production).

## Demo Pages

### Home (`/`)
Overview of the package and links to all demos.

### Checkbox reCAPTCHA (`/contact/checkbox/`)
Contact form with traditional visible checkbox reCAPTCHA.

### Invisible reCAPTCHA (`/contact/invisible/`)
Contact form with invisible reCAPTCHA that validates on submit.

### Simple Form (`/simple/`)
Basic form without reCAPTCHA for comparison.

### CSP Info (`/csp-info/`)
Information about Content Security Policy and how the nonce system works.

## Project Structure

```
demo_site/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── demo_site/            # Project configuration
│   ├── __init__.py
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py
│   ├── asgi.py
│   └── simple_csp_middleware.py  # Demo CSP middleware
└── demo_app/             # Demo application
    ├── __init__.py
    ├── apps.py
    ├── models.py         # Optional contact model
    ├── forms.py          # Example forms with reCAPTCHA
    ├── views.py          # View functions
    ├── urls.py           # App URL patterns
    └── templates/
        └── demo_app/
            ├── base.html
            ├── index.html
            ├── contact_checkbox.html
            ├── contact_invisible.html
            ├── simple_form.html
            ├── success.html
            └── csp_info.html
```

## Configuration Notes

### CSP Middleware

The demo uses [django-csp](https://github.com/mozilla/django-csp) for production-ready Content Security Policy support.

**Configuration in settings.py (django-csp 4.0+ format):**

```python
# settings.py
MIDDLEWARE = [
    ...
    'csp.middleware.CSPMiddleware',  # django-csp
    'recaptcha_csp.middleware.CSPNonceMiddleware',  # Our middleware (must be after CSP)
]

# CSP Settings (v4.0+ format)
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": [
            "'nonce'",  # Enable nonce support
            "'strict-dynamic'",  # Allow dynamically loaded scripts
            "https:",  # Fallback for older browsers
            "'unsafe-inline'",  # Fallback (ignored with nonce support)
        ],
        "frame-src": [
            "https://www.google.com/recaptcha/",
            "https://www.gstatic.com/recaptcha/",
        ],
    }
}
```

**Important:** When using `'nonce'` and `'strict-dynamic'`, you cannot include URL whitelists
in `script-src`. The reCAPTCHA scripts are loaded dynamically by trusted scripts with valid nonces.
The `frame-src` directive is separate and can still whitelist the reCAPTCHA iframe domains.

Our `CSPNonceMiddleware` captures the nonce from django-csp for use in reCAPTCHA widgets.

### Database

The demo uses SQLite by default. For testing purposes, the ContactSubmission model is defined but not required for the reCAPTCHA functionality to work.

## Development

### Testing Package Changes

Since the package is installed in editable mode (`pip install -e .`), changes to the package source code in `recaptcha_csp/` will be immediately reflected in the demo site.

Just refresh your browser or restart the dev server to see changes.

### Adding New Examples

1. Create a new form in `demo_app/forms.py`
2. Create a view in `demo_app/views.py`
3. Add URL pattern in `demo_app/urls.py`
4. Create template in `demo_app/templates/demo_app/`
5. Add link to navigation in `base.html`

## Troubleshooting

### reCAPTCHA not loading?

Check that:
- CSP headers are set correctly (check browser DevTools → Network tab)
- Middleware order is correct (CSP middleware before CSPNonceMiddleware)
- JavaScript console for CSP violations

### Forms not validating?

With test keys, all validations should pass. If using real keys:
- Check keys are correct in settings
- Verify domain is registered for the keys in Google reCAPTCHA admin
- Check that request is coming from an allowed domain

### CSP violations in console?

- Ensure nonce is being generated (visit `/csp-info/`)
- Check that CSP header includes nonce placeholder
- Verify inline scripts have `nonce` attribute

## Resources

- [django-recaptcha-csp GitHub](https://github.com/horrocksm/django-recaptcha-csp)
- [django-recaptcha Documentation](https://github.com/django-recaptcha/django-recaptcha)
- [Google reCAPTCHA Admin](https://www.google.com/recaptcha/admin)
- [MDN CSP Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [django-csp Documentation](https://django-csp.readthedocs.io/)

## License

This demo site is part of the django-recaptcha-csp package and is licensed under the MIT License.
