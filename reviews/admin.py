from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'podcast_id',
        'title',
        'content',
        'rating',
        'created',
        'user',
    )

    ordering = ('created',)

admin.site.register(Review, ReviewAdmin)

