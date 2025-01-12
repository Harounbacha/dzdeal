#!/usr/bin/env bash
# exit on error
set -o errexit

# Print Python version and path
python --version
echo "PYTHONPATH: $PYTHONPATH"
which python

# Upgrade pip
python -m pip install --upgrade pip

# Install python dependencies
pip install -r requirements.txt

# Create static directory if it doesn't exist
mkdir -p staticfiles

# List installed packages
pip list

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
