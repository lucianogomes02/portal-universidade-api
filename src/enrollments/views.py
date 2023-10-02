from rest_framework import viewsets, generics

from src.enrollments.models import Enrollment
from src.enrollments.service.commands import EnrollStudentToCourse
from src.enrollments.service.serializers import (
    EnrollmentSerializer,
    StudentsEnrollmentsSerializer,
    StudentsCoursesSerializer,
)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        command = EnrollStudentToCourse()
        return command.handle(request.data)


class ListStudentsEnrollmentsAPIView(generics.ListAPIView):
    def get_queryset(self):
        queryset = Enrollment.objects.filter(student=self.kwargs.get("pk"))
        return queryset

    serializer_class = StudentsEnrollmentsSerializer


class ListStudentsCoursesAPIVIew(generics.ListAPIView):
    def get_queryset(self):
        queryset = Enrollment.objects.filter(course=self.kwargs.get("pk"))
        return queryset

    serializer_class = StudentsCoursesSerializer
