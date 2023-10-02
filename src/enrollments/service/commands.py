from rest_framework import status
from rest_framework.response import Response

from src.courses.service.course.services import CourseService
from src.libs.command import Command


class EnrollStudentToCourse(Command):
    def add_arguments(self, parser):
        parser.add_argument("student", type=str)
        parser.add_argument("course", type=str)

    def handle(self, *args, **kwargs):
        student_id = args[0].get("student")
        course_id = args[0].get("course")
        course, student = CourseService.enroll_student_to_course(
            course_id=course_id, student_id=student_id
        )
        if isinstance(course, Response):
            return course
        success_response: str = (
            f"Aluno {student.name} matrículado à Disciplina {course.name} com sucesso"
        )
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response}, status=status.HTTP_201_CREATED)
