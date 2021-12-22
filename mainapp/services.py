from basketapp.models import Basket
from mainapp.models import Product, Category


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


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


def get_links_menu():
    return Category.objects.all()
