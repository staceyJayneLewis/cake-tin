from decimal import Decimal
from django.conf import settings

def basket_order(request):

    basket_items = []
    order_total = 0
    number_of_items = 0

    delivery = order_total * Decimal(settings.STANDARD_DELIVERY / 100)

    grand_total = order_total + delivery

    context = {
        'basket_items': basket_items,
        'order_total': order_total,
        'number_of_items': number_of_items,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context