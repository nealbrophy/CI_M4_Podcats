from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'podcast_id',
        'title',
        'content',
        'rating',
        'created',
    )

    ordering = ('created',)

admin.site.register(Review, ReviewAdmin)
