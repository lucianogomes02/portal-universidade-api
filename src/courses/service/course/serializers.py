from rest_framework import serializers

from src.courses.models import Course
from src.users.models import Professor, Student


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=False)
    workload = serializers.IntegerField(required=False)
    professor = serializers.PrimaryKeyRelatedField(
        queryset=Professor.objects.all(), required=False
    )
    students = serializers.SlugRelatedField(
        many=True, queryset=Student.objects.all(), slug_field="id", required=False
    )

    class Meta:
        model = Course
        fields = ["id", "name", "workload", "professor", "students"]

    def validate_workload(self):
        if self.workload is not None and (
            not isinstance(self.workload, int) or self.workload <= 0
        ):
            raise serializers.ValidationError(
                "A carga horária deve ser um número inteiro maior que zero."
            )
        return self.workload

    def validate(self, data):
        if self.instance:
            return data

        self.validate_workload()

        model_fields = self.Meta.fields.copy()
        model_fields.pop(0)
        model_fields.pop(3)
        for field in model_fields:
            if field not in data:
                raise serializers.ValidationError({field: "Este campo é obrigatório."})

        return data


class EnrollmentSerializer(serializers.Serializer):
    course_id = serializers.UUIDField(read_only=True)
    student_ids = serializers.ListField(child=serializers.UUIDField(), read_only=True)
