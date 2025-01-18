from rest_framework import serializers
from users.models import User, UserData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined']


class UserDataSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # user = UserSerializer(User)

    class Meta:
        model = UserData
        fields = ['id', 'user', 'message', 'message_type', 'message_date_time']
