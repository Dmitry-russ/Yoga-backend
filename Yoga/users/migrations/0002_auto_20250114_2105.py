# Generated by Django 2.2.16 on 2025-01-14 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='message_date_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время и дата сообщения.'),
        ),
    ]
