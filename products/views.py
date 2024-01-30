from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product

# Create your views here.

def all_products(request):
    """ Displays all products, including sorting and searching """

    products = Product.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter a product to search, please enter the product you are searching for.")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)

            products = products.filter(queries)

    context = {
        'products': products,
        'search_item':query,
    }

    return render(request, 'products/products.html', context)


def product_description(request, product_id):
    """ Displays product description page """

    product = get_object_or_404(Product, pk=product_id )

    context = {
        'product': product,
    }

    return render(request, 'products/product_description.html', context)