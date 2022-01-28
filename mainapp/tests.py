from django.test import TestCase

from authapp.statuses import status
from mainapp.models import Category, Product


class MainAppSmokeTest(TestCase):

    def setUp(self):
        category = Category.objects.create(
            name='cat_1',
            slug='cat_1',
            description='test_cat_description',
        )
        for i in range(10):
            Product.objects.create(
                category=category,
                slug=f'prod_{i}',
                name=f'prod_{i}',
                description='test_description',
                price=100,
            )

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_categories_urls(self):
        for cat in Category.objects.all():
            response = self.client.get(f'/products/{cat.slug}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_urls(self):
        for prod in Product.objects.all():
            response = self.client.get(f'/product/{prod.slug}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        pass
