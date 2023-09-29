from rest_framework.response import Response

from src.libs.command import Command
from src.users.service.professor.services import ProfessorService


class SearchForProfessor(Command):
    def add_arguments(self, parser):
        parser.add_argument("professor_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        professor_id = kwargs["professor_id"]
        professor_search_response = ProfessorService.search_for_professor(
            professor_id=professor_id
        )
        return professor_search_response


class RegisterProfessor(Command):
    def add_arguments(self, parser):
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        request_data = kwargs["request_data"]
        professor_user = ProfessorService.register_professor(request_data)
        if isinstance(professor_user, Response):
            return professor_user
        success_response: str = "Professor criado com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})


class ChangeProfessorRegistry(Command):
    def add_arguments(self, parser):
        parser.add_argument("professor_id", type=str)
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        professor_id = kwargs["professor_id"]
        request_data = kwargs["request_data"]
        professor_user = ProfessorService.change_professor_registry(
            professor_id=professor_id, request_data=request_data
        )
        if isinstance(professor_user, Response):
            return professor_user
        success_response: str = "Professor atualizado com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})


class UnregisterProfessor(Command):
    def add_arguments(self, parser):
        parser.add_argument("professor_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        professor_id = kwargs["professor_id"]
        ProfessorService.unregister_professor(professor_id=professor_id)
        success_response: str = "Professor excluído com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})
