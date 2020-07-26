from django.urls import path
from . import views


urlpatterns = [
    path('pods/', views.pods, name='pods'),
    path('upload/', views.upload_pod_data, name='upload'),
    path('upload_cats/', views.upload_category_data, name='upload_category_data'),
    path('delete_all/', views.delete_all, name='delete_all'),
    path('add_podcast/', views.add_podcast, name='add_podcast'),
    path('podcast/<int:id>/', views.podcast_detail, name='podcast_detail'),
    path('import_podcast/<int:id>/', views.import_from_itunes, name='import_from_itunes'),
    path('edit_podcast/<int:id>/', views.edit_podcast, name='edit_podcast'),
    path('delete_podcast/<int:id>/', views.delete_podcast, name='delete_podcast'),
]
