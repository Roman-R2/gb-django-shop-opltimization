from django.conf import settings
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    STATUS_FORMING = 'forming'
    STATUS_SEND_TO_PROCEED = 'send to proceed'
    STATUS_PROCEEDED = 'proceeded'
    STATUS_PAID = 'paid'
    STATUS_CANCEL = 'cancel'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_FORMING, 'формируется'),
        (STATUS_SEND_TO_PROCEED, 'отправлено в обработку'),
        (STATUS_PROCEEDED, 'обработано'),
        (STATUS_PAID, 'оплачено'),
        (STATUS_CANCEL, 'отменено'),
        (STATUS_DONE, 'завершено'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        choices=STATUSES,
        default=STATUS_FORMING,
        max_length=30
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_related_items(self):
        return self.orderitems.select_related()

    def get_total_quantity(self):
        return sum(
            x.quantity
            for x in self.get_related_items()
        )
        # _total_quantity = sum(list(map(lambda x: x.quantity, _items)))

    def get_total_cost(self):
        return sum(
            x.quantity * x.product.price
            for x in self.get_related_items()
        )


class OrderItem(models.Model):
    """Связывает основной заказ с продуктами и хранит количество этих
    продуктов"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='orderitems'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество'
    )

    def get_product_cost(self):
        return self.product.price * self.quantity
