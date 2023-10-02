from typing import Union, Dict
from uuid import UUID

from rest_framework import status
from rest_framework.response import Response

from src.courses.repository.course_repository import CourseRepository
from src.enrollments.repository.enrollment_repository import EnrollmentRepository
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
            course = CourseRepository().search_by_id_and_professor(
                course_id=request_data.get("course", None),
                professor_id=request_data.get("professor", None),
            )
            student_enrolled_to_course = (
                EnrollmentRepository().search_by_student_and_course(
                    student_id=request_data.get("student", None),
                    course_id=request_data.get("course", None),
                )
            )
            if course and student_enrolled_to_course:
                grade_is_registered = GradeRepository().search_by_student_and_course(
                    course_id=course.id, student_id=request_data.get("student")
                )
                if not grade_is_registered:
                    grade_data = serializer.validated_data
                    GradeRepository().save(grade_data=grade_data)
                    return Response(
                        {"message": "Nota regsitrada com sucesso"},
                        status.HTTP_201_CREATED,
                    )
                return Response(
                    {
                        "message": f"Nota do Aluno já foi registada para a Disciplina {course.name}",
                    },
                    status.HTTP_406_NOT_ACCEPTABLE,
                )
            return Response(
                {
                    "message": "Não foi encontrada uma Disciplina que seja "
                    + "ministrada pelo Professor selecionado, ou que o Aluno selecionado esteja matrículado"
                },
                status.HTTP_404_NOT_FOUND,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(
                {"message": "Nota não foi encontrada para alteração"},
                status.HTTP_404_NOT_FOUND,
            )
        new_grade_value = {"value": request_data.get("value")}
        serializer = GradeSerializer(instance=grade, data=new_grade_value)
        if serializer.is_valid():
            GradeRepository().update(grade=grade, updated_data=new_grade_value)
            return Response(
                {"message": "Nota foi alterada com sucesso"}, status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def unregister_grade(grade_id: UUID):
        grade = GradeRepository().search_by_id(grade_id=grade_id)
        if grade:
            GradeRepository().delete(grade=grade)
            return Response(
                {"message": "Nota excluída com sucesso"}, status.HTTP_202_ACCEPTED
            )
        return Response(
            {"message": "Nota não foi encontrada"}, status.HTTP_404_NOT_FOUND
        )
