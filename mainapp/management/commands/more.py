from django.core.management import BaseCommand

from mainapp.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        Product.objects.create(
            category=Category.objects.get(pk=1),
            name='Мегастул',
            slug='megastul',
            description='Много описания',
            price='3100.50',
            created_at="2021-11-24T07:54:41.409Z",
            quantity=99,
        )
        print("Мегастул создан!")
