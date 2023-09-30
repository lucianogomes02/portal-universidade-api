from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from src.courses.repository.course_repository import CourseRepository
from src.courses.service.course.commands import (
    RegisterCourse,
    ChangeCourseRegistry,
    UnregisterCourse,
    SearchForCourse,
)
from src.courses.service.course.serializers import CourseSerializer


class CoursesViewSet(ModelViewSet):
    queryset = CourseRepository().search_all_objects()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

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
