from typing import Union

from rest_framework import status
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
            return Response(
                {"error": "Coordenador não encontrado"}, status.HTTP_404_NOT_FOUND
            )
        serializer = CoordinatorSerializer(coordinator)
        return Response({"success": serializer.data}, status.HTTP_200_OK)

    @staticmethod
    def register_coordinator(request_data) -> Union[Response, Coordinator]:
        serializer = CoordinatorSerializer(data=request_data)
        if serializer.is_valid():
            coordinator_data = serializer.validated_data
            CoordinatorRepository().save(coordinator_data=coordinator_data)
            return Response(
                {"success": "Coordenador registrado com sucesso"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Dados inválidos para cadastrar Coordenador"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def change_coordinator_registry(
        coordinator_id, request_data
    ) -> Union[Response, Coordinator]:
        coordinator = CoordinatorRepository().search_by_id(
            coordinator_id=coordinator_id
        )
        if not coordinator:
            return Response(
                {"message": "Coordenador não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CoordinatorSerializer(instance=coordinator, data=request_data)
        if serializer.is_valid():
            CoordinatorRepository().update(
                coordinator=coordinator, updated_data=request_data
            )
            return Response(
                {"success": "Coordenador alterado com sucesso"},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"error": "Dados inválidos para alteração do Coordenador"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def unregister_coordinator(coordinator_id):
        coordinator = CoordinatorRepository().search_by_id(
            coordinator_id=coordinator_id
        )
        if coordinator:
            CoordinatorRepository().delete(coordinator=coordinator)
            return Response(
                {"message": "Coordenador removido com sucesso"},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"message": "Coordenador não foi encontrado"},
            status=status.HTTP_404_NOT_FOUND,
        )
