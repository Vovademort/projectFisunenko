import requests

# Замените на ваш API ключ от Telegram бота
TELEGRAM_API_KEY = '8107057098:AAF5-GLXDJExpYinKDyHy4Ey9FIMob8y8gE'  
# Замените на ваш chat_id
CHAT_ID = '1448031662'  

# Сообщение, которое вы хотите отправить
message = "Тестовое сообщение от бота"

# URL для отправки сообщения в Telegram
url = f'https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage'

# Параметры запроса
params = {
    'chat_id': CHAT_ID,
    'text': message
}

# Отправляем запрос GET к Telegram API
response = requests.get(url, params=params)

# Выводим ответ от Telegram (для отладки)
print(response.json())