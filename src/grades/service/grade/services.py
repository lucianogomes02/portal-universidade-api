from typing import Union, Dict
from uuid import UUID

from rest_framework.response import Response

from src.grades.models import Grade
from src.grades.repository.grade_repository import GradeRepository
from src.grades.service.grade.serializers import GradeSerializer


class GradeService:
    @staticmethod
    def search_grade_for_student(student_id: UUID) -> Response:
        grade = GradeRepository().search_by_student(student_id=student_id)
        if not grade:
            return Response({"message": "Nota do Aluno não foi encontrada"})
        serializer = GradeSerializer(grade)
        return Response(serializer.data)

    @staticmethod
    def register_grade(request_data: Dict) -> Union[Response, Grade]:
        serializer = GradeSerializer(data=request_data)
        if serializer.is_valid():
            grade_data = serializer.validated_data
            grade = GradeRepository().save(grade_data=grade_data)
            return grade
        return Response(serializer.errors, status=400)

    @staticmethod
    def change_grade(grade_id: UUID, request_data: Dict) -> Union[Response, Grade]:
        grade = GradeRepository().search_by_id(grade_id=grade_id)
        if not grade:
            raise ValueError("Nota não foi encontrada para alteração")
        serializer = GradeSerializer(instance=grade, data=request_data)
        if serializer.is_valid():
            grade_changed = GradeRepository().update(
                grade=grade, updated_data=request_data
            )
            return grade_changed
        return Response(serializer.errors, status=400)

    @staticmethod
    def unregister_grade(grade_id: UUID):
        grade = GradeRepository().search_by_id(grade_id=grade_id)
        if grade:
            GradeRepository().delete(grade=grade)
