from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, \
    DetailView, DeleteView


class OrderListView(ListView):
    pass


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
