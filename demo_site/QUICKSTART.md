# Quick Start Guide

The fastest way to run the django-recaptcha-csp demo site.

The demo uses [django-csp](https://github.com/mozilla/django-csp) for production-ready CSP support.

## Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## One-Command Start

From the project root directory:

```bash
make demo-run
```

That's it! This will start the development server.

Then open your browser to: **http://localhost:8000/**

### First Time Setup

If this is your first time running the demo:

```bash
make demo-setup    # Install dependencies and run migrations
make demo-run      # Start the server
```

## Available Make Commands

```bash
make demo-setup     # Complete setup (install dependencies + migrations)
make demo-install   # Install dependencies only
make demo-migrate   # Run database migrations only
make demo-run       # Start the development server
make demo-clean     # Clean database and temporary files
make help           # Show all available commands
```

## Manual Setup

If you prefer to set up manually:

```bash
# 1. Go to parent directory and activate venv
cd ..
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install the package in editable mode
pip install -e .

# 3. Go to demo_site and install requirements
cd demo_site
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

## What to Try

1. **Home Page** (`/`) - Overview and documentation
2. **Checkbox reCAPTCHA** (`/contact/checkbox/`) - Traditional visible challenge
3. **Invisible reCAPTCHA** (`/contact/invisible/`) - Seamless validation
4. **CSP Info** (`/csp-info/`) - See how the nonce system works

## Using Real reCAPTCHA Keys

The demo uses Google's test keys by default. To use real keys:

```bash
export RECAPTCHA_PUBLIC_KEY='your-site-key'
export RECAPTCHA_PRIVATE_KEY='your-secret-key'
python manage.py runserver
```

Get your keys from: https://www.google.com/recaptcha/admin

## Troubleshooting

**ModuleNotFoundError: No module named 'captcha'**
- Make sure you're using django-recaptcha version 3.x (not 4.x)
- Run: `pip install "django-recaptcha>=3.0.0,<4.0"`

**Port already in use**
- Run on a different port: `python manage.py runserver 8001`

**Database errors**
- Delete `db.sqlite3` and run `python manage.py migrate` again

## Development

The package is installed in editable mode, so any changes to the source code in `../recaptcha_csp/` will be reflected immediately. Just refresh your browser!

## Next Steps

- Check out [README.md](README.md) for detailed documentation
- Explore the source code in `demo_app/` to see example implementations
- Try modifying forms in `demo_app/forms.py` to experiment
