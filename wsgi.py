"""
WSGI config for ecommerce_project project.
"""

import os
import sys

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# For Gunicorn
app = application
