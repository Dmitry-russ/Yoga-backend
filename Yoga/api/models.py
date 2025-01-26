from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        indexes = [models.Index(fields=['created']), ]


WEEK_DAYS_CHOICE = [
    ("понедельник", 'понедельник'),
    ("вторник", 'вторник'),
    ("среда", 'среда'),
    ("четверг", 'четверг'),
    ("пятница", 'пятница'),
    ("суббота", 'суббота'),
    ("воскресенье", 'воскресенье'),
]


class Schedule(CreatedModel):
    """Модель расписания."""

    yoga = models.TextField(verbose_name="Наименование занятия.",)
    start_time = models.TimeField(verbose_name="Время начала занятия.",)
    week_day = models.TextField(verbose_name="День недели заняти.", choices=WEEK_DAYS_CHOICE)
    teacher = models.TextField(verbose_name="Фамилия преподавателя.", null=True,)
    sort_days = models.IntegerField(verbose_name="Для сортировки дней недели, понедельник = 0.", default=0)

    class Meta:
        ordering = ['sort_days', 'start_time']

    def __str__(self) -> str:
        return self.yoga
