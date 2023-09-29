import abc

from django.core.management import BaseCommand
from rest_framework.response import Response

from src.users.service.services import CoordinatorService


class Command(abc.ABC, BaseCommand):
    @abc.abstractmethod
    def add_arguments(self, parser):
        raise NotImplementedError()

    @abc.abstractmethod
    def handle(self, *args, **options):
        raise NotImplementedError()


class RegisterCoordinator(Command):
    def add_arguments(self, parser):
        parser.add_argument("name", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)
        parser.add_argument("birth_date", type=str)

    def handle(self, *args, **kwargs) -> Response:
        name = kwargs["name"]
        email = kwargs["email"]
        password = kwargs["password"]
        birth_date = kwargs["birth_date"]

        CoordinatorService.register_coordinator(name, email, password, birth_date)

        success_response: str = "Coordenador criado com sucesso"

        self.stdout.write(self.style.SUCCESS("Coordenador criado com sucesso"))

        return Response({"message": success_response})
