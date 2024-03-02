from django.shortcuts import render, reverse, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST

from products.models import Product
from .models import Order_details, Item_ordered

from .forms import form_order_request
from basket.contexts import basket_order
import stripe
import json

@require_POST
def cache_checkout_data(request):
        try:
            pid = request.POST.get('client_secret').split('_secret')[0]
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.PaymentIntent.modify(pid, metadata={
                'basket_session': json.dumps(request.session.get('basket_session', {})),
                'save_details': request.POST.get('save-details'),
                'username': request.user,
            })
            return HttpResponse(status=200)
        except Exception as e:
            messages.error(request, 'Sorry, your payment cannot be \
                processed right now. Please try again later.')
            return HttpResponse(content=e, status=400)

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        basket = request.session.get('basket_session', {})

        form_details = {
        'full_name': request.POST['full_name'],
        'email': request.POST['email'],
        'contact_number': request.POST['contact_number'],
        'country': request.POST['country'],
        'postcode': request.POST['postcode'],
        'town_or_city': request.POST['town_or_city'],
        'address_line_1': request.POST['address_line_1'],
        'address_line_2': request.POST['address_line_2'],
        }

        order_form = form_order_request(form_details)

        # checking form is valid
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in basket.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = Item_ordered(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                    order_line_item.save()

                except Product.DoesNotExist:
                    messages.error(request, (
                        "There was an issue with an item in your basket, please contact us.")
                    )
                    order.delete()
                    return redirect(reverse('basket'))

            request.session['save-details'] = 'save_details' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(
                request, 
                'There was an error with your form, please correct any errors.'
            )
    else:
        basket_session = request.session.get('basket_session', {})
        if not basket_session:
            messages.error(request, 'There are no items in your basket')
            return redirect(reverse('all_products'))

        current_basket = basket_order(request)
        total = current_basket['order_total']
        stripe_amount = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(amount=stripe_amount, currency=settings.STRIPE_CURRENCY)

        order_request = form_order_request()

        template = 'checkout/checkout.html'
        context = {
            'order_request': order_request,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)

def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order_details, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'basket_session' in request.session:
        del request.session['basket_session']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
