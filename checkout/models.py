from django.db import models
from django.db.models import Sum
from django.conf import settings
from products.models import Product
import uuid

class Order_details(models.Model):
    order_number = models.CharField(max_length=30, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    contact_number = models.CharField(max_length=20, null=False, blank=False)
    address_line_1 = models.CharField(max_length=80, null=False, blank=False)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=40, null=False, blank=False)
    delivery = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def _order_id(self):
        """ Create unique id order number for items """

        return uuid.uuid4().hex.upper()

    def grand_total_update(self):
        """Update grand total each time new item is added including delivery"""

        self.sub_total = self.items_ordered.aggregate(Sum('item_ordered_total'))['order_total__sum']
        self.delivery =  settings.STANDARD_DELIVERY
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
    order = models.ForeignKey(Order_details, null=False, blank=False, on_delete=models.CASCADE, related_name='items_ordered')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    item_ordered_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *price, **data):
        """Set the items ordered total and update the overall total."""
        self.item_ordered_total = self.product.price * self.quantity
        super().save(*price, **data)

    def __str__(self):
        return f'Your order number : {self.order.order_number}'

