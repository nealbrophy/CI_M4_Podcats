from django.urls import path
from . import views


urlpatterns = [
    path("upgrade/", views.upgrade, name="upgrade"),
    path("upgrade_success/<order_number>", views.upgrade_success, name="upgrade_success"),
    path("benefits/", views.benefits, name="benefits"),
]
