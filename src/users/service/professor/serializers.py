from rest_framework import serializers

from src.users.models import Professor


class ProfessorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    birth_date = serializers.DateField(required=False)

    class Meta:
        model = Professor
        fields = ["id", "name", "email", "password", "birth_date"]

    def validate(self, data):
        if self.instance:
            return data

        model_fields = self.Meta.fields.copy()
        model_fields.remove("id")
        for field in model_fields:
            if field not in data:
                raise serializers.ValidationError({field: "Este campo é obrigatório."})

        return data
