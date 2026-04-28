from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import User
from .serializers import UserSerializer


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

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)