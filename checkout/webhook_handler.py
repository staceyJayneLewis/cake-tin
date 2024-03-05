from django.http import HttpResponse

from .models import Order_details, Item_ordered
from products.models import Product

import json
import time
import stripe

class StripeWebhook_Handler:
    """Manages the Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """Manage all types of webhook event"""

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket_session
        save_info = intent.metadata.save_info

        # Get the charge object
        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        order_total = round(stripe_charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order_details.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    contact_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    address_line_1__iexact=shipping_details.address.line1,
                    address_line_2__iexact=shipping_details.address.line2,
                    order_total=order_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )

                order_exists = True
                break

            except Order_details.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order_details.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    contact_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    address_line_1=shipping_details.address.line1,
                    address_line_2=shipping_details.address.line2,
                    order_total=order_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )

                for item_id, item_data in json.loads(basket).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = Item_ordered(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: {event["type"]} | ERROR: {e}', status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
