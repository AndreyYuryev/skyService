from django.db import models

NULLABLE = {'blank': True, 'null': True}
REGULARITY_VALUES = [('d', 'раз в день'), ('w', 'раз в неделю', 'm', 'раз в месяц'), ]
STATUS_VALUES = [('l', 'завершена'), ('r', 'создана'), ('s', 'запущена'), ]


class Client(models.Model):
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=255)
    comments = models.TextField()

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'


class Stream(models.Model):
    post_time = models.DateTimeField()
    regularity = models.CharField(max_length='1', choices=REGULARITY_VALUES, verbose_name='Периодичность')
    status = models.CharField(max_length='1', choices=STATUS_VALUES, verbose_name='Статус рассылки')

    def __str__(self):
        return f'{self.status} - {self.regularity}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
