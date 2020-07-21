from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Podcast(models.Model):
    uuid = models.UUIDField()
    title = models.CharField(max_length=254)
    friendly_title = models.CharField(max_length=254, blank=True, null=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)
    itunes_url = models.URLField(max_length=1024, null=True, blank=True)
    website = models.URLField(max_length=1024, null=True, blank=True)
    itunes_id = models.BigIntegerField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_friendly_title(self):
        return self.friendly_title
