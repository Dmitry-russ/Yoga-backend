# from django.db import modelss
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        indexes = [models.Index(fields=['created']), ]


class UserData(CreatedModel):
    """Расширение модели User."""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=False,
                             related_name='userdata', )

    message = models.TextField(verbose_name="Текст сообщения.",)
    message_date_time = models.DateTimeField(auto_now_add=True, verbose_name="Время и дата сообщения.",)
    message_type = models.TextField(verbose_name="Тип сообщения: бот или пользователь.",)

    def __str__(self) -> str:
        return self.message
