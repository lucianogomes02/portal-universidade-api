from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.grades.repository.grade_repository import GradeRepository
from src.grades.service.grade.commands import (
    SearchGradeForStudent,
    RegisterGrade,
    ChangeStudentsGrade,
    UnregisterGrade,
)
from src.grades.service.grade.serializers import GradeSerializer
from src.users.models import User


class BaseGradeModelViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        from src.grades.service.grade.strategies import (
            FilterGradeByStudent,
            FilterGradeByProfessor,
        )

        queryset = self.filter_queryset(self.get_queryset())
        user_id_admin = request.user.is_staff
        if (
            not user_id_admin
            and not request.user.user_type == User.UserType.COORDINATOR
        ):
            filtering_strategies = {
                User.UserType.STUDENT: FilterGradeByStudent.filter_entity_based_user_type(
                    student_id=request.user.id, queryset=queryset
                ),
                User.UserType.PROFESSOR: FilterGradeByProfessor.filter_entity_based_user_type(
                    professor_id=request.user.id, queryset=queryset
                ),
            }
            queryset = filtering_strategies[request.user.user_type]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GradesViewSet(BaseGradeModelViewSet):
    queryset = GradeRepository().search_all_objects()
    serializer_class = GradeSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        command = SearchGradeForStudent()
        return command.handle(student_id=pk)

    def create(self, request, *args, **kwargs):
        command = RegisterGrade()
        return command.handle(request_data=request.data)

    def update(self, request, pk=None, *args, **kwargs):
        command = ChangeStudentsGrade()
        return command.handle(grade_id=pk, request_data=request.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        command = UnregisterGrade()
        return command.handle(grade_id=pk)
