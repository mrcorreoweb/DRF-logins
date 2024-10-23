from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # Automatically populate owner

    class Meta:
        model = Post
        fields = ['id', 'owner', 'content', 'created_at', 'updated_at']
