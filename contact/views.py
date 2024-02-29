from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contact(request):
    """Return to the contact page """
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks for your message we will be in touch soon! "
            )
            return redirect(contact)
        messages.error(
                request,
                "Error, please try again!"
            )
    template = 'contact/contact-us.html'
    context = {
        "form": form,
    }
    return render(request, template, context)
