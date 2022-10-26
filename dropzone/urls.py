from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('upload/', views.file_upload),
    path('update_image/', views.update_image),
    path('download_image/', views.download_image),    
    path('download_keypoints/', views.download_keypoints),  
    path('calculate_keypoints/', views.calculate_keypoints),   
]



