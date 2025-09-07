from django.core.management import BaseCommand, call_command
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Load test categories and products with extra products'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        try:
            call_command('loaddata', 'categories.json', app_label='catalog')
            self.stdout.write(self.style.SUCCESS('Categories loaded from fixture'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Categories not loaded: {e}'))

        try:
            call_command('loaddata', 'products.json', app_label='catalog')
            self.stdout.write(self.style.SUCCESS('Products loaded from fixture'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Products not loaded: {e}'))

        extra_products = [
            {'name': 'Apple Watch', 'description': 'Умные часы', 'price': 500.00, 'category': Category.objects.get(name='Телефоны')},
            {'name': 'iPad', 'description': 'Планшет Apple', 'price': 800.00, 'category': Category.objects.get(name='Телефоны')},
            {'name': 'Gaming Laptop', 'description': 'Ноутбук для игр', 'price': 3000.00, 'category': Category.objects.get(name='Ноутбуки')},
        ]

        for prod_data in extra_products:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'category': prod_data['category'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Extra product added: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))
