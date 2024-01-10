from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}
DAILY = 'D'
WEEKLY = 'W'
MONTHLY = 'M'
REGULARITY_VALUES = [(DAILY, 'раз в день'), (WEEKLY, 'раз в неделю'), (MONTHLY, 'раз в месяц'), ]

CREATED = 'CR'
STARTED = 'ST'
ENDED = 'ED'
STATUS_VALUES = [(ENDED, 'завершена'), (CREATED, 'создана'), (STARTED, 'запущена'), ]


class Client(models.Model):
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email адрес')
    comments = models.TextField(**NULLABLE)

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'
        ordering = ['-fullname']


class Message(models.Model):
    subject = models.CharField(max_length=120, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма', **NULLABLE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Stream(models.Model):
    name = models.CharField(max_length=50, verbose_name='название рассылки', default='Расылка')
    started_at = models.DateTimeField(verbose_name='начать с', default=timezone.now)
    ended_at = models.DateTimeField(verbose_name='закончить к', default=timezone.now)
    message = models.ForeignKey(Message, on_delete=models.RESTRICT, **NULLABLE)
    regularity = models.CharField(max_length=1, choices=REGULARITY_VALUES, default=MONTHLY,
                                  verbose_name='периодичность')
    status = models.CharField(max_length=2, choices=STATUS_VALUES, default=CREATED, verbose_name='Статус рассылки',
                              **NULLABLE)
    all_recipient = models.BooleanField(default=True, verbose_name='отправить всем')

    def __str__(self):
        # regularity = ''
        # status = ''
        # for item in REGULARITY_VALUES:
        #     if item[0] == self.regularity:
        #         regularity = item[1]
        #         break
        # for item in STATUS_VALUES:
        #     if item[0] == self.status:
        #         status = item[1]
        #         break
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailList(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.PROTECT, verbose_name='рассылка',
                               limit_choices_to={'all_recipient': False})
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='получатель', **NULLABLE)

    def __str__(self):
        return f'Список получателей рассылки'

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'


class Log(models.Model):
    SUCCESS_ATTEMPT = 'S'
    ERROR_ATTEMPT = 'E'
    ATTEMPT_VALUES = [(SUCCESS_ATTEMPT, 'успешно'), (ERROR_ATTEMPT, 'с ошибкой'), ]

    stream = models.ForeignKey(Stream, on_delete=models.PROTECT, verbose_name='рассылка', **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='получатель', **NULLABLE)
    attempt_status = models.CharField(max_length=1, choices=ATTEMPT_VALUES, verbose_name='Статус попытки')
    last_attempt = models.DateTimeField()
    response = models.TextField(**NULLABLE)

    def __str__(self):
        return f'{self.stream.id} {self.client.id} {self.attempt_status}'

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'
