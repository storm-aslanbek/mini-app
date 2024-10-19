from django.shortcuts import render
from django.http import HttpResponse
import openai
from .db_connect import db
from django.http import JsonResponse

# Подключение к коллекции пользователей
user_collection = db['Users']

# Устанавливаем API ключ OpenAI
openai.api_key = 'dd'


# Главная страница
def index(request):
    return render(request, 'courses/index.html')


# Простая регистрация пользователя (без Telegram)
def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telegram_id = request.POST.get('telegram_id')  # Можно оставить как фиктивное поле

        # Сохранение пользователя в БД
        new_user = {
            "first_name": first_name,
            "last_name": last_name,
            "telegram_id": telegram_id,
            "points": 0
        }
        user_collection.insert_one(new_user)

        return HttpResponse("Қолданушы тіркелді")
    return render(request, 'courses/register.html')


# Генерация задания с помощью ChatGPT
def generate_python_task(request):
    if request.method == 'POST':
        # Используем фиктивный ID пользователя
        user_id = "12345"
        user = db['users'].find_one({"telegram_id": user_id})

        # Генерация задания через ChatGPT
        task_prompt = "Python тілі бойынша бастауыш адамға арналған тапсырма генерацияла"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": task_prompt}]
        )
        task = response['choices'][0]['message']['content']

        return JsonResponse({"task": task}, status=200)

    return JsonResponse({"error": "Тек POST сұрауларын қолдайды"}, status=400)


# Проверка выполнения задания
def check_python_task(request):
    if request.method == 'POST':
        # Здесь фиксируем код пользователя и результат выполнения
        user_code = request.POST.get('user_code')
        task_id = request.POST.get('task_id')  # Фиктивное поле

        # Используем ChatGPT для проверки кода
        check_prompt = f"Мына кодты Python-да тексер: {user_code}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": check_prompt}]
        )
        result = response['choices'][0]['message']['content']

        return HttpResponse(f"Тексеріс нәтижесі: {result}")

    return render(request, 'courses/check_task.html')


# Показ прогресса пользователя
def show_user_progress(request, telegram_id):
    user = user_collection.find_one({"telegram_id": telegram_id})
    if user:
        return HttpResponse(f"Прогресс пользователя: {user['points']} очков")
    return HttpResponse("Пользователь не найден")
