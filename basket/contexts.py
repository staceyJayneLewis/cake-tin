from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def basket_order(request):

    basket_items = []
    order_total = 0
    number_of_items = 0
    basket_session = request.session.get('basket_session', {})

    for item, quantity in basket_session.items():
        product = get_object_or_404(Product, pk=item)
        total += quantity * product_price
        product_count += quantity
        basket_items.append({
            'item': item,
            'quantity': quantity,
            'product':product,
        })


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