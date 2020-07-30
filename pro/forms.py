from django import forms
from django.contrib.auth.models import User
from .models import Purchase



class PurchaseForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.TextInput)
    class Meta:
        model = Purchase
        fields = ("full_name", "email",
                  "phone_number", "country", "postcode",
                  "town_or_city", "street_address1",
                  "street_address2", "user")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "country": "Country",
            "postcode": "Postal/Zip Code",
            "town_or_city": "Town or City",
            "street_address1": "Street Address 1",
            "street_address2": "Street Address 2",
            "county": "County",
            "user": "",
        }

        self.fields["full_name"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f"{placeholders[field]} *"
                self.fields[field].widget.attrs["placeholder"] = placeholder
            else:
                placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "stripe-style-input form-control"
            self.fields[field].label = False
            if self.fields[field] == "user":
                self.fields[field].widget.attrs["class"] = "d-none"
