# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordResetDoneView)
from django.urls import include, path

app_name = 'Yoga'

user_patterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name='password_reset_done'),
]

urlpatterns = [
    path('', include(user_patterns)),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
