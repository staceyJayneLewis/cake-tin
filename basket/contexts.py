from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def basket_order(request):

    basket_items = []
    sub_total = 0
    total_number_of_items = 0

    basket_session = request.session.get('basket_session', {})

    for item, quantity in basket_session.items():
        product = get_object_or_404(Product, pk=item)
        if product.is_on_sale:
            sub_total += quantity * product.sale_price
        else:
            sub_total += quantity * product.price
        total_number_of_items += quantity
        basket_items.append({
            'item': item,
            'quantity': quantity,
            'product': product,
        })

    delivery = Decimal(settings.STANDARD_DELIVERY)

    order_total = sub_total + delivery

    context = {
        'basket_items': basket_items,
        'sub_total': sub_total,
        'total_number_of_items': total_number_of_items,
        'delivery': delivery,
        'order_total': order_total,
    }

    return context
