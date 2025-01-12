from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Creates default categories if they do not exist'

    def handle(self, *args, **kwargs):
        # Delete all existing categories
        Category.objects.all().delete()
        
        categories = [
            {
                'name': 'Electronics',
                'description': 'Phones, Computers, and other electronic devices'
            },
            {
                'name': 'Fashion',
                'description': 'Men, Women, and Kids clothing'
            },
            {
                'name': 'Home & Garden',
                'description': 'Furniture, Decor, and Garden tools'
            },
            {
                'name': 'Sports',
                'description': 'Sports equipment, clothing, and fitness tools'
            },
            {
                'name': 'Automotive',
                'description': 'Cars, Parts, and Accessories'
            },
            {
                'name': 'Books & Entertainment',
                'description': 'Books, Games, and Entertainment'
            },
            {
                'name': 'Health & Beauty',
                'description': 'Cosmetics, Personal Care, and Health products'
            },
        ]

        for category_data in categories:
            category = Category.objects.create(
                name=category_data['name'],
                description=category_data['description']
            )
            self.stdout.write(f'Created category "{category.name}" with slug "{category.slug}"')
