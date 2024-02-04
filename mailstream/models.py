from django.db import models
from django.utils import timezone
from mailstream.services import (NULLABLE,
                                 DAILY, WEEKLY, MONTHLY, REGULARITY_VALUES,
                                 CREATED, STARTED, ENDED, STATUS_VALUES,
                                 SUCCESS_ATTEMPT, ERROR_ATTEMPT, ATTEMPT_VALUES)
from django.conf import settings


class Client(models.Model):
    fullname = models.CharField(max_length=100, verbose_name='Пользователь')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email адрес')
    comments = models.TextField(**NULLABLE, verbose_name='Комментарии')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Автор',
                                   **NULLABLE)

    def __str__(self):
        return f'{self.email} {self.fullname}'

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'
        ordering = ['-fullname']


class Message(models.Model):
    subject = models.CharField(max_length=120, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Содержимое письма', **NULLABLE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Stream(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название рассылки', default='Рассылка')
    started_at = models.DateField(verbose_name='Начало', default=timezone.now)
    ended_at = models.DateField(verbose_name='Завершение', default=timezone.now)
    start_time = models.TimeField(verbose_name='Время рассылки', default=timezone.now)
    message = models.ForeignKey(Message, on_delete=models.RESTRICT, verbose_name='Сообщение')
    regularity = models.CharField(max_length=1, choices=REGULARITY_VALUES, default=MONTHLY,
                                  verbose_name='Периодичность')
    status = models.CharField(max_length=2, choices=STATUS_VALUES, default=CREATED, verbose_name='Текущий статус',
                              **NULLABLE)
    client = models.ManyToManyField(Client, verbose_name='Подписчик')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Автор',
                                   **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [('set_active', 'Активация рассылки'),
                       ('set_client', 'Изменение подписчиков'),]


class Log(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.PROTECT, verbose_name='Рассылка')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Получатель')
    attempt_status = models.CharField(max_length=1, choices=ATTEMPT_VALUES, verbose_name='Статус попытки')
    attempt_date = models.DateField()
    attempt_time = models.TimeField()
    response = models.TextField(**NULLABLE)

    def __str__(self):
        return f'{self.stream.id} {self.client.id} {self.attempt_status}'

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'
