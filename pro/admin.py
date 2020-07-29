from django.contrib import admin
from .models import Purchase


class PurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ("order_number", "date", "purchase_amount", "stripe_pid")

    fields = ("order_number", "date", "full_name", "email",
              "phone_number", "country", "postcode",
              "town_or_city", "street_address1", "street_address2",
              "county", "purchase_amount", "stripe_pid")

    list_display = ("order_number", "date", "full_name", "purchase_amount")

    ordering = ("-date",)


admin.site.register(Purchase, PurchaseAdmin)
