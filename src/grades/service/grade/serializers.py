from _decimal import Decimal

from rest_framework import serializers

from src.courses.repository.course_repository import CourseRepository
from src.grades.models import Grade
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository


class GradeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    course = serializers.PrimaryKeyRelatedField(
        queryset=CourseRepository().search_all_objects(),
        required=False,
        write_only=True,
    )
    professor = serializers.PrimaryKeyRelatedField(
        queryset=ProfessorRepository().search_all_objects(),
        required=False,
        write_only=True,
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=StudentRepository().search_all_objects(),
        required=False,
        write_only=True,
    )
    course_name = serializers.SerializerMethodField()
    professor_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    value = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Grade
        fields = [
            "id",
            "course",
            "professor",
            "student",
            "course_name",
            "professor_name",
            "student_name",
            "value",
        ]

    def get_course_name(self, obj):
        if obj.course:
            return obj.course.name
        return None

    def get_professor_name(self, obj):
        if obj.professor:
            return obj.professor.name
        return None

    def get_student_name(self, obj):
        if obj.student:
            return obj.student.name
        return None

    def validate_grade_value(self, value):
        if not value or (not isinstance(value, Decimal) or value < 0):
            raise serializers.ValidationError(
                {"value": "A Nota deve ser maior ou igual a 0 e decimal"}
            )
        return value

    def validate(self, data):
        if self.instance:
            return data

        self.validate_grade_value(data.get("value"))

        model_fields = self.Meta.fields.copy()
        model_fields.remove("id")
        model_fields.remove("course_name")
        model_fields.remove("professor_name")
        model_fields.remove("student_name")
        for field in model_fields:
            if field not in data:
                raise serializers.ValidationError({field: "Este campo é obrigatório."})

        return data
