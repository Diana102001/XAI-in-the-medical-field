from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AIModelViewSet

router = DefaultRouter()
router.register(r"models", AIModelViewSet, basename="aimodel")

urlpatterns = [
    path("", include(router.urls)),
]
