from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_view, name='weather'),
    path('send/', views.send_weather_view, name='send_weather'),
    path('settings/', views.settings_view, name='settings'),
]