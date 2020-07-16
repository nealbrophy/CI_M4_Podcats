from django.contrib import admin
from .models import Podcast, Category


class PodcastAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'title',
        'friendly_title',
        'category',
        'website',
        'itunes_url',
        'image_url',
    )

    ordering = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
        'id',
    )


admin.site.register(Podcast, PodcastAdmin)
admin.site.register(Category, CategoryAdmin)
