from django import forms
from .models import Podcast, Category


class PodcastForm(forms.ModelForm):
    """ A form for submitting podcasts to the database """

    class Meta:
        model = Podcast
        fields = ('friendly_title', 'image_url', 'image', 'category', 'itunes_url', 'website', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        placeholders = {
            'friendly_title': 'Podcast name',
            'image_url': 'URL for podcast image',
            'image': 'Upload an image',
            'itunes_url': 'iTunes page for this podcast',
            'website': 'Homepage of this podcast',
            'description': 'Describe the podcast',
        }

        self.fields['category'].choices = friendly_names
        self.fields['friendly_title'].widget.attrs['autofocus'] = True
        self.fields['friendly_title'].widget.attrs['required'] = True
        self.fields['description'].widget.attrs['required'] = True

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
        self.fields['description'].widget.attrs['placeholder'] = placeholder
        self.fields[field].label = False

