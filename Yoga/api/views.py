from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import UserSerializer, UserDataSerializer
from users.models import User, UserData


class UserRegistration(APIView):

    permission_classes = [IsAdminUser]  # не работает разрешение, кто угодно видимо может зарегестрироваться

    @extend_schema(
        summary="Регистрация пользователя",
        description="Создаёт нового пользователя с уникальным email, именем, фамилией, возрастом и ником в телеграм. ",
        request=UserSerializer,
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Пользователь успешно создан"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"status": "User created", "id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Вместо класса вверху можно использовать вот этот класс, но надо разобраться
# class UserRegistration(generics.CreateAPIView):
#     serializer_class = UserSerializer


class UserList(APIView):
    filter_backends = [filters.OrderingFilter]
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Получение информации обо всех пользователях",
        description="Возвращает список всех зарегистрированных пользователей.",
        responses={
            200: OpenApiResponse(response=UserSerializer(many=True), description="Список всех пользователей")
        }
    )
    def get(self, request):
        users = User.objects.all().order_by('username')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Получение информации о пользователе",
        description="Возвращает информацию о пользователе по его ID.",
        responses={
            200: OpenApiResponse(response=UserSerializer, description="Информация о пользователе"),
            404: OpenApiResponse(description="Пользователь не найден")
        }
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserDelete(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Удаление пользователя",
        description="Удаляет пользователя по его ID. Если пользователь не найден, возвращает ошибку.",
        responses={
            200: OpenApiResponse(description="Пользователь успешно удалён"),
            404: OpenApiResponse(description="Пользователь не найден"),
            400: OpenApiResponse(description="ID пользователя не предоставлен")
        }
    )
    def delete(self, request, user_id):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user.delete()
                return Response({"status": "User deleted"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)


class UserConversation(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Получение и создание диалога пользователя.",
        description="Список сообщений чата пользваотеля.",
        responses={
            200: OpenApiResponse(response=UserDataSerializer(many=True), description="Чат пользователя"),
            201: OpenApiResponse(response=UserDataSerializer, description="Сообщение создано"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def get(self, request, username):
        if username:
            try:
                user = User.objects.get(username=username)
                conversation = UserData.objects.filter(user=user).order_by('message_date_time')
                serializer = UserDataSerializer(conversation, many=True)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, username):
        user = User.objects.get(username=username)
        data = request.data
        data['user'] = user.id
        print(request.data)
        serializer = UserDataSerializer(data=data)
        # serializer = UserDataSerializer(user=user.id)
        if serializer.is_valid():
            message = serializer.save()
            return Response({"status": "Message created", "id": message.user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserDeleteAll(APIView):
#     @extend_schema(
#         summary="Удаление всех пользователей",
#         description="Удаляет всех пользователей из базы данных.",
#         responses={
#             200: OpenApiResponse(description="Все пользователи успешно удалены")
#         }
#     )
#     def delete(self, request):
#         User.objects.all().delete()
#         return Response({"status": "All users deleted"}, status=status.HTTP_200_OK)
