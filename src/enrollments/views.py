from rest_framework import viewsets

from src.enrollments.models import Enrollment
from src.enrollments.service.commands import EnrollStudentToCourse
from src.enrollments.service.serializers import EnrollmentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        command = EnrollStudentToCourse()
        return command.handle(request.data)
