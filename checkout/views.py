from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from .forms import form_order_request

def checkout(request):
    basket_session = request.session.get('basket_session', {})
    if not basket_session:
        messages.error(request, 'There are no items in your basket')
        return redirect(reverse('all_products'))


    order_request = form_order_request()
    template = 'checkout/checkout.html'
    context = {
        'order_request': order_request,
    }

    return render(request, template, context)
