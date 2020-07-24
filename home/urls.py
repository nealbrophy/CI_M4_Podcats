from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload_users/', views.upload_users, name='upload_users'),
]
