from rest_framework.viewsets import ModelViewSet

from src.users.repository.coordinator_repository import CoordinatorRepository
from src.users.service.commands import (
    RegisterCoordinator,
    UnregisterCoordinator,
    ChangeCoordinatorRegistry,
    SearchForCoordinator,
)
from src.users.service.serializers import CoordinatorSerializer


class CoordinatorsViewSet(ModelViewSet):
    queryset = CoordinatorRepository().search_all_objects()
    serializer_class = CoordinatorSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        command = SearchForCoordinator()
        return command.handle(coordinator_id=pk)

    def create(self, request, *args, **kwargs):
        command = RegisterCoordinator()
        return command.handle(request_data=request.data)

    def update(self, request, pk=None, *args, **kwargs):
        command = ChangeCoordinatorRegistry()
        return command.handle(coordinator_id=pk, request_data=request.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        command = UnregisterCoordinator()
        return command.handle(coordinator_id=pk)
