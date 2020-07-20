from django import forms
from .models import Podcast, Category


class PodcastForm(forms.ModelForm):
    """ A form for submitting podcasts to the database """

    class Meta:
        model = Podcast
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'category_choices_field'
