from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .db_connect import db
import openai
import json
import os
from conf import OPENAI


# Установите ваш OpenAI API ключ
openai.api_key = os.getenv(OPENAI)

# Коллекции в базе данных
user_collection = db['Users']
tasks_collection = db['PythonTasks']

# Главная страница, которая рендерит шаблон index.html
def index(request):
    return render(request, 'courses/index.html')


# Регистрация пользователя через данные из Telegram Web App
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            user_data = json.loads(request.body.decode('utf-8'))
            telegram_id = user_data.get('telegram_id')
            username = user_data.get('username')
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')

            # Проверяем, существует ли пользователь в базе данных
            if not user_collection.find_one({"telegram_id": telegram_id}):
                user_collection.insert_one(user_data)
                return JsonResponse({'status': 'success', 'message': 'Пайдаланушы сәтті тіркелді.'})
            else:
                return JsonResponse({'status': 'failure', 'message': 'Пайдаланушы тіркелген.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'failure', 'message': 'Қате сұрау әдісі.'})


# Генерация задания по Python с использованием GPT-3.5 Turbo
def generate_python_task(request):
    try:
        # Запрос к GPT-3.5 для генерации задания по Python на казахском
        prompt = "Бағдарламалау тілі Python бойынша қарапайым тапсырма жасаңыз."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Сен Python тілін үйрететін көмекшісің."},
                {"role": "user", "content": prompt}
            ]
        )

        task = response['choices'][0]['message']['content']

        # Сохраняем задание в коллекции
        task_document = {
            "task": task
        }
        tasks_collection.insert_one(task_document)

        return JsonResponse({'status': 'success', 'task': task})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# Проверка правильности решения пользователя с использованием GPT-3.5 Turbo
@csrf_exempt
def check_python_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            telegram_id = data.get('telegram_id')
            task_id = data.get('task_id')
            user_solution = data.get('solution')

            # Извлечение задания из базы данных
            task = tasks_collection.find_one({"_id": task_id})

            if not task:
                return JsonResponse({'status': 'failure', 'message': 'Тапсырма табылмады.'})

            # Отправляем решение пользователя и задание в GPT-3.5 для проверки
            prompt = f"Міне тапсырма: {task['task']}. Міне пайдаланушының шешімі: {user_solution}. Бұл шешім дұрыс па?"

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Сен Python тіліндегі тапсырмаларды тексерушісің."},
                    {"role": "user", "content": prompt}
                ]
            )

            result = response['choices'][0]['message']['content']

            # Проверка правильности решения и начисление баллов
            if "дұрыс" in result.lower():
                user = user_collection.find_one({"telegram_id": telegram_id})
                if user:
                    new_points = user.get('points', 0) + 10  # Начисляем 10 баллов
                    user_collection.update_one(
                        {"telegram_id": telegram_id},
                        {"$set": {"points": new_points}}
                    )
                    return JsonResponse({'status': 'success', 'message': 'Шешім дұрыс! Сіз 10 ұпай алдыңыз!'})
                else:
                    return JsonResponse({'status': 'failure', 'message': 'Пайдаланушы табылмады.'})
            else:
                return JsonResponse({'status': 'failure', 'message': 'Шешім қате, қайта көріңіз.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'failure', 'message': 'Қате сұрау әдісі.'})


# Функция для отображения текущего прогресса пользователя
def show_user_progress(request, telegram_id):
    user = user_collection.find_one({"telegram_id": telegram_id})
    if user:
        points = user.get('points', 0)
        return JsonResponse({'status': 'success', 'points': points})
    return JsonResponse({'status': 'failure', 'message': 'Пайдаланушы табылмады.'})

