"""
Generate tokens for all the existing users
running the command:
python manage.py generate_tokens
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Generate tokens for all users in the system'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            token, created = Token.objects.get_or_create(user=user)
            if created:
                self.stdout.write(f'Token for {user.username} created: {token.key}')
            else:
                self.stdout.write(f'Token for {user.username} already exists: {token.key}')
