#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
python -m pip install --upgrade pip

# Install python dependencies
pip install -r requirements.txt

# Make sure the wsgi.py file is executable
chmod +x wsgi.py

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
