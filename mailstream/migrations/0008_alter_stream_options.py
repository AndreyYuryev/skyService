# Generated by Django 5.0.1 on 2024-02-03 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailstream', '0007_alter_stream_created_by_alter_stream_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stream',
            options={'permissions': [('set_active', 'Активация рассылки'), ('set_client', 'Изменение подписчиков')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
