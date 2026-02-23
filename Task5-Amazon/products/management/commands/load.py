import requests
from django.core.management.base import BaseCommand
from products.models import Product, Category


class Command(BaseCommand):
    help = 'Seed database with products from fakestoreapi.com'

    def handle(self, *args, **kwargs):
        self.stdout.write('Fetching products from fakestoreapi...')

        try:
            data = requests.get('https://fakestoreapi.com/products', timeout=10).json()
        except Exception as e:
            self.stderr.write(f'Failed to fetch: {e}')
            return

        for item in data:
            category, _ = Category.objects.get_or_create(name=item['category'])
            product, created = Product.objects.get_or_create(
                name=item['title'],
                defaults={
                    'price': item['price'],
                    'description': item['description'],
                    'stock': 10,
                    'is_available': True,
                    'category': category,
                    'image_url': item['image'],
                }
            )
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'  [{status}] {product.name}')

        self.stdout.write(self.style.SUCCESS('Done! Database seeded.'))