from django.contrib import admin
from .models import UserData


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'message_date_time', 'message_type', 'exercise_date', 'exercise_type')
    search_fields = ('user', 'message_date_time',)
    list_filter = ('created', 'message_date_time',)
    empty_value_display = '-пусто-'


admin.site.register(UserData, UserDataAdmin)
