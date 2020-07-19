from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.basic_search, name='basic_search'),
]
