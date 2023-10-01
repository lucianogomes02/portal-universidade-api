from typing import Union, Dict
from uuid import UUID

from rest_framework import status
from rest_framework.response import Response

from src.courses.repository.course_repository import CourseRepository
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
            course = CourseRepository().search_by_id_professor_and_student(
                course_id=request_data.get("course", None),
                professor_id=request_data.get("professor", None),
                student_id=request_data.get("student", None),
            )
            if course:
                grade_data = serializer.validated_data
                grade = GradeRepository().save(grade_data=grade_data)
                return grade
            return Response(
                {
                    "message": "Não foi encontrada uma Disciplina que seja "
                    + "ministrada pelo Professor selecionado, ou que o Aluno selecionado esteja matrículado"
                },
                status.HTTP_404_NOT_FOUND,
            )
        return Response(serializer.errors, status=400)

    @staticmethod
    def change_grade(grade_id: UUID, request_data: Dict) -> Union[Response, Grade]:
        if not request_data.get("student", None):
            return Response(
                {"message": "Necessário informar o Aluno que deseja alterar a Nota"}
            )
        grade = GradeRepository().search_by_id_and_student(
            grade_id=grade_id, student_id=request_data.get("student")
        )
        if not grade:
            return Response({"message": "Nota não foi encontrada para alteração"})
        new_grade_value = {"value": request_data.get("value")}
        serializer = GradeSerializer(instance=grade, data=new_grade_value)
        if serializer.is_valid():
            grade_changed = GradeRepository().update(
                grade=grade, updated_data=new_grade_value
            )
            return grade_changed
        return Response(serializer.errors, status=400)

    @staticmethod
    def unregister_grade(grade_id: UUID):
        grade = GradeRepository().search_by_id(grade_id=grade_id)
        if grade:
            GradeRepository().delete(grade=grade)
