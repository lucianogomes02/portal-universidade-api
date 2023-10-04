from rest_framework import viewsets
from rest_framework.response import Response

from src.users.models import User
from src.users.repository.coordinator_repository import CoordinatorRepository
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository
from src.users.service.coordinator.commands import (
    RegisterCoordinator,
    UnregisterCoordinator,
    ChangeCoordinatorRegistry,
    SearchForCoordinator,
)
from src.users.service.coordinator.serializers import CoordinatorSerializer
from src.users.service.professor.commands import (
    SearchForProfessor,
    RegisterProfessor,
    ChangeProfessorRegistry,
    UnregisterProfessor,
)
from src.users.service.professor.serializers import ProfessorSerializer
from src.users.service.student.commands import (
    SearchForStudent,
    RegisterStudent,
    ChangeStudentRegistry,
    UnregisterStudent,
)
from src.users.service.student.serializers import StudentSerializer


class BaseUsersModelViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_is_admin = request.user.is_staff
        user_is_coordinator = request.user.user_type == User.UserType.COORDINATOR.value
        if not user_is_admin:
            if user_is_coordinator:
                queryset = queryset.filter(
                    user_type__in=[
                        request.user.user_type,
                        User.UserType.PROFESSOR,
                        User.UserType.STUDENT,
                    ]
                )
            else:
                queryset = queryset.filter(id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CoordinatorsViewSet(BaseUsersModelViewSet):
    queryset = CoordinatorRepository().search_all_objects()
    serializer_class = CoordinatorSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        command = SearchForCoordinator()
        return command.handle(coordinator_id=pk)

    def create(self, request, *args, **kwargs):
        command = RegisterCoordinator()
        return command.handle(request_data=request.data)

    def update(self, request, pk=None, *args, **kwargs):
        command = ChangeCoordinatorRegistry()
        return command.handle(coordinator_id=pk, request_data=request.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        command = UnregisterCoordinator()
        return command.handle(coordinator_id=pk)


class ProfessorsViewSet(BaseUsersModelViewSet):
    queryset = ProfessorRepository().search_all_objects()
    serializer_class = ProfessorSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        command = SearchForProfessor()
        return command.handle(professor_id=pk)

    def create(self, request, *args, **kwargs):
        command = RegisterProfessor()
        return command.handle(request_data=request.data)

    def update(self, request, pk=None, *args, **kwargs):
        command = ChangeProfessorRegistry()
        return command.handle(professor_id=pk, request_data=request.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        command = UnregisterProfessor()
        return command.handle(professor_id=pk)


class StudentsViewSet(BaseUsersModelViewSet):
    queryset = StudentRepository().search_all_objects()
    serializer_class = StudentSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        command = SearchForStudent()
        return command.handle(student_id=pk)

    def create(self, request, *args, **kwargs):
        command = RegisterStudent()
        return command.handle(request_data=request.data)

    def update(self, request, pk=None, *args, **kwargs):
        command = ChangeStudentRegistry()
        return command.handle(student_id=pk, request_data=request.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        command = UnregisterStudent()
        return command.handle(student_id=pk)
