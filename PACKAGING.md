# Extracting and Packaging django-recaptcha-csp

## Quick Start - Extract from Project

1. **Copy the app directory to a new location:**
   ```bash
   cp -r recaptcha_csp /path/to/new/django-recaptcha-csp/
   cd /path/to/new/django-recaptcha-csp/
   ```

2. **Update pyproject.toml** with your details:
   - Author name and email
   - GitHub repository URLs
   - Any additional metadata

3. **Test locally in another project:**
   ```bash
   # In your other Django project
   pip install -e /path/to/django-recaptcha-csp/
   ```

4. **Build the package:**
   ```bash
   python -m build
   ```

5. **Publish to PyPI (optional):**
   ```bash
   twine upload dist/*
   ```

## Or Use as Git Dependency

In your `requirements.txt`:
```
django-recaptcha-csp @ git+https://github.com/yourorg/django-recaptcha-csp.git@main
```

## Testing in Current Project

To test the package in this project before extraction:

1. Add `'recaptcha_csp'` to `INSTALLED_APPS` in your settings
2. Update your forms to import from `recaptcha_csp` instead of local modules
3. Run migrations (if any models were added - currently none)

Example migration in tpforms:
```python
# Old
from tpforms.mixins import FormCSPMixin
from tpforms.widgets import TpReCaptchaV2Checkbox

# New
from recaptcha_csp.mixins import FormCSPMixin
from recaptcha_csp.widgets import CSPReCaptchaV2Checkbox
```

## Directory Structure

```
recaptcha_csp/
├── __init__.py           # Package initialization
├── apps.py              # Django app config
├── mixins.py            # FormCSPMixin
├── widgets.py           # CSP-aware widget classes
├── examples.py          # Usage examples
├── README.md            # Documentation
├── pyproject.toml       # Package metadata and dependencies
├── MANIFEST.in          # Include templates in package
├── LICENSE              # MIT License
├── .gitignore          # Git ignore patterns
└── templates/
    └── recaptcha_csp/
        ├── widget_v2_checkbox.html
        ├── widget_v2_invisible.html
        └── includes/
            ├── js_v2_checkbox.html
            └── js_v2_invisible.html
```

## Building and Distribution

### Local Development
```bash
pip install -e .
```

### Build Package
```bash
pip install build
python -m build
```

This creates:
- `dist/django_recaptcha_csp-0.1.0-py3-none-any.whl`
- `dist/django-recaptcha-csp-0.1.0.tar.gz`

### Upload to PyPI
```bash
pip install twine
twine check dist/*
twine upload dist/*  # Requires PyPI account
```

### Private Git Repository
If you want to keep it private or just use across your organization:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:yourorg/django-recaptcha-csp.git
git push -u origin main
```

Then in projects:
```
# requirements.txt
django-recaptcha-csp @ git+ssh://git@github.com/yourorg/django-recaptcha-csp.git@main
```
