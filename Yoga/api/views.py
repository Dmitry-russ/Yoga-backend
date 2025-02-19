from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import UserSerializer, UserDataSerializer, ScheduleSerializer
from users.models import User, UserData
from .models import Schedule
import datetime


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
        serializer = UserDataSerializer(data=data)
        # serializer = UserDataSerializer(user=user.id)
        if serializer.is_valid():
            message = serializer.save()
            return Response({"status": "Message created", "id": message.user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleView(APIView):
    '''Получаем расписание по запросу пользователя.'''
    permission_classes = [IsAdminUser]

    #  получение расписания на определнный день или на всю неделю
    def get(self, request):
        data = request.data
        if data:
            #  смотрим какие данные были переданы: день, название йоги
            #  ищем в базе без учета регистра (icontains)
            if data.get("days") and data.get("yoga"):
                schedule = Schedule.objects.filter(
                    week_day__in=data.get("days"), yoga__icontains=data.get("yoga"))
                serializer = ScheduleSerializer(schedule, many=True)
                return Response(serializer.data)
            elif data.get("days"):
                schedule = Schedule.objects.filter(week_day__in=data.get("days"))
                serializer = ScheduleSerializer(schedule, many=True)
                return Response(serializer.data)
            elif data.get("yoga"):
                schedule = Schedule.objects.filter(yoga__icontains=data.get("yoga"))
                serializer = ScheduleSerializer(schedule, many=True)
                return Response(serializer.data)

        # если данные не были переданы то выводим все расписание
        schedule = Schedule.objects.all()
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)

    def post(self, request):
        #  записываем клиента на занятие, данные переданы в запросе
        data = request.data
        username = data.get('username')
        day_request = data.get('date')
        exercise_id = data.get('id')
        chat_id = data.get('chat_id')
        user = User.objects.get(username=username)

        data = {
            "message": "запись на занятие",
            "message_type": "системное",
            }
        data['user'] = user.id
        day_request = datetime.datetime.strptime(day_request, '%Y-%m-%d %H:%M:%S')
        data['exercise_date'] = day_request
        data['exercise_type'] = int(exercise_id)
        data['chat_id'] = int(chat_id)

        serializer = UserDataSerializer(data=data)
        if serializer.is_valid():
            message = serializer.save()
            exercise_type = Schedule.objects.get(id=int(exercise_id))
            return Response({"status": "Запись на занятие создана.",
                             "id": message.id,
                             "exercise_type": exercise_type.yoga,
                             "teacher": exercise_type.teacher,
                             "duration": exercise_type.duration,
                             "exercise_date": str(day_request)},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleViewId(APIView):
    """Получаю одно конкретное занятие из расписания."""
    permission_classes = [IsAdminUser]

    def get(self, request, id):
        exercise = Schedule.objects.get(id=int(id))
        serializer = ScheduleSerializer(exercise)
        return Response(serializer.data)


class UserDataView(APIView):
    """Класс для проверки наличия записи и удаления."""
    permission_classes = [IsAdminUser]

    def get(self, request, username):
        user = User.objects.get(username=username)

        # в списке всех данных о сообщениях пользователя ищем запись
        # которая удовлетворяет условиям, которые я сам придумал
        # по сути запись на занятие сейчас это просто еще одна запись в таблице userdata 
        # среди других записей, надо над этим подумать
        sign_up = UserData.objects.filter(user=user, message_type="системное", message="запись на занятие")
        serializer = UserDataSerializer(sign_up, many=True)
        return Response(serializer.data)

    def put(self, request, username, id):
        data = request.data
        messege = data[0].get('messege')
        try:
            sign_up = UserData.objects.get(id=id)
            exercise_date = sign_up.exercise_date
            exercise_type = sign_up.exercise_type
            sign_up.message = messege
            sign_up.save()
            return Response({"status": "Sign_up deleted",
                             "exercise_date": exercise_date,
                             "exercise_type": exercise_type.yoga}, status=status.HTTP_200_OK)
        except sign_up.DoesNotExist:
            return Response({"error": "Sign_up not found"}, status=status.HTTP_404_NOT_FOUND)


class PlanDataView(APIView):
    """Для вывода записанных на занятия людей."""
    def get(self, request):
        data = request.data
        id = data.get('id')
        if id:
            # когда запрашивает пользователь выдаем одно занятие ивсех кто записан на это занятие
            schedule = [Schedule.objects.get(id=id)]
        else:
            # выводим все занятия для даимна чтобы смотреть запись
            schedule = Schedule.objects.all()
        schedule_dict = {}  # итоговый словарь с занятием и записанными людми
        result = []
        for sch in schedule:
            yoga = sch.yoga
            start_time = sch.start_time
            week_day = sch.week_day
            id = sch.id
            teacher = sch.teacher
            users_dict = []
            schedule_dict = {
                "yoga": yoga,
                "start_time": start_time,
                "week_day": week_day,
                "users": users_dict,
                "id": id,
                "teacher": teacher,

            }
            users = sch.userexercise.all()  # получаем всех пользователей, записанных на занятие (через свзяь в модели)
            if users:
                for user in users:
                    username = user.user.username
                    exercise_date = user.exercise_date
                    first_name = user.user.first_name
                    message = user.message
                    if message == 'запись на занятие':
                        users_dict.append({"username": username,
                                           "exercise_date": exercise_date,
                                           "first_name": first_name,
                                           "message": message})
            schedule_dict["users"] = users_dict
            result.append(schedule_dict)
        return Response(result, status=status.HTTP_200_OK)
