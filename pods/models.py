from django.db import models


class Podcast(models.Model):
    uuid = models.UUIDField()
    title = models.CharField(max_length=254)
    friendly_title = models.CharField(max_length=254, blank=True, null=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    categories = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_friendly_title(self):
        return self.friendly_title
