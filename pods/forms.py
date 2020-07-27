from django import forms
from .models import Podcast, Category
from django.forms.widgets import CheckboxSelectMultiple
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import InlineCheckboxes


class PodcastForm(forms.ModelForm):
    """ A form for submitting podcasts to the database """

    class Meta:
        model = Podcast
        exclude = ("title", "uuid", "itunes_id")
        labels = {
            "friendly_title": "Name*",
            "category": "Categories <small>(ctrl+click to select more than one)</small>"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.friendly_name) for c in categories]
        placeholders = {
            "friendly_title": "Friendly name",
            "title": "Podcast name",
            "image_url": "URL for podcast image",
            "itunes_url": "iTunes page for this podcast",
            # "itunes_id": "The iTunes ID for this podcast",
            "website": "Homepage of this podcast",
            "description": "Describe the podcast",
            "category": "Select category"
        }

        self.fields["category"].choices = friendly_names
        self.fields["category"].widget.attrs["class"] = " mdb-select md-form mb-4 initialized"
        self.fields["friendly_title"].widget.attrs["required"] = True
        self.fields["description"].widget.attrs["required"] = True
        self.fields["description"].widget.attrs["rows"] = 3

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "input-sm form-control"
            if field != "category" and field != "image":
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                    self.fields[field].widget.attrs["placeholder"] = placeholder
                elif field != "image":
                    placeholder = placeholders[field]
                    self.fields[field].widget.attrs["placeholder"] = placeholder

    def clean_title(self):
        title = self.cleaned_data["friendly_title"].replace(" ", "")
        title = title.lower()
        return title
