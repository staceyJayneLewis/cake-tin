from django.shortcuts import render

# Create your views here.
def basket(request):
    """ see items in the basket """
    return render(request, 'basket/basket.html')
