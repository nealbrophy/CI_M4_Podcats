from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from pods.models import Podcast
from eos_name_generator import RandomNameGenerator


class Review(models.Model):

    podcast_id = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    content = models.TextField()
    RATINGS_CHOICES = (
        ('', 'Select a rating'),
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    rating = models.CharField(max_length=1, choices=RATINGS_CHOICES, default='0')
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
