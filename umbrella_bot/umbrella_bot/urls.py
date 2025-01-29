from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('weather/', include('weather_bot.urls')),  # Подключаем маршруты из приложения
]