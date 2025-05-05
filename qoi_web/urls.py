from django.urls import include, path
from django.contrib import admin
from qoi import views

urlpatterns = [
    path('', views.upload_students, name='upload_students'),  # Root path now points to upload_students view
    path('admin/', admin.site.urls),
    path('qoi/', include("qoi.urls")),  # Include URLs from the 'qoi' app
    path('upload-students/', views.upload_students, name='upload_students'),
]
