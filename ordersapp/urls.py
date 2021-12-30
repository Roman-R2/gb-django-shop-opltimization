from django.urls import path
from ordersapp.views import OrderListView, OrderCreateView, OrderUpdateView, \
    OrderDeleteView, OrderDetailView, complete

app_name = 'ordersapp'

urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    path('create/', OrderCreateView.as_view(), name='create'),
    path('update/<pk: int>/', OrderUpdateView.as_view(), name='update'),
    path('read/<pk: int>/', OrderDetailView.as_view(), name='read'),
    path('delete/<pk: int>/', OrderDeleteView.as_view(), name='delete'),
    path('complete/<pk: int>/', complete, name='complete')
]
