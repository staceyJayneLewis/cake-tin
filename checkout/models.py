import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField
from decimal import Decimal

from products.models import Product
from profiles.models import UserProfile


class Order_details(models.Model):
    class Meta:
        verbose_name_plural = 'Orders'

    order_number = models.CharField(max_length=100, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    contact_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    address_line_1 = models.CharField(max_length=80, null=False, blank=False)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    sub_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _order_id(self):
        """ Create unique id order number for items """

        return uuid.uuid4().hex.upper()

    def order_total_update(self):
        """Update grand total each time new item is added including delivery"""

        self.sub_total = self.items_ordered.aggregate(
            Sum('item_ordered_total'))['item_ordered_total__sum'] or 0
        self.delivery = Decimal(settings.STANDARD_DELIVERY)
        self.order_total = self.sub_total + self.delivery
        self.save()

    def save(self, *num, **data):
        """Add order number if it hasn't been added already."""
        if not self.order_number:
            self.order_number = self._order_id()
        super().save(*num, **data)

    def __str__(self):
        return self.order_number


class Item_ordered(models.Model):
    class Meta:
        verbose_name_plural = 'Items'

    order = models.ForeignKey(
        Order_details, null=False, blank=False,
        on_delete=models.CASCADE, related_name='items_ordered')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    item_ordered_total = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """Set the items ordered total and update the overall total."""
        self.item_ordered_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Your order number : {self.order.order_number}'
