from rest_framework import status
from rest_framework.response import Response

from src.libs.command import Command
from src.users.service.coordinator.services import CoordinatorService


class SearchForCoordinator(Command):
    def add_arguments(self, parser):
        parser.add_argument("coordinator_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        coordinator_id = kwargs["coordinator_id"]
        return CoordinatorService.search_for_coordinator(coordinator_id=coordinator_id)


class RegisterCoordinator(Command):
    def add_arguments(self, parser):
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        request_data = kwargs["request_data"]
        return CoordinatorService.register_coordinator(request_data)


class ChangeCoordinatorRegistry(Command):
    def add_arguments(self, parser):
        parser.add_argument("coordinator_id", type=str)
        parser.add_argument("request_data", type=dict)

    def handle(self, *args, **kwargs) -> Response:
        coordinator_id = kwargs["coordinator_id"]
        request_data = kwargs["request_data"]
        return CoordinatorService.change_coordinator_registry(
            coordinator_id=coordinator_id, request_data=request_data
        )


class UnregisterCoordinator(Command):
    def add_arguments(self, parser):
        parser.add_argument("coordinator_id", type=str)

    def handle(self, *args, **kwargs) -> Response:
        coordinator_id = kwargs["coordinator_id"]
        return CoordinatorService.unregister_coordinator(coordinator_id=coordinator_id)
