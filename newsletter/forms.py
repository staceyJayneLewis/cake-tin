from django import forms
from .models import NewsletterUser


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterUser
        fields = "__all__"
