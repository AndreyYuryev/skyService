# Generated by Django 5.0.1 on 2024-01-10 19:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailstream', '0005_stream_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maillist',
            name='stream',
            field=models.ForeignKey(limit_choices_to={'all_recipient': False}, on_delete=django.db.models.deletion.PROTECT, to='mailstream.stream', verbose_name='рассылка'),
        ),
    ]
