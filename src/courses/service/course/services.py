from typing import Union

from rest_framework import status
from rest_framework.response import Response

from src.courses.models import Course
from src.courses.repository.course_repository import CourseRepository
from src.courses.service.course.serializers import CourseSerializer
from src.users.repository.professor_repository import ProfessorRepository


class CourseService:
    @staticmethod
    def search_for_course(course_id) -> Response:
        course = CourseRepository().search_by_id(course_id=course_id)
        if not course:
            return Response(
                {"error": "Disciplina não encontrada"}, status.HTTP_404_NOT_FOUND
            )
        serializer = CourseSerializer(course)
        return Response({"success": serializer.data}, status.HTTP_200_OK)

    @staticmethod
    def register_course(request_data) -> Union[Response, Course]:
        serializer = CourseSerializer(data=request_data)
        if serializer.is_valid():
            course_data = serializer.validated_data
            CourseRepository().save(course_data=course_data)
            return Response(
                {"success": "Disciplina cadastrada com sucesso"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": "Dados inválidos para cadastro de Disciplina"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def change_course_registry(course_id, request_data) -> Union[Response, Course]:
        course = CourseRepository().search_by_id(course_id=course_id)
        if not course:
            return Response(
                {"message": "Disciplina não encontrada"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CourseSerializer(instance=course, data=request_data)
        if serializer.is_valid():
            professor = ProfessorRepository().search_by_id(
                professor_id=request_data.get("professor")
            )
            request_data["professor"] = professor
            CourseRepository().update(course=course, updated_data=request_data)
            return Response(
                {"success": "Disciplina alterada com sucesso"},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"error": "Dados inválidos para alteração de Disciplina"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def unregister_course(course_id):
        course = CourseRepository().search_by_id(course_id=course_id)
        if course:
            CourseRepository().delete(course=course)
            return Response(
                {"success": "Disciplina removida com sucesso"},
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            {"error": "Disciplina não encontrada"},
            status=status.HTTP_404_NOT_FOUND,
        )
