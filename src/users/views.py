from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.users.models import CoordinatorUser
from src.users.service.commands import (
    RegisterCoordinator,
    UnregisterCoordinator,
    ChangeCoordinatorRegistry,
)
from src.users.service.serializers import CoordinatorSerializer


class CoordinatorsViewSet(ModelViewSet):
    queryset = CoordinatorUser.objects.all()
    serializer_class = CoordinatorSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        coordinator = CoordinatorUser.objects.filter(id=pk).first()
        serializer = CoordinatorSerializer(coordinator)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        command = RegisterCoordinator()
        return command.handle(request_data=request.data)

    def update(self, request, pk=None, *args, **kwargs):
        command = ChangeCoordinatorRegistry()
        return command.handle(coordinator_id=pk, request_data=request.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        command = UnregisterCoordinator()
        return command.handle(coordinator_id=pk)
