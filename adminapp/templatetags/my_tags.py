from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='or_default_avatar')
def or_default_avatar(avatar):
    if not avatar:
        avatar = 'users/def_avatar.png'

    return f'{settings.MEDIA_URL}{avatar}'


def or_default_product(image):
    if not image:
        image = 'products/def_product.png'

    return f'{settings.MEDIA_URL}{image}'


register.filter('or_default_product', or_default_product)
