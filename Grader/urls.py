from django.contrib import admin
from django.urls import path, include
from core import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
]
