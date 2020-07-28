from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    raw_id_fields = ('podcast_id', 'user',)
    list_display = (
        'id',
        'podcast_id',
        'title',
        'rating',
        'created',
        'user_id',
    )

    ordering = ('created',)

admin.site.register(Review, ReviewAdmin)

