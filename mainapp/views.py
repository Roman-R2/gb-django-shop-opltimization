import json
from urllib.request import urlopen

from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from mainapp.models import Category, Product
from mainapp.services import get_hot_product, get_same_products, \
    get_links_menu


def index(request):
    PRODUCT_COUNT = 4

    products = Product.objects.all()[:PRODUCT_COUNT]
    context = {
        "products": products,
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, slug=None, page=1):
    if slug is None or slug == "all":
        this_category = {"name": "Все", "slug": "all"}
        products_list = Product.objects.all()
        hot_product = products_list.order_by('?').first()
    else:
        this_category = get_object_or_404(Category, slug=slug)
        products_list = Product.objects.filter(category__slug=slug)
        hot_product = get_hot_product(this_category)

    paginator = Paginator(products_list, 3)

    # Плохой код ... для напоминания
    # try:
    #     products_paginator = paginator.page(page)
    # except PageNotAnInteger:
    #     # products_paginator = paginator.page(1)
    #     raise Http404
    # except EmptyPage:
    #     # products_paginator = paginator.page(paginator.num_pages)
    #     raise Http404

    if 0 > page or page > paginator.num_pages:
        raise Http404

    products_paginator = paginator.page(page)

    context = {
        'links_menu': get_links_menu(),
        'products_list': products_paginator,
        'this_category': this_category,
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
    }
    return render(request, 'mainapp/products.html', context=context)


def contact(request):
    url = 'https://jsonplaceholder.typicode.com/users'
    json_response = urlopen(url)
    fake_json = json.loads(json_response.read())

    context = {
        "contacts": fake_json[:3],
    }

    return render(request, 'mainapp/contact.html', context=context)


def product(request, slug):
    context = {
        'links_menu': get_links_menu(),
        'product': get_object_or_404(Product, slug=slug),
    }
    return render(request, 'mainapp/product.html', context=context)
