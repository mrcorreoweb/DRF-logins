from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')  # Register view set for post management

urlpatterns = router.urls
