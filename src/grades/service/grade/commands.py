from rest_framework.response import Response

from src.grades.service.grade.services import GradeService
from src.libs.command import Command


class SearchGradeForStudent(Command):
    def add_arguments(self, parser):
        parser.add_argument("student_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        student_id = kwargs["student_id"]
        grade_search_response = GradeService.search_grade_for_student(
            student_id=student_id
        )
        return grade_search_response


class RegisterGrade(Command):
    def add_arguments(self, parser):
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        request_data = kwargs["request_data"]
        grade = GradeService.register_grade(request_data)
        if isinstance(grade, Response):
            return grade
        success_response: str = "Nota registrada com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})


class ChangeGrade(Command):
    def add_arguments(self, parser):
        parser.add_argument("grade_id", type=str)
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        grade_id = kwargs["grade_id"]
        request_data = kwargs["request_data"]
        grade = GradeService.change_grade(grade_id=grade_id, request_data=request_data)
        if isinstance(grade, Response):
            return grade
        success_response: str = "Nota atualizada com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})


class UnregisterGrade(Command):
    def add_arguments(self, parser):
        parser.add_argument("grade_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        grade_id = kwargs["grade_id"]
        GradeService.unregister_grade(grade_id=grade_id)
        success_response: str = "Nota excluída com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})
