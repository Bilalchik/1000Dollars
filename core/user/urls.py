from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('user/register/', views.MyUserRegisterView.as_view()),

    path('user/reset_password/get_otp', views.MyUserResetPasswordView.as_view()),
    path('user/reset_password/restore/', views.MyUserRestorePasswordView.as_view())
    # path('user/confirm_otp/<int:user_id>/', ...)
]
