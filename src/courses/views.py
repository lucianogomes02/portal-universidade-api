from rest_framework import viewsets
from rest_framework.response import Response

from src.courses.repository.course_repository import CourseRepository
from src.courses.service.course.commands import (
    RegisterCourse,
    ChangeCourseRegistry,
    UnregisterCourse,
    SearchForCourse,
)
from src.courses.service.course.serializers import (
    CourseSerializer,
)
from src.users.models import User


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


class CoursesViewSet(BaseCourseModelViewSet):
    queryset = CourseRepository().search_all_objects()
    serializer_class = CourseSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        command = SearchForCourse()
        return command.handle(course_id=pk)

    def create(self, request, *args, **kwargs):
        command = RegisterCourse()
        return command.handle(request_data=request.data)

    def update(self, request, pk=None, *args, **kwargs):
        command = ChangeCourseRegistry()
        return command.handle(course_id=pk, request_data=request.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        command = UnregisterCourse()
        return command.handle(course_id=pk)
