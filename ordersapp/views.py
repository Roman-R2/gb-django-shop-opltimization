from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, \
    DetailView, DeleteView

from ordersapp.models import Order


class OrderListView(ListView):
    model = Order


class OrderCreateView(CreateView):
    pass


class OrderUpdateView(UpdateView):
    pass


class OrderDetailView(DetailView):
    pass


class OrderDeleteView(DeleteView):
    pass


def complete(request, pk):
    pass
