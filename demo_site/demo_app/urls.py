"""
URL configuration for demo_app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/checkbox/', views.contact_checkbox, name='contact_checkbox'),
    path('contact/invisible/', views.contact_invisible, name='contact_invisible'),
    path('simple/', views.simple_form, name='simple_form'),
    path('success/', views.success, name='success'),
    path('csp-info/', views.csp_info, name='csp_info'),
]
