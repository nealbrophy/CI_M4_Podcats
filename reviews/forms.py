from django import forms
from django.contrib.auth.models import User

from .models import Review
from pods.models import Podcast


class ReviewForm(forms.ModelForm):
    podcast_id = forms.ModelChoiceField(queryset=Podcast.objects.all(), widget=forms.TextInput)
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.TextInput)

    class Meta:
        model = Review
        exclude = ('created',)
        labels = {
            "podcast_id": "",
            "user": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "title": "Enter a title for your review",
            "content": "Type your review here"
        }
        for field in self.fields:
            if field == "podcast_id" or field == "user":
                self.fields[field].widget.attrs["class"] = "d-none form-control-sm"
                self.fields[field].label = ""
            elif field != "rating" and field != "podcast_id":
                self.fields[field].widget.attrs["class"] = "form-control-sm"
                placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder