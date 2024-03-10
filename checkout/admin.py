from django.contrib import admin
from .models import Order_details, Item_ordered


class Item_ordered_admin_inline(admin.TabularInline):
    model = Item_ordered
    readonly_fields = ('item_ordered_total',)


class Order_admin(admin.ModelAdmin):
    inlines = (Item_ordered_admin_inline,)
    readonly_fields = (
        'order_number', 'user_profile', 'sub_total', 'order_total', 'delivery',
        'date', 'original_basket', 'stripe_pid'
    )

    order_of_fields_displayed = (
        'order_number', 'full_name', 'address_line_1',
        'address_line_2', 'town_or_city', 'postcode', 'country', 'email',
        'contact_number', 'sub_total', 'delivery',
        'order_total', 'date', 'original_basket', 'stripe_pid'
        )

    ordering = ('-date',)


admin.site.register(Order_details, Order_admin)
