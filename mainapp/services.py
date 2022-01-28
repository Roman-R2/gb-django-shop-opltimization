from django.conf import settings
from django.core.cache import cache

from mainapp.models import Product, Category


def get_hot_product(current_category):
    return Product.objects.order_by('?').filter(
        category=current_category).first()


def get_same_products(hot_product):
    if hot_product:
        same_products_list = Product.objects.filter(
            category=hot_product.category
        ).exclude(pk=hot_product.pk)
        return same_products_list[:3]
    return []


# def get_links_menu():
#     return Category.objects.all()


def get_links_menu():
    """Решит забрать список категорий из базы или из кэша"""
    if settings.LOW_CACHE:
        # Ключ, по которому информация лежит в кэше
        key = "links_menu"
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = Category.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return Category.objects.filter(is_active=True)
