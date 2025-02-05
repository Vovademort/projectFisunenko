from django.contrib import admin  # Импортируем модуль админки Django
from .models import UserSettings  # Импортируем модель UserSettings из текущего приложения

# Регистрируем модель UserSettings в админке с помощью декоратора @admin.register
@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    # Настройки отображения модели в админке
    list_display = ('chat_id', 'city', 'notification_time')  # Указываем, какие поля модели будут отображаться в списке(а именно ID пользователя, город для уведомления и время)