from django.core.management import BaseCommand
from django.db.models import Q

from mainapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        sofas_cat_query = Q(category__name='Диваны')
        chairs_cat_query = Q(category__name='Cтулья')

        print(sofas_cat_query)
        print(type(sofas_cat_query))

        products_list = Product.objects.filter(
            sofas_cat_query | chairs_cat_query
        )
        print(products_list.query)
        print(products_list)

        products_list_2 = Product.objects.filter(
            category__name__in=['Диваны', 'Cтулья']
        )
        print(products_list_2.query)
        print(products_list_2)
