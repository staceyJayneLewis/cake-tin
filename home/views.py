from django.shortcuts import render

def index(request):
    """Return to the index page """
    return render(request, 'home/index.html')
