from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=255)
    comments = models.TextField()

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'
