from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductFormAdmin

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


def add_product(request):
    """Add product to store through the admin"""
    if request.method == 'POST':
        form = ProductFormAdmin(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Unable to add product. Please ensure the form is valid.')
    else:
        form = ProductFormAdmin()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
