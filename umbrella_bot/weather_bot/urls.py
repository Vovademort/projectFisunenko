from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_view, name='weather'),   # Проверка погоды отдельно
    path('send/', views.send_weather_view, name='send_weather'),  # Проверка отправки уведомлений
    path('settings/', views.settings_view, name='settings'),   # Добавление настроек
    path('telegram_auth/', views.telegram_auth, name='telegram_auth'),  # Обработка chat_id
]