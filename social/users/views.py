from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

    def get_permissions(self):
        """
        Permissions needed here to override the default one
        which is IsAuthenticatedOrReadOnly in the settings.py    
        user registration should be open to unauthenticated users        
        """
        # Allow anyone to create (register) a new user
        if self.action == 'create':
            return [AllowAny()]
        # Otherwise, use the default permission established in settings.py
        return super().get_permissions()
