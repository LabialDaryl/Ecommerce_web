from django.core.management.base import BaseCommand
import requests
from decimal import Decimal, InvalidOperation
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from shop.models import Product, Category


def fetch_products():
    urls = [
        'https://fakestoreapi.com/products',
        'https://dummyjson.com/products',
        'https://api.escuelajs.co/api/v1/products',
    ]

    for url in urls:
        response = requests.get(url)
        data = response.json()
        items = data['products'] if 'products' in data else data  # Handle both formats

        for item in items:
            # DummyJSON has nested 'category' as a string, not a dict
            cat_raw = item.get('category')
            cat_name = cat_raw['name'] if isinstance(cat_raw, dict) else str(cat_raw)
            cat_name = cat_name.title()
            category, _ = Category.objects.get_or_create(name=cat_name)

            product_name = item.get('title') or item.get('name')
            description = item.get('description', '')
            raw_price = item.get('price')

            try:
                price = Decimal(str(raw_price)).quantize(Decimal('0.01'))
            except (InvalidOperation, TypeError, ValueError):
                print(f"❌ Skipping product {item.get('id')!r}: invalid price {raw_price!r}")
                continue

            # Handle both 'image' (string) and 'images' (list or string)
            raw_images = item.get('images') or item.get('image')
            if isinstance(raw_images, str):
                images = [raw_images]
            elif isinstance(raw_images, list):
                images = raw_images
            else:
                images = []

            main_image_url = images[0] if images else None

            Product.objects.get_or_create(
                title=product_name,
                defaults={
                    'category': category,
                    'description': description,
                    'price': price,
                    'image': main_image_url,
                    'stock': 100,  # Default stock value
                }
            )


class Command(BaseCommand):
    help = 'Fetch products from API and store in database'

    def handle(self, *args, **kwargs):
        fetch_products()
        self.stdout.write(self.style.SUCCESS('Products fetched successfully'))