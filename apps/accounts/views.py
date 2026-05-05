from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .models import User
from .serializers import UserSerializer,ChangePasswordSerializer
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver

@extend_schema(tags=['Accounts'], summary="Yangi foydalanuvchi ro'yxatdan o'tkazish")
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(tags=['Accounts'], summary="Foydalanuvchi o'z profil ma'lumotlarini olishi va yangilashi")
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema(tags=['Accounts'], summary="Login (Token olish)")
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

@extend_schema(tags=['Accounts'], summary="Tokenni yangilash (Refresh)")
class TokenRefreshView(TokenRefreshView):
    pass

@extend_schema(tags=['Accounts'], summary="Logout (Tokenni bekor qilish)")
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Muvaffaqiyatli chiqildi."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Token yaroqsiz yoki topilmadi."}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, queryset=None):
        return self.request.user
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Eski parol noto'g'ri."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"message": "Parol muvaffaqiyatli yangilandi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print(f"\nRECOVERY TOKEN: {reset_password_token.key}\n")