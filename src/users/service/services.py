from typing import Union

from rest_framework.response import Response

from src.users.models import CoordinatorUser
from src.users.service.serializers import CoordinatorSerializer


class CoordinatorService:
    @staticmethod
    def search_for_coordinator(coordinator_id) -> Response:
        coordinator = CoordinatorUser.objects.filter(id=coordinator_id).first()
        if not coordinator:
            return Response({"message": "Coordenador não encontrado"})
        serializer = CoordinatorSerializer(coordinator)
        return Response(serializer.data)

    @staticmethod
    def register_coordinator(request_data) -> Union[Response, CoordinatorUser]:
        serializer = CoordinatorSerializer(data=request_data)
        if serializer.is_valid():
            coordinator_data = serializer.validated_data
            # validade coordinator here
            coordinator = CoordinatorUser.objects.create(**coordinator_data)
            coordinator.set_password(coordinator.password)
            coordinator.save()
            return coordinator
        return Response(serializer.errors, status=400)

    @staticmethod
    def change_coordinator_registry(
        coordinator_id, request_data
    ) -> Union[Response, CoordinatorUser]:
        coordinator_user = CoordinatorUser.objects.filter(id=coordinator_id).first()
        serializer = CoordinatorSerializer(coordinator_user, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return coordinator_user
        return Response(serializer.errors, status=400)

    @staticmethod
    def unregister_coordinator(coordinator_id):
        coordinator = CoordinatorUser.objects.filter(id=coordinator_id).first()
        if coordinator:
            coordinator.delete()
