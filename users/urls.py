from django.urls import path
from .views import RegisterView, RefreshTokenView, UserLoginTokenView
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', UserLoginTokenView.as_view(), name='token'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]