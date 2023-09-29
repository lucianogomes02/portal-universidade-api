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
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        request_data = kwargs["request_data"]
        CoordinatorService.register_coordinator(request_data)
        success_response: str = "Coordenador criado com sucesso"
        self.stdout.write(self.style.SUCCESS("Coordenador criado com sucesso"))
        return Response({"message": success_response})


class UnregisterCoordinator(Command):
    def add_arguments(self, parser):
        parser.add_argument("coordinator_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        coordinator_id = kwargs["coordinator_id"]
        CoordinatorService.unregister_coordinator(coordinator_id=coordinator_id)
        success_response: str = "Coordenador excluído com sucesso"
        self.stdout.write(self.style.SUCCESS("Coordenador excluído com sucesso"))
        return Response({"message": success_response})
