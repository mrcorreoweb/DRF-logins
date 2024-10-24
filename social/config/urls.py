from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),             # Django Admin
    path('users/', include('users.urls')),       # Include URLs from the 'users' app
    path('posts/', include('posts.urls')),       # Include URLs from the 'posts' app
    path('api-auth/', include('rest_framework.urls')), # Added for basic authentication login/logout
]
