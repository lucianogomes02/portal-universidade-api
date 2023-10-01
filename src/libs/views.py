from rest_framework import viewsets
from rest_framework.response import Response

from src.users.models import User


class BaseUsersModelViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_id_admin = request.user.is_staff
        if not user_id_admin:
            queryset = queryset.filter(id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BaseCourseModelViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        from src.courses.service.course.strategies import (
            FilterCourseByStudent,
            FilterCourseByProfessor,
        )

        queryset = self.filter_queryset(self.get_queryset())
        user_id_admin = request.user.is_staff
        if (
            not user_id_admin
            and not request.user.user_type == User.UserType.COORDINATOR
        ):
            filtering_strategies = {
                User.UserType.STUDENT: FilterCourseByStudent.filter_entity_based_user_type(
                    student_id=request.user.id, queryset=queryset
                ),
                User.UserType.PROFESSOR: FilterCourseByProfessor.filter_entity_based_user_type(
                    professor_id=request.user.id, queryset=queryset
                ),
            }
            queryset = filtering_strategies[request.user.user_type]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
