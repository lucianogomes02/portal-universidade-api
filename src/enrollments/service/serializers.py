from rest_framework import serializers

from src.courses.repository.course_repository import CourseRepository
from src.enrollments.models import Enrollment
from src.users.repository.student_repository import StudentRepository


class EnrollmentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    course = serializers.PrimaryKeyRelatedField(
        queryset=CourseRepository().search_all_objects(),
        required=False,
        write_only=True,
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=StudentRepository().search_all_objects(),
        required=False,
        write_only=True,
    )
    course_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ["id", "course", "student", "course_name", "student_name"]

    def get_course_name(self, obj):
        if obj.course:
            return obj.course.name
        return None

    def get_student_name(self, obj):
        if obj.student:
            return obj.student.name
        return None

    def validate(self, data):
        if self.instance:
            return data

        model_fields = self.Meta.fields.copy()
        model_fields.remove("id")
        model_fields.remove("course_name")
        model_fields.remove("student_name")
        for field in model_fields:
            if field not in data:
                raise serializers.ValidationError({field: "Este campo é obrigatório."})

        return data


class StudentsEnrollmentsSerializer(serializers.ModelSerializer):
    course = serializers.ReadOnlyField(source="course.name")

    class Meta:
        model = Enrollment
        fields = ["course"]


class StudentsCoursesSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source="student.name")

    class Meta:
        model = Enrollment
        fields = ["student"]
