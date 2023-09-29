from rest_framework.viewsets import ModelViewSet

from src.users.repository.coordinator_repository import CoordinatorRepository
from src.users.repository.professor_repository import ProfessorRepository
from src.users.service.coordinator.commands import (
    RegisterCoordinator,
    UnregisterCoordinator,
    ChangeCoordinatorRegistry,
    SearchForCoordinator,
)
from src.users.service.coordinator.serializers import CoordinatorSerializer
from src.users.service.professor.commands import (
    SearchForProfessor,
    RegisterProfessor,
    ChangeProfessorRegistry,
    UnregisterProfessor,
)
from src.users.service.professor.serializers import ProfessorSerializer


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


class ProfessorsViewSet(ModelViewSet):
    queryset = ProfessorRepository().search_all_objects()
    serializer_class = ProfessorSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        command = SearchForProfessor()
        return command.handle(professor_id=pk)

    def create(self, request, *args, **kwargs):
        command = RegisterProfessor()
        return command.handle(request_data=request.data)

    def update(self, request, pk=None, *args, **kwargs):
        command = ChangeProfessorRegistry()
        return command.handle(professor_id=pk, request_data=request.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        command = UnregisterProfessor()
        return command.handle(professor_id=pk)
