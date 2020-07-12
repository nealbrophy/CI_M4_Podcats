from django.urls import path
from . import views


urlpatterns = [
    path('pods/', views.pods, name='pods'),
    path('upload/', views.upload_pod_data, name='upload'),
    path('delete_all/', views.delete_all, name='delete_all'),
]
