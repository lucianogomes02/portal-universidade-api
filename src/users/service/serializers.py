from rest_framework import serializers

from src.users.domain.entities import Coordinator


class CoordinatorSerializer(serializers.Serializer):
    # id: UUID
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    birth_date = serializers.DateField()

    def create(self, validated_data):
        return Coordinator(**validated_data)
