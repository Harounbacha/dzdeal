from django.core.cache import cache
from .models import Category

def categories(request):
    # Try to get categories from cache
    categories = cache.get('all_categories')
    
    if categories is None:
        # If not in cache, get from database
        categories = Category.objects.all()
        # Store in cache for 1 hour
        cache.set('all_categories', categories, 3600)
    
    # Print for debugging
    print("Categories from context processor:", [(c.name, c.slug) for c in categories])
    
    return {
        'categories': categories
    }
