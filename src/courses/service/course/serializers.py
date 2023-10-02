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

    class Meta:
        model = Course
        fields = ["id", "name", "workload", "professor"]

    def validate_workload(self, workload):
        if workload is not None and (not isinstance(workload, int) or workload <= 0):
            raise serializers.ValidationError(
                "A carga horária deve ser um número inteiro maior que zero."
            )
        return workload

    def validate(self, data):
        if self.instance:
            return data

        self.validate_workload(data.get("workload"))

        model_fields = self.Meta.fields.copy()
        model_fields.pop(0)
        for field in model_fields:
            if field not in data:
                raise serializers.ValidationError({field: "Este campo é obrigatório."})

        return data
