from django.db import models
from django.contrib.auth.models import User # Imports built-in User model

# Post model where 'owner' refers to the user who created the post
class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.username}: {self.content[:30]}..."  # Display part of the post content
