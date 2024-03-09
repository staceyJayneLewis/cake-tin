from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterForm


def newsletter_subscription(request):
    """Return to the contact page """
    form = NewsletterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Piece of cake! You have successfully subscribed."
            )
            return redirect(newsletter_subscription)
        messages.error(
                request,
                "Error, please try again!"
            )
    template = 'newsletter/newsletter.html'
    context = {
        "form": form,
    }
    return render(request, template, context)
    