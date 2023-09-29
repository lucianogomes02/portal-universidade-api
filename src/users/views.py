from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.users.models import CoordinatorUser
from src.users.service.commands import RegisterCoordinator
from src.users.service.serializers import CoordinatorSerializer


class CoordinatorsViewSet(ModelViewSet):
    queryset = CoordinatorUser.objects.all()
    serializer_class = CoordinatorSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        coordinator = CoordinatorUser.objects.filter(id=pk).first()
        serializer = CoordinatorSerializer(coordinator)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CoordinatorSerializer(data=request.data)
        if serializer.is_valid():
            coordinator_data = serializer.validated_data
            command = RegisterCoordinator()
            return command.handle(**coordinator_data)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None, *args, **kwargs):
        coordinator_user = CoordinatorUser.objects.filter(id=pk).first()
        serializer = CoordinatorSerializer(coordinator_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Coordenador atualizado com sucesso"})
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None, *args, **kwargs):
        coordinator = CoordinatorUser.objects.filter(id=pk).first()
        coordinator.delete()
        return Response({"message": "Coordenador excluído com sucesso"})
