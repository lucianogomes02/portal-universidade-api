from _decimal import Decimal

from rest_framework import serializers

from src.courses.repository.course_repository import CourseRepository
from src.grades.models import Grade
from src.users.repository.professor_repository import ProfessorRepository
from src.users.repository.student_repository import StudentRepository


class GradeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    course = serializers.PrimaryKeyRelatedField(
        queryset=CourseRepository().search_all_objects(), required=False
    )
    professor = serializers.PrimaryKeyRelatedField(
        queryset=ProfessorRepository().search_all_objects(), required=False
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=StudentRepository().search_all_objects(), required=False
    )
    value = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Grade
        fields = ["id", "course", "professor", "student", "value"]

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
        model_fields.pop(0)
        for field in model_fields:
            if field not in data:
                raise serializers.ValidationError({field: "Este campo é obrigatório."})

        return data
