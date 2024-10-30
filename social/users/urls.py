"""This file is used to map incoming requests to the corresponding views, 
enabling interaction with the user resources, 
such as registering a new user, viewing user profiles, 
and updating user details."""

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import include

# Router Configuration: Create a router and register our viewset with it

# The DefaultRouter is a feature provided by Django Rest Framework 
# to automatically generate URL configurations for viewsets.
router = DefaultRouter()

# This line registers the UserViewSet with the router.
# By using an empty string (r'') as the prefix, we are telling the router to
# put the URLs at the root of the endpoint (e.g., /users/).
# The basename is used for generating URL names (e.g., user-list, user-detail).
router.register(r'', UserViewSet, basename='user')  # Register view set for user management

# Registering the user URLs using the router
# This assigns the URLs generated by the router to the variable urlpatterns.
# This means that all the URLs for CRUD operations on the UserViewSet will be handled, for example:
# GET /users/: Lists all users.
# POST /users/: Creates a new user.
# GET /users/{id}/: Retrieves a single user.
# PUT /users/{id}/: Updates an existing user.
# DELETE /users/{id}/: Deletes an existing user.
urlpatterns = router.urls

