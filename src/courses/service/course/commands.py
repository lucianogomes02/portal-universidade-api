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
        return CourseService.register_course(request_data)


class ChangeCourseRegistry(Command):
    def add_arguments(self, parser):
        parser.add_argument("course_id", type=str)
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        course_id = kwargs["course_id"]
        request_data = kwargs["request_data"]
        return CourseService.change_course_registry(
            course_id=course_id, request_data=request_data
        )


class UnregisterCourse(Command):
    def add_arguments(self, parser):
        parser.add_argument("course_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        course_id = kwargs["course_id"]
        return CourseService.unregister_course(course_id=course_id)
