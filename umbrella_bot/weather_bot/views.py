
import requests
from django.http import JsonResponse
from telegram import Bot
import asyncio  
from django.shortcuts import render, redirect
from .models import UserSettings
from .forms import UserSettingsForm
from django.conf import settings

API_KEY = settings.API_KEY   # OpenWeatherMap
TELEGRAM_API_KEY = settings.TELEGRAM_API_KEY

def get_weather(city):
    # Получаем данные о погоде для заданного города
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru'
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('weather'):
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f'Погода в {city}: {weather_description}, {temperature}°C'
        return 'Не удалось получить данные о погоде'
    except requests.exceptions.RequestException as e:
        return f'Ошибка при подключении к API: {e}'


async def send_weather_to_telegram(chat_id, weather_message):
    # Отправляет сообщение с погодой в Telegram
    bot = Bot(token=TELEGRAM_API_KEY)
    await bot.send_message(chat_id=chat_id, text=weather_message)

def weather_view(request):
    # Возвращает погоду в JSON
    city = request.GET.get("city", "Moscow") 
    weather = get_weather(city)
    return JsonResponse({'status': 'success', 'message': weather})

def send_weather_view(request):
    # Отправляет погоду всем пользователям, у которых есть настройки
    try:
        users = UserSettings.objects.all()  # Получаем всех пользователей из базы

        if not users:
            return JsonResponse({'status': 'error', 'message': 'Нет пользователей с настройками'}, status=400)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        for user in users:
            city = user.city
            chat_id = user.chat_id
            weather = get_weather(city)
            loop.run_until_complete(send_weather_to_telegram(chat_id, weather))

        return JsonResponse({'status': 'success', 'message': 'Погода отправлена всем пользователям'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def telegram_auth(request):
    # Функция для получения chat_id и сохранения его в сессию и базу данных
    chat_id = request.GET.get('chat_id')
    if chat_id:
        request.session['chat_id'] = chat_id  # Сохраняем chat_id в сессии
        user_settings, created = UserSettings.objects.get_or_create(chat_id=chat_id)
        return JsonResponse({'status': 'success', 'message': 'Chat ID сохранен'})
    return JsonResponse({'status': 'error', 'message': 'Chat ID не получен'}, status=400)

def settings_view(request):
    # Обработчик страницы настроек
    chat_id = request.session.get('chat_id')
    if not chat_id:
        return redirect('weather')  # Перенаправляем, если chat_id отсутствует
    
    user_settings, created = UserSettings.objects.get_or_create(chat_id=chat_id)

    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            return redirect('settings')  # Перезагрузка страницы после сохранения
    else:
        form = UserSettingsForm(instance=user_settings)

    return render(request, 'weather_bot/settings.html', {'form': form})