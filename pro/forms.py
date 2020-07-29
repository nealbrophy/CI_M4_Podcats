from django import forms
from .models import Purchase


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ("full_name", "email",
                  "phone_number", "country", "postcode",
                  "town_or_city", "street_address1", "street_address2",)

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
