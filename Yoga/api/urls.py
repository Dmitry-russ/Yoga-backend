from django.urls import path
from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularRedocView,
                                   SpectacularSwaggerView,)
from .views import (UserRegistration, UserDetail, UserList,
                    UserDelete, UserConversation, ScheduleView,
                    UserDataView, PlanDataView, ScheduleViewId,)

app_name = 'api'

urlpatterns = [
    # Генерация OpenAPI схемы
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # регистрация нового пользователя после того как он включил первый раз бот
    path('register/', UserRegistration.as_view(), name='user-register'),
    # информация о пользователе по его id
    path('user/<int:user_id>/', UserDetail.as_view(), name='user-detail'),
    # список зарегестрированных пользователей
    path('users/', UserList.as_view(), name='user-list'),
    # удаление пользователя
    path('delete/<int:user_id>/', UserDelete.as_view(), name='user-delete'),
    # получение истории общения с ботом конкретного пользователя, запись диалога пользователя с ботом
    path('conversation/<str:username>/', UserConversation.as_view(), name='user-conversation'),
    # получение распсиания занятий или запись на занятие
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    # получение информации о конкретном занятии в расписании
    path('schedule/<int:id>/', ScheduleViewId.as_view(), name='schedule'),
    # проверка информации о налияии записи на занятие у клиента
    path('userdata/<str:username>/', UserDataView.as_view(), name='userdata'),
    # удаление записи на занятие
    path('userdata/<str:username>/<int:id>/', UserDataView.as_view(), name='userdata'),
    # вывод списка записанных на занятие людей
    path('plan/', PlanDataView.as_view(), name='plan'),
]
