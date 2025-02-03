from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, AsyncMock
from .models import UserSettings

class WeatherBotTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserSettings.objects.create(chat_id="123456", city="Moscow")

    @patch("weather_bot.views.requests.get")
    def test_get_weather(self, mock_get):
        mock_get.return_value.json.return_value = {
            "weather": [{"description": "дождь"}],
            "main": {"temp": 15}
        }
        response = self.client.get(reverse("weather"), {"city": "Moscow"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("дождь", response.json()["message"])

    def test_telegram_auth(self):
        response = self.client.get(reverse("telegram_auth"), {"chat_id": "654321"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserSettings.objects.filter(chat_id="654321").exists())

    def test_settings_view_get(self):
        session = self.client.session
        session["chat_id"] = "123456"
        session.save()
        response = self.client.get(reverse("settings"))
        self.assertEqual(response.status_code, 200)

    def test_settings_view_post(self):
        session = self.client.session
        session["chat_id"] = "123456"
        session.save()
        response = self.client.post(reverse("settings"), {"city": "Berlin", "notification_time": "08:00"})
        self.assertEqual(response.status_code, 302)  # Должен перенаправить
        self.user.refresh_from_db()
        self.assertEqual(self.user.city, "Berlin")

    @patch("weather_bot.views.send_weather_to_telegram", new_callable=AsyncMock)
    def test_send_weather_view(self, mock_send_weather):
        response = self.client.get(reverse("send_weather"))
        self.assertEqual(response.status_code, 200)
        mock_send_weather.assert_called_once_with("123456", "Погода в Moscow")
