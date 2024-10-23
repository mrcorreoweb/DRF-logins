from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny 
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] # Allow anyone to register new users
