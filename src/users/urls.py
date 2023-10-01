from django.urls import path, include
from rest_framework import routers

from src.users.views import (
    CoordinatorsViewSet,
    ProfessorsViewSet,
    StudentsViewSet,
    UserPermissionsViewSet,
)

router = routers.DefaultRouter()
router.register("coordinators", CoordinatorsViewSet, basename="Coordinators")
router.register("professors", ProfessorsViewSet, basename="Professors")
router.register("students", StudentsViewSet, basename="Students")
router.register("user_permissions", UserPermissionsViewSet, basename="User Permissions")

urlpatterns = [
    path("api/", include(router.urls)),
]
