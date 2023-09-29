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


class SearchForCoordinator(Command):
    def add_arguments(self, parser):
        parser.add_argument("coordinator_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        coordinator_id = kwargs["coordinator_id"]
        coordinator_search_response = CoordinatorService.search_for_coordinator(
            coordinator_id=coordinator_id
        )
        return coordinator_search_response


class RegisterCoordinator(Command):
    def add_arguments(self, parser):
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        request_data = kwargs["request_data"]
        coordinator_user = CoordinatorService.register_coordinator(request_data)
        if coordinator_user is Response:
            return coordinator_user
        success_response: str = "Coordenador criado com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})


class ChangeCoordinatorRegistry(Command):
    def add_arguments(self, parser):
        parser.add_argument("coordinator_id", type=str)
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs):
        coordinator_id = kwargs["coordinator_id"]
        request_data = kwargs["request_data"]
        coordinator_user = CoordinatorService.change_coordinator_registry(
            coordinator_id=coordinator_id, request_data=request_data
        )
        if coordinator_user is Response:
            return coordinator_user
        success_response: str = "Coordenador atualizado com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})


class UnregisterCoordinator(Command):
    def add_arguments(self, parser):
        parser.add_argument("coordinator_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        coordinator_id = kwargs["coordinator_id"]
        CoordinatorService.unregister_coordinator(coordinator_id=coordinator_id)
        success_response: str = "Coordenador excluído com sucesso"
        self.stdout.write(self.style.SUCCESS(success_response))
        return Response({"message": success_response})
