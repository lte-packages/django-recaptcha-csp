# Django ReCaptcha CSP Support

A lightweight Django app that provides Content Security Policy (CSP) nonce support for django-recaptcha widgets.

## Problem

The [django-recaptcha](https://github.com/django-recaptcha/django-recaptcha) package doesn't natively support passing CSP nonces to widget templates, making it difficult to use with strict Content Security Policies. See [issue #101](https://github.com/django-recaptcha/django-recaptcha/issues/101).

## Solution

This app provides:
- **Automatic CSP nonce injection** via middleware
- CSP-aware widget classes that properly render the nonce in templates

## Installation

```bash
pip install django-recaptcha
# Then add this app to your project
```

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'recaptcha_csp',
]
```

Add middleware (AFTER your CSP middleware):
```python
MIDDLEWARE = [
    # ... other middleware ...
    'csp.middleware.CSPMiddleware',  # Your CSP middleware
    'recaptcha_csp.middleware.CSPNonceMiddleware',  # Add this AFTER CSP middleware
    # ... other middleware ...
]
```

## Usage

### Recommended: Automatic with Middleware

The middleware automatically captures the CSP nonce and makes it available to widgets. **No changes needed to your view code!**

```python
from django import forms
from captcha.fields import ReCaptchaField
from recaptcha_csp.widgets import CSPReCaptchaV2Checkbox

class MyForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    captcha = ReCaptchaField(widget=CSPReCaptchaV2Checkbox)
```

In your view - **no request passing needed**:
```python
def my_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)  # That's it!
        if form.is_valid():
            # Process form
            pass
    else:
        form = MyForm()  # Just instantiate normally

    return render(request, 'template.html', {'form': form})
```

### With ModelForms

```python
from django.forms import ModelForm
from recaptcha_csp.widgets import CSPReCaptchaV2Checkbox

class MyModelForm(ModelForm):
    captcha = ReCaptchaField(widget=CSPReCaptchaV2Checkbox)

    class Meta:
        model = MyModel
        fields = ['field1', 'field2']

# In your view - no changes needed with middleware!
form = MyModelForm()
```

## Available Widgets

- `CSPReCaptchaV2Checkbox` - Standard checkbox reCAPTCHA
- `CSPReCaptchaV2Invisible` - Invisible reCAPTCHA

## Requirements

- Django >= 4.2
- django-recaptcha >= 3.0

## How It Works

### With Middleware (Recommended)

1. `CSPNonceMiddleware` captures `request.csp_nonce` from your CSP middleware
2. Stores it in thread-safe context storage using `contextvars`
3. Widgets automatically retrieve the nonce when rendering
4. No code changes needed in views or form instantiation


# In view

```
form = MyForm()  # No request needed!
```

Simply add `CSPNonceMiddleware` to your settings

## License

MIT
