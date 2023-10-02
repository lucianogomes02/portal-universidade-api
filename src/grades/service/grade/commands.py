from rest_framework.response import Response

from src.grades.service.grade.services import GradeService
from src.libs.command import Command


class SearchGradeForStudent(Command):
    def add_arguments(self, parser):
        parser.add_argument("student_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        student_id = kwargs["student_id"]
        return GradeService.search_grade_for_student(
            student_id=student_id
        )


class RegisterGrade(Command):
    def add_arguments(self, parser):
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        request_data = kwargs["request_data"]
        return GradeService.register_grade(request_data)


class ChangeStudentsGrade(Command):
    def add_arguments(self, parser):
        parser.add_argument("grade_id", type=str)
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        grade_id = kwargs["grade_id"]
        request_data = kwargs["request_data"]
        return GradeService.change_grade(grade_id=grade_id, request_data=request_data)


class UnregisterGrade(Command):
    def add_arguments(self, parser):
        parser.add_argument("grade_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        grade_id = kwargs["grade_id"]
        return GradeService.unregister_grade(grade_id=grade_id)
