from typing import Union

from rest_framework import status
from rest_framework.response import Response

from src.users.models import Student
from src.users.repository.student_repository import StudentRepository
from src.users.service.student.serializers import StudentSerializer


class StudentService:
    @staticmethod
    def search_for_student(student_id) -> Response:
        student = StudentRepository().search_by_id(student_id=student_id)
        if not student:
            return Response(
                {"error": "Aluno não encontrado"}, status.HTTP_404_NOT_FOUND
            )
        serializer = StudentSerializer(student)
        return Response({"success": serializer.data}, status.HTTP_200_OK)

    @staticmethod
    def register_student(request_data) -> Union[Response, Student]:
        serializer = StudentSerializer(data=request_data)
        if serializer.is_valid():
            student_data = serializer.validated_data
            StudentRepository().save(student_data=student_data)
            return Response(
                {"success": "Aluno cadastrado com sucesso"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Dados inválidos para cadastro de Aluno"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def change_student_registry(student_id, request_data) -> Union[Response, Student]:
        student = StudentRepository().search_by_id(student_id=student_id)
        if not student:
            return Response(
                {"message": "Aluno não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = StudentSerializer(instance=student, data=request_data)
        if serializer.is_valid():
            StudentRepository().update(student=student, updated_data=request_data)
            return Response(
                {"success": "Aluno alterado com sucesso"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Dados inválidos para alteração de Aluno"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def unregister_student(student_id):
        student = StudentRepository().search_by_id(student_id=student_id)
        if student:
            StudentRepository().delete(student=student)
            return Response(
                {"message": "Aluno removido com sucesso"},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"message": "Aluno não foi encontrado"}, status=status.HTTP_404_NOT_FOUND
        )
