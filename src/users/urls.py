from django.urls import path, include
from rest_framework import routers

from src.users.views import CoordinatorsViewSet, ProfessorsViewSet, StudentsViewSet

router = routers.DefaultRouter()
router.register("coordinators", CoordinatorsViewSet, basename="Coordinators")
router.register("professors", ProfessorsViewSet, basename="Professors")
router.register("students", StudentsViewSet, basename="Students")

urlpatterns = [
    path("api/", include(router.urls)),
]
