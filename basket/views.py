from django.shortcuts import render, redirect

# Create your views here.
def basket(request):
    """ see items in the basket """
    return render(request, 'basket/basket.html')


def add_to_basket(request, item):
    """ add quantity of items to the basket """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket_session = request.session.get('basket_session', {})

    if item in list(basket_session.keys()):
        basket_session[item] += quantity

    else:
        basket_session[item] = quantity

    request.session['basket_session'] = basket_session
    return redirect(redirect_url)