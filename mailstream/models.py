from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=255, unique=True)
    comments = models.TextField(**NULLABLE)

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'


class Stream(models.Model):
    DAILY = 'D'
    WEEKLY = 'W'
    MONTHLY = 'M'
    REGULARITY_VALUES = [(DAILY, 'раз в день'), (WEEKLY, 'раз в неделю'), (MONTHLY, 'раз в месяц'), ]
    STATUS_VALUES = [('CL', 'завершена'), ('CR', 'создана'), ('ST', 'запущена'), ]
    post_time = models.DateTimeField()
    regularity = models.CharField(max_length=1, choices=REGULARITY_VALUES, default=MONTHLY,
                                  verbose_name='Периодичность')
    status = models.CharField(max_length=2, choices=STATUS_VALUES, verbose_name='Статус рассылки', **NULLABLE)

    def __str__(self):
        return f'{self.status} - {self.regularity}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    subject = models.CharField(max_length=120, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма', **NULLABLE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Log(models.Model):
    SUCCESS_ATTEMPT = 'S'
    ERROR_ATTEMPT = 'E'
    ATTEMPT_VALUES = [(SUCCESS_ATTEMPT, 'успешно'), (ERROR_ATTEMPT, 'с ошибкой'), ]
    last_attempt = models.DateTimeField()
    attempt_status = models.CharField(max_length=1, choices=ATTEMPT_VALUES, verbose_name='Статус попытки')
    response = models.TextField(**NULLABLE)

    def __str__(self):
        return f'{self.attempt_status}'

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'
