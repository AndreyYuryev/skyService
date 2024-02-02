# Generated by Django 5.0.1 on 2024-02-01 12:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailstream', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(blank=True, null=True, verbose_name='содержимое письма'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='ended_at',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='закончить к'),
        ),
        migrations.AlterField(
            model_name='stream',
            name='started_at',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='начать с'),
        ),
    ]