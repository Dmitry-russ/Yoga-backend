from rest_framework import serializers
from users.models import User, UserData
from .models import Schedule


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'yoga', 'start_time', 'week_day', 'teacher', 'sort_days', 'cost', 'cost_first']
        ordering = ['sort_days', 'start_time']


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id', 'user', 'message', 'message_type',
                  'message_date_time', 'exercise_date', 'exercise_type', 'chat_id']
