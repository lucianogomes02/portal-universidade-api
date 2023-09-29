from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.users.domain.entities import Coordinator
from src.users.models import CoordinatorUser, User
from src.users.service.serializers import CoordinatorSerializer


class CoordinatorsViewSet(ModelViewSet):
    queryset = CoordinatorUser.objects.all()
    serializer_class = CoordinatorSerializer

    def create(self, request, *args, **kwargs):
        serializer = CoordinatorSerializer(data=request.data)
        if serializer.is_valid():
            coordinator_data = serializer.validated_data
            coordinator = Coordinator(**coordinator_data)
            coordinator_user = CoordinatorUser(
                name=coordinator.name,
                email=coordinator.email,
                birth_date=coordinator.birth_date,
                password=coordinator.password,
                username=coordinator.email,
                user_type=User.UserType.COORDINATOR
            )
            coordinator_user.save()
            return Response({"message": "Coordenador criado com sucesso"})
        return Response(serializer.errors, status=400)
