from typing import Union

from rest_framework.response import Response

from src.users.models import Coordinator
from src.users.repository.coordinator_repository import CoordinatorRepository
from src.users.service.coordinator.serializers import CoordinatorSerializer


class CoordinatorService:
    @staticmethod
    def search_for_coordinator(coordinator_id) -> Response:
        coordinator = CoordinatorRepository().search_by_id(
            coordinator_id=coordinator_id
        )
        if not coordinator:
            return Response({"message": "Coordenador não encontrado"})
        serializer = CoordinatorSerializer(coordinator)
        return Response(serializer.data)

    @staticmethod
    def register_coordinator(request_data) -> Union[Response, Coordinator]:
        serializer = CoordinatorSerializer(data=request_data)
        if serializer.is_valid():
            coordinator_data = serializer.validated_data
            coordinator = CoordinatorRepository().save(
                coordinator_data=coordinator_data
            )
            return coordinator
        return Response(serializer.errors, status=400)

    @staticmethod
    def change_coordinator_registry(
        coordinator_id, request_data
    ) -> Union[Response, Coordinator]:
        coordinator = CoordinatorRepository().search_by_id(
            coordinator_id=coordinator_id
        )
        serializer = CoordinatorSerializer(instance=coordinator, data=request_data)
        if serializer.is_valid():
            coordinator_changed = CoordinatorRepository().update(
                coordinator=coordinator, updated_data=request_data
            )
            return coordinator_changed
        return Response(serializer.errors, status=400)

    @staticmethod
    def unregister_coordinator(coordinator_id):
        coordinator = CoordinatorRepository().search_by_id(
            coordinator_id=coordinator_id
        )
        if coordinator:
            CoordinatorRepository().delete(coordinator=coordinator)
