from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'nickname',
        'pro_user',
        'id',
    )


admin.site.register(UserProfile, UserProfileAdmin)