# background_removal/urls.py
from django.urls import path
from .views import BackgroundRemovalAPIView, upload_form

urlpatterns = [
    path('remove-background/', BackgroundRemovalAPIView.as_view(), name='remove_background'),
    path('upload/', upload_form, name='upload_form'),
]
