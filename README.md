# E-Commerce Website

A Django-based e-commerce website with user authentication, product listing, and an admin dashboard.

## Features

- User Authentication (Login, Register, Logout)
- Product Catalog with Categories
- Product Details with Image Support
- Admin Dashboard for Product Management
- Responsive Design using Bootstrap 5

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Visit the admin interface at `http://127.0.0.1:8000/admin/` to add products and categories.

## Project Structure

- `core/` - Main application directory
  - `models.py` - Database models for Product and Category
  - `views.py` - View functions for handling requests
  - `urls.py` - URL routing
  - `admin.py` - Admin interface configuration
  - `templates/` - HTML templates
    - `base.html` - Base template with common layout
    - `home.html` - Homepage template
    - `product_list.html` - Product listing template
    - `product_detail.html` - Product detail template
    - `category_products.html` - Category-specific products template

## Technologies Used

- Django 5.1.2
- Python 3.x
- Bootstrap 5
- SQLite (default database)
- django-allauth for authentication
- Pillow for image handling
- django-crispy-forms for form styling
