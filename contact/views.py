from django.shortcuts import render

def contact(request):
    """Return to the contact page """
    return render(request, 'contact/contact-us.html')