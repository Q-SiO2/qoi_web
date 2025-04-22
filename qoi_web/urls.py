from django.urls import include, path
from . import views
from django.contrib import admin
from qoi.views import home, custom_admin_dashboard, custom_professor_dashboard


# Custom error handlers
handler404 = 'qoi.views.custom_404'
handler500 = 'qoi.views.custom_500'

urlpatterns = [
    path('', home, name='home'),  # Root path for the home page
    path('admin/', admin.site.urls),
    path('qoi/', include("qoi.urls")),
    path('admin/dashboard/', custom_admin_dashboard, name='custom_admin_dashboard'),
    path('professor/dashboard/', custom_professor_dashboard, name='custom_professor_dashboard'),
]
