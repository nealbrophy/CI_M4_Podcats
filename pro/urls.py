from django.urls import path
from . import views


urlpatterns = [
    path('upgrade/', views.upgrade, name='upgrade'),
    path('benefits/', views.benefits, name='benefits'),
]
