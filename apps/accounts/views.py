from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UserRegisterView(generics.CreateAPIView):
    """
    Yangi foydalanuvchilarni ro'yxatdan o'tkazish (Signup)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # Hamma ro'yxatdan o'tishi mumkin

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Tizimga kirgan foydalanuvchining o'z profil ma'lumotlarini ko'rish va yangilash
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user