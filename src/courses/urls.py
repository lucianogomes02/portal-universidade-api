from django.urls import path, include
from rest_framework import routers

from src.courses.views import CoursesViewSet

router = routers.DefaultRouter()
router.register("courses", CoursesViewSet, basename="Courses")

urlpatterns = [
    path("api/", include(router.urls)),
]
