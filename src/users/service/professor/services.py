from typing import Union

from rest_framework import status
from rest_framework.response import Response

from src.users.models import Professor
from src.users.repository.professor_repository import ProfessorRepository
from src.users.service.professor.serializers import ProfessorSerializer


class ProfessorService:
    @staticmethod
    def search_for_professor(professor_id) -> Response:
        professor = ProfessorRepository().search_by_id(professor_id=professor_id)
        if not professor:
            return Response({"message": "Professor não encontrado"})
        serializer = ProfessorSerializer(professor)
        return Response(serializer.data)

    @staticmethod
    def register_professor(request_data) -> Union[Response, Professor]:
        serializer = ProfessorSerializer(data=request_data)
        if serializer.is_valid():
            professor_data = serializer.validated_data
            professor = ProfessorRepository().save(professor_data=professor_data)
            return professor
        return Response(serializer.errors, status=400)

    @staticmethod
    def change_professor_registry(
        professor_id, request_data
    ) -> Union[Response, Professor]:
        professor = ProfessorRepository().search_by_id(professor_id=professor_id)
        serializer = ProfessorSerializer(instance=professor, data=request_data)
        if serializer.is_valid():
            professor_changed = ProfessorRepository().update(
                professor=professor, updated_data=request_data
            )
            return professor_changed
        return Response(serializer.errors, status=400)

    @staticmethod
    def unregister_professor(professor_id):
        professor = ProfessorRepository().search_by_id(professor_id=professor_id)
        if professor:
            ProfessorRepository().delete(professor=professor)
            return Response(
                {"message": "Professor removido com sucesso"},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"message": "Professor não encontrado"}, status=status.HTTP_404_NOT_FOUND
        )
