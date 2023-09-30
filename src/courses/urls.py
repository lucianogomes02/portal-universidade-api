from django.urls import path, include
from rest_framework import routers

from src.courses.views import CoursesViewSet, EnrollStudentToCourseViewSet

router = routers.DefaultRouter()
router.register("courses", CoursesViewSet, basename="Courses")
router.register(
    "courses/enroll", EnrollStudentToCourseViewSet, basename="Enroll Student To Course"
)

urlpatterns = [
    path("api/", include(router.urls)),
]
