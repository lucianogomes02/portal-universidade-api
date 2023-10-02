from rest_framework import status
from rest_framework.response import Response

from src.courses.service.course.services import CourseService
from src.libs.command import Command


class SearchForCourse(Command):
    def add_arguments(self, parser):
        parser.add_argument("course_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        course_id = kwargs["course_id"]
        course_search_response = CourseService.search_for_course(course_id=course_id)
        return course_search_response


class RegisterCourse(Command):
    def add_arguments(self, parser):
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        request_data = kwargs["request_data"]
        course = CourseService.register_course(request_data)
        if isinstance(course, Response):
            return course
        success_response: str = "Disciplina criada com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response}, status=status.HTTP_201_CREATED)


class ChangeCourseRegistry(Command):
    def add_arguments(self, parser):
        parser.add_argument("course_id", type=str)
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        course_id = kwargs["course_id"]
        request_data = kwargs["request_data"]
        course = CourseService.change_course_registry(
            course_id=course_id, request_data=request_data
        )
        if isinstance(course, Response):
            return course
        success_response: str = "Disciplina atualizada com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})


class EnrollStudentToCourse(Command):
    def add_arguments(self, parser):
        parser.add_argument("course_id", type=str)
        parser.add_argument("student_id", type=dict)

    def handle(self, *args, **kwargs):
        student_id = kwargs["student_id"]
        course_id = kwargs["course_id"]
        course, student = CourseService.enroll_student_to_course(
            course_id=course_id, student_id=student_id
        )
        if isinstance(course, Response):
            return course
        success_response: str = (
            f"Aluno {student.name} matrículado à Disciplina {course.name} com sucesso"
        )
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})


class UnregisterCourse(Command):
    def add_arguments(self, parser):
        parser.add_argument("course_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        course_id = kwargs["course_id"]
        return CourseService.unregister_course(course_id=course_id)
