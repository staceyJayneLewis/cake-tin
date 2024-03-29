from django import forms
from .models import Order_details


class form_order_request(forms.ModelForm):
    class Meta:
        model = Order_details
        fields = ('full_name', 'address_line_1', 'address_line_2',
                  'town_or_city', 'postcode', 'country', 'email',
                  'contact_number')

    def __init__(self, *args, **kwargs):
        """Add placeholders """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'address_line_1': 'Address Line 1',
            'address_line_2': 'Address Line 2',
            'town_or_city': 'Town/City',
            'postcode': 'Postcode',
            'email': 'Email Address',
            'contact_number': 'Contact Number',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
