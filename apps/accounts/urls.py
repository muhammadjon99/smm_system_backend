from django.urls import path,include
from .views import (
    UserRegisterView,
    UserProfileView,
    LoginView,
    LogoutView,
    TokenRefreshView,
    ChangePasswordView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='token_blacklist'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserProfileView.as_view(), name='user_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]