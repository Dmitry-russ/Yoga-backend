# from django.db import modelss
from django.contrib.auth import get_user_model
from django.db import models

from api.models import Schedule

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
    exercise_date = models.DateTimeField(verbose_name="Дата и время занятия.", null=True, blank=True)

    exercise_type = models.ForeignKey(Schedule,
                                      verbose_name="Занятие из расписания занятий.",
                                      on_delete=models.CASCADE,
                                      null=True,
                                      blank=True,
                                      related_name='userexercise', )
    chat_id = models.IntegerField(verbose_name="Номер чата пользователя.", null=True, blank=True)

    def __str__(self) -> str:
        return self.message
