from django.contrib import admin
from .models import Schedule
from django.conf.locale.es import formats as es_formats

es_formats.DATETIME_FORMAT = "d M Y H:i"


class ScheduleDataAdmin(admin.ModelAdmin):
    list_display = ('yoga', 'formatted_time_field', 'week_day', 'teacher', 'cost', 'cost_first', 'duration')
    search_fields = ('yoga', 'week_day', 'teacher',)
    list_filter = ('yoga', 'week_day', 'teacher',)
    empty_value_display = '-пусто-'

    def formatted_time_field(self, obj):
        return obj.start_time.strftime("%H:%M")

    formatted_time_field.short_description = 'Время начала занятия'


admin.site.register(Schedule, ScheduleDataAdmin)
