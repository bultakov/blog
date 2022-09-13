from django.urls import path

from .views import (
    UserRegistrationView,
    UserLoginView,
    token_send,
    success,
    verify,
    error_page
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name="login"),
    path('token', token_send, name="token_send"),
    path('success', success, name='success'),
    path('verify/<token>', verify, name="verify"),
    path('error', error_page, name="error")
]
