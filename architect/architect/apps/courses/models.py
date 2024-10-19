from django.db import models

# Create your models here.
class Course(models.Model):
    course_name = models.CharField('Курс атауы', max_length=200)
    course_description = models.TextField('Курс сипаттамасы')

class Task(models.Model):
    task = models.ForeignKey(Course, on_delete=models.CASCADE)

    task_title = models.CharField('Тапсырма атауы', max_length = 200)
    task_description = models.TextField('Тапсырма сипаттамасы')


class Game(models.Model):
    game_name = models.CharField('Ойын атауы', max_length=200)
