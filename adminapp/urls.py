from django.urls import path

from adminapp.views import user_create, user_update, user_delete, \
    categories, products, product_update, product_delete, \
    UsersListView, CategoryCreate, CategoryUpdate, DeleteCategory, \
    ProductDetail, ProductCreate

app_name = 'adminapp'

urlpatterns = [
    path('users/', UsersListView.as_view(), name='users'),
    path('user/create/', user_create, name='user_create'),
    path('user/update/<int:pk>/', user_update, name='user_update'),
    path('user/delete/<int:pk>/', user_delete, name='user_delete'),

    path('categories/', categories, name='categories'),
    path('category/create/', CategoryCreate.as_view(), name='category_create'),
    path(
        'category/update/<int:pk>/',
        CategoryUpdate.as_view(),
        name='category_update'
    ),
    path(
        'category/delete/<int:pk>/',
        DeleteCategory.as_view(),
        name='category_delete'
    ),

    path('products/<int:pk>/', products, name='products'),
    path(
        'products/create/in_category/<int:pk>/',
        ProductCreate.as_view(),
        name='product_create'
    ),
    path('products/update/<int:pk>/', product_update, name='product_update'),
    path('products/delete/<int:pk>/', product_delete, name='product_delete'),
    path('products/read/<int:pk>/', ProductDetail.as_view(),
         name='product_read'),

]
