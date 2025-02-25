# Generated by Django 2.2.16 on 2025-02-25 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userdata_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя.'),
        ),
        migrations.AddField(
            model_name='userdata',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Номер телефона.'),
        ),
    ]
