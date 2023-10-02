from typing import Union, Tuple

from rest_framework import status
from rest_framework.response import Response

from src.courses.models import Course
from src.courses.repository.course_repository import CourseRepository
from src.courses.service.course.serializers import CourseSerializer
from src.enrollments.repository.enrollment_repository import EnrollmentRepository
from src.users.models import Student
from src.users.repository.student_repository import StudentRepository


class CourseService:
    @staticmethod
    def search_for_course(course_id) -> Response:
        course = CourseRepository().search_by_id(course_id=course_id)
        if not course:
            return Response({"message": "Disciplina não encontrada"})
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @staticmethod
    def register_course(request_data) -> Union[Response, Course]:
        serializer = CourseSerializer(data=request_data)
        if serializer.is_valid():
            course_data = serializer.validated_data
            course = CourseRepository().save(course_data=course_data)
            return course
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def change_course_registry(course_id, request_data) -> Union[Response, Course]:
        course = CourseRepository().search_by_id(course_id=course_id)
        serializer = CourseSerializer(instance=course, data=request_data)
        if serializer.is_valid():
            course_changed = CourseRepository().update(
                course=course, updated_data=request_data
            )
            return course_changed
        return Response(serializer.errors, status=400)

    @staticmethod
    def enroll_student_to_course(
        course_id, student_id
    ) -> Union[Response, Tuple[Course, Student]]:
        course = CourseRepository().search_by_id(course_id=course_id)
        student = StudentRepository().search_by_id(student_id=student_id)

        if not course:
            return Response(
                {
                    "message": "Erro ao matrícular Aluno à Disciplina. Disciplina não encontrada"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not student:
            return Response(
                {
                    "message": "Erro ao matrícular Aluno à Disciplina. Aluno não encontrado(a)"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        EnrollmentRepository().save({"student": student, "course": course})
        return course, student

    @staticmethod
    def unregister_course(course_id):
        course = CourseRepository().search_by_id(course_id=course_id)
        if course:
            CourseRepository().delete(course=course)
            return Response(
                {"message": "Disciplina removida com sucesso"},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"message": "Disciplina não encontrada"},
            status=status.HTTP_404_NOT_FOUND,
        )
