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
            return Response(
                {"success": "Professor não encontrado"}, status.HTTP_404_NOT_FOUND
            )
        serializer = ProfessorSerializer(professor)
        Response({"success": serializer.data}, status.HTTP_200_OK)

    @staticmethod
    def register_professor(request_data) -> Union[Response, Professor]:
        serializer = ProfessorSerializer(data=request_data)
        if serializer.is_valid():
            professor_data = serializer.validated_data
            ProfessorRepository().save(professor_data=professor_data)
            return Response(
                {"success": "Professor cadastrado com sucesso"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Dados inválidos para cadastro de Professor"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def change_professor_registry(
        professor_id, request_data
    ) -> Union[Response, Professor]:
        professor = ProfessorRepository().search_by_id(professor_id=professor_id)
        if not professor:
            return Response(
                {"message": "Professor não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ProfessorSerializer(instance=professor, data=request_data)
        if serializer.is_valid():
            ProfessorRepository().update(professor=professor, updated_data=request_data)
            return Response(
                {"success": "Professor alterado com sucesso"},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"error": "Dados inválidos para alteração de Professor"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def unregister_professor(professor_id):
        professor = ProfessorRepository().search_by_id(professor_id=professor_id)
        if professor:
            ProfessorRepository().delete(professor=professor)
            return Response(
                {"success": "Professor removido com sucesso"},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"error": "Professor não encontrado"}, status=status.HTTP_404_NOT_FOUND
        )
