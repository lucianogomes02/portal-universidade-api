from rest_framework import serializers
from src.enrollments.models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"


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
