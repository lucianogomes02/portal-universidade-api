from typing import Union, Tuple

from rest_framework import status
from rest_framework.response import Response

from src.courses.models import Course
from src.courses.repository.course_repository import CourseRepository
from src.enrollments.repository.enrollment_repository import EnrollmentRepository
from src.users.models import Student
from src.users.repository.student_repository import StudentRepository


class EnrollmentService:
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
