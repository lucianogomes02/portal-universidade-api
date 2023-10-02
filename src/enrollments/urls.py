from django.urls import path, include
from rest_framework import routers

from src.enrollments.views import EnrollmentViewSet

router = routers.DefaultRouter()
router.register("enrollments", EnrollmentViewSet, basename="Enrollments")

urlpatterns = [
    path("api/", include(router.urls)),
]
