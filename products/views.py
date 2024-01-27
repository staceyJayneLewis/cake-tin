from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def all_products(request):
    """ Displays all products, including sorting and searching """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_description(request, product_id):
    """ Displays product description page """

    product = get_object_or_404(Product, pk=product_id )

    context = {
        'product': product,
    }

    return render(request, 'products/product_description.html', context)