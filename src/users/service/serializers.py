from rest_framework import serializers

from src.users.domain.entities import Coordinator


class CoordinatorSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False, read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    birth_date = serializers.DateField()

    def create(self, validated_data):
        return Coordinator(**validated_data)

    def update(self, instance, validated_data):
        pass
