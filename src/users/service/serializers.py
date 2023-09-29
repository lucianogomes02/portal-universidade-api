from rest_framework import serializers

from src.users.models import CoordinatorUser


class CoordinatorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CoordinatorUser
        fields = ["id", "name", "email", "password", "birth_date"]
