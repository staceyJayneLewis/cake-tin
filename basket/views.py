from django.shortcuts import render, redirect, reverse, HttpResponse

# Create your views here.
def basket(request):
    """ View items in the basket """
    return render(request, 'basket/basket.html')


def add_to_basket(request, item):
    """ Add quantity of items to the basket """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket_session = request.session.get('basket_session', {})

    if item in list(basket_session.keys()):
        basket_session[item] += quantity

    else:
        basket_session[item] = quantity

    request.session['basket_session'] = basket_session
    return redirect(redirect_url)


def amend_basket(request, item):
    """ Amend quantity of items in basket """

    quantity = int(request.POST.get('quantity'))
    basket_session = request.session.get('basket_session', {})

    if quantity > 0:
        basket_session[item] = quantity
    else:
        basket_session.pop(item)
        
    request.session['basket_session'] = basket_session
    return redirect(reverse('basket'))


def remove_basket(request, item):
    """ Remove selected item from basket """
    
    try:
        basket_session = request.session.get('basket_session', {})
        basket_session.pop(item)
            
        request.session['basket_session'] = basket_session
        return HttpResponse(status=200)
    
    except Exception as e:
        return HttpResponse(status=500)
