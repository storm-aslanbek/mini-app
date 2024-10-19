# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.index, name='index'),  # Путь для главной страницы
#     path('register/', views.register_user, name='register_user'),
#     path('generate-task/', views.generate_python_task, name='generate_python_task'),
#     path('check-task/', views.check_python_task, name='check_python_task'),
#     path('progress/<str:telegram_id>/', views.show_user_progress, name='show_user_progress'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register_user'),
    path('generate-task/', views.generate_python_task, name='generate_python_task'),
    path('check-task/', views.check_python_task, name='check_python_task'),
    path('progress/<str:telegram_id>/', views.show_user_progress, name='show_user_progress'),
]
