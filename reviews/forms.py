from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ('created', 'user', 'podcast_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
