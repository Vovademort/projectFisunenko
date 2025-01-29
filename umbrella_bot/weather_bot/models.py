from django.db import models

class UserSettings(models.Model):
    chat_id = models.CharField(max_length=50, unique=True)  # ID пользователя Telegram
    city = models.CharField(max_length=100, default="Moscow")  # Город
    notification_time = models.TimeField(default="08:00")  # Время уведомлений

    def __str__(self):
        return f"{self.chat_id} - {self.city} ({self.notification_time})"