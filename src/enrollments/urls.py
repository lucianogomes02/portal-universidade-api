from django.urls import path, include
from rest_framework import routers

from src.enrollments.views import (
    EnrollmentViewSet,
    ListStudentsCoursesAPIVIew,
    ListStudentsEnrollmentsAPIView,
)

router = routers.DefaultRouter()
router.register("enrollments", EnrollmentViewSet, basename="Enrollments")

urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "api/students/<uuid:pk>/enrollments", ListStudentsEnrollmentsAPIView.as_view()
    ),
    path("api/courses/<uuid:pk>/enrollments", ListStudentsCoursesAPIVIew.as_view()),
]
