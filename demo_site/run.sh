#!/bin/bash
# Legacy startup script for the django-recaptcha-csp demo site
# 
# This script is deprecated in favor of using the Makefile from the project root:
#   make demo-setup    # First time setup
#   make demo-run      # Run the server
#
# This wrapper is maintained for backward compatibility.

set -e

echo "⚠️  Note: This script is deprecated. Use 'make demo-run' from the project root instead."
echo ""

# Go to project root
cd "$(dirname "$0")/.."

# Check if make is available
if ! command -v make &> /dev/null; then
    echo "Error: make is not installed"
    echo "Please install make or run manually:"
    echo "  cd demo_site && python manage.py runserver"
    exit 1
fi

# Run via Makefile
exec make demo-run
