from django.urls import path
from . import views

urlpatterns = [
    path('upload-students/', views.upload_students, name='upload_students'),
]

