from django.db import models
from order.enums import OrderStatus
from order.querysets import OrderQuerySet

from django.db.models import Sum


class Order(models.Model):
    customer = models.ForeignKey('user_management.Customer', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default=OrderStatus.PENDING, choices=OrderStatus.choices)
    total_price = models.FloatField(default=0)
    
    objects = OrderQuerySet.as_manager()

    def calculate_total_price(self):
        total_price = self.orderitem_set.aggregate(total=Sum(models.F('product__price') * models.F('quantity')))['total']
        return round(total_price or 0, 2)

    def accept(self):
        self.status = OrderStatus.ACCEPTED
        self.save()

    def reject(self):
        self.status = OrderStatus.REJECTED
        self.save()

    def deliver(self):
        self.status = OrderStatus.DELIVERED
        self.save()

    def cancel(self):
        self.status = OrderStatus.CANCELLED
        self.save()


class OrderItemManager(models.Manager):
    def create(self, **kwargs):
        order_item = super().create(**kwargs)
        order_item.order.total_price = order_item.order.calculate_total_price()
        order_item.order.save()
        return order_item


class OrderItem(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    objects = OrderItemManager()

    def __str__(self):
        return f'{self.order.customer.user.username} - {self.product.name}'

    def save(self, *args, **kwargs):
        """You can not modify this method"""
        self.order.total_price = self.order.calculate_total_price()
        self.order.save()
        super().save(*args, **kwargs)