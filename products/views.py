from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

# Create your views here.

def all_products(request):
    """ Displays all products, including sorting and searching """

    products = Product.objects.all()
    search_request = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
                categories = request.GET['category'].split(',')
                products = products.filter(category__name__in=categories)
                categories = Category.objects.filter(name__in=categories).first()
                    
        if 'q' in request.GET:
            search_request = request.GET['q']
            if not search_request:
                messages.error(request, "You didn't enter a product to search, please enter the product you are searching for.")
                return redirect(reverse('all_products'))

            search_requests = Q(name__icontains=search_request) | Q(description__icontains=search_request)
            products = products.filter(search_requests)

    context = {
        'products': products,
        'search_query':search_request,
        'current_category': categories,
    }

    return render(request, 'products/products.html', context)


def product_description(request, product_id):
    """ Displays product description page """

    product = get_object_or_404(Product, pk=product_id )

    context = {
        'product': product,
    }

    return render(request, 'products/product_description.html', context)