from django.shortcuts import render
from products.models import Product

def index(request):
    """Return to the index page """
    products = Product.objects.order_by('?')[:2]
    template = 'home/index.html'
    context = {
        'products': products,
    }
    return render(request, template, context)
