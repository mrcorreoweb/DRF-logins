from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication 
from rest_framework.exceptions import PermissionDenied
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Permissions and authentication methods are not needed to be declared
    # in the view because has been established by default
    # for the whole project in settings.py
    # only needed if you want to override the default settings
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # authentication_classes = [
    #    SessionAuthentication, 
    #    TokenAuthentication] 

    def perform_create(self, serializer):
        # Automatically set the owner of the post to the logged-in user
        serializer.save(owner=self.request.user)
    
    def perform_update(self, serializer):
        # Check if the user trying to update the post is the owner
        if self.request.user != serializer.instance.owner:
            raise PermissionDenied("You do not have permission to update this post.")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Check if the user trying to delete the post is the owner
        if self.request.user != instance.owner:
            raise PermissionDenied("You do not have permission to delete this post.")
        instance.delete()
