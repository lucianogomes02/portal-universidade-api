from typing import Union

from rest_framework.response import Response

from src.users.domain.entities import Coordinator
from src.users.models import CoordinatorUser, User
from src.users.service.serializers import CoordinatorSerializer


class CoordinatorService:
    @staticmethod
    def register_coordinator(request_data) -> Union[Response, CoordinatorUser]:
        serializer = CoordinatorSerializer(data=request_data)
        if serializer.is_valid():
            coordinator_data = serializer.validated_data
            coordinator = Coordinator(**coordinator_data)
            # validade coordinator here
            coordinator_user = CoordinatorUser.objects.create(
                name=coordinator.name,
                email=coordinator.email,
                birth_date=coordinator.birth_date,
                username=coordinator.email,
                user_type=User.UserType.COORDINATOR,
            )
            coordinator_user.set_password(coordinator.password)
            coordinator_user.save()
            return coordinator_user
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
