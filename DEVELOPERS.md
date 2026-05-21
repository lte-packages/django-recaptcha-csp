# django-recaptcha-csp - Maintainer Guide

This document provides information for package maintainers. For end-user documentation, see [README.md](README.md).

## Overview

**django-recaptcha-csp** is a lightweight Django app that provides Content Security Policy (CSP) nonce support for django-recaptcha widgets. It solves the problem described in [django-recaptcha issue #101](https://github.com/django-recaptcha/django-recaptcha/issues/101).

- **Package name**: `django-recaptcha-csp`
- **License**: MIT
- **Python**: >=3.8
- **Django**: >=4.2

## Development Setup

### Prerequisites

- Python 3.8+
- pip
- make (optional, but recommended)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourorg/django-recaptcha-csp.git
   cd django-recaptcha-csp
   ```

2. **Set up virtual environment and install dependencies:**
   ```bash
   make pip_env
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

3. **Install build dependencies:**
   ```bash
   pip install build ruff
   ```

## Project Structure

```
recaptcha-csp/
├── recaptcha_csp/          # Main package directory
│   ├── __init__.py         # Package initialization, version
│   ├── apps.py             # Django app configuration
│   ├── context.py          # Context processors
│   ├── middleware.py       # CSP nonce middleware
│   ├── widgets.py          # CSP-aware ReCaptcha widgets
│   ├── examples.py         # Usage examples
│   ├── README.md           # User-facing documentation
│   └── templates/          # Widget templates
│       └── recaptcha_csp/
│           ├── widget_v2_checkbox.html
│           ├── widget_v2_invisible.html
│           └── includes/
│               ├── js_v2_checkbox.html
│               └── js_v2_invisible.html
├── pyproject.toml          # Package metadata and build config
├── MANIFEST.in             # Additional files to include in distribution
├── Makefile                # Development task automation
├── PACKAGING.md            # Packaging notes and instructions
├── LICENSE                 # MIT License
└── README.md               # This file (maintainer documentation)
```

## Development Tasks

The `Makefile` provides common development tasks:

```bash
make help           # Show available targets
make pip_env        # Create/update virtual environment
make lint           # Run linting with ruff
make format         # Format code and fix auto-fixable issues
make clean          # Remove build artifacts and caches
```

### Code Quality

We use **Ruff** for both linting and formatting:

```bash
# Check code style
make lint

# Auto-format and fix issues
make format
```

Configuration is in `[tool.ruff]` section of `pyproject.toml`.

## Building the Package

### Local Development Install

Install package in editable mode for local development:

```bash
pip install -e .
```

### Build Distribution

1. **Clean previous builds:**
   ```bash
   make clean
   ```

2. **Build wheel and source distribution:**
   ```bash
   python -m build
   ```

   This creates:
   - `dist/django_recaptcha_csp-{version}-py3-none-any.whl`
   - `dist/django-recaptcha-csp-{version}.tar.gz`

3. **Verify package contents:**
   ```bash
   tar -tzf dist/django_recaptcha_csp-*.tar.gz
   unzip -l dist/django_recaptcha_csp-*.whl
   ```

4. **Test installation locally:**
   ```bash
   pip install dist/django_recaptcha_csp-*.whl
   ```

## Release Process

### Pre-release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `recaptcha_csp/__init__.py` (if applicable)
- [ ] Update CHANGELOG or release notes
- [ ] Update author and URL placeholders in `pyproject.toml`
- [ ] Update copyright year in LICENSE
- [ ] Run tests (if test suite exists)
- [ ] Run `make lint` and fix issues
- [ ] Run `make format`
- [ ] Build package: `python -m build`
- [ ] Test install in clean environment

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality, backward compatible
- **PATCH**: Bug fixes, backward compatible

## Configuration Files

### pyproject.toml

Main configuration file containing:
- Build system requirements
- Package metadata (name, version, dependencies)
- Tool configurations (ruff)

**Key sections to update for releases:**
- `version` in `[project]`
- `authors` (replace placeholders)
- `project.urls` (replace placeholders)

### MANIFEST.in

Specifies additional files to include in source distribution:
- `README.md`
- `LICENSE`
- Template files (`*.html`)

## Testing

### Manual Testing

Currently, testing is manual. To test the package:

1. **Install in a test Django project:**
   ```bash
   pip install -e /path/to/django-recaptcha-csp
   ```

2. **Add to INSTALLED_APPS:**
   ```python
   INSTALLED_APPS = [
       # ...
       'recaptcha_csp',
   ]
   ```

3. **Add middleware after CSP middleware:**
   ```python
   MIDDLEWARE = [
       # ...
       'csp.middleware.CSPMiddleware',
       'recaptcha_csp.middleware.CSPNonceMiddleware',
   ]
   ```

4. **Use CSP-aware widgets in forms:**
   ```python
   from recaptcha_csp.widgets import CSPReCaptchaV2Checkbox
   ```

### Future: Automated Testing

Consider adding:
- `pytest` and `pytest-django` for unit tests
- `tox` for testing across Python/Django versions
- GitHub Actions for CI/CD
- Coverage reporting

## Dependencies

### Runtime Dependencies
- `Django>=4.2`
- `django-recaptcha>=3.0.0`

### Development Dependencies
- `build` - Package building
- `twine` - PyPI uploads
- `ruff` - Linting and formatting

## Troubleshooting

### Templates not included in package

Ensure `MANIFEST.in` includes template files and `pyproject.toml` has:
```toml
[tool.setuptools]
include-package-data = true

[tool.setuptools.package-data]
recaptcha_csp = ["templates/**/*.html"]
```

### Import errors after installation

Verify package structure uses `__init__.py` in all directories and package discovery is configured:
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["recaptcha_csp*"]
```

### Version conflicts

Check Django and django-recaptcha version compatibility. Adjust version constraints in `pyproject.toml` if needed.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Run `make format` and `make lint`
5. Submit a pull request

## Maintenance Notes

- This package is designed to be lightweight with minimal dependencies
- Keep django-recaptcha compatibility in mind when making changes
- Template changes should maintain CSP nonce functionality
- Document any breaking changes clearly

## Resources

- [PEP 517 - Build system requirements](https://peps.python.org/pep-0517/)
- [PEP 518 - pyproject.toml specification](https://peps.python.org/pep-0518/)
- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)
- [Setuptools documentation](https://setuptools.pypa.io/)
- [Semantic Versioning](https://semver.org/)

## Support

- Report issues: https://github.com/yourorg/django-recaptcha-csp/issues
- Documentation: https://github.com/yourorg/django-recaptcha-csp#readme

## License

MIT License - see [LICENSE](LICENSE) file for details.
