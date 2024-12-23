#!/bin/bash

set -e # Exit script immediately on first error

# Check if .env file exists
if [ -f .env ]; then
  # Read and export variables from .env file
  export $(cat .env | xargs)
fi

# Clean package directories if they exist
[ -d dist ] && rm -rf dist

# Remove all .egg-info directories if they exist
find . -name "*.egg-info" -type d -exec rm -rf {} +

# Clean all __pycache__ directories
find . -name "__pycache__" -type d -exec rm -rf {} +

# Run npm build before publishing
npm --prefix djing_ui install
npm --prefix djing_ui run build

# Check if CYTHONIZE_ENABLED is set to True
if [ "$CYTHONIZE_ENABLED" = "true" ]; then
  echo "Cythonization and stub generation are enabled."

  # Generate stubs
  python manage_stubs.py generate

  # Generate .so modules using Cython
  python cythonize.py build_ext --inplace
else
  echo "Cythonization and stub generation are skipped."
fi

# Publish package using Twine
poetry publish --username "$PYPI_USERNAME" --password "$PYPI_PASSWORD" --build
