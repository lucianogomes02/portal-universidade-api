from typing import Union

from rest_framework.response import Response

from src.users.models import Student
from src.users.repository.student_repository import StudentRepository
from src.users.service.student.serializers import StudentSerializer


class StudentService:
    @staticmethod
    def search_for_student(student_id) -> Response:
        student = StudentRepository().search_by_id(student_id=student_id)
        if not student:
            return Response({"message": "Aluno não encontrado"})
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    @staticmethod
    def register_student(request_data) -> Union[Response, Student]:
        serializer = StudentSerializer(data=request_data)
        if serializer.is_valid():
            student_data = serializer.validated_data
            student = StudentRepository().save(student_data=student_data)
            return student
        return Response(serializer.errors, status=400)

    @staticmethod
    def change_student_registry(student_id, request_data) -> Union[Response, Student]:
        student = StudentRepository().search_by_id(student_id=student_id)
        serializer = StudentSerializer(instance=student, data=request_data)
        if serializer.is_valid():
            student_changed = StudentRepository().update(
                student=student, updated_data=request_data
            )
            return student_changed
        return Response(serializer.errors, status=400)

    @staticmethod
    def unregister_student(student_id):
        student = StudentRepository().search_by_id(student_id=student_id)
        if student:
            StudentRepository().delete(student=student)
