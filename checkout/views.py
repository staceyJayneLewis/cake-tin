from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.conf import settings
from .forms import form_order_request
from basket.contexts import basket_order
import stripe 

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    basket_session = request.session.get('basket_session', {})
    if not basket_session:
        messages.error(request, 'There are no items in your basket')
        return redirect(reverse('all_products'))

    current_basket = basket_order(request)
    total = current_basket['order_total']
    stripe_amount = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(amount=stripe_amount, currency=settings.STRIPE_CURRENCY)

    print(intent)

    order_request = form_order_request()
    template = 'checkout/checkout.html'
    context = {
        'order_request': order_request,
        'stripe_public_key': 'stripe_public_key',
        'client_secret_key': 'intent.client_secret_key',
    }

    return render(request, template, context)
