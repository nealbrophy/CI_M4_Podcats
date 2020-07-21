from django import forms
from .models import Podcast, Category


class PodcastForm(forms.ModelForm):
    """ A form for submitting podcasts to the database """

    class Meta:
        model = Podcast
        fields = ('title', 'image_url', 'image', 'category', 'itunes_url', 'website', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        placeholders = {
            'title': 'Podcast name',
            'image_url': 'URL for podcast image',
            'image': 'Upload an image',
            'itunes_url': 'iTunes page for this podcast',
            'website': 'Homepage of this podcast',
            'description': 'Describe the podcast',
            'category': 'Select category'
        }

        self.fields['category'].choices = friendly_names
        self.fields['title'].widget.attrs['autofocus'] = True
        self.fields['title'].widget.attrs['required'] = True
        self.fields['description'].widget.attrs['required'] = True

        for field in self.fields:
            if field != 'category':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                    self.fields[field].widget.attrs['placeholder'] = placeholder
                else:
                    placeholder = placeholders[field]
                    self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].label = False

