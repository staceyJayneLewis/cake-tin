from django.shortcuts import render
from .models import Product

# Create your views here.

def all_products(request):
    """ Displays all products, including sorting and searching """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)