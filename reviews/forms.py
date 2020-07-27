from django import forms
from .models import Review
from pods.models import Podcast


class ReviewForm(forms.ModelForm):
    podcast_id = forms.ModelChoiceField(queryset=Podcast.objects.all(), widget=forms.TextInput)

    class Meta:
        model = Review
        exclude = ('created', 'user',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
