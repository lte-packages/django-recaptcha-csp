"""
URL configuration for demo_site project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('demo_app.urls')),
]
