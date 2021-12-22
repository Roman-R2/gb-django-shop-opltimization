from django.urls import path

from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),

    path('products/<str:slug>/', views.products, name='categorys'),
    path(
        'products/<str:slug>/<int:page>',
        views.products,
        name='category_paginate'
    ),
    path('product/<str:slug>/', views.product, name='product'),
]
