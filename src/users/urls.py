from django.urls import path, include
from rest_framework import routers

from src.users.views import CoordinatorsViewSet

router = routers.DefaultRouter()
router.register("coordinators", CoordinatorsViewSet, basename="Coordinators")

urlpatterns = [
    path("api/", include(router.urls), name="Coordinators"),
]
