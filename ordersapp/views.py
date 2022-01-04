from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, \
    DetailView, DeleteView

from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderListView(ListView):
    model = Order


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order,
            OrderItem,
            form=OrderItemForm,
            extra=1
        )
        if self.request.method == 'POST':
            formset = OrderFormSet(self.request.POST)
        else:
            formset = OrderFormSet()

        context_data['orderitems'] = formset

        return context_data


class OrderUpdateView(UpdateView):
    pass


class OrderDetailView(DetailView):
    pass


class OrderDeleteView(DeleteView):
    pass


def complete(request, pk):
    pass
