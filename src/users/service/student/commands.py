from rest_framework.response import Response

from src.libs.command import Command
from src.users.service.student.services import StudentService


class SearchForStudent(Command):
    def add_arguments(self, parser):
        parser.add_argument("student_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        student_id = kwargs["student_id"]
        student_search_response = StudentService.search_for_student(
            student_id=student_id
        )
        return student_search_response


class RegisterStudent(Command):
    def add_arguments(self, parser):
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        request_data = kwargs["request_data"]
        student_user = StudentService.register_student(request_data)
        if isinstance(student_user, Response):
            return student_user
        success_response: str = "Aluno criado com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})


class ChangeStudentRegistry(Command):
    def add_arguments(self, parser):
        parser.add_argument("student_id", type=str)
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        student_id = kwargs["student_id"]
        request_data = kwargs["request_data"]
        student_user = StudentService.change_student_registry(
            student_id=student_id, request_data=request_data
        )
        if isinstance(student_user, Response):
            return student_user
        success_response: str = "Aluno atualizado com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})


class UnregisterStudent(Command):
    def add_arguments(self, parser):
        parser.add_argument("student_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        student_id = kwargs["student_id"]
        StudentService.unregister_student(student_id=student_id)
        success_response: str = "Aluno excluído com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})
