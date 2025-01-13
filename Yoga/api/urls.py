from django.urls import path
from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularRedocView,
                                   SpectacularSwaggerView,)
from .views import (UserRegistration,
                    UserDetail,
                    UserList,
                    UserDelete,
                    # UserDeleteAll,
                    )

app_name = 'api'

urlpatterns = [
    # Генерация OpenAPI схемы
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('register/', UserRegistration.as_view(), name='user-register'),
    path('user/<int:user_id>/', UserDetail.as_view(), name='user-detail'),
    path('users/', UserList.as_view(), name='user-list'),
    path('delete/<int:user_id>/', UserDelete.as_view(), name='user-delete'),
    #  path('delete-all/', UserDeleteAll.as_view(), name='user-delete-all'),
]
