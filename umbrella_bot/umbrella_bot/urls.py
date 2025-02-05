# Импортируем необходимые модули Django
from django.contrib import admin  # Для админки Django
from django.urls import path, include  # Для работы с маршрутами и включения других URL-ов

urlpatterns = [
    path('admin/', admin.site.urls),  # Маршрут для админки Django. Доступ к ней будет по адресу /admin/
    path('weather/', include('weather_bot.urls')),  # Все маршруты из приложения weather_bot будут доступны по пути /weather/
]