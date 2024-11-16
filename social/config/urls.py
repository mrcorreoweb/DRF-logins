from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as auth_token_views

urlpatterns = [
    path('admin/', admin.site.urls),             # Django Admin
    path('users/', include('users.urls')),       # Include URLs from the 'users' app
    path('posts/', include('posts.urls')),       # Include URLs from the 'posts' app
    # Session-based login/logout views for the browsable API
    path('api-auth/', include('rest_framework.urls')),  # Adds login/logout

    # Token-based authentication view for stateless clients
    path('api-token-auth/', auth_token_views.obtain_auth_token, name='api-token-auth'),
]