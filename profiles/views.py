from django.shortcuts import render

# Create your views here.

def profile(request):
    "return profile page of user"

    template = "profiles/profile.html"
    context = {}

    return render(request, template, context)