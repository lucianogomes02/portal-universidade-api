from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from src.grades.repository.grade_repository import GradeRepository
from src.grades.service.grade.commands import (
    SearchGradeForStudent,
    RegisterGrade,
    ChangeStudentsGrade,
    UnregisterGrade,
)
from src.grades.service.grade.serializers import GradeSerializer


class GradesViewSet(ModelViewSet):
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
