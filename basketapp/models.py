from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product


# # Менеджер объектов для обработки QuerySet
# class BasketQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         # self это QuerySet
#         for item in self:
#             # Если заказ удаляем, то вернем товары обратно на склад
#             item.product.quantity += item.quantity
#             item.product.save()
#         super().delete(*args, **kwargs)


class Basket(models.Model):
    # # Укажем, что менеджером объектов теперь является BasketQuerySet
    # object = BasketQuerySet.as_manager()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_item_cached(self):
        return self.user.basket.select_related()

    @property
    def total_quantity(self):
        # items = Basket.objects.filter(user=self.user)
        items = self.get_item_cached
        _total_quantity = sum([x.quantity for x in items])
        return _total_quantity

    @property
    def total_cost(self):
        # items = Basket.objects.filter(user=self.user)
        items = self.get_item_cached
        _total_cost = sum([x.product_cost for x in items])
        return _total_cost

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
