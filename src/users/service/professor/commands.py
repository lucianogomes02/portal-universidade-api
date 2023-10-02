from rest_framework import status
from rest_framework.response import Response

from src.libs.command import Command
from src.users.service.professor.services import ProfessorService


class SearchForProfessor(Command):
    def add_arguments(self, parser):
        parser.add_argument("professor_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        professor_id = kwargs["professor_id"]
        return ProfessorService.search_for_professor(professor_id=professor_id)


class RegisterProfessor(Command):
    def add_arguments(self, parser):
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        request_data = kwargs["request_data"]
        return ProfessorService.register_professor(request_data)


class ChangeProfessorRegistry(Command):
    def add_arguments(self, parser):
        parser.add_argument("professor_id", type=str)
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        professor_id = kwargs["professor_id"]
        request_data = kwargs["request_data"]
        return ProfessorService.change_professor_registry(
            professor_id=professor_id, request_data=request_data
        )


class UnregisterProfessor(Command):
    def add_arguments(self, parser):
        parser.add_argument("professor_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        professor_id = kwargs["professor_id"]
        return ProfessorService.unregister_professor(professor_id=professor_id)
