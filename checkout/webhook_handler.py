from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

from .models import Order_details, Item_ordered
from products.models import Product
from profiles.models import UserProfile

import json
import time
import stripe


class StripeWebhook_Handler:
    """Manages the Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

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

        # Update profile info if save details button checked
        profile = None
        username = intent.metadata.username
        if username != "AnonymousUser":
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_contact_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_address_line_1 = shipping_details.address.line1
                profile.default_address_line_2 = shipping_details.address.line2
                profile.save()

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
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',  # noqa
                status=200)
        else:
            order = None
            try:
                order = Order_details.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
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
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',  # noqa
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
