from django.contrib import admin
from .models import Podcast, Category


class PodcastAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'friendly_title',
        'category',
        'language',
        'website',
        'image_url',
    )

    ordering = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
    )

admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Category, CategoryAdmin)
