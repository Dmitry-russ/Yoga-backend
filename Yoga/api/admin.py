from django.contrib import admin
from .models import Schedule
from django.conf.locale.es import formats as es_formats

es_formats.DATETIME_FORMAT = "d M Y H:i"


class ScheduleDataAdmin(admin.ModelAdmin):
    list_display = ('yoga', 'start_time', 'week_day', 'teacher', 'cost', 'cost_first',)
    search_fields = ('yoga', 'week_day',)
    list_filter = ('yoga', 'week_day',)
    empty_value_display = '-пусто-'


admin.site.register(Schedule, ScheduleDataAdmin)
