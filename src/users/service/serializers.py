from rest_framework import serializers

from src.users.domain.entities import Coordinator


class CoordinatorSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    birth_date = serializers.DateField(required=False)

    def create(self, validated_data):
        return Coordinator(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
