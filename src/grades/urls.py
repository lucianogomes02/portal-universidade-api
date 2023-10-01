from django.urls import include, path
from rest_framework import routers

from src.grades.views import GradesViewSet

router = routers.DefaultRouter()
router.register("grades", GradesViewSet, basename="Grades")

urlpatterns = [
    path("api/", include(router.urls)),
]
