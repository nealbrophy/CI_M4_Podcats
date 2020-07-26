from django.db import models
import uuid


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254, default=None)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.friendly_name

    def get_name(self):
        return self.name


class Podcast(models.Model):
    class Meta:
        ordering = ['title']

    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=254)
    friendly_title = models.CharField(max_length=254, blank=True, null=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ManyToManyField('Category', blank=True)
    itunes_url = models.URLField(max_length=1024, null=True, blank=True)
    website = models.URLField(max_length=1024, null=True, blank=True)
    itunes_id = models.BigIntegerField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_friendly_title(self):
        return self.friendly_title

    def get_category(self):
        return self.category.count()
