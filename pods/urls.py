from django.urls import path
from . import views


urlpatterns = [
    path('pods/', views.pods, name='pods'),
    path('upload/', views.upload_pod_data, name='upload'),
    path('upload_cats/', views.upload_category_data, name='upload_category_data'),
    path('delete_all/', views.delete_all, name='delete_all'),
    path('add_podcast/', views.add_podcast, name='add_podcast'),
]
