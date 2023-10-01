from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from src.courses.repository.course_repository import CourseRepository
from src.courses.service.course.commands import (
    RegisterCourse,
    ChangeCourseRegistry,
    UnregisterCourse,
    SearchForCourse,
    EnrollStudentToCourse,
)
from src.courses.service.course.serializers import (
    CourseSerializer,
    EnrollmentSerializer,
)
from src.libs.views import BaseCourseModelViewSet


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


class EnrollStudentToCourseViewSet(UpdateModelMixin, ListModelMixin, ViewSet):
    @action(detail=True, methods=["GET"], url_path="")
    def custom_list(self, request, *args, **kwargs):
        courses = CourseRepository().search_all_objects()
        enrollments = []

        for course in courses:
            serializer = EnrollmentSerializer(
                {
                    "course_id": course.id,
                    "student_ids": list(course.students.values_list("id", flat=True)),
                }
            )
            enrollments.append(serializer.data)

        return Response(enrollments, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        command = EnrollStudentToCourse()
        return command.handle(
            course_id=pk, student_id=request.data.get("student_id", None)
        )
