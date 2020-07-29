from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.basic_search, name="basic_search"),
    path("search/itunes/<str:q>", views.search_itunes, name="search_itunes"),
]
